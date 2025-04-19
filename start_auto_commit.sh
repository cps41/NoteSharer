#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the auto commit script
chmod +x auto_commit.py
nohup python3 auto_commit.py > auto_commit.log 2>&1 &