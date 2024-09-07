# Check if virtual environment exists
if (!(Test-Path -Path ".\venv")) {
    # Create virtual environment if it doesn't exist
    python -m venv venv
}

# Activate the virtual environment
.\venv\Scripts\Activate

# Upgrade pip
pip install --upgrade pip

# Install the required dependencies from requirements.txt
if (Test-Path -Path ".\requirements.txt") {
    pip install -r requirements.txt
} else {
    # If requirements.txt does not exist, manually install dependencies
    pip install matplotlib pandas openpyxl
}

# Run the Python script
python main.py
