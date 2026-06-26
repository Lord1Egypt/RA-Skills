"""
Sentinel Configuration Example
Copy this file to sentinel_config.py and customize for your environment.

Author: Shadow Rose
License: MIT
"""

# ============================================================================
# WORKSPACE SETTINGS
# ============================================================================

# Root directory of your AI agent workspace
# All critical files will be resolved relative to this path
WORKSPACE_ROOT = "/path/to/your/workspace"

# Critical files to monitor (supports glob patterns)
# Examples:
#   - "agent.md"    → exact file
#   - "memory/*.md" → all markdown files in memory/
#   - "**/*.py"     → all Python files recursively
CRITICAL_FILES = [
    "agent.md",
    "profile.md",
    "identity.md",
    "config.md",
    "memory/*.md",
    "config/*.json",
    "state/*.json",
]

# ============================================================================
# BACKUP SETTINGS
# ============================================================================

# Directory where backups are stored
# Backups are organized by timestamp: BACKUP_DIR/YYYYMMDD_HHMMSS/file/path
BACKUP_DIR = "/path/to/backup/directory"

# Maximum number of backup versions to keep per file
# Set to 0 for unlimited (not recommended — backups can grow very large)
# Older backups are automatically pruned when this limit is exceeded
MAX_BACKUP_VERSIONS = 10

# Backup compression (not yet implemented — reserved for future use)
# Options: None, 'gzip', 'bzip2', 'xz'
BACKUP_COMPRESSION = None

# ============================================================================
# MONITORING SETTINGS
# ============================================================================

# How often to check files (in seconds)
# Recommended: 300-900 (5-15 minutes)
CHECK_INTERVAL_SECONDS = 600

# Auto-restore corrupted files from backup
# If True, Sentinel will automatically restore files that become empty or corrupted
# If False, Sentinel will alert but not restore automatically
AUTO_RESTORE_ON_CORRUPTION = True

# Skip files currently in use by running processes
# If True, Sentinel won't back up or check files that are locked
# If False, Sentinel will attempt to check all files (may fail on locked files)
SKIP_FILES_IN_USE = True

# ============================================================================
# STATE TRACKING
# ============================================================================

# File where Sentinel stores its state manifest (file hashes, last check times)
# This file is critical for change detection — DO NOT DELETE
STATE_FILE = "/path/to/sentinel_state.json"

# ============================================================================
# ALERTING
# ============================================================================

# Log file for Sentinel's own operations
# Set to None to disable file logging (console only)
LOG_FILE = "/path/to/sentinel.log"

# Alert file for integrity violations and restore events
# Sentinel writes critical alerts here for external monitoring
# Set to None to disable
ALERT_FILE = "/path/to/sentinel_alerts.txt"

# Alert thresholds
# Sentinel will send alerts when these conditions are met
ALERT_ON_FILE_CHANGE = True          # Alert when any monitored file changes
ALERT_ON_CORRUPTION = True           # Alert when file corruption detected
ALERT_ON_AUTO_RESTORE = True         # Alert when auto-restore is performed
ALERT_ON_BACKUP_FAILURE = True       # Alert when backup fails

# ============================================================================
# EXCLUSIONS
# ============================================================================

# Patterns to exclude from manifest generation
# These files/directories will be ignored during workspace scans
EXCLUDE_PATTERNS = [
    '.git',
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '*.swp',
    '*.swo',
    '.DS_Store',
    'node_modules',
    '.venv',
    'venv',
]

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Debug mode (verbose logging)
DEBUG = False

# Hash algorithm (do not change unless you have a specific reason)
# Options: 'sha256', 'sha1', 'md5'
# Recommendation: keep as 'sha256' for security and collision resistance
HASH_ALGORITHM = 'sha256'

# Maximum file size to hash (in bytes)
# Files larger than this will be monitored by size/mtime only (no hash)
# Default: 100 MB
MAX_HASH_FILE_SIZE = 100 * 1024 * 1024

# ============================================================================
# WEBHOOK ALERTING (optional — not yet implemented)
# ============================================================================

# Send alerts to a webhook URL
# Set to None to disable webhook alerts
WEBHOOK_URL = None

# Webhook authentication
WEBHOOK_AUTH_HEADER = None  # e.g., "Authorization: Bearer TOKEN"

# Alert levels to send to webhook
# Options: 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
WEBHOOK_ALERT_LEVELS = ['ERROR', 'CRITICAL']
