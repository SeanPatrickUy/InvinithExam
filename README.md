## Invinith Technical Exam ##

## Features

- **Add, Update, and Delete Recipes**
- **Rate Recipes (1-5 stars)**
- **Add and Retrieve Comments for Recipes**
- **Stored in a SQL Server database**

## Prerequisites

- **Docker**: Ensure Docker is installed and running on your system.
- **Docker Compose**: Required to run the multi-container setup with Flask and SQL Server.

## Getting Started

- Follow the steps below to get the project up and running on your local machine.

## 1. Clone the Repository

- **bash**
- git clone https://github.com/yourusername/recipe-management-api.git
- cd recipe-management-api

## 2. Build and Run the Application with Docker Compose

- **bash**
- docker-compose up --build

## 3. Accessing the API

- Base URL: http://127.0.0.1:5000

- **Example Usage**
- GET /recipes: Get all recipes
- POST /recipes: Add a new recipe
- GET /recipes/{id}: Get a recipe by ID
- PUT /recipes/{id}: Update a recipe by ID
- DELETE /recipes/{id}: Delete a recipe by ID
- POST /recipes/{id}/ratings: Add a rating to a recipe (1-5)
- POST /recipes/{id}/comments: Add a comment to a recipe
- GET /recipes/{id}/comments: Get all comments for a recipe

## 4. Stopping the Application

- **bash**
- docker-compose down