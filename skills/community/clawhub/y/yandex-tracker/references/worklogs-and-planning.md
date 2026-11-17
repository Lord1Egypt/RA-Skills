# Worklogs and planning

Read this file for time tracking, queue metadata, users, boards, or sprints.

## Worklogs

Durations use ISO 8601, such as `PT30M`, `PT2H`, or `P1DT2H30M`.

```python
entry = issue.worklog.create(
    duration="PT1H30M",
    comment="Fixed auth bug",
    start="2026-02-24T10:00:00+03:00",
)

for entry in list(issue.worklog.get_all()):
    print(entry.id, entry.duration, entry.comment, entry.createdBy.login)

issue.worklog[42].update(duration="PT2H", comment="Revised estimate")
issue.worklog[42].delete()

entries = list(
    client.worklog.find(
        issue=["QUEUE-1", "QUEUE-2"],
        createdBy="me()",
    )
)
```

Confirm the duration, start time, issue key, and user scope before creating, updating, or deleting worklog entries.

## Queues

```python
queue = client.queues["QUEUE"]
print(queue.key, queue.name, queue.lead.login)

for queue in client.queues.get_all():
    print(queue.key, queue.name)
```

## Users

Resolve a user's login when the request names a person rather than a Tracker login:

```python
for user in client.users.get_all():
    print(user.login, user.display, user.email)

me = client.myself
print(me.login)
```

If more than one user matches a name, do not guess; present the candidates or ask for the exact account.

## Boards and sprints

```python
for board in client.boards.get_all():
    print(board.id, board.name)

for sprint in client.boards[123].sprints.get_all():
    print(sprint.id, sprint.name, sprint.status)

issue.update(sprint={"id": 456})
```

Discover the board and sprint ID first. Sprint statuses commonly include `active`, `closed`, and `draft`.
