# Number Classification API

## Introduction
This is a simple **Flask API** that classifies numbers based on their mathematical properties. It can determine whether a number is **prime, perfect, or an Armstrong number** and provides a **fun fact** about the number. If the number is too large, negative, or invalid, the API handles those cases gracefully.

## Features
✅ Check if a number is **prime** (only divisible by 1 and itself).  
✅ Check if a number is **perfect** (sum of its divisors equals itself).  
✅ Check if a number is an **Armstrong number** (sum of its digits raised to the power of the number of digits equals itself).  
✅ Calculate the **sum of its digits**.  
✅ Fetch a **fun fact** about the number from the Numbers API.  
✅ Handle large numbers, negative numbers, and invalid inputs properly.

## How It Works
The API takes a number as input through a **GET request** and returns a JSON response with its classification and a fun fact.

## Getting Started
### Prerequisites
Before running the API, ensure you have the following installed:
- Python 3
- pip (Python package manager)

### Installation
1. **Clone the repository** (if using version control):
   ```bash
   git clone https://github.com/gideonisbuilding/number-classification-api.git
   cd number-classification-api
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the API:**
   ```bash
   python api.py
   ```
   By default, the API will start at: `http://127.0.0.1:5000/`

## API Usage
### **Endpoint: `/api/classify-number`**
#### **Request:**
Make a **GET** request with a `number` parameter:
```bash
http://127.0.0.1:5000/api/classify-number?number=28
```
#### **Response Example:**
```json
{
    "number": 28,
    "is_prime": false,
    "is_perfect": true,
    "properties": ["perfect"],
    "digit_sum": 10,
    "fun_fact": "28 is a perfect number because its divisors sum to itself."
}
```

### Handling Errors
| Scenario            | Response Example |
|---------------------|-----------------|
| Missing input      | `{ "number": "missing input", "error": true }` |
| Non-numeric input  | `{ "number": "alphabet", "error": true }` |
| Negative number    | `{ "number": "negative number", "error": true }` |

## Configuration
The API fetches fun facts using the **Numbers API** (`http://numbersapi.com`). This URL can be customized using an **environment variable**:
```bash
export NUMBERS_API_URL="https://your-custom-api.com"
```
This makes it easy to switch data sources if needed.

## Running Tests
To ensure everything works as expected, run:
```bash
pytest test_api.py -v
```
This will check various cases such as prime detection, error handling, and fun fact retrieval.
