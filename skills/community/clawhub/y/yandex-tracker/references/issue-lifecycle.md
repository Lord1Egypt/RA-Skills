# Issue lifecycle

Read this file when getting, creating, updating, or transitioning issues.

## Get an issue

```python
issue = client.issues["QUEUE-42"]
print(
    issue.key,
    issue.summary,
    issue.status.id,
    issue.assignee.login if issue.assignee else None,
)
```

## Create an issue

Queue and summary are required. Discover queue-specific types, fields, components, users, and sprint IDs rather than guessing them.

```python
issue = client.issues.create(
    queue="QUEUE",
    summary="Bug: login fails",
    type={"name": "Bug"},  # or {"id": "bug"}
    description="Steps...",
    assignee="user_login",
    priority="critical",
    followers=["login1", "login2"],
    tags=["backend", "urgent"],
    components=["component_name"],
    parent="QUEUE-10",
    sprint={"id": 123},
)
print(issue.key)
```

List issue types with `client.issue_types.get_all()` when the valid ID is unknown.

## Update an issue

Inspect current values before a context-dependent update. Passing a list replaces the entire field; use a mutation dictionary for a partial change.

```python
issue.update(
    summary="New title",
    description="Updated text",
    assignee="other_login",
    priority="minor",
    tags={"add": ["reviewed"], "remove": ["draft"]},
    followers={"add": ["login1"]},
    components={"add": ["comp"], "remove": []},
)
```

Full replacement remains valid when explicitly intended:

```python
issue.update(tags=["new_tag"])
```

## Transition status

Transition IDs and valid resolutions are queue-specific. Always inspect them before execution:

```python
for transition in issue.transitions.get_all():
    print(transition.id, transition.to.id, transition.to.display)

for resolution in client.resolutions.get_all():
    print(resolution.id, resolution.display)
```

Then execute the selected transition:

```python
issue.transitions["close"].execute(
    comment="Fixed in v2.3",
    resolution="fixed",
)
```

After creating, updating, or transitioning, re-read or inspect the returned object when confirmation of the resulting state matters.
