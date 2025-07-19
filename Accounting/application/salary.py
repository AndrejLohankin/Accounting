import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
from datetime import datetime
import json

def create_db():
    Base = declarative_base()

    class Employee(Base):
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        position = Column(String)
        base_salary = Column(Float, nullable=False)
        hired_date = Column(Date)
        is_active = Column(Boolean, default=True)
        work_logs = relationship('WorkLog', back_populates='employee')
        bonuses = relationship('Bonus', back_populates='employee')
        penalties = relationship('Penalty', back_populates='employee')
        salaries = relationship('Salary', back_populates='employee')

    class WorkLog(Base):
        __tablename__ = 'work_log'
        id = Column(Integer, primary_key=True)
        employee_id = Column(Integer, ForeignKey('employee.id'))
        work_date = Column(Date)
        hours_worked = Column(Float)
        employee = relationship('Employee', back_populates='work_logs')

    class Bonus(Base):
        __tablename__ = 'bonus'
        id = Column(Integer, primary_key=True)
        employee_id = Column(Integer, ForeignKey('employee.id'))
        amount = Column(Float)
        reason = Column(Text)
        date_given = Column(Date)
        employee = relationship('Employee', back_populates='bonuses')


    class Penalty(Base):
        __tablename__ = 'penalty'
        id = Column(Integer, primary_key=True)
        employee_id = Column(Integer, ForeignKey('employee.id'))
        amount = Column(Float)
        reason = Column(Text)
        date_given = Column(Date)
        employee = relationship('Employee', back_populates='penalties')


    class Salary(Base):
        __tablename__ = 'salary'
        id = Column(Integer, primary_key=True)
        employee_id = Column(Integer, ForeignKey('employee.id'))
        month = Column(String)  # формат YYYY-MM
        base_amount = Column(Float)
        bonus_amount = Column(Float)
        penalty_amount = Column(Float)
        total_amount = Column(Float)
        generated_at = Column(Date)
        employee = relationship('Employee', back_populates='salaries')


    def create_tables(engine):
        Base.metadata.create_all(engine)

    def drop_tables(engine):
        Base.metadata.drop_all(engine)

    def load_data():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        with open(r'C:\Users\serge\PyCharmMiscProject\Учеба\py-homeworks-advanced\py-homeworks-advanced\1.Import.Module.Package\Accounting\application\db\data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        session = Session()
        employee_cache = {}
        for emp_data in data['employees']:
            employee = Employee(**emp_data)
            session.add(employee)
            session.flush()  # чтобы получить ID
            employee_cache[employee.name] = employee
        for log in data['work_logs']:
            employee = employee_cache.get(log['employee_name'])
            if employee:
                work_log = WorkLog(
                    employee_id=employee.id,
                    work_date=datetime.strptime(log['work_date'], '%Y-%m-%d').date(),
                    hours_worked=log['hours_worked']
                )
                session.add(work_log)
        for bonus in data['bonuses']:
            employee = employee_cache.get(bonus['employee_name'])
            if employee:
                bonus_entry = Bonus(
                    employee_id=employee.id,
                    amount=bonus['amount'],
                    reason=bonus['reason'],
                    date_given=datetime.strptime(bonus['date_given'], '%Y-%m-%d').date()
                )
                session.add(bonus_entry)
        for penalty in data['penalties']:
            employee = employee_cache.get(penalty['employee_name'])
            if employee:
                penalty_entry = Penalty(
                    employee_id=employee.id,
                    amount=penalty['amount'],
                    reason=penalty['reason'],
                    date_given=datetime.strptime(penalty['date_given'], '%Y-%m-%d').date()
                )
                session.add(penalty_entry)
        for salary in data['salaries']:
            employee = employee_cache.get(salary['employee_name'])
            if employee:
                total = calculate_salary(
                    salary['base_amount'],
                    salary['bonus_amount'],
                    salary['penalty_amount']
                )
                salary_entry = Salary(
                    employee_id=employee.id,
                    month=salary['month'],
                    base_amount=salary['base_amount'],
                    bonus_amount=salary['bonus_amount'],
                    penalty_amount=salary['penalty_amount'],
                    total_amount=total,
                    generated_at=datetime.strptime(salary['generated_at'], '%Y-%m-%d').date()
                )
                session.add(salary_entry)
        session.commit()
        session.close()
        print("Данные успешно загружены.")

    load_dotenv()
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = sqlalchemy.create_engine(DSN)
    Session = sessionmaker(bind=engine)

    load_data()

def calculate_salary(base_amount: float, bonus_amount: float, penalty_amount: float) -> float:
    total_amount = base_amount + bonus_amount - penalty_amount
    return total_amount
