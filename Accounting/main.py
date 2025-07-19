from dateutil.utils import today
from application.salary import calculate_salary,create_db
from application.db.people import get_employees
from datetime import datetime


if __name__ == '__main__':
    create_db()
    print(calculate_salary(100, 100, 20))
    get_employees(r'C:\Users\serge\PyCharmMiscProject\Учеба\py-homeworks-advanced\py-homeworks-advanced\1.Import.Module.Package\Accounting\application\db\data.json')
    print(datetime.date(today()))