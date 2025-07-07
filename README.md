**Travel Booking Application**
A simple travel booking web application built using Python Django that allows users to:
View available travel options, Book tickets, Manage their bookings with profile management

Features
- User registration, login, logout, profile update
- Travel options listing with filters (type, source, destination, date, price range)
- Booking system with seat availability updates
- View current and past bookings
- Cancel bookings
- Responsive UI with Bootstrap
- MySQL database integration

Tech Stack
- Backend: Python, Django
- Frontend: Django Templates, HTML, CSS, Bootstrap
- Database: MySQL

**Instructions to setup the project locally**

1. Clone the Repository
git clone https://github.com/maithilimahadik/Travel-Booking-Application.git
cd travel_booking

2. Create a Virtual Environment
python -m venv venv

Activate the environment:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Database Using MySQL
1. Install MySQL server locally and create a database travel_db.
2. Update DATABASES config in settings.py with your MySQL username and password as given below:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'travel_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
3. Run migrations:
python manage.py makemigrations
python manage.py migrate

5. Create Superuser
python manage.py createsuperuser
Follow prompts to set username, email, password.

6. Collect static files
python manage.py collectstatic

7. Run the development server
python manage.py runserver
Visit:
http://127.0.0.1:8000/

The app should then load locally.

8. To access the Admin Panel
Go to:
http://127.0.0.1:8000/admin
Login with superuser credentials(created in step 5) to add Travel Options data for testing.
