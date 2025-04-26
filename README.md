# Learn Python Through a Project: Personal Finance Manager

## Project Overview

We'll create a console-based application that:
1. Tracks income and expenses
2. Categorizes transactions
3. Generates reports
4. Saves data to files
5. Connects to a currency exchange API
6. Uses a database for persistence

## Step-by-Step Implementation

### 1. Basic Setup and Data Types

```python
# main.py
import json
import csv
import os
from datetime import datetime
import requests
import asyncio
import sqlite3
from typing import List, Dict, Tuple, Optional

# Basic data types in Python
initial_balance: float = 0.0  # float
app_name: str = "Personal Finance Manager"  # string
is_active: bool = True  # boolean
version: int = 1  # integer
```

### 2. Variables and Arithmetic Operators

```python
class Transaction:
    def __init__(self, amount: float, category: str, description: str, date: str):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def __repr__(self):
        return f"{self.date} - {self.category}: ${self.amount:.2f} ({self.description})"
```

### 3. Conditional Operators and Functions

```python
def categorize_transaction(amount: float) -> str:
    """Categorize transaction based on amount"""
    if amount > 1000:
        return "Large Income" if amount > 0 else "Major Expense"
    elif amount > 100:
        return "Medium Income" if amount > 0 else "Medium Expense"
    else:
        return "Small Income" if amount > 0 else "Small Expense"
```

### 4. Lists and Tuples

```python
class FinanceManager:
    def __init__(self):
        self.transactions: List[Transaction] = []  # List
        self.categories: Tuple[str, ...] = (  # Tuple
            "Food", "Transport", "Entertainment", 
            "Utilities", "Salary", "Investment"
        )
        
    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        
    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        return [t for t in self.transactions if t.category == category]
```

### 5. Dictionaries and Nested Dictionaries

```python
    def generate_report(self) -> Dict[str, Dict[str, float]]:
        """Generate a nested dictionary report"""
        report = {
            "income": {"total": 0.0, "categories": {}},
            "expenses": {"total": 0.0, "categories": {}}
        }
        
        for t in self.transactions:
            if t.amount > 0:
                report["income"]["total"] += t.amount
                report["income"]["categories"].setdefault(t.category, 0.0)
                report["income"]["categories"][t.category] += t.amount
            else:
                report["expenses"]["total"] += abs(t.amount)
                report["expenses"]["categories"].setdefault(t.category, 0.0)
                report["expenses"]["categories"][t.category] += abs(t.amount)
                
        return report
```

### 6. Working with Files

```python
    def save_to_file(self, filename: str, format_type: str = "json"):
        """Save transactions to file in different formats"""
        data = [vars(t) for t in self.transactions]
        
        try:
            if format_type == "json":
                with open(f"{filename}.json", "w") as f:
                    json.dump(data, f, indent=2)
            elif format_type == "csv":
                with open(f"{filename}.csv", "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=["amount", "category", "description", "date"])
                    writer.writeheader()
                    writer.writerows(data)
            print(f"Data saved to {filename}.{format_type}")
        except IOError as e:
            print(f"Error saving file: {e}")
            
    def load_from_file(self, filename: str):
        """Load transactions from file"""
        try:
            if filename.endswith(".json"):
                with open(filename, "r") as f:
                    data = json.load(f)
                    self.transactions = [Transaction(**item) for item in data]
            elif filename.endswith(".csv"):
                with open(filename, "r") as f:
                    reader = csv.DictReader(f)
                    self.transactions = [Transaction(
                        float(row["amount"]),
                        row["category"],
                        row["description"],
                        row["date"]
                    ) for row in reader]
            print(f"Data loaded from {filename}")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading file: {e}")
```

### 7. Error Handling

```python
    def get_transaction_by_index(self, index: int) -> Optional[Transaction]:
        """Safely get transaction by index with error handling"""
        try:
            return self.transactions[index]
        except IndexError:
            print(f"Error: No transaction at index {index}")
            return None
        except TypeError:
            print("Error: Index must be an integer")
            return None
```

### 8. Object-Oriented Programming and Encapsulation

```python
class User:
    def __init__(self, username: str, email: str):
        self.__username = username  # Private attribute
        self.__email = email
        self.__password_hash = None
        
    @property
    def username(self) -> str:
        return self.__username
        
    def set_password(self, password: str):
        """Encapsulation example - hide password hashing"""
        import hashlib
        self.__password_hash = hashlib.sha256(password.encode()).hexdigest()
        
    def verify_password(self, password: str) -> bool:
        import hashlib
        return self.__password_hash == hashlib.sha256(password.encode()).hexdigest()
```

### 9. Inheritance

```python
class PremiumUser(User):
    def __init__(self, username: str, email: str, premium_level: int):
        super().__init__(username, email)
        self.premium_level = premium_level
        self.__premium_features = ["Advanced Reports", "Budget Forecasting"]
        
    def get_features(self) -> List[str]:
        return self.__premium_features + ["Basic Features"]
```

### 10. Decorators and Lambda Functions

