# Secure User Authentication System

A full-stack web application implementing secure user registration, login, and role-based access control — built as part of the Prodigy InfoTech internship (Task-01).

## Features

- User registration with input validation
- Secure password hashing using bcrypt
- Login with JWT-based session tokens
- Protected routes (backend + frontend) accessible only after authentication
- Role-based access control (user vs admin)
- Persistent login using localStorage
- Clean, responsive UI built with React

## Tech Stack

**Backend:** Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Bcrypt, SQLite
**Frontend:** React (Vite), React Router, Axios

## Project Structure

```
secure-user-auth/
├── backend/
│   ├── app/
│   │   ├── __init__.py      # App factory, extensions setup
│   │   ├── config.py        # Configuration settings
│   │   ├── models.py        # User database model
│   │   └── routes.py        # Auth API endpoints
│   ├── run.py                # Entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/auth.js       # API call functions
│   │   ├── pages/            # Register, Login, Dashboard
│   │   ├── components/       # ProtectedRoute
│   │   └── App.jsx           # Routing setup
│   └── package.json
└── README.md
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|--------------|----------------|
| POST | `/api/auth/register` | Create new user account | No |
| POST | `/api/auth/login` | Login and receive JWT | No |
| GET | `/api/auth/me` | Get current user's profile | Yes |
| GET | `/api/auth/admin-only` | Example admin-only route | Yes (admin role) |

## Setup Instructions

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
python run.py
```
Backend runs on `http://127.0.0.1:5000`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`

## Security Notes

- Passwords are never stored in plain text — hashed using bcrypt before saving
- JWT tokens expire after 1 hour
- Login errors don't reveal whether a username exists (prevents enumeration attacks)
- Sensitive config (`.env` files) excluded from version control

## Possible Future Improvements

- Store JWTs in httpOnly cookies instead of localStorage for better XSS protection
- Add refresh tokens for longer sessions
- Add email verification on signup
- Add rate limiting on login attempts to prevent brute force attacks