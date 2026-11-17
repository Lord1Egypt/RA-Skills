# Bulk operations

Read this file before updating, transitioning, or moving multiple issues.

## Preflight

1. Materialize the exact issue set and print the keys plus the intended change.
2. Verify the request authorizes the operation and scope.
3. For transitions, inspect valid transition IDs and required fields on representative issues. Do not assume every queue uses the same workflow.
4. For queue moves, verify the destination queue and whether fields or statuses should be preserved.

The `issues` argument may be a list of issue keys or issue objects returned by `find()`.

## Bulk update

```python
change = client.bulkchange.update(
    ["QUEUE-1", "QUEUE-2", "QUEUE-3"],
    priority="minor",
    assignee="user_login",
    tags={"add": ["reviewed"], "remove": ["draft"]},
)
change.wait()
print(change.status, change.statusText)
```

## Bulk transition

```python
change = client.bulkchange.transition(
    ["QUEUE-1", "QUEUE-2"],
    "close",
    resolution="wontFix",
)
change.wait()
print(change.status, change.statusText)
```

## Bulk move

```python
change = client.bulkchange.move(
    ["QUEUE-1", "QUEUE-2"],
    "NEWQUEUE",
    move_all_fields=False,
    move_to_initial_status=False,
)
change.wait()
print(change.status, change.statusText)
```

## Verification loop

After `wait()`, require `change.status == "COMPLETE"`. If it is `FAILED`, report `statusText` and do not claim success. For high-impact operations, fetch the affected issues again and verify the requested state before reporting completion.
