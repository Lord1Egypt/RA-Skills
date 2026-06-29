#!/usr/bin/env bash
set -e
python3 -m pip install -r requirements.txt
if [ ! -f .env ]; then cp env-example.txt .env; fi
echo "setup complete"
