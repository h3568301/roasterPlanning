from utils.roster_generator import generate_daily_roster
import openpyxl
import os
import re
import requests
from datetime import date, timedelta


class Scheduler:
    def __init__(self, staff_data):
        self.staff_data = staff_data

    def extract_date_ranges(date_string):
        if not date_string:
            return []

        result = []
        if isinstance(date_string, str):
            parts = re.split(r'\)\s*,\s*\(', date_string.strip())

            for part in parts:
                part = part.strip('() ')
                dates = [d.strip() for d in part.split(',') if d.strip()]

                if len(dates) == 1:
                    y, m, d = map(int, dates[0].split('-'))
                    result.append([date(y, m, d)])

                elif len(dates) == 2:
                    y1, m1, d1 = map(int, dates[0].split('-'))
                    y2, m2, d2 = map(int, dates[1].split('-'))
                    result.append([date(y1, m1, d1), date(y2, m2, d2)])
        return result           
    
    def get_holidays(year=2025):
        try:
            # Fetch the iCal JSON from 1823.gov.hk
            url = "https://www.1823.gov.hk/common/ical/en.json"
            response = requests.get(url, timeout=10)  # Timeout to handle network issues
            response.raise_for_status()  # Raise error if request fails
            
            # Parse JSON
            data = response.json()
            holidays = []
            current_date = date.today()
            end_date = current_date + timedelta(days=90)
            # Extract vevent objects and convert dtstart to date
            for event in data["vcalendar"][0]["vevent"]:
                dtstart_str = event["dtstart"][0]  # Get the YYYYMMDD string
                event_date = date(int(dtstart_str[:4]), int(dtstart_str[4:6]), int(dtstart_str[6:]))
                if current_date <= event_date <= end_date:
                    holidays.append(event_date)
            
            temp_date = current_date
            while temp_date <= end_date:
                if temp_date.weekday() == 5 or temp_date.weekday() == 6:  # Saturday or Sunday
                    holidays.append(temp_date)
                temp_date += timedelta(days=1)

            holidays.sort()

            print(f"Successfully fetched {len(holidays)} public holidays from 1823.gov.hk.")
            return holidays
            
        except Exception as e:
            print(f"Error fetching from 1823.gov.hk: {e}. Using hardcoded fallback for {year}.")
            return [
                date(2025, 1, 1),
                date(2025, 1, 29),
                date(2025, 1, 30),
                date(2025, 1, 31),
                date(2025, 4, 4),
                date(2025, 4, 18),
                date(2025, 4, 19),
                date(2025, 4, 21),
                date(2025, 5, 1),
                date(2025, 5, 5),
                date(2025, 5, 31),
                date(2025, 7, 1),
                date(2025, 9, 26),
                date(2025, 10, 1),
                date(2025, 10, 7),
                date(2025, 10, 29),
                date(2025, 12, 25),
                date(2025, 12, 26)
            ]

    def schedule_roster(self):
        print('If you dont know the last assigned OT and Assistant or It is the first time using this program. Please press Enter for the following input value')
        first_ot = input('Last assigned OT: ')
        first_assistant = input('Last assigned Assistant: ')
        sorted_staff = sorted(self.staff_data, key=lambda x: x[0])
        for transform_date in sorted_staff:
            transform_date[2] = Scheduler.extract_date_ranges(transform_date[2])
            transform_date[3] = Scheduler.extract_date_ranges(transform_date[3])
        roster = generate_daily_roster(sorted_staff, 90, Scheduler.get_holidays(), [first_ot, first_assistant])
        
        return roster
    
    def write_excel(self, data):
        file_path = 'schedule.xlsx'
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Existing {file_path} deleted.")

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Schedule"

        sheet['A1'] = 'Date'
        sheet['B1'] = 'Ot'
        sheet['C1'] = 'Assistant'

        for row, entry in enumerate(data, start=2):
            sheet[f'A{row}'] = entry['date']
            sheet[f'B{row}'] = entry['Ot']
            sheet[f'C{row}'] = entry['Assistant']
        
        print("File will be saved in:", os.getcwd())
        workbook.save('schedule.xlsx')
        print("Schedule saved to schedule.xlsx")

        if os.path.exists(file_path):
            print(f"New {file_path} successfully created and verified.")
        else:
            print(f"Error: {file_path} was not created.")
