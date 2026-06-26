# SimpleFIN Developer Guide

This guide is for programmers that want to create an application that can access a user's financial data. Your application never sees the user's bank account credentials. In summary, this is the flow:

- A user gets a Setup Token from this server.
- The user gives the Setup Token to your application.
- Your application sends the Setup Token to this server and receives an Access Token in return.
- Your application uses the Access Token to get the user's transaction data from this server.
- At any point, the user can disable the Access Token.

## Bash/cURL Example

### 1. Generate a Setup Token
Send your users here to sign up for this service and generate a token: https://bridge.simplefin.org/simplefin/create

### 2. Exchange the Setup Token for an Access Token
As per the SimpleFIN specification, base64-decode the token to get a URL, then issue a POST to that URL.

```bash
SETUP_TOKEN='aHR0cHM6...'
CLAIM_URL="$(echo "$SETUP_TOKEN" | base64 --decode)"
ACCESS_URL=$(curl -H "Content-Length: 0" -X POST "$CLAIM_URL")
```

You can only do the above step once. Once you receive an ACCESS_URL, save it—the corresponding SETUP_TOKEN will no longer work.

### 3. Use the Access Token to get some data
Make an HTTP GET request to `{ACCESS_URL}/accounts` with Basic Auth credentials.

```bash
curl -L "${ACCESS_URL}/accounts?version=2"
```

## Specification
Read the SimpleFIN specification for more details: https://www.simplefin.org/protocol.html

## Errors
Responses from the `/accounts` endpoint will include an array of structured errors in the "errlist" property as described here: https://www.simplefin.org/protocol.html#error. Always show those errors to your end users.

## Limits
The SimpleFIN Bridge is intended to provide daily updates to transaction data. As such, you are expected to make 24 requests or fewer per day. There is a little leeway above this limit, which is helpful when doing initial setup. Quotas are replenished throughout the day.
Requests for all accounts `GET /accounts` have a quota. Requests for individual accounts have their own quota `GET /accounts?account=...`.
Making more requests than expected will eventually cause warning messages to appear in the "errors" array. Exceeding the expected rate limits beyond the warning level will result in Access Tokens being disabled.
The date range of requests to `/accounts` (i.e. difference between start-date and end-date) is limited to 90 days at a time. The number of days of history available varies for each institution.