# Salesflare API endpoint usage notes

This file is intentionally practical and short. For full coverage, use:

```bash
python scripts/sf.py discover --format table
python scripts/sf.py discover --format markdown > references/endpoints-generated.md
```

## Auth

```bash
export SALESFLARE_API_KEY='YOUR_KEY'
```

## Read examples

### Me / users

```bash
python scripts/sf.py get --path /me
python scripts/sf.py get --path /users --query limit=20
```

### Accounts

```bash
python scripts/sf.py get --path /accounts --query limit=20
python scripts/sf.py get --path /accounts --query search=acme --query limit=10
python scripts/sf.py get --path /accounts/123/feed
```

`GET /accounts/{account_id}/feed` returns the account feed/timeline when account feed API access is enabled for the workspace. If this endpoint is unavailable, contact `support@salesflare.com` and ask Salesflare to turn it on.

### Contacts

```bash
python scripts/sf.py get --path /contacts --query limit=20
python scripts/sf.py get --path /contacts --query email=someone@example.com
```

### Opportunities

```bash
python scripts/sf.py get --path /opportunities --query limit=20
python scripts/sf.py get --path /opportunities --query search=renewal --query closed=false
```

### Tasks

```bash
python scripts/sf.py get --path /tasks --query limit=20
```

### Tags / pipelines

```bash
python scripts/sf.py get --path /tags --query limit=50
python scripts/sf.py get --path /pipelines
```

## Write examples

### Create account

```bash
python scripts/sf.py post --path /accounts --data-json '{
  "name": "Acme BV",
  "domain": "acme.com"
}'
```

### Create contact

```bash
python scripts/sf.py post --path /contacts --data-json '{
  "email": "john@acme.com",
  "firstname": "John",
  "lastname": "Doe",
  "account": 123
}'
```

### Create opportunity

```bash
python scripts/sf.py post --path /opportunities --data-json '{
  "account": 123,
  "name": "Acme Expansion",
  "value": 12000
}'
```

### Create task

```bash
python scripts/sf.py post --path /tasks --data-json '{
  "description": "Follow up on proposal",
  "account": 123
}'
```

## Pagination

Use `--paginate` for GET list endpoints:

```bash
python scripts/sf.py get --path /accounts --paginate --page-limit 100 --max-pages 10
```

## Discover all endpoints by tag

```bash
python scripts/sf.py discover --tag Accounts
python scripts/sf.py discover --tag Contacts
python scripts/sf.py discover --tag Opportunities
python scripts/sf.py discover --tag Tasks
python scripts/sf.py discover --tag Workflows
```

## Notes

- API docs include legacy/deprecated query-builder filter shapes (`q`, `rules` variants). Prefer simple filters first.
- For complex filtering, test with a read request before using write calls.
- Script retries 429/5xx with exponential backoff.
- Advanced filtering support is raw/pass-through: you can send `q` payloads manually, but this skill does not provide a high-level query-builder abstraction.
- Use `sf_smoketest.py` for re-validation in your own environment. Default mode is read-only. With `--allow-write --allow-delete`, it runs a lifecycle test: POST controlled fixtures first, then GET list endpoints, then specific GETs, then PUT only those fixtures, then DELETE only those fixtures.

## Smoke test lifecycle

The lifecycle write set is intentionally cleanup-safe:

- Created with `POST`: account, contact, opportunity, task, internal note/message, tag.
- Also covered: meeting create/update/delete, account-contact relationship updates on the test account, account-user relationship updates when a user ID is available, and feedback posts on the test message.
- Updated with `PUT`: only the records created by the same run.
- Deleted with `DELETE`: only the records created by the same run, in dependency-safe order.
- Skipped writes: settings routes, datasource updates, workflow creation/actions, custom-field schema creation/update/delete, call-log writes without a matching cleanup endpoint, and any route that cannot be safely owned and cleaned up by the smoke test.

In production testing, `PUT /messages/{message_id}` required both `account` and `body` in the update payload; sending only `body` returned 400.
`POST /accounts/{account_id}/users` needs a user ID before the list phase, so the lifecycle smoke may skip that POST while still testing `PUT /accounts/{account_id}/users` after `GET /users` has discovered a user ID.
If a lifecycle smoke test is interrupted, search for records named `OpenClaw Smoke` and tags starting with `openclaw-smoke-` before rerunning.

## Endpoint-specific caveats (from live tests)

### Account feed
- `GET /accounts/{account_id}/feed` is available in Salesflare's OpenAPI and returned 200 in live read-only smoke testing.
- This endpoint can be workspace/feature gated. If it returns unavailable/not found for a workspace, contact `support@salesflare.com` and ask Salesflare to turn on account feed API access.

### Persons
- Bare `GET /persons` can return 500.
- Prefer `GET /persons?search=...` or `GET /persons?id=...`.

### Tags
- Treat `GET /tags/{tag_id}` as unsupported in this skill (reproduced 500 with valid IDs).
- Use `GET /tags` and `GET /tags/{tag_id}/usage`.

### Calls and meetings
- `POST /calls` and `POST /meetings` require at least `date` and `participants`.
- The lifecycle smoke test covers meetings because they can be deleted through `/meetings/{meeting_id}`. It skips call creation because the OpenAPI exposes `POST /calls` and `PUT /calls/{meeting_id}`, but no matching `DELETE /calls/{id}` cleanup route.
- Minimal working payload:
  - `{"date":"<ISO8601>","participants":[<contact_id>]}`

### Custom fields
- For `GET /customfields/{itemClass}/{customFieldApiField}/options`, `itemClass` must be plural (`accounts|contacts|opportunities`).
- The smoke test now probes `accounts`, `contacts`, and `opportunities` custom-field lists first, then uses a real custom field ID for `GET /customfields/{itemClass}/{id}` when one exists.
- The options endpoint is tested only when a select custom field with an `api_field` is discovered; otherwise it is skipped instead of inventing an ID or API field.
- `POST /customfields/{itemClass}` expects schema-specific payloads, and `type` is numeric in practice. Use `GET /customfields/types` to map valid type IDs.

### Filter fields
- `GET /filterfields/{entity}` works for `contact`, `account`, `opportunity`, `task`, `workflow`, `lead`.
- `person` returned 400 in tests.

### Account relationship update routes
- `POST /accounts/{account_id}/contacts` and `POST /accounts/{account_id}/users` expect an array body like `[{"id": <id>}]`.

### Message feedback
- `POST /messages/{message_id}/feedback` works with a valid accessible message ID and body `{"feedback":"helpful"}`.
- Singular alias `/message/{id}/feedback` also worked in this workspace.

### Fixture dependencies
- Some endpoints require existing resource IDs (groups, meetings, messages). If no such records exist, failures can be fixture/context related instead of endpoint incompatibility.
