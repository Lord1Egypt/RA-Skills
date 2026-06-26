import os
import requests
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Temporam Temp Mail")

# Configuration
BASE_URL = "https://api.temporam.com/v1"
API_KEY = os.environ.get("TEMPORAM_API_KEY")

def get_headers():
    if not API_KEY:
        raise ValueError("TEMPORAM_API_KEY environment variable is not set.")
    return {"Authorization": f"Bearer {API_KEY}"}

@mcp.tool()
def get_domains():
    """Get a list of available email domains from Temporam."""
    response = requests.get(f"{BASE_URL}/domains", headers=get_headers())
    response.raise_for_status()
    data = response.json()
    if not data.get("error"):
        return [d["domain"] for d in data.get("data", [])]
    return []

@mcp.tool()
def list_emails(email: str, page: int = 1, limit: int = 20):
    """List emails received by a specific email address."""
    params = {"email": email, "page": page, "limit": limit}
    response = requests.get(f"{BASE_URL}/emails", headers=get_headers(), params=params)
    response.raise_for_status()
    data = response.json()
    if not data.get("error"):
        return data.get("data", [])
    return []

@mcp.tool()
def get_email_content(email_id: str):
    """Get the full content of a specific email by its ID."""
    response = requests.get(f"{BASE_URL}/emails/{email_id}", headers=get_headers())
    response.raise_for_status()
    data = response.json()
    if not data.get("error"):
        return data.get("data", {})
    return {}

@mcp.tool()
def get_latest_email(email: str):
    """Get the most recent email received by a specific email address, including full content."""
    params = {"email": email}
    response = requests.get(f"{BASE_URL}/emails/latest", headers=get_headers(), params=params)
    response.raise_for_status()
    data = response.json()
    if not data.get("error"):
        return data.get("data", {})
    return {}

if __name__ == "__main__":
    mcp.run()
