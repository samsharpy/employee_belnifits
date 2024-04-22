# # Copyright (c) 2024, Samuvelramesh2@gmail.com and contributors
# # For license information, please see license.txt

import frappe
import requests

def execute(filters=None):
    columns = [
        {"label": "Date", "fieldname": "meal_date", "fieldtype": "Data"},
        {"label": "Department ID", "fieldname": "dept_id", "fieldtype": "Int"},
        {"label": "Employee Name", "fieldname": "name", "fieldtype": "Data"},
        # {"label": "Email", "fieldname": "email", "fieldtype": "Data"},
        {"label": "Meal Type", "fieldname": "meal_type", "fieldtype": "Data"},
        {"label": "Break Fast", "fieldname": "morg", "fieldtype": "Data"},
        {"label": "Lunch", "fieldname": "lunch", "fieldtype": "Data"},
        {"label": "Dinner", "fieldname": "dinner", "fieldtype": "Data"},
        {"label": "Penality applicable", "fieldname": "pen_decition", "fieldtype": "Data"},
        {"label": "Missed Meal Count", "fieldname": "missed_meal_count", "fieldtype": "Int"},
        {"label": "Penality Amount", "fieldname": "penality_amt", "fieldtype": "Int"}
    ]
    data = get_filters(filters)
    # print(data)
    # get_filters(filters)
    return columns, data

def call_api_and_get_data(month=None):

    # API details
    url = "http://canteen.benzyinfotech.com/api/v3/customer/report"
    bearer_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZWRhNWExODU0OTFhYWE0MmY5YzMyZjRhMTU5MDM1ODk4ZjZiMzMxNWUzZjJjNGRiZDA1N2IyNGE3NTAzMDc3NDBlMjFlYjZmNGE4Mjk0MGUiLCJpYXQiOjE3MDQ4MDA4OTAuODc5OTI1OTY2MjYyODE3MzgyODEyNSwibmJmIjoxNzA0ODAwODkwLjg3OTkyOTA2NTcwNDM0NTcwMzEyNSwiZXhwIjoxNzM2NDIzMjkwLjgzNDkxMjA2MTY5MTI4NDE3OTY4NzUsInN1YiI6IjI2NSIsInNjb3BlcyI6W119.CwDEjlHoRtOXdFcaO6KGGxV202AOA7MMtJVPtKzgLqzTFzUUnDLGBd7PNAtHO2--3YOathM9HOG8hYjY8wjktXZIoCGUR9GWIaEVUxLwFq927CrSf05NuqTBTrJcDeBOjXDvKcSBiJ2A994FC2IunPcdkaZ4jpoaWBIaWueYUbHviYSQuLec3tFcAMg4njrImAlaN9k-QKkHetpdrdbUEX1Wzq4X-1QwuOx7W3W2nbbxaoNgFX1gaabxi00ZO7h5MokGvtqy_gCkS9TYoM74VfxmTyAAczjttLcPqDNiAL_ZJdutDMezw32CZj8G8l8PUL46F_BuaxatZDBUZxeClZh4_0Wvo9GX4zqF2XvHdzZHnwdB414vNCl8itaGW9w7QWbdchPOglhnek32ZmkH0MIqeOBhnAyHo5_WbP0uLd_3qmz3w04nvTbTGV25-QebaxPAsVD0-7Za1sVpqB_FD6yEeliaEzdxl_8gA5IH59uowpfPYgUIjom8NVEASuYsAwb0q3f0jhNRfwg2zmXNenoDunh_dN9l2NRjI2gdZueSMwu6IJLQK46jpn01uG2iQ1xx-pFJAGe_bzSceLsho3dbtabym3tMqi0Ac02xUP9Mn50LdkFJGNVU9jiuHQfyjQirDtGUfya3aIvpJlCGx9Cx99s_4P89uDnOiXy3A1Q"

    # Parameters
    params = {
        "month": month
    }

    # Headers
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    try:
        # Making POST request using requests.post
        response = requests.post(url, json=params, headers=headers)

        # Parsing response
        if response.status_code == 200:
            data = response.json()
            # print(data)
            user_info = data.get("user", {})  # Extracting user information
            reports = data.get("reports", []) 
            meal_date_rows = []
            for report in reports:
                if isinstance(report['opt_ins'], dict):  # Check if 'opt_ins' is a dictionary
                    meal_date_row = {
                        "meal_date": report.get('date', ''),
                        "breakfast": report['opt_ins'].get('breakfast', ''),
                        "lunch": report['opt_ins'].get('lunch', ''),
                        "dinner": report['opt_ins'].get('dinner', '')
                    }
                    meal_date_rows.append(meal_date_row)
                else:
                    meal_date_row = {
                        "meal_date": report.get('date', ''),
                        "breakfast": '',
                        "lunch": '',
                        "dinner": ''
                    }
                    meal_date_rows.append(meal_date_row)

            meal_info = [report.get('opt_ins', '') for report in reports]
            # print("Meal Dates:", meal_info)  # Print meal_dates
            f_name = user_info.get("f_name", "")  # Extracting the first name
            l_name = user_info.get("l_name", "")
            full_name = f_name + " " + l_name
            email = user_info.get("email", "")
            is_veg = user_info.get("is_veg", "")
            deprt_id = user_info.get("department_id", "")
            reports_count = len(data.get("reports", []))
            # print("                       " + str(reports_count) + "                               ")
            meal_type = "Veg" if is_veg == "1" else "Non-Veg"
            names = [f_name] * reports_count
            user_meal_data = []
            for meal_row in meal_date_rows:
                # Check if any meal is pending
                # if "Pending" in [meal_row["breakfast"], meal_row["lunch"], meal_row["dinner"]]:
                #     penalty_applicable = "yes"
                # else:
                #     penalty_applicable = "No"
                pending_meals_count = sum(1 for meal in meal_row.values() if meal == "Pending")
                user_meal_data.append({
                    "meal_date": meal_row["meal_date"],
                    "name": full_name,
                    "dept_id": deprt_id,
                    "email": email,
                    "meal_type": meal_type,
                    "morg": meal_row["breakfast"],
                    "lunch": meal_row["lunch"],
                    "dinner": meal_row["dinner"],
                    "pen_decition": "Yes" if pending_meals_count > 0 else "No",
                    "missed_meal_count": pending_meals_count,
                    "penality_amt": pending_meals_count * 100 #calculating fine amount
                })
            meal_date_rows = []
            return user_meal_data
        else:
            print("API request failed with status code:", response.status_code)
    except Exception as e:
        print("Exception occurred:", e)

def get_filters(filters):
    pen_aplbe = filters.get("pen_aplbe") if filters else None
    is_veg = filters.get("is_veg") if filters else None
    month = filters.get("month") if filters else None
    data = call_api_and_get_data(month)
    
    filtered_data = data
    
    if pen_aplbe is not None:
        filtered_data = [item for item in filtered_data if item.get("pen_decition") == pen_aplbe]
    
    if is_veg is not None:
        if is_veg == 1:
            filtered_data = [item for item in filtered_data if item.get("meal_type") == "Veg"]
    
    print(filtered_data)
    return filtered_data
