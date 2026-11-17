# Collaboration resources

Read this file only when the request involves comments, mentions, attachments, or links between issues.

## Comments

```python
for comment in list(issue.comments.get_all()):
    print(comment.id, comment.createdBy.login, comment.text)

comment = issue.comments.create(
    text="Fixed in v2.3",
    summonees=["login1", "login2"],
    attachments=["path/to/file.png"],
)

issue.comments[42].update(
    text="Corrected note",
    summonees=["login1"],
)
issue.comments[42].delete()
```

`summonees` triggers mention notifications. Verify recipients and attachment paths before creating the comment. Delete a comment only when the user has explicitly requested deletion.

## Issue links

```python
for link in issue.links:
    print(link.type.id, link.direction, link.object.key)

issue.links.create(issue="OTHER-10", relationship="relates")
issue.links[42].delete()
```

Common relationship values include:

- `relates`
- `blocks` / `is blocked by`
- `duplicates` / `is duplicated by`
- `depends on` / `is dependent of`
- `is subtask for` / `is parent task for`

Confirm the direction and both issue keys before creating or deleting a link.

## Attachments

```python
for attachment in issue.attachments:
    print(
        attachment.id,
        attachment.name,
        attachment.mimetype,
        attachment.size,
    )

attachment = issue.attachments.create("path/to/file.txt")
attachment.download_to("path/to/output-directory")
issue.attachments[42].delete()
```

Use runtime-appropriate paths. Do not hardcode `/tmp` or a platform-specific directory. Confirm the target file before upload and the attachment ID before deletion.
