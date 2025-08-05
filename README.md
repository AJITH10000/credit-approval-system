 Credit-Approval-System (Backend)

This is a Django-based backend project for a *Credit Approval System*, designed to handle loan customer registration, eligibility checking, and loan management. The system exposes RESTful APIs to support a modern credit approval process.

---

##  Features

-  Register a customer
-  Check loan eligibility
-  Create new loan for eligible customers
-  View individual loan details
-  View all loans for a specific customer

---

##  Tech Stack

- Python 3.13.1
- Django 5.2.4
- Django REST Framework
- SQLite (Default DB, can be switched to PostgreSQL)
- Postman for API Testing

---

##  Installation & Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/credit-approval-system.git
cd credit-approval-system

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