```python
def log_operation(func):
    """Decorator to log function calls"""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

class FinanceManager:
    # ... previous code ...
    
    @log_operation
    def calculate_balance(self) -> float:
        """Calculate current balance"""
        return sum(t.amount for t in self.transactions)
    
    def filter_transactions(self, condition) -> List[Transaction]:
        """Use lambda function to filter transactions"""
        return list(filter(condition, self.transactions))
```

### 11. Working with JSON

```python
    def export_report_json(self, filename: str):
        """Export report to JSON file"""
        report = self.generate_report()
        try:
            with open(filename, "w") as f:
                json.dump(report, f, indent=2)
            print(f"Report exported to {filename}")
        except IOError as e:
            print(f"Error exporting report: {e}")
```

### 12. Modules and Packages

Create a new file `currency.py`:

```python
# currency.py
import requests

EXCHANGE_RATE_API = "https://api.exchangerate-api.com/v4/latest/USD"

def get_exchange_rates() -> dict:
    """Get current exchange rates"""
    response = requests.get(EXCHANGE_RATE_API)
    return response.json().get("rates", {})
```

Then in main.py:

```python
from currency import get_exchange_rates

class FinanceManager:
    # ... previous code ...
    
    def convert_currency(self, amount: float, from_curr: str, to_curr: str) -> float:
        """Convert amount from one currency to another"""
        rates = get_exchange_rates()
        if from_curr not in rates or to_curr not in rates:
            raise ValueError("Invalid currency code")
        return amount * rates[to_curr] / rates[from_curr]
```

### 13. Working with APIs

```python
async def fetch_financial_news(limit: int = 5) -> List[str]:
    """Asynchronously fetch financial news"""
    API_URL = "https://newsapi.org/v2/everything?q=finance&apiKey=YOUR_API_KEY"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            data = await response.json()
            return [article["title"] for article in data.get("articles", [])[:limit]]
```

### 14. Asynchronous Programming

```python
async def main_async_operations():
    """Run async operations concurrently"""
    news_task = asyncio.create_task(fetch_financial_news())
    exchange_task = asyncio.create_task(get_exchange_rates())
    
    news, rates = await asyncio.gather(news_task, exchange_task)
    print("Latest Financial News:", news[:2])
    print("USD Exchange Rates:", list(rates.items())[:3])
```

### 15. Database (SQLite)

```python
class FinanceDatabase:
    def __init__(self, db_name: str = "finance.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        
    def create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        """)
        self.conn.commit()
        
    def save_transaction(self, transaction: Transaction):
        """Save transaction to database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (amount, category, description, date)
            VALUES (?, ?, ?, ?)
        """, (transaction.amount, transaction.category, 
              transaction.description, transaction.date))
        self.conn.commit()
        
    def get_all_transactions(self) -> List[Transaction]:
        """Retrieve all transactions from database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT amount, category, description, date FROM transactions")
        return [Transaction(*row) for row in cursor.fetchall()]
    
    def close(self):
        self.conn.close()
```

## Putting It All Together

```python
def main():
    # Initialize components
    manager = FinanceManager()
    db = FinanceDatabase()
    user = User("john_doe", "john@example.com")
    user.set_password("secure123")
    
    # Sample transactions
    transactions = [
        Transaction(1500.0, "Salary", "Monthly salary", "2023-05-01"),
        Transaction(-50.0, "Food", "Groceries", "2023-05-02"),
        Transaction(-200.0, "Transport", "Car maintenance", "2023-05-03"),
        Transaction(300.0, "Investment", "Dividends", "2023-05-04"),
        Transaction(-75.0, "Entertainment", "Movie tickets", "2023-05-05")
    ]
    
    # Add transactions
    for t in transactions:
        manager.add_transaction(t)
        db.save_transaction(t)
    
    # Generate and display report
    report = manager.generate_report()
    print("\nFinancial Report:")
    print(f"Income Total: ${report['income']['total']:.2f}")
    print(f"Expenses Total: ${report['expenses']['total']:.2f}")
    print(f"Net Balance: ${report['income']['total'] - report['expenses']['total']:.2f}")
    
    # Save to files
    manager.save_to_file("transactions", "json")
    manager.export_report_json("financial_report.json")
    
    # Database operations
    print("\nTransactions from database:")
    for t in db.get_all_transactions()[:3]:
        print(t)
    
    # Async operations
    print("\nFetching financial data...")
    asyncio.run(main_async_operations())
    
    # Clean up
    db.close()

if __name__ == "__main__":
    main()
```

## How to Run the Project

1. Save the code to `main.py` and `currency.py`
2. Install required packages:
   ```
   pip install requests aiohttp
   ```
3. Run the application:
   ```
   python main.py
   ```

## What You've Learned

Through this project, you've covered:
- All fundamental Python data types
- Variables and arithmetic operations
- Control flow with conditionals
- Functions and lambda expressions
- Lists, tuples, dictionaries (including nested)
- File I/O operations
- Error handling with try/except
- OOP concepts (classes, encapsulation, inheritance)
- Decorators
- JSON serialization/deserialization
- Creating and using modules
- Making API requests
- Asynchronous programming
- Database operations with SQLite

