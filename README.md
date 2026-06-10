# REST API Workflow & Validation System

## 📌 Project Overview
This project demonstrates a fully functional REST API simulating an e-commerce backend for user and shopping basket management[cite: 2, 4]. Developed in Python using the FastAPI framework, the system ensures robust data validation, structured JSON persistence, and comprehensive error handling[cite: 4, 5].

## 🛠️ Technologies & Tools
* **Backend Framework:** Python, FastAPI[cite: 4]
* **Data Modeling & Validation:** Pydantic[cite: 3]
* **API Testing:** Postman, Swagger UI[cite: 2]
* **Data Persistence:** Local JSON storage (`data.json`)[cite: 2, 5]

## 🚀 Key Endpoints
The API operates on localhost (`127.0.0.1:9000`) and provides the following core endpoints[cite: 2]:

* **`POST /adduser`**: Registers a new user and saves the record to the database[cite: 2]. Includes strict email format validation[cite: 3].
* **`POST /addshoppingbag`**: Generates and assigns a new, empty shopping basket to a specific user ID[cite: 2].
* **`POST /additem`**: Appends a specified product to a user's basket and returns the updated contents[cite: 2].
* **`GET /shoppingbag`**: Retrieves the complete list of items currently stored in a user's basket[cite: 2].
* **`GET /getusertotal`**: Calculates and returns the total payable amount based on the items and quantities in the basket[cite: 2].
* **`PUT /updateitem` & `DELETE /deleteitem`**: Allows for dynamic modification and removal of items within an active basket[cite: 4].

## 🛡️ Exception Handling & Validation
Ensuring system reliability was a primary focus during development. The API strictly handles invalid requests and missing data:

* **422 Unprocessable Entity:** Utilizing Pydantic schema validators, the system intercepts invalid data structures (e.g., negative prices or invalid email formats) and prevents them from reaching the database, returning a detailed `422` error to the client[cite: 2, 3].
  
  ![Validation Error] <!-- [KÉP HELYE: Illeszd be ide a 422-es hiba képét a 3.1-es pontból] -->

* **404 Not Found:** If a client attempts to query or modify non-existent data (such as requesting the basket of a user ID that does not exist), the system safely catches the exception and returns a `404` status code[cite: 2].
  
  ![Not Found Error] <!-- [KÉP HELYE: Illeszd be ide a 404-es hiba képét a 3.2-es pontból] -->

## ⚙️ How to Run & Test
1. Clone the repository and install the required dependencies (FastAPI, Uvicorn, Pydantic).
2. Start the server using Uvicorn. The API will be available at `http://127.0.0.1:9000`[cite: 2].
3. Navigate to `http://127.0.0.1:9000/docs` to access the built-in Swagger UI for interactive testing[cite: 2].
4. Alternatively, use Postman to send `POST` and `GET` requests with JSON payloads to validate the workflows[cite: 2].

  ![Postman Success] <!-- [KÉP HELYE: Illeszd be ide a sikeres 201 Created Postman képet a 2.1-es pontból] -->
