# Search and reporting

Read this file for Tracker Query Language, structured filters, custom-field discovery, pagination, grouping, or reporting.

## Search

```python
# Tracker Query Language copied or adapted from Tracker UI
issues = client.issues.find(
    "Queue: QUEUE Assignee: me() Status: inProgress"
)

# Structured filter
issues = client.issues.find(
    filter={
        "queue": "QUEUE",
        "assignee": "user_login",  # login or "me()"
        "author": "user_login",
        "status": "inProgress",
        "type": "bug",
        "priority": "critical",
        "tags": ["backend", "urgent"],
        "created": {"from": "2026-01-01", "to": "2026-02-01"},
        "updated": {"from": "2026-01-15"},
        "deadline": {"to": "2026-03-01"},
        "followers": "user_login",
        "components": "component_name",
    },
    order=["-updatedAt", "+priority"],
    per_page=100,
)

# Batch fetch known issue keys
issues = client.issues.find(keys=["QUEUE-1", "QUEUE-2", "QUEUE-3"])
```

Iteration fetches additional pages automatically. Materialize the result before counting, sorting, reusing, or aggregating it:

```python
issues = list(issues)
```

## Aggregation

Combine related queries in one script and fetch each resource only as needed. For example:

```python
from collections import Counter

issues = list(client.issues.find(filter={"queue": "QUEUE"}, per_page=100))
counts = Counter(
    issue.assignee.login if issue.assignee else "unassigned"
    for issue in issues
)

for assignee, count in counts.most_common():
    print(f"{count:3d}  {assignee}")
```

## Custom fields

Custom field keys are queue-specific and usually use camelCase. Discover them from a real issue or the field catalog before filtering or updating:

```python
print(issue.as_dict())

for field in client.fields.get_all():
    print(field.id, field.name)
```

Use the discovered field ID as an attribute or keyword:

```python
print(issue.storyPoints)
issue.update(storyPoints=5, myCustomField="value")

issues = client.issues.find(
    filter={"queue": "QUEUE", "storyPoints": {"from": 3}}
)
```

Do not guess a custom field key from its display name.
