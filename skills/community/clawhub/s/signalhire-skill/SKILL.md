---
name: signalhire
description: Interact with the SignalHire API to enrich and verify professional contacts. Use this skill when asked to find email addresses, phone numbers, or search for professional profiles and companies using SignalHire. Supports Person API for comprehensive profile/contact data and Search API for lead generation.
---

# SignalHire API Skill

This skill provides context and instructions for using the SignalHire API to retrieve contact information (emails, phone numbers, social media profiles) from a global database of professionals.

## Authentication
To access the SignalHire API, an API key is required. The API key must be included in the `apikey` request header.

If the user hasn't provided their SignalHire API key in their request or environment, ask them to provide it before making API calls. Ensure it is kept secure and not exposed publicly.

## Endpoints

### 1. Person API
Retrieves comprehensive profile and full contact details about a specific individual based on unique identifiers (e.g., LinkedIn® profile links, email addresses, phone numbers, or ID).
- **Use Case:** Find a specific person's contact info.
- **Rate Limit:** 600 items per minute.
- **Callback URL:** The Person API is asynchronous — SignalHire POSTs the result to a callback URL you provide. See **Callback Setup** below.

### 2. Search API
Searches for individuals or companies using various filters (e.g., job title, location, industry). Returns a brief overview of information **without** contact details.
- **Use Case:** Lead generation, talent acquisition, market research.
- **Rate Limit:** 1 concurrent request.

---

## Callback Setup

The Person API is asynchronous: you submit a request with a `callbackUrl`, and SignalHire POSTs the enriched result to that URL when ready.

### Requirements
- A publicly reachable HTTPS endpoint that accepts POST requests with JSON body.
- A **shared secret** in the callback URL as a query parameter (e.g. `?k=<secret>`), because SignalHire controls the outbound request and cannot set custom headers.

### Step 1 — Deploy a webhook receiver
You need an HTTP server that:
1. Accepts `POST /signalhire/callback?k=<secret>`
2. Validates the `k` parameter against your stored secret
3. Saves the JSON payload to a known file (e.g. `signalhire_result.json`) so the agent can read it back

A minimal Flask example:
```python
import hmac, os
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
SECRET = os.environ["SIGNALHIRE_WEBHOOK_SECRET"]

@app.before_request
def auth():
    if request.method == "POST":
        k = request.args.get("k", "")
        if not hmac.compare_digest(k, SECRET):
            return jsonify({"error": "unauthorized"}), 403

@app.route("/signalhire/callback", methods=["POST"])
def callback():
    payload = request.get_json()
    with open("signalhire_result.json", "w") as f:
        json.dump(payload, f, indent=2)
    return jsonify({"status": "accepted"}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
```

### Step 2 — Generate a shared secret
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```
Store this value as `SIGNALHIRE_WEBHOOK_SECRET` in your server's environment.

### Step 3 — Set `SIGNALHIRE_CALLBACK_URL`
Construct the full callback URL including the secret:
```
https://<your-domain>/signalhire/callback?k=<your-secret>
```
Store it as the environment variable `SIGNALHIRE_CALLBACK_URL`, or in a config file your agent reads. **Never hardcode it in source files** — rotate the secret by updating it in one place.

Example (shell / `.env` file):
```
SIGNALHIRE_CALLBACK_URL=https://your-domain.com/signalhire/callback?k=your-secret-here
SIGNALHIRE_WEBHOOK_SECRET=your-secret-here
```

### Step 4 — Use it in requests
Read `SIGNALHIRE_CALLBACK_URL` from the environment at runtime and pass it as `callbackUrl` in every Person API request body. Do **not** hardcode the URL.

```python
import os
callback_url = os.environ["SIGNALHIRE_CALLBACK_URL"]
```

### Step 5 — Read the result
After submitting the enrichment request, poll or wait for `signalhire_result.json` to be written by your webhook server, then read and return the data to the user.

---

## Handling Responses & Credits

### Credits
The HTTP response headers provide the total remaining credits in the `X-Credits-Left` header. Always keep track of this if possible and alert the user if they are running low.

### Common HTTP Status Codes
- **200**: Request is completed successfully, data collected.
- **201**: Request is accepted, server started collecting data.
- **204**: Request is still in progress.
- **401**: Authentication failed (invalid API key).
- **402**: Out of credit limit.
- **403**: Account disabled or querying unauthorized request status.
- **406**: Requested more than the maximum allowed items (limit is 100).
- **422**: Incorrect or malformed parameters.
- **429**: Rate limit exceeded.

## Execution Pattern
When the user asks you to search for a contact or company using SignalHire:
1. Verify you have the `apikey`.
2. Determine if the goal is enrichment (Person API) or discovery (Search API).
3. For Person API: read `SIGNALHIRE_CALLBACK_URL` from the environment; if unset, prompt the user to complete Callback Setup above before proceeding.
4. Use the `exec` tool to run a `curl` or `fetch` script passing the `apikey` header (`-H "apikey: $API_KEY"`) and the `callbackUrl` in the request body.
5. Wait for the callback to arrive, then read `signalhire_result.json` and return the findings to the user cleanly.
