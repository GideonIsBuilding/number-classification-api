from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Load Numbers API URL from environment variable (defaulting to the public API if not set)
NUMBERS_API_URL = os.getenv("NUMBERS_API_URL", "http://numbersapi.com")

def is_prime(n):
    """
    Check if a number is prime.
    
    Args:
        n (int): The number to check.
    
    Returns:
        bool: True if the number is prime, False otherwise.
    """
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):  # Only check up to the square root of n
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """
    Check if a number is a perfect number.
    A perfect number is a number whose sum of divisors (excluding itself) equals itself.
    
    Args
        n (int): Integer number to check
    
    Returns:
        bool: True if perfect, False otherwise
    """
    if n < 2:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n

def is_armstrong(n):
    """
    Check if a number is an Armstrong number.
    An Armstrong number is one where the sum of its own digits each raised to the power of the number of digits equals itself.
    
    Args:
        n (int): Integer number to check
    
    Returns
        bool: True if Armstrong number, False otherwise
    """
    digits = [int(d) for d in str(n)]  # Extract digits
    num_digits = len(digits)
    return sum(d ** num_digits for d in digits) == n

def digit_sum(n):
    """
    Compute the sum of digits of a number.
    
    Args:
        n (int): Integer number
    
    Returns:
        int: Sum of digits of n
    """
    return sum(int(d) for d in str(n))

def get_fun_fact(n):
    """
    Fetch a fun math fact about the given number from the Numbers API.
    If the API is unavailable, return a fallback fact based on Armstrong number check.
    
    Args:
        n (int): Integer number
    
    Returns:
        string: A fun fact
    """
    if len(str(n)) > 10:
        return f"{n} is too large to process for fun facts."
    # First, check if the number is an Armstrong number
    if is_armstrong(n):
        return f"{n} is an Armstrong number because {' + '.join(f'{d}^{len(str(n))}' for d in str(n))} = {n}"
    
    try:
        # Making a request to Numbers API to fetch a math-related fact
        response = requests.get(f"{NUMBERS_API_URL}/{n}/math", timeout=5)
        if response.status_code == 200:
            return response.text  # Return the API response as the fun fact
    except requests.RequestException:
        pass  # If the API fails, use the fallback logic
    
    return f"{n} is a fascinating number!"

# API route to classify numbers and return various properties
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """
    API endpoint to classify a number and return its properties.
    
    Query Args:
        number: The number to classify
    
    Returns:
        object: JSON containing classification details
    """
    number = request.args.get('number')  # Get number from query parameters
    if number is None:
        return jsonify({"number": "missing input", "error": True}), 400
    if not number.lstrip('-').isdigit():  # Check if input is not a number
        return jsonify({"number": "alphabet", "error": True}), 400
    number = int(number)
    if number < 0:
        return jsonify({"number": "negative number", "error": True}), 400
    
    number = int(number)
    properties = []
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 != 0:
        properties.append("odd")
    
    # Return JSON response containing number properties and a fun fact
    return jsonify({
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)  # Run the Flask app in debug mode
