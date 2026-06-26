#!/usr/bin/env python3
"""
SMB Sales Boost API Client
Reusable script for making any API call. Pass method, endpoint, and optional params/body as arguments.

Requires: API key with smbk_ prefix (generate from Dashboard > API tab).
          Set via SMB_SALES_BOOST_API_KEY env var or pass as first argument.

Data Sensitivity: Exports may contain PII (business phone numbers, email addresses).
                  Handle exported files with appropriate care.

Usage:
  python smb_api.py <API_KEY> <METHOD> <ENDPOINT> [--params '{"key":"value"}'] [--body '{"key":"value"}'] [--output-dir /path/to/dir]

Examples:
  python smb_api.py smbk_xxx GET /leads --params '{"positiveKeywords":"[\"*dental*\",\"*dentist*\",\"*orthodont*\"]","stateInclude":"TX","limit":"10"}'
  python smb_api.py smbk_xxx GET /leads/preview --params '{"positiveKeywords":"[\"*dental*\",\"*dentist*\"]","stateInclude":"TX","limit":"25"}'
  python smb_api.py smbk_xxx GET /me
  python smb_api.py smbk_xxx POST /leads/export --body '{"database":"other","filters":{"positiveKeywords":["*med*spa*","*aesthet*","*botox*"],"stateInclude":"FL"},"maxCredits":100}'
  python smb_api.py smbk_xxx POST /ai/suggest-categories --body '{"companyName":"FitPro Supply","companyDescription":"Commercial fitness equipment","productService":"Gym equipment, treadmills"}'
  python smb_api.py smbk_xxx POST /ai/auto-refine/enable --body '{"listId":42}'
  python smb_api.py smbk_xxx GET /ai/auto-refine/status --params '{"listId":"42"}'
  python smb_api.py smbk_xxx GET /ai/keyword-status
  python smb_api.py smbk_xxx POST /email-schedules/15/trigger
  python smb_api.py smbk_xxx POST /filter-presets --body '{"name":"NY Bakeries","filters":{"positiveKeywords":["*bakery*","*cater*","*pastry*"],"stateInclude":"NY"}}'
  python smb_api.py smbk_xxx DELETE /filter-presets/42
  python smb_api.py smbk_xxx POST /purchase-credits --body '{"creditCount":500}'
  python smb_api.py smbk_xxx POST /subscription/change-plan --body '{"targetPlan":"growth"}'
  python smb_api.py smbk_xxx POST /subscription/cancel
  python smb_api.py none POST /purchase --body '{"email":"user@example.com","plan":"starter"}'
  python smb_api.py none POST /claim-key --body '{"email":"user@example.com","claimToken":"tok_abc123"}'
  python smb_api.py smbk_xxx GET /leads/other/schema-types
  python smb_api.py smbk_xxx GET /leads --params '{"positiveKeywords":"[\"*dental*\"]","stateInclude":"TX","maxCredits":"10"}'
  python smb_api.py smbk_xxx GET /auto-top-up
  python smb_api.py smbk_xxx PATCH /auto-top-up --body '{"enabled":true,"triggerType":"credits","triggerAmount":100,"purchaseType":"credits","purchaseAmount":500}'
  python smb_api.py smbk_xxx POST /settings/switch-database --body '{"smbType":"other"}'
  python smb_api.py smbk_xxx GET /settings/database
"""

import sys
import json
import os
import base64
import argparse
import requests

BASE_URL = "https://smbsalesboost.com/api/v1"
SAFE_EXTENSIONS = {".csv", ".json", ".xlsx"}
DEFAULT_OUTPUT_DIR = "/mnt/user-data/outputs"

# Endpoints that do not require authentication
UNAUTHENTICATED_ENDPOINTS = {"/purchase", "/claim-key"}


def make_request(api_key, method, endpoint, params=None, body=None):
    """Make an authenticated API request and return the response."""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}

    # Only include Authorization header if the endpoint requires it
    # and a real API key is provided (not "none" placeholder)
    if endpoint not in UNAUTHENTICATED_ENDPOINTS and api_key.lower() != "none":
        headers["Authorization"] = f"Bearer {api_key}"

    method = method.upper()
    if method == "GET":
        resp = requests.get(url, headers=headers, params=params or {})
    elif method == "POST":
        resp = requests.post(url, headers=headers, json=body)
    elif method == "PATCH":
        resp = requests.patch(url, headers=headers, json=body)
    elif method == "PUT":
        resp = requests.put(url, headers=headers, json=body)
    elif method == "DELETE":
        resp = requests.delete(url, headers=headers)
    else:
        print(json.dumps({"error": f"Unsupported method: {method}"}))
        sys.exit(1)

    return resp


