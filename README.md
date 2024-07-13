# Spam Detection and Contact Search API

This project provides a REST API for a mobile app that allows users to detect spam phone numbers and search for contacts by phone number or name. The API is built using Django and Django REST Framework, ensuring performance, security, and scalability. The API supports functionalities such as user registration, login, contact management, and spam detection.

## Features

- **User Registration and Authentication**
  - Register new users with a name, phone number, password, and optionally an email address.
  - Authenticate users and generate tokens for API access.
- **Contact Management**

  - Save personal contacts for each registered user.
  - Import phone contacts automatically into the app's database.

- **Spam Detection**

  - Mark phone numbers as spam to alert other users.

- **Search Functionality**
  - Search for contacts by name or phone number in the global database.
  - Display search results with details like name, phone number, and spam likelihood.
  - Show additional details if the person is a registered user and the searcher is in their contact list.

## Installation

To get started with the project, follow these steps:

### Prerequisites

- Python 3.x
- Django
- Django REST Framework
- SQLite (default for Django)

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install dependencies:**

   ```bash
   pip install django djangorestframework
   ```

3. **Apply migrations:**

   ```bash
   python manage.py makemigrations api
   python manage.py migrate
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Usage

1. **Create users via Django admin or register using the API.**
2. **Login using the API and generate an authentication token.**
3. **Use the token to access the following functionalities:**
   - Mark a number as spam.
   - Save contacts.
   - Get contacts.
   - Search by phone number.
   - Search by name.

## API Endpoints

- **Registration:** `/api/register/`
- **Login:** `/api/login/`
- **Mark Spam:** `/api/mark_spam/`
- **Save Contacts:** `/api/contacts/`
- **Get Contacts:** `/api/contacts/`
- **Search by Phone Number:** `/api/search/phone/`
- **Search by Name:** `/api/search/name/`




