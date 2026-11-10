# Note-Taking App

A full-stack note-taking application with a Node.js + Express backend and a Python Streamlit frontend.

## Live App

👉 **Open the app locally:** [http://localhost:8501](http://localhost:8501)

This link works only on the computer where the app is running. Start the backend and Streamlit frontend using the instructions below first.

## Overview

This project allows users to:
- sign up and log in securely
- create, view, update, and delete personal notes
- keep each note tied to the user who created it
- access the app through a clean Streamlit interface

## Features

- Secure user authentication using JWT tokens
- Password hashing with bcrypt
- CRUD operations for personal notes
- Input validation for signup, login, and note creation/update
- User-specific access control so one user cannot view another user's notes
- REST API with consistent JSON error responses

## Tech Stack

- Frontend: Streamlit (Python)
- Backend: Node.js, Express.js
- Database: MySQL
- Authentication: JWT + bcrypt

## Project Structure

```text
Note-Taking App/
├── README.md
├── .gitignore
├── backend/
│   ├── .env.example
│   ├── package.json
│   ├── package-lock.json
│   ├── schema.sql
│   └── src/
│       ├── db.js
│       ├── server.js
│       ├── middleware/
│       │   └── auth.js
│       └── routes/
│           ├── auth.js
│           └── notes.js
└── frontend/
    ├── app.py
    └── requirements.txt
```

## Prerequisites

Before running the app, make sure you have:
- Node.js installed
- Python 3.10+ installed
- MySQL server running locally
- Access to the MySQL root user or a configured database user

## Setup

### 1. Create the database

```bash
mysql -u root -p < backend/schema.sql
```

### 2. Configure backend environment

```bash
cd backend
copy .env.example .env
```

Then update the values in `.env` with your local database settings and a long, random JWT secret. Do not commit `.env` or real credentials.

Example:

```env
PORT=5000
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=infrasity_assignment
JWT_SECRET=your_secret_key
```

### 3. Install backend dependencies

```bash
cd backend
npm install
```

### 4. Start the backend server

```bash
cd backend
npm start
```

The backend will run at:

```text
http://localhost:5000
```

### 5. Install frontend dependencies

Open a new terminal and run:

```bash
cd frontend
pip install -r requirements.txt
```

### 6. Start the Streamlit app

```bash
cd frontend
streamlit run app.py
```

The frontend will run at:

```text
http://localhost:8501
```

## How to Use

1. Open the app in your browser at [http://localhost:8501](http://localhost:8501)
2. Click **Sign up** and create an account
3. Log in with your email and password
4. Add a new note with a title and content
5. View all your notes in the dashboard
6. Edit or delete notes as needed
7. Click **Log out** when finished

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/signup` | No | Register a new user |
| POST | `/api/auth/login` | No | Log in and receive a JWT |
| GET | `/api/notes` | Yes | Fetch all notes for the logged-in user |
| GET | `/api/notes/:id` | Yes | Fetch one specific note |
| POST | `/api/notes` | Yes | Create a new note |
| PUT | `/api/notes/:id` | Yes | Update a note |
| DELETE | `/api/notes/:id` | Yes | Delete a note |

## Security Notes

- JWTs are verified before accessing protected routes
- The user ID is always taken from the verified token, never from the request body
- All database queries use parameterized SQL
- Each note query is filtered by `user_id` to prevent unauthorized access
- `.env` should remain local and private and should not be committed to version control

## License

This project is intended for learning and personal use.
