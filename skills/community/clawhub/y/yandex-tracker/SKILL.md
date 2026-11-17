---
name: yandex-tracker
description: Manages Yandex Tracker issues, queues, comments, attachments, links, worklogs, searches, and bulk changes through the Python yandex_tracker_client. Use when a user asks to read, create, update, transition, organize, or report on Yandex Tracker data.
license: MIT
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: ["python3"]
      env: ["TRACKER_TOKEN"]
      envOneOf: ["TRACKER_ORG_ID", "TRACKER_CLOUD_ORG_ID"]
    install:
      - id: pip-yandex-tracker-client
        kind: pip
        package: yandex_tracker_client
        label: Install yandex_tracker_client (pip)
        provenance: https://pypi.org/project/yandex-tracker-client/
---

# Yandex Tracker

Use `yandex_tracker_client` to interact with Yandex Tracker API v2. Use the execution, secret-management, and temporary-file facilities available in the current runtime.

## Workflow

1. Identify whether the request is read-only or mutating. Do not create, update, transition, delete, or bulk-change data unless the user has authorized that action and its scope is clear.
2. Read only the topic references needed for the request.
3. Before the first API call in an environment, follow [setup and authentication](references/setup-and-auth.md).
4. For multi-step work, create one self-contained Python script in a runtime-appropriate temporary or working directory. Combine related queries and mutations in that script, then print a concise structured result.
5. Materialize lazy API iterables with `list(...)` before counting, sorting, reusing, or summarizing them.
6. Discover queue-specific values instead of guessing custom field keys, transition IDs, resolutions, users, or sprint IDs.
7. After a mutation, report the affected issue keys and the confirmed result. For asynchronous bulk changes, wait for completion and surface failures.

## Safety

- Treat tokens and organization identifiers as secrets. Read them from the runtime's secret or environment mechanism; never print, persist, or embed them in generated scripts.
- Use least-privilege credentials. Do not broaden permissions or install dependencies without the authorization required by the current runtime.
- Inspect the current issue state before applying a context-dependent update. For list-valued fields, distinguish full replacement from `add`/`remove` mutations.
- Before a broad or destructive bulk operation, show or otherwise verify the exact issue set and intended change.

## Topic index

- **Environment, credentials, client initialization, and portable execution:** read [setup and authentication](references/setup-and-auth.md) before the first API call or when setup fails.
- **Queries, filters, custom fields, pagination, and aggregation:** read [search and reporting](references/search-and-reporting.md) for discovery or reporting tasks.
- **Get, create, update, and transition issues:** read [issue lifecycle](references/issue-lifecycle.md) for issue mutations and status changes.
- **Comments, mentions, attachments, and issue links:** read [collaboration](references/collaboration.md) only when the request involves those resources.
- **Worklogs, queues, users, boards, and sprints:** read [worklogs and planning](references/worklogs-and-planning.md) for time tracking or planning metadata.
- **Multi-issue updates, transitions, and moves:** read [bulk operations](references/bulk-operations.md) before any bulk change.
- **Dynamic objects, field shapes, and exceptions:** read [object reference](references/object-reference.md) when inspecting unfamiliar return values or handling API errors.
- **OpenClaw-specific installation and configuration:** read [OpenClaw compatibility](references/openclaw.md) only when the skill runs in OpenClaw.
