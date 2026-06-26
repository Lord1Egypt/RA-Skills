"""
RedactKit Configuration Example

Copy this file to `config.py` and customize for your needs.

Author: Shadow Rose
License: MIT
"""

# ====================
# Sensitivity Settings
# ====================

# Default sensitivity level
# Options: 'low', 'medium', 'high'
# - low: Only high-sensitivity patterns (SSN, credit cards, API keys)
# - medium: Medium+ (adds emails, phone numbers)
# - high: All patterns including person names (may have false positives)
SENSITIVITY_LEVEL = 'medium'


# ====================
# Pattern Categories
# ====================

# Enable/disable specific categories
ENABLED_CATEGORIES = {
    'pii': True,        # Personal Identifiable Information
    'secrets': True,    # API keys, passwords, tokens
    'financial': True,  # Credit cards, bank accounts
    'network': True,    # IP addresses, URLs
}

# Alternative: Enable only specific categories
# ENABLED_CATEGORIES = ['pii', 'secrets']  # Disable financial and network


# ====================
# Custom Patterns
# ====================

# Add your own regex patterns for domain-specific redaction
CUSTOM_PATTERNS = [
    # Example: Internal employee IDs
    # {
    #     'name': 'employee_id',
    #     'regex': r'EMP-\d{6}',
    #     'category': 'custom',
    #     'sensitivity': 'medium',
    #     'description': 'Internal employee IDs',
    #     'placeholder_template': '[EMPLOYEE-{index}]'
    # },
    
    # Example: Project code names
    # {
    #     'name': 'project_code',
    #     'regex': r'PROJECT-[A-Z]{3}-\d{4}',
    #     'category': 'custom',
    #     'sensitivity': 'low',
    #     'description': 'Project code names',
    #     'placeholder_template': '[PROJECT-{index}]'
    # },
]


# ====================
# File Processing
# ====================

# Supported file extensions for batch mode
SUPPORTED_EXTENSIONS = [
    '.txt',
    '.md',
    '.py',
    '.js',
    '.json',
    '.csv',
    '.yaml',
    '.yml',
    '.xml',
    '.html',
]

# Default encoding
FILE_ENCODING = 'utf-8'

# Maximum file size to process (bytes)
# 0 = no limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# ====================
# Mapping Storage
# ====================

# Default mapping directory (for batch operations)
# None = same as output directory
DEFAULT_MAPPING_DIR = None

# Mapping file suffix
MAPPING_FILE_SUFFIX = '.mapping.json'


# ====================
# Report Mode Settings
# ====================

# Maximum matches to show in report mode
REPORT_MAX_MATCHES = 10

# Show match context (characters before/after)
REPORT_CONTEXT_CHARS = 20


# ====================
# Placeholder Formats
# ====================

# Override default placeholder templates
# Use {index} for sequential numbering
PLACEHOLDER_OVERRIDES = {
    # 'email': '[EMAIL-REDACTED-{index}]',
    # 'phone': '[PHONE-REDACTED-{index}]',
}


# ====================
# Exclusions
# ====================

# Patterns to exclude from redaction (regex)
# Useful for known false positives
EXCLUSION_PATTERNS = [
    # Example: Exclude example.com emails
    # r'.*@example\.com',
    
    # Example: Exclude localhost IPs
    # r'127\.0\.0\.1',
]

# Paths to exclude from batch processing
EXCLUDED_PATHS = [
    # '.git',
    # 'node_modules',
    # '__pycache__',
]


# ====================
# Advanced Settings
# ====================

# Enable debug output
DEBUG = False

# Preserve file metadata (timestamps, permissions)
PRESERVE_METADATA = True
