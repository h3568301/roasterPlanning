import pandas as pd
import os

def load_staff_data(file_path):
    print("Load staff data from an Excel file and return a list of staff members.")
    print("Load staff from: " + os.getcwd() + file_path)
    df = pd.read_excel(file_path)
    staff_list = df[['name', 'position', 'holiday', 'special holiday']].values.tolist()
    return staff_list