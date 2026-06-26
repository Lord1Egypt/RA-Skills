"""
Token Tamer Configuration Example
Copy this file to token_config.py and customize for your environment.

Author: Shadow Rose
License: MIT
"""

# ============================================================================
# STORAGE SETTINGS
# ============================================================================

# File where usage data is stored
USAGE_FILE = "/path/to/token_usage.json"

# ============================================================================
# BUDGET LIMITS
# ============================================================================

# Daily, weekly, and monthly budget limits (in USD)
# Set to 0 to disable budget tracking for that period
BUDGETS = {
    'daily': 10.00,      # $10/day
    'weekly': 50.00,     # $50/week
    'monthly': 150.00,   # $150/month
}

# ============================================================================
# ALERT THRESHOLDS
# ============================================================================

# Percentage thresholds for alerts
ALERT_THRESHOLDS = {
    'warning': 80,    # Warn at 80% of budget
    'critical': 95,   # Critical at 95% of budget
    # At 100%, kill switch activates automatically
}

# ============================================================================
# MODEL PRICING
# ============================================================================

# Pricing per million tokens (input, output)
# Format: "provider/model": {"input": price, "output": price}
# Use "provider/*" for wildcard (applies to all models from that provider)

MODEL_PRICING = {
    # OpenAI
    'openai/gpt-4': {
        'input': 30.00,
        'output': 60.00
    },
    'openai/gpt-4-turbo': {
        'input': 10.00,
        'output': 30.00
    },
    'openai/gpt-3.5-turbo': {
        'input': 0.50,
        'output': 1.50
    },
    'openai/gpt-4o': {
        'input': 2.50,
        'output': 10.00
    },
    'openai/gpt-4o-mini': {
        'input': 0.15,
        'output': 0.60
    },
    
    # Anthropic
    'anthropic/claude-3-opus': {
        'input': 15.00,
        'output': 75.00
    },
    'anthropic/claude-3-sonnet': {
        'input': 3.00,
        'output': 15.00
    },
    'anthropic/claude-3-haiku': {
        'input': 0.25,
        'output': 1.25
    },
    'anthropic/claude-sonnet-4': {
        'input': 3.00,
        'output': 15.00
    },
    'anthropic/claude-sonnet-4-5': {
        'input': 3.00,
        'output': 15.00
    },
    
    # Google
    'google/gemini-1.5-pro': {
        'input': 1.25,
        'output': 5.00
    },
    'google/gemini-1.5-flash': {
        'input': 0.075,
        'output': 0.30
    },
    'google/gemini-2.0-flash': {
        'input': 0.10,
        'output': 0.40
    },
    
    # xAI
    'xai/grok-beta': {
        'input': 5.00,
        'output': 15.00
    },
    'xai/grok-2': {
        'input': 2.00,
        'output': 10.00
    },
    
    # OpenRouter (average pricing)
    'openrouter/*': {
        'input': 5.00,
        'output': 15.00
    },
    
    # Custom provider example
    'custom/my-model': {
        'input': 1.00,
        'output': 2.00
    },
}

# ============================================================================
# WASTE DETECTION THRESHOLDS
# ============================================================================

WASTE_THRESHOLDS = {
    # Time window for detecting duplicate calls (minutes)
    'duplicate_window_minutes': 5,
    
    # Number of retries before considering excessive
    'excessive_retries_count': 3,
    
    # Input token count considered "large" (might have unnecessary context)
    'large_context_tokens': 50000,
    
    # Output/input ratio below this is suspicious (sending huge context, getting little output)
    'low_output_ratio': 0.01,  # 1%
}

# ============================================================================
# OPTIMIZATION SETTINGS
# ============================================================================

# Suggest cheaper model when expensive model is used for small requests
SUGGEST_CHEAPER_MODEL_THRESHOLD_TOKENS = 1000

# Models considered "expensive" (will trigger optimization suggestions)
EXPENSIVE_MODELS = [
    'gpt-4',
    'claude-3-opus',
    'claude-opus',
]

# Recommended cheaper alternatives
CHEAPER_ALTERNATIVES = {
    'gpt-4': 'gpt-4o-mini',
    'claude-3-opus': 'claude-3-haiku',
}

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Automatically activate kill switch when daily budget exceeded
AUTO_KILL_SWITCH = True

# Log every API call to console (verbose mode)
VERBOSE_LOGGING = False

# Retention period for usage data (days)
# Set to 0 to keep all data indefinitely
USAGE_DATA_RETENTION_DAYS = 90

# ============================================================================
# INTEGRATION SETTINGS
# ============================================================================

# Export usage data to external systems
# Options: None, 'webhook', 'file'
EXPORT_MODE = None

# Webhook URL for cost alerts (optional)
WEBHOOK_URL = None

# Webhook authentication header (optional)
WEBHOOK_AUTH_HEADER = None  # e.g., "Authorization: Bearer TOKEN"

# Export file path (if EXPORT_MODE = 'file')
EXPORT_FILE = "/path/to/usage_export.json"

# ============================================================================
# PROVIDER-SPECIFIC SETTINGS
# ============================================================================

# Some providers report usage differently
# Configure parsing rules here if needed

PROVIDER_CONFIG = {
    'openai': {
        'token_field': 'usage',
        'input_field': 'prompt_tokens',
        'output_field': 'completion_tokens'
    },
    'anthropic': {
        'token_field': 'usage',
        'input_field': 'input_tokens',
        'output_field': 'output_tokens'
    },
    # Add custom providers as needed
}
