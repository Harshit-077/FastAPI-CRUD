# FastAPI CRUD API

A simple REST API built with **FastAPI**, **SQLModel**, and **PostgreSQL** for managing campaigns.

The project demonstrates the fundamentals of building a database-backed CRUD API with request validation, dependency injection, SQLModel sessions, and automatic API documentation.

## Tech Stack

* **Python 3.12.14**
* **FastAPI**
* **SQLModel**
* **PostgreSQL**
* **Pydantic**
* **psycopg**
* **python-dotenv**
* **uv** for dependency management

## Features

* Create campaigns
* Retrieve all campaigns
* Retrieve a campaign by ID
* Update campaigns
* Delete campaigns
* PostgreSQL persistence
* Pydantic/SQLModel request validation
* Automatic database table creation
* Automatic seed data for development
* Interactive Swagger API documentation

## Project Structure

```text
FastAPI-CRUD/
├── main.py
├── pyproject.toml
├── uv.lock
├── .env.example
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Harshit-077/FastAPI-CRUD.git
cd FastAPI-CRUD
```

### 2. Install dependencies

This project uses `uv` for dependency management.

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Update the PostgreSQL credentials in `.env`.

### 4. Create the PostgreSQL database

Make sure PostgreSQL is running and create the database specified by `POSTGRES_DB`.

For example:

```sql
CREATE DATABASE fastapi_crud;
```

The application creates the required `campaign` table automatically when it starts.

### 5. Start the server

```bash
uv run fastapi dev main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/api/v1/docs
```

### ReDoc

```text
http://127.0.0.1:8000/api/v1/redoc
```

## API Endpoints

| Method   | Endpoint                 | Description          |
| -------- | ------------------------ | -------------------- |
| `GET`    | `/api/v1/campaigns`      | Get all campaigns    |
| `GET`    | `/api/v1/campaigns/{id}` | Get a campaign by ID |
| `POST`   | `/api/v1/campaigns`      | Create a campaign    |
| `PUT`    | `/api/v1/campaigns/{id}` | Update a campaign    |
| `DELETE` | `/api/v1/campaigns/{id}` | Delete a campaign    |

## Example Requests

### Create Campaign

```http
POST /api/v1/campaigns
Content-Type: application/json
```

```json
{
  "name": "Winter Campaign",
  "due_date": "2026-12-01T10:00:00"
}
```

### Response

```json
{
  "data": {
    "id": 3,
    "name": "Winter Campaign",
    "due_date": "2026-12-01T10:00:00",
    "created_at": "2026-09-16T10:00:00"
  }
}
```

### Get All Campaigns

```http
GET /api/v1/campaigns
```

### Get Campaign by ID

```http
GET /api/v1/campaigns/1
```

### Update Campaign

```http
PUT /api/v1/campaigns/1
Content-Type: application/json
```

```json
{
  "name": "Updated Campaign",
  "due_date": "2026-12-15T10:00:00"
}
```

### Delete Campaign

```http
DELETE /api/v1/campaigns/1
```

A successful deletion returns:

```text
204 No Content
```

## Database

The application uses **PostgreSQL** as its database and **SQLModel** as the ORM/model layer.

At application startup:

1. The database connection is created from environment variables.
2. SQLModel creates the required tables if they do not already exist.
3. Development seed campaigns are inserted if the `campaign` table is empty.

The application currently uses the following database configuration:

```text
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
```

## Environment Variables

See [`.env.example`](.env.example) for the required configuration.

**Never commit your actual `.env` file or database credentials to Git.**

## Error Handling

The API returns appropriate HTTP status codes for common situations:

* `200 OK` — Successful request
* `201 Created` — Resource successfully created
* `204 No Content` — Resource successfully deleted
* `404 Not Found` — Campaign does not exist
* `422 Unprocessable Entity` — Request validation failed

## Learning Goals

This project was built to practice:

* REST API design
* FastAPI routing
* Request and response validation
* Dependency injection
* SQLModel models and sessions
* PostgreSQL integration
* CRUD operations
* Environment-based configuration
* API documentation with OpenAPI/Swagger

## License

This project is intended for learning and educational purposes.
