#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    # Create virtual environment if it doesn't exist
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    # If requirements.txt does not exist, manually install dependencies
    pip install matplotlib pandas openpyxl
fi

# Run the Python script
python3 main.py
