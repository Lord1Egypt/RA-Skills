---
name: backlink-submission
description: Use Ranklybee's confirmed Backlink Submission Profile to prepare and carry out compliant backlink submissions.
---

# Ranklybee Backlink Submission

Use this skill when the user asks to submit a website to a directory, community,
resource page, launch platform, or another backlink source through Ranklybee.

## Authentication and MCP tools

Use the authenticated Ranklybee MCP tools from a direct MCP connection or the
Ranklybee plugin. The production endpoint is `https://api.ranklybee.com/mcp`.
Clients may prefix tool names with the configured server name; resolve the tools
by their names below. If authentication is required, use the client's MCP OAuth
login flow and let the user complete Ranklybee login and consent. Never ask the
user to paste an API token into the conversation or save one in a file.

The full submission workflow needs both `backlink-submissions:read` and
`backlink-submissions:submit`. A read-only connection can check readiness but
cannot submit. On `SCOPE_REQUIRED`, `needs additional permissions`, or
`403 after trying upscoping`, stop the submission and direct the user to clear
the client's saved Ranklybee OAuth authentication and sign in again with both
permissions. Token refresh does not increase permissions. Recovery instructions
are at `https://ranklybee.com/docs/mcp#reconnect-with-submission-permissions`.
After reauthorization, retry the blocked check; retain any existing job and
idempotency key, and never repeat a final third-party submit action blindly.

The available tools are:

- `list_backlink_submission_projects`
- `get_backlink_submission_profile`
- `list_backlink_submission_sources`
- `preflight_backlink_submission`
- `create_backlink_submission`
- `get_backlink_submission`
- `record_backlink_submission_outcome`

The user does not need to know an internal Project ID. If the target
Project is not already clear from the conversation, call
`list_backlink_submission_projects` and show the user the available
Project names, roles, paid status, and active Site details. Ask the user to
choose when there is more than one reasonable target, then use its returned
`id` as `projectId`. Include `siteId` when the Project has more than one
active Site or when the user specifies one.
If the MCP connection is unavailable, direct the user to configure the endpoint
and authenticate using their client's MCP settings. Setup instructions are at
`https://ranklybee.com/docs/mcp`. Do not fall back to manual credentials.

## Browser capability

Reading profiles and preparing a submission plan only require Ranklybee MCP.
Executing an HTTP/HTTPS submission also requires an interactive browser or
Computer Use tool that can inspect the page, fill fields, and perform the
approved action. Use the client's available browser tools. A search or fetch
tool alone cannot submit a form. Confirm this capability before creating a job
or consuming a daily attempt; if unavailable, stop with the prepared plan and
explain that a browser tool must be connected. Do not claim MCP submitted the
form, create a job as a substitute, or record success without observed evidence.

## Required workflow

1. Resolve the target Project with `list_backlink_submission_projects`
   when the user has not already selected one. Then call
   `get_backlink_submission_profile` before opening any third-party page. The
   profile is usable only when `status` is `confirmed`,
   `confirmedVersion` equals `version`, and `isReady` is `true`. Stop on any
   other state and direct the user to update and confirm the profile in
   Ranklybee.
2. Call `list_backlink_submission_sources` when the user has not selected a
   source. Show each candidate's name, domain, acquisition method, pricing
   model, requirements, and acquisition URL. Do not select a source implicitly.
3. Call `preflight_backlink_submission` for the selected `siteId` and
   `sourceId`. The backend is authoritative for paid entitlement, source
   visibility, profile confirmation, backlink inventory readiness, duplicate
   detection, and daily capacity. Stop on `UPGRADE_REQUIRED`,
   `PROFILE_CONFIRMATION_REQUIRED`, `PROFILE_INCOMPLETE`,
   `BACKLINK_INVENTORY_NOT_READY`, `BACKLINK_ALREADY_EXISTS`, or an unavailable
   source. Do not open the destination when preflight fails or returns an
   existing backlink.
4. Show the user the selected source, destination, and profile fields/copy that
   will be used. Obtain explicit approval for this specific submission before
   creating a job or making an external write.
5. Generate a new idempotency key of at least 8 characters and call
   `create_backlink_submission`. Reuse that exact key for retries; never create
   a second job for the same attempt. The job is created in `waiting_human`
   state and does not click the third-party site's final submit control.
6. For HTTP/HTTPS sources, use the interactive browser to open the returned
   source acquisition URL and map only the confirmed profile fields to the
   source form. Use source `requirements`; do not invent claims, traffic,
   customers, testimonials, pricing, or integrations.
7. Before clicking a third-party form's final submit control, show the user the
   exact source and content again and obtain explicit approval if that approval
   was not already tied to the final action. Never bypass CAPTCHA, MFA, bot
   detection, rate limits, payment, email verification, consent screens, or
   site policies. Pause for human action when required.
8. After an unambiguous result, call `record_backlink_submission_outcome` with
   `submitted`, `pending_review`, `needs_verification`, or `failed`. If the
   result is timed out or ambiguous, record `needs_verification` and never
   repeat the final submit click.

For `mailto:` sources, prepare a reviewable email draft from the confirmed
profile and source requirements. Do not send it or claim that it was sent.

Ranklybee permits at most 15 backlink submission attempts per Project-local
calendar day. A slot is consumed when the durable job is created, including an
attempt that later fails or needs verification. When the backend reports
`DAILY_LIMIT_EXCEEDED`, do not open a source or retry by creating another job;
tell the user the limit resets at the next Project-local calendar day.
