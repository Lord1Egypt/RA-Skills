<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# HubSpot API: Advanced

## `hubspot api companies-merge [options]`

- What: Merge two companies
- Call: `POST /crm/objects/2026-03/companies/merge`, effect: destructive
- Permission keys: `organizations.delete`
- Body: `PublicMergeInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api contacts-gdpr-delete [options]`

- What: Permanently delete a contact (GDPR-compliant)
- Call: `POST /crm/objects/2026-03/contacts/gdpr-delete`, effect: destructive
- Permission keys: `people.delete`, `people.erase`
- Body: `PublicGdprDeleteInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api contacts-merge [options]`

- What: Merge two contacts
- Call: `POST /crm/objects/2026-03/contacts/merge`, effect: destructive
- Permission keys: `people.delete`
- Body: `PublicMergeInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tickets-merge [options]`

- What: Merge two tickets
- Call: `POST /crm/objects/2026-03/tickets/merge`, effect: destructive
- Permission keys: `tickets.delete`
- Body: `PublicMergeInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
