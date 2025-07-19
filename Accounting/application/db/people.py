import json


def get_employees(data):
    with open(data, 'r', encoding='utf-8') as f:
        data1 = json.load(f).get('employees')
    for employee in data1:
        print(employee['name'])


# get_employees('data.json')
