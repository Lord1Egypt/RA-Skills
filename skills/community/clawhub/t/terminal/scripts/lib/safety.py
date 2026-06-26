#!/usr/bin/env python3
import re

HIGH_RISK_PATTERNS = [
    r'(^|\s)rm(\s|$)',
    r'(^|\s)mv(\s|$)',
    r'(^|\s)chmod(\s|$)',
    r'(^|\s)chown(\s|$)',
    r'(^|\s)kill(\s|$)',
    r'(^|\s)pkill(\s|$)',
    r'(^|\s)killall(\s|$)',
    r'(^|\s)sudo(\s|$)',
    r'(^|\s)curl(\s|$)',
    r'(^|\s)wget(\s|$)',
    r'curl\s+.*\|\s*(bash|sh)',
    r'wget\s+.*\|\s*(bash|sh)',
    r'(^|\s)bash\s+-c(\s|$)',
    r'(^|\s)sh\s+-c(\s|$)',
    r'(^|\s)python3?\s+-c(\s|$)',
    r'(^|\s)perl\s+-e(\s|$)',
    r'(^|\s)ruby\s+-e(\s|$)',
    r'(^|\s)osascript(\s|$)',
    r'(^|\s)ssh(\s|$)',
    r'(^|\s)scp(\s|$)',
    r'(^|\s)nc(\s|$)',
    r'(^|\s)dd(\s|$)',
    r'(^|\s)mkfs(\s|$)',
    r'diskutil\s+eraseDisk',
    r'find\s+.*-delete',
    r'sed\s+-i',
    r'>\s*\S',
    r'>>\s*\S',
]

SENSITIVE_PATTERNS = [
    (r'sk-[A-Za-z0-9_\-]+', '[REDACTED_OPENAI_KEY]'),
    (r'AKIA[0-9A-Z]{16}', '[REDACTED_AWS_KEY]'),
    (r'Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*', 'Bearer [REDACTED_TOKEN]'),
    (r'(?i)(token\s*=\s*)([^\s\'"]+)', r'\1[REDACTED]'),
    (r'(?i)(password\s*=\s*)([^\s\'"]+)', r'\1[REDACTED]'),
    (r'(?i)(api[_-]?key\s*=\s*)([^\s\'"]+)', r'\1[REDACTED]'),
]

def risk_level(command: str) -> str:
    cmd = command.strip()
    for pattern in HIGH_RISK_PATTERNS:
        if re.search(pattern, cmd):
            return "high"
    return "normal"

def requires_confirmation(command: str) -> bool:
    return risk_level(command) == "high"

def redact_sensitive(text: str) -> str:
    result = text or ""
    for pattern, replacement in SENSITIVE_PATTERNS:
        result = re.sub(pattern, replacement, result)
    return result
