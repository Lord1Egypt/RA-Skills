<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# HubSpot API: Search

## `hubspot api calls-search [options]`

- What: Search for calls
- Call: `POST /crm/objects/2026-03/calls/search`, effect: read
- Permission keys: `activities.list`
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `hubspot api companies-search [options]`

- What: Search for companies
- Call: `POST /crm/objects/2026-03/companies/search`, effect: read
- Permission keys: `organizations.list`
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `hubspot api contacts-search [options]`

- What: Search for contacts
- Call: `POST /crm/objects/2026-03/contacts/search`, effect: read
- Permission keys: `people.list`
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `hubspot api deals-search [options]`

- What: Search for deals using various filters and criteria to retrieve specific records.
- Call: `POST /crm/objects/2026-03/0-3/search`, effect: read
- Permission keys: `deals.list`
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `hubspot api emails-search [options]`

- What: Search for emails using specified criteria and filters.
- Call: `POST /crm/objects/2026-03/emails/search`, effect: read
- Permission keys: `activities.list`
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `hubspot api leads-search [options]`

- What: Search for leads using specified criteria.
- Call: `POST /crm/objects/2026-03/leads/search`, effect: read
- Permission keys: `leads.list`
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `hubspot api meetings-search [options]`

- What: Search for meetings
- Call: `POST /crm/objects/2026-03/meetings/search`, effect: read
- Permission keys: `activities.list`
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `hubspot api notes-search [options]`

- What: Search for notes based on specified criteria.
- Call: `POST /crm/objects/2026-03/notes/search`, effect: read
- Permission keys: `activities.list`
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `hubspot api search [options]`

- What: post-/crm/objects/2026-03/{objectType}/search_/crm/objects/2025-09/{objectType}/search
- Call: `POST /crm/objects/2026-03/{objectType}/search`, effect: read
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `hubspot api tasks-search [options]`

- What: Search for tasks using specified criteria.
- Call: `POST /crm/objects/2026-03/tasks/search`, effect: read
- Permission keys: `activities.list`
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `hubspot api tickets-search [options]`

- What: Search for tickets
- Call: `POST /crm/objects/2026-03/tickets/search`, effect: read
- Pages: cursor: send `after` (body), read the next one from `paging.next.after`; items in `results`; page size in `limit` (body)
- Body: `PublicObjectSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |
