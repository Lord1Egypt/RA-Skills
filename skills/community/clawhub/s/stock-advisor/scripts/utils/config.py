import os

# Base directory for local data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local data storage
PORTFOLIO_FILE = os.path.join(BASE_DIR, "data", "portfolio.json")

# Cloud Backend API
# Use the local dev server by default
API_BASE_URL = os.environ.get("STOCK_ADVISOR_API_URL", "https://api.daas.ai")
API_KEY = os.environ.get("STOCK_ADVISOR_API_KEY", "demo-key-123456")

