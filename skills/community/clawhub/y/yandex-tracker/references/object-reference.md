# Object reference and errors

Read this file when inspecting unfamiliar return values, formatting API results, or handling failures.

## Contents

- Dynamic object behavior
- Issue fields
- Comment, link, attachment, transition, and worklog fields
- Queue, user, and bulk-change fields
- Error handling

## Dynamic object behavior

Tracker objects are dynamic. Accessing a missing attribute returns `None` rather than raising `AttributeError`. Call `.as_dict()` to inspect the complete object, including custom fields.

Reference-valued fields such as status, priority, assignee, queue, and type expose attributes such as `.id`, `.display`, `.key`, or `.login` without a second request.

## Issue fields

| Attribute | Shape and notes |
|---|---|
| `key` | `str`, for example `QUEUE-42` |
| `summary` | `str` |
| `description` | `str \| None` |
| `status` | Reference with `.id` and `.display` |
| `priority` | Reference with `.id` |
| `type` | Reference with `.id` |
| `queue` | Reference with `.key` |
| `assignee` | Reference or `None`, with `.login` and `.display` |
| `reporter` / `createdBy` | Reference with `.login` |
| `createdAt` / `updatedAt` | ISO 8601 string |
| `deadline` | Date string or `None` |
| `tags` | `list[str]` |
| `followers` | `list[Reference]` |
| `components` / `fixVersions` | `list[Reference]` |
| `sprint` | `list[Reference] \| None` |
| `parent` | Reference or `None`, with `.key` |
| `votes` | `int` |

## Related resource fields

### Comment

| Attribute | Shape and notes |
|---|---|
| `id` | `int` |
| `text` / `textHtml` | `str` |
| `createdBy` | Reference with `.login` and `.display` |
| `createdAt` / `updatedAt` | ISO 8601 string |
| `summonees` / `attachments` | `list[Reference]` |

### Link

| Attribute | Shape and notes |
|---|---|
| `id` | `int` |
| `type` | Reference with relationship `.id` |
| `direction` | `inward` or `outward` |
| `object` | Reference with linked issue `.key` and `.display` |
| `createdBy` / `createdAt` | Reference and ISO 8601 string |

### Attachment

| Attribute | Shape and notes |
|---|---|
| `id` | `int` |
| `name` | Filename |
| `content` | Download URL |
| `mimetype` | MIME type string |
| `size` | Bytes as `int` |
| `createdBy` / `createdAt` | Reference and ISO 8601 string |

### Transition

| Attribute | Shape and notes |
|---|---|
| `id` | Queue-specific transition ID |
| `to` | Reference with target status `.id` and `.display` |
| `screen` | Reference or `None` |

### Worklog entry

| Attribute | Shape and notes |
|---|---|
| `id` | `int` |
| `issue` | Reference with `.key` |
| `comment` | `str \| None` |
| `start` / `createdAt` | ISO 8601 string |
| `duration` | ISO 8601 duration string |
| `createdBy` | Reference with `.login` |

## Administrative fields

### Queue

| Attribute | Shape and notes |
|---|---|
| `id` | `int` |
| `key` / `name` | `str` |
| `description` | `str \| None` |
| `lead` | Reference with `.login` and `.display` |
| `assignAuto` | `bool` |
| `defaultType` / `defaultPriority` | Reference |
| `teamUsers` | `list[Reference]` |

### User

| Attribute | Shape and notes |
|---|---|
| `uid` | `int` |
| `login` / `display` / `email` | `str` |
| `firstName` / `lastName` | `str` |

### BulkChange

| Attribute | Shape and notes |
|---|---|
| `id` | `str` |
| `status` | `COMPLETE`, `FAILED`, or `PROCESSING` |
| `statusText` | Status details |
| `executionChunkPercent` | `int` |
| `executionIssuePercent` | `int` |

## Error handling

Catch specific client exceptions and return actionable context without exposing credentials or sensitive payloads:

```python
from yandex_tracker_client import exceptions

try:
    issue = client.issues["QUEUE-99999"]
except exceptions.NotFound:
    print("Issue not found")
except exceptions.Forbidden:
    print("No access to this queue or issue")
except exceptions.BadRequest as error:
    print("Invalid field or value:", error)
except exceptions.Conflict:
    # Re-fetch before deciding whether the authorized update is still valid.
    issue = client.issues["QUEUE-42"]
except exceptions.TrackerClientError as error:
    print("Tracker request failed:", error)
```

On `Conflict`, re-fetch and reassess; do not blindly repeat a context-dependent mutation. On authentication or permission failures, stop and identify the missing access rather than requesting broader credentials automatically.
