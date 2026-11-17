---
name: smtping-email-verification
description: Verify email addresses with the SMTPing API before sending, importing or storing them. Use when the user asks to verify, validate, check or clean one email address or a list (CSV, pasted text, CRM export), wants to know which contacts are safe to email, asks about bounces, disposable, spamtrap, spambot or complainer addresses, or asks for their SMTPing credit balance.
license: MIT
metadata:
  homepage: https://smtping.com/email-verification-ai-agent
  docs: https://smtping.com/docs
  requires_env: SMTPING_API_KEY
---

# SMTPing email verification

Verify email addresses through SMTPing and turn the results into a clear decision for the user: send, remove, or review.

## Setup

An API key must be available in the `SMTPING_API_KEY` environment variable.
If it is missing, ask the user to create a key at https://app.smtping.com (free account, 25 free credits per day) and set it. Never invent or guess a key, and never print the key back in full.

## Pick the right path

1. **MCP tools available** (`verify_email`, `verify_list`, `get_bulk_job`, `check_threat`, `get_credits`): use them. They handle retries and bulk polling.
2. **No MCP tools, shell available**: call the REST API with `curl` as shown below.
3. **Neither**: tell the user to install the MCP server (`npx -y @smtping/mcp`, see https://smtping.com/email-verification-mcp) or give them the curl command to run.

## Cost rules

- 1 credit per verified address, 1 credit per threat-list check. `get_credits` and job status are free.
- Before verifying more than 100 addresses, state the number of unique addresses and the credit cost, and ask for confirmation.
- Always deduplicate (lowercase, trim) before sending a list. Skip values that are not email addresses and tell the user how many you skipped.

## REST API

Base URL: `https://api.smtping.com/api/v1`
Auth header on every request: `X-API-Key: $SMTPING_API_KEY`

### One address

```bash
curl -s -X POST https://api.smtping.com/api/v1/verify/single \
  -H "X-API-Key: $SMTPING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "someone@example.com"}'
```

### A list (up to 100,000 unique addresses per job)

For 10 addresses or fewer, call the single endpoint for each. Above that, create a bulk job:

```bash
curl -s -X POST https://api.smtping.com/api/v1/verify/bulk \
  -H "X-API-Key: $SMTPING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"emails": ["a@example.com", "b@example.com"]}'
# returns { "jobId": "...", "status": "Queued" }
```

Poll the job every 5 to 30 seconds (increase the interval as you go):

```bash
curl -s https://api.smtping.com/api/v1/verify/bulk/JOB_ID \
  -H "X-API-Key: $SMTPING_API_KEY"
# status: Queued | Processing | Succeeded | Failed | Cancelled
```

When `status` is `Succeeded`, fetch the results:

```bash
curl -s https://api.smtping.com/api/v1/verify/bulk/JOB_ID/result \
  -H "X-API-Key: $SMTPING_API_KEY"
```

Large jobs can take minutes. If the user does not want to wait, give them the job id so they can come back to it.

### One threat list

```bash
curl -s -X POST https://api.smtping.com/api/v1/checks/spamtrap \
  -H "X-API-Key: $SMTPING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "someone@example.com"}'
# also: /checks/disposable, /checks/spambot, /checks/complainer
```

### Credits

```bash
curl -s https://api.smtping.com/api/v1/credits -H "X-API-Key: $SMTPING_API_KEY"
```

### Errors

- 401 or 403: key missing or wrong. Ask the user to check `SMTPING_API_KEY`.
- 402: not enough credits. Tell the user, link https://smtping.com/pricing, do not retry.
- 429 or 5xx: wait a few seconds and retry, at most 3 times.

## Reading the results

Map every `status` to one of three bands and report by band:

| band | statuses | what to tell the user |
| --- | --- | --- |
| safe | valid, alias | Send. |
| avoid | invalid, spamtrap, disposable, blacklisted, complainer, spambot, inbox_full | Remove before sending. |
| judgement | catch_all, unknown, role and anything else | Review. Send only to engaged or high-value contacts, in small batches. |

Explain the risky ones in one line each when they appear:

- **spamtrap**: address used to catch senders with poor list hygiene. One hit can damage domain reputation. Always remove.
- **complainer**: known to mark mail as spam. Remove.
- **disposable**: throwaway inbox, usually gone within hours. Remove from marketing lists, block at signup.
- **catch_all**: the domain accepts every address, so the mailbox cannot be confirmed. Judgement call.
- **role** (info@, sales@): shared inbox, higher complaint rate. Fine for B2B replies, avoid for bulk marketing.

## Output

- For one address: the status, the band, and one sentence on what to do.
- For a list: totals per band, the count per status, then the addresses to remove. Offer a CSV with columns `email,status,band` when the list is longer than about 20 rows.
- Never claim an address is "guaranteed deliverable". Verification lowers bounce risk; it does not guarantee inbox placement.

## Limits

- Do not verify addresses the user has no legitimate reason to process. Verification is list hygiene, not a way to find or identify people.
- Do not send email. This skill only checks addresses.

More: https://smtping.com/docs and the verdict guide at https://smtping.com/13-verdict-types-guide
