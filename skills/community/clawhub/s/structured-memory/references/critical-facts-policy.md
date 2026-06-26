# Critical Facts Policy

## What belongs here

Store reusable execution-critical facts such as:
- IPs
- domains
- usernames
- stable paths
- service endpoints
- cron identifiers
- chat or account identifiers
- document references

## Sensitivity levels

- low
- medium
- high
- critical

## Rules

- Do not store passwords or tokens in plain text by default.
- For critical secrets, store only usage notes or where the secret is retrieved from.
- Use `critical-facts/` for future execution, not general topic memory.
- Prefer structured entries over prose.
