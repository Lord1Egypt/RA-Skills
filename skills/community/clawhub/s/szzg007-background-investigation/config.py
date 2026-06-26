# SZZG007 Background Investigation Configuration

# Investigation Settings
INVESTIGATION_TIMEOUT = 300  # seconds
MAX_DATA_POINTS = 1000
CONFIDENCE_THRESHOLD = 0.7

# Social Media API Settings (placeholder - configure actual APIs when available)
SOCIAL_MEDIA_CONFIG = {
    "twitter": {
        "enabled": False,  # Enable when API keys are available
        "api_key": "",  # Configure in secure environment
        "api_secret": ""
    },
    "instagram": {
        "enabled": False,
        "access_token": ""
    },
    "linkedin": {
        "enabled": False,
        "client_id": "",
        "client_secret": ""
    },
    "tiktok": {
        "enabled": False,
        "api_key": ""
    }
}

# Data Sources Priority
DATA_SOURCES_PRIORITY = [
    "social_media_profiles",
    "public_records",
    "professional_networks",
    "news_mentions",
    "content_archives",
    "business_registries"
]

# Risk Assessment Factors
RISK_FACTORS = {
    "account_age": 0.2,  # 20% weight
    "content_quality": 0.25,  # 25% weight
    "engagement_patterns": 0.15,  # 15% weight
    "network_connections": 0.2,  # 20% weight
    "consistency": 0.1,  # 10% weight
    "red_flags": 0.1  # 10% weight
}

# Trust Scoring
MIN_TRUST_SCORE = 0  # Minimum possible score
MAX_TRUST_SCORE = 10  # Maximum possible score
APPROVAL_THRESHOLD = 7.0  # Minimum score for automatic approval

# Privacy Settings
RESPECT_PRIVACY_SETTINGS = True
ANONYMOUS_MODE = True
LIMIT_TO_PUBLIC_DATA_ONLY = True

# Output Settings
REPORT_FORMAT = "json"  # Options: json, yaml, markdown
SAVE_RAW_DATA = False  # Whether to save collected raw data
ANONYMIZE_OUTPUT = True  # Whether to anonymize personal identifiers in logs

# Notification Settings
NOTIFY_ON_HIGH_RISK = True
HIGH_RISK_THRESHOLD = 3.0  # Trust score below which to notify
NOTIFY_ON_NEW_RED_FLAGS = True