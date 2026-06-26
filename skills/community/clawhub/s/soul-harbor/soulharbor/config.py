"""
Configuration file
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data storage path
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# KV store path
KV_STORE_PATH = DATA_DIR / "memory_store"

# Log configuration
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Sentiment threshold
SENTIMENT_NEGATIVE_THRESHOLD = -0.3

# Silence wake-up threshold (hours)
SILENCE_WAKEUP_HOURS = 48

# Cron Job configuration
CRON_CHECK_INTERVAL_SECONDS = 3600  # Check every hour

# Prompt template path
PROMPTS_DIR = Path(__file__).parent / "prompts"
