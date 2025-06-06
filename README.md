# Order Management System Template

This project is a robust template for an Order Management System backend, built with Django Rest Framework (DRF). It demonstrates integration of Google OAuth 2.0 authentication and secure, user-specific data entry and retrieval APIs.

## Features

- **Google OAuth 2.0 Authentication**: Secure login using Google accounts, returning JWT access and refresh tokens.
- **Data Entry API**: Authenticated users can add items (with `title` and `description`) to their account.
- **Data Retrieval API**: Authenticated users can fetch their items, with optional filtering by title.

## Technologies Used

- Django 5.x
- Django Rest Framework
- Simple JWT for authentication
- Google OAuth 2.0
- python-dotenv for environment variable management
- django-cors-headers

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Create and Configure Environment Variables

Copy `.env.example` to `.env` and fill in your Google OAuth credentials:

```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=your-google-redirect-uri
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Apply Migrations

```sh
python manage.py migrate
```

### 5. Run the Development Server

```sh
python manage.py runserver
```

## API Endpoints

### 1. Google OAuth 2.0 Authentication

- **POST** `/api/google-auth/`
    - Request: `{ "code": "<authorization_code_from_google>" }`
    - Response: `{ "refresh": "<refresh_token>", "access": "<access_token>" }`
    - Use Postman or your frontend to initiate the OAuth flow and exchange the code.

### 2. Add Item

- **POST** `/api/add-item/`
    - Headers: `Authorization: Bearer <access_token>`
    - Body: `{ "title": "Sample Title", "description": "Sample Description" }`
    - Response: Created item data.

### 3. Get Items

- **GET** `/api/get-items/?title=<optional_title_filter>`
    - Headers: `Authorization: Bearer <access_token>`
    - Response: List of items belonging to the authenticated user, filtered by title if provided.

## Security Notes

- **Sensitive keys** are loaded from environment variables using `python-dotenv`. Never commit your `.env` file.
- All data APIs are protected and require JWT authentication.
- CORS is enabled for all origins for development; restrict this in production.

## Project Structure

- [`api/models.py`](api/models.py): Defines the `Item` model.
- [`api/views.py`](api/views.py): Implements Google OAuth, add item, and get items APIs.
- [`api/serializers.py`](api/serializers.py): Serializes the `Item` model.
- [`api/urls.py`](api/urls.py): API endpoint routing.
- [`ordermanagement/settings.py`](ordermanagement/settings.py): Project settings, including REST and JWT configuration.

## How Components Work Together

- Users authenticate via Google OAuth and receive JWT tokens.
- Authenticated users can add and retrieve their own items.
- All sensitive configuration is handled via environment variables.

---

**For any issues or questions, please refer to the code comments or reach out as instructed in the assignment.**