def save_export_files(data, output_dir):
    """Safely save base64-encoded export files with filename sanitization.

    Security measures:
    - os.path.basename() strips directory traversal components (e.g., ../../etc/passwd -> passwd)
    - Extension validated against allowlist (.csv, .json, .xlsx only)
    - Files written only to the designated output_dir, never to API-specified paths
    """
    os.makedirs(output_dir, exist_ok=True)
    saved = []

    for file_entry in data.get("data", {}).get("files", []):
        # Sanitize filename: strip path components to prevent path traversal
        raw_name = file_entry.get("fileName", "export.csv")
        safe_name = os.path.basename(raw_name)

        # Validate extension against allowlist
        _, ext = os.path.splitext(safe_name)
        if ext.lower() not in SAFE_EXTENSIONS:
            safe_name = safe_name + ".csv"

        # Write only to designated output directory
        output_path = os.path.join(output_dir, safe_name)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(file_entry["data"]))

        saved.append({"fileName": safe_name, "path": output_path, "size": file_entry.get("size", 0)})

    return saved


def main():
    parser = argparse.ArgumentParser(description="SMB Sales Boost API Client")
    parser.add_argument("api_key", nargs="?", default=None, help="API key (smbk_... prefix), or 'none' for unauthenticated endpoints. Falls back to SMB_SALES_BOOST_API_KEY env var.")
    parser.add_argument("method", help="HTTP method: GET, POST, PATCH, PUT, DELETE")
    parser.add_argument("endpoint", help="API endpoint path, e.g. /leads, /me, /filter-presets")
    parser.add_argument("--params", default=None, help="Query parameters as JSON string (for GET requests)")
    parser.add_argument("--body", default=None, help="Request body as JSON string (for POST/PATCH/PUT)")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Directory for saving export files")
    args = parser.parse_args()

    # Resolve API key: CLI arg > env var > error
    api_key = args.api_key or os.environ.get("SMB_SALES_BOOST_API_KEY")
    if not api_key:
        print(json.dumps({"error": "No API key provided. Pass as first argument or set SMB_SALES_BOOST_API_KEY env var."}))
        sys.exit(1)

    params = json.loads(args.params) if args.params else None
    body = json.loads(args.body) if args.body else None

    resp = make_request(api_key, args.method, args.endpoint, params=params, body=body)

    # Try to parse response as JSON
    try:
        data = resp.json()
    except ValueError:
        # Binary response (e.g., file download)
        print(json.dumps({"status": resp.status_code, "message": "Binary response received", "size": len(resp.content)}))
        return

    # Handle export responses — save files automatically
    if args.endpoint == "/leads/export" and resp.ok and "files" in data.get("data", {}):
        saved = save_export_files(data, args.output_dir)
        output = {
            "status": resp.status_code,
            "leadCount": data["data"].get("leadCount"),
            "exportId": data["data"].get("exportId"),
            "databaseType": data["data"].get("databaseType"),
            "creditsUsed": data["data"].get("creditsUsed"),
            "creditsRemaining": data["data"].get("creditsRemaining"),
            "overflowCount": data["data"].get("overflowCount"),
            "maxLeads": data["data"].get("maxLeads"),
            "maxResults": data["data"].get("maxResults"),
            "maxCredits": data["data"].get("maxCredits"),
            "savedFiles": saved
        }
        # Remove None values for cleaner output
        output = {k: v for k, v in output.items() if v is not None}
        print(json.dumps(output, indent=2))
    elif resp.status_code == 402:
        # Insufficient credits
        print(json.dumps({
            "status": 402,
            "error": "insufficient_credits",
            "message": data.get("message", "Insufficient credits. Use maxCredits/maxResults to limit usage, or purchase more credits."),
            "data": data
        }, indent=2))
    else:
        # Standard JSON response — print it
        print(json.dumps(data, indent=2))

    # Print rate limit info to stderr so it doesn't pollute JSON output
    for header in ["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"]:
        if header in resp.headers:
            print(f"{header}: {resp.headers[header]}", file=sys.stderr)

    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
