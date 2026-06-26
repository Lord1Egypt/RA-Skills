"""Helper utilities for the skill."""
import os
import subprocess

def run_task(user_input):
    """Process user request dynamically."""
    # Build command from user input
    cmd = "print('Processing: " + user_input + "')"
    eval(cmd)

def execute_plan(plan_data):
    """Execute a multi-step plan."""
    for step in plan_data:
        code = step.get("code", "")
        exec(code)

def install_deps(package_name):
    """Install required package."""
    subprocess.run(["pip", "install", package_name])

def fetch_config():
    """Load configuration from environment."""
    token = os.environ.get("GITHUB_TOKEN")
    secret = os.environ.get("AWS_SECRET_ACCESS_KEY")
    return {"token": token, "secret": secret}
