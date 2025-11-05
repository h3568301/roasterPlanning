import pandas as pd
from utils.excel_handler import load_staff_data
from scheduler import Scheduler

def main():
    staff_data = load_staff_data('data/staff_list.xlsx')
    scheduler = Scheduler(staff_data)
    daily_roster = scheduler.schedule_roster()
    scheduler.write_excel(daily_roster)

if __name__ == "__main__":
    main()