# COMMON_SECURITY.md

This document defines shared conventions for security-sensitive Flink skills.
Reference this file for skills involving login, account switching, credentials,
endpoint configuration, dependency files, or other secret-adjacent operations.

## Security Rules (MUST)

- Never request or accept plaintext AK/SK in chat.
- Never suggest `volc_flink login --ak ... --sk ...` as a copy-paste example.
- Never place secrets in command-line arguments when avoidable.
- Never echo secrets back to the user.
- Never log or summarize sensitive values in the final response.

## Approved Login Guidance

Preferred options:

- interactive login: `volc_flink login`
- enterprise-approved secret management flow
- pre-provisioned local credential/profile directory

If the user is not logged in:

1. Stop the workflow.
2. Ask the user to complete interactive login or the approved internal method.
3. Resume only after login state is confirmed.

## Sensitive Operations

Treat the following as security-sensitive:

- auth / account management
- endpoint configuration that may involve credentials
- dependency or file uploads that may contain confidential artifacts
- local profile switching
- any step that exposes token / secret / password-like values

## Redaction Rules

When showing examples or summaries:

- keep endpoint hostnames only if necessary
- redact usernames, tokens, passwords, and secret fields
- show placeholders like `<redacted>` instead of actual values

## Local Environment Guidance

- Prefer environment-based or profile-based secret loading over inline command arguments.
- If a command may reveal secrets in shell history, do not recommend it.
- If a file contains secrets, do not suggest printing the whole file.

## Output Contract

When responding from a security-sensitive workflow, include:

- what secure method was recommended
- what state was confirmed (logged in / profile selected / endpoint configured)
- what was intentionally not displayed for safety
- the next safe step for the user

