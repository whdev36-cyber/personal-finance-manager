# main.py
import json
import csv
import os
from datetime import datetime as dt
import requests
import asyncio
import sqlite3
from typing import List, Dict, Tuple, Optional

# Basic data types in Python
initial_balance: float = 0.0 # float
app_name: str = 'Personal Finance Manager' # string
is_active: bool = True # boolean
version: int = 1 # integer

class Transaction:
    def __init__(self, amount: float, category: str, description: str, date: str):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def __repr__(self):
        return f'{self.date} - {self.category}: ${self.amount:.2f} ({self.description})'

def categorize_transaction(amount: float) -> str:
    '''Categorize transaction based on amount'''
    if amount > 1000:
        return 'Large Income' if amount > 0 else 'Major Expense'
    elif amount > 100:
        return 'Medium Income' if amount > 0 else 'Major Expense'
    else:
        return 'Small Income' if amount > 0 else 'Small Expense'
