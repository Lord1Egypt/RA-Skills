# Auth and Security Controls

## AuthN and AuthZ Separation

- Authenticate first (API key, session token, JWT, OAuth access token).
- Authorize second at resource boundary.
- Never trust client-provided roles without server verification.

## Input and Output Defenses

- Validate and coerce all request payloads.
- Enforce strict schema on query and path parameters.
- Sanitize or encode output when returning user-generated fields.

## Secret and Token Handling

- Keep secrets in server-side secret managers.
- Rotate keys on schedule and on incident.
- Avoid logging tokens, credentials, or full PII.

## Abuse Controls

- Apply per-user and per-IP rate limits.
- Add request size limits.
- Use timeout budgets to reduce resource exhaustion.

## CORS and Transport

- Restrict CORS origins explicitly.
- Require HTTPS in production.
- Use secure cookie flags when cookie-based auth is enabled.

## Security Review Gate

Before release, verify:

- Threat model reviewed for auth bypass and broken object-level authorization.
- Sensitive endpoints covered by tests.
- Audit logs include actor, action, resource, and request_id.
