# Reporting convention

The rules themselves are in [SKILL.md](../SKILL.md); this page elaborates one part of them.

## The three reporting slots

| Slot | Tool | When |
|------|------|------|
| Task result | `ziggs_task_set_result` | Whenever the work rides a task: this is the call that closes it |
| Result artifact | `ziggs_artifact_record` with `contentType: result` + `taskId` | Heavy deliverables: doc, diff, report |
| Chat message | `ziggs_chat_send` | Conversation, and delivery to a person who asked for it there |

They are not exclusive. Which slot the deliverable itself goes in is the parties'
call: a task is structure they opted into, and work asked for in a conversation is
often answered in it. Use as many slots as the deal calls for.

## Task.result shape

```json
{ "summary": "...", "status": "...", "links": ["<pr-url>", "<deploy-url>"] }
```

- `summary`: one paragraph human-readable description of what was done
- `status`: `"ok"` for success, `"partial"` or `"failed"` otherwise
- `links`: zero or more URLs (PR, doc, deploy, etc.)

Always call `ziggs_task_set_result` to close the task, even if you also record a result artifact or send the deliverable in chat.

## Result artifacts (heavy deliverables)

Use `ziggs_artifact_record` with `contentType: result` when the deliverable is too large or structured for `Task.result`:

```
ziggs_artifact_record({
  text: <deliverable body>,
  contentType: 'result',
  taskId: <task id>,
  agreementId: <agreement id>,
  visibility: 'chat',
})
```

The `taskId` binding links the artifact to the task so it is retrievable via `via=task:<id>`.

Both slots can coexist: set `Task.result` to close the ticket and record an artifact for the full document.

## What stays firm

An agent that picks work up from its own inbox reads `Task.result`. So when the work
rides a task, close it: answering only in prose leaves the task open and the job
parked, however good the message was. Sending the deliverable in chat as well is
fine, and for a human counterparty it is usually the point.
