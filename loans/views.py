# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.http import JsonResponse

# def root_view(request):
#     return JsonResponse({"message": "Credit Approval System Backend is Live"})


# @api_view(['POST'])
# def register_customer(request):
#     return Response({"message": "Register endpoint working."})

# @api_view(['POST'])
# def check_eligibility(request):
#     return Response({"message": "Check eligibility endpoint working."})

# @api_view(['POST'])
# def create_loan(request):
#     return Response({"message": "Create loan endpoint working."})

# @api_view(['GET'])
# def view_loan(request, loan_id):
#     return Response({"message": f"View loan {loan_id} endpoint working."})

# @api_view(['GET'])
# def view_loans_by_customer(request, customer_id):
#     return Response({"message": f"View loans for customer {customer_id} endpoint working."})



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse
from .models import Customer, Loan
from django.shortcuts import get_object_or_404
from django.db import IntegrityError



def root_view(request):
    return JsonResponse({"message": "Credit Approval System Backend is Live"})


# @api_view(['GET', 'POST'])
# def register_customer(request):
#     if request.method == 'GET':
#         return Response({"message": "Register endpoint ready. Use POST to send data."})
    
#     data = request.data
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')
#     age = data.get('age')
#     salary = data.get('monthly_income')
#     phone = data.get('phone_number')

#     approved_limit = round(salary * 36, -5)

#     customer = Customer.objects.create(
#         first_name=first_name,
#         last_name=last_name,
#         age=age,
#         monthly_salary=salary,
#         approved_limit=approved_limit,
#         phone_number=phone
#     )

#     return Response({
#         "message": "Customer registered successfully",
#         "customer_id": customer.id,
#         "approved_limit": approved_limit
#     })

@api_view(['POST'])
def register_customer(request):
    try:
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        age = request.data.get('age')
        income = request.data.get('monthly_income')
        phone = request.data.get('phone_number')

        # Check if customer already exists
        if Customer.objects.filter(phone_number=phone).exists():
            return Response(
                {"error": "Customer with this phone number already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        approved_limit = round(0.36 * income, -5)

        customer = Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            monthly_salary=income,
            approved_limit=approved_limit,
            phone_number=phone
        )

        return Response(
            {"message": "Customer registered successfully."},
            status=status.HTTP_201_CREATED
        )
    except IntegrityError as e:
        return Response(
            {"error": "Duplicate phone number. Customer already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def check_eligibility(request):
    data = request.data
    customer_id = data.get("customer_id")
    requested_amount = data.get("loan_amount")
    interest_rate = 0.10
    tenure_years = 5

    customer = get_object_or_404(Customer, pk=customer_id)

    # Simple eligibility logic
    max_loan_amount = customer.monthly_income * 20
    is_eligible = requested_amount <= max_loan_amount

    return Response({
        "is_eligible": is_eligible,
        "approved_amount": min(requested_amount, max_loan_amount),
        "interest_rate": interest_rate,
        "tenure": tenure_years
    })


@api_view(['POST'])
def create_loan(request):
    data = request.data
    customer_id = data.get("customer_id")
    loan_amount = data.get("loan_amount")
    interest_rate = data.get("interest_rate")
    tenure = data.get("tenure")

    customer = get_object_or_404(Customer, pk=customer_id)

    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        interest_rate=interest_rate,
        tenure=tenure
    )

    return Response({
        "message": "Loan created successfully",
        "loan_id": loan.id
    })


@api_view(['GET'])
def view_loan(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    return Response({
        "loan_id": loan.id,
        "customer_id": loan.customer.id,
        "loan_amount": loan.loan_amount,
        "interest_rate": loan.interest_rate,
        "tenure": loan.tenure,
        "created_at": loan.created_at
    })


@api_view(['GET'])
def view_loans_by_customer(request, customer_id):
    loans = Loan.objects.filter(customer_id=customer_id)
    loan_list = [{
        "loan_id": loan.id,
        "amount": loan.loan_amount,
        "interest_rate": loan.interest_rate,
        "tenure": loan.tenure,
        "created_at": loan.created_at
    } for loan in loans]

    return Response({
        "customer_id": customer_id,
        "loans": loan_list
    })
