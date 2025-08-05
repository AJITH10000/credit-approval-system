from celery import shared_task
import pandas as pd
from .models import Customer, Loan

@shared_task
def ingest_customer_data():
    df = pd.read_excel('customer_data.xlsx')
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            phone_number=row['phone_number'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'monthly_salary': row['monthly_salary'],
                'approved_limit': row['approved_limit'],
                'current_debt': row['current_debt']
            }
        )

@shared_task
def ingest_loan_data():
    df = pd.read_excel('loan_data.xlsx')
    for _, row in df.iterrows():
        customer = Customer.objects.get(id=row['customer_id'])
        Loan.objects.update_or_create(
            customer=customer,
            loan_amount=row['loan_amount'],
            interest_rate=row['interest_rate'],
            tenure=row['tenure'],
            emi=row['monthly_repayment'],
            emis_paid_on_time=row['EMIs paid on time'],
            start_date=row['start_date'],
            end_date=row['end_date']
        )
