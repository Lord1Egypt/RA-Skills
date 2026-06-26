# Event System

The Copilot SDK emits a rich stream of session events. Event names and payloads have expanded since early preview builds, so older examples are often incomplete.

## Event envelope

Every event includes the same top-level structure:

| Field | Meaning |
| --- | --- |
| `id` | Event UUID |
| `timestamp` | ISO 8601 timestamp |
| `parentId` | Previous event in the chain, if any |
| `ephemeral` | `true` for transient events that are not persisted |
| `type` | Event name |
| `data` | Event-specific payload |

## Subscription patterns

### TypeScript

```typescript
session.on((event) => {
  console.log(event.type, event.data);
});

session.on("assistant.message_delta", (event) => {
  process.stdout.write(event.data.deltaContent ?? "");
});
```

### Python

```python
from copilot.generated.session_events import SessionEventType

def handle(event):
    if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
        print(event.data.delta_content, end="", flush=True)

session.on(handle)
```

### Go

```go
session.On(func(event copilot.SessionEvent) {
    if event.Type == "assistant.message_delta" && event.Data.DeltaContent != nil {
        fmt.Print(*event.Data.DeltaContent)
    }
})
```

### .NET

```csharp
session.On(evt =>
{
    if (evt is AssistantMessageDeltaEvent delta)
    {
        Console.Write(delta.Data.DeltaContent);
    }
});
```

### Java

```java
session.on(AssistantMessageDeltaEvent.class, event -> {
    System.out.print(event.getData().deltaContent());
});
```

## Typical turn flow

Exact order varies, but a normal streamed turn often looks like this:

1. `user.message`
2. `assistant.turn_start`
3. `assistant.intent`
4. `assistant.reasoning_delta` / `assistant.reasoning`
5. `assistant.message_delta`
6. `tool.execution_start`
7. `tool.execution_partial_result` / `tool.execution_progress`
8. `tool.execution_complete`
9. `assistant.message`
10. `assistant.turn_end`
11. `session.idle`
12. `session.usage_info`

For a completed task you may also see `session.task_complete`.

## High-signal event types

### Assistant events

| Event | Purpose | Key fields |
| --- | --- | --- |
| `assistant.turn_start` | Start of a model turn | `turnId`, `interactionId` |
| `assistant.intent` | Human-readable current intent | `intent` |
| `assistant.reasoning` | Full reasoning block | `reasoningId`, `content` |
| `assistant.reasoning_delta` | Streaming reasoning chunk | `reasoningId`, `deltaContent` |
| `assistant.message` | Final assistant message | `messageId`, `content`, `toolRequests`, `reasoningText` |
| `assistant.message_delta` | Streaming response chunk | `messageId`, `deltaContent` |
| `assistant.turn_end` | End of a model turn | `turnId` |
| `assistant.usage` | Per-call token/cost metadata | `model`, `inputTokens`, `outputTokens`, `cost`, `duration` |
| `assistant.streaming_delta` | Network-level stream progress | `totalResponseSizeBytes` |

### Tool events

| Event | Purpose | Key fields |
| --- | --- | --- |
| `tool.execution_start` | Tool started | `toolCallId`, `toolName`, `arguments` |
| `tool.execution_partial_result` | Streaming tool output | `toolCallId`, `partialOutput` |
| `tool.execution_progress` | Progress message | `toolCallId`, `progressMessage` |
| `tool.execution_complete` | Tool finished | `toolCallId`, `success`, `result`, `error` |
| `tool.user_requested` | Tool execution was explicitly user-requested | tool call metadata |

### Session lifecycle events

| Event | Purpose | Notes |
| --- | --- | --- |
| `session.idle` | Turn is done and session can accept more work | Best completion signal |
| `session.error` | Session-level error | Check `data` for details |
| `session.compaction_start` / `session.compaction_complete` | Infinite-session compaction lifecycle | Relevant for long-running sessions |
| `session.title_changed` | Session title updated | Useful for UIs |
| `session.context_changed` | Context window changed | Useful for monitoring |
| `session.usage_info` | Aggregate session usage | Session-wide stats |
| `session.task_complete` | Agent considers the task complete | Useful in managed workflows |
| `session.shutdown` | Session is shutting down | Cleanup signal |

### Permission, user input, and elicitation

| Event | Purpose |
| --- | --- |
| `permission.requested` / `permission.completed` | Permission workflow around tool usage |
| `user_input.requested` / `user_input.completed` | Agent is asking the user a question |
| `elicitation.requested` / `elicitation.completed` | UI form/dialog requests |

### Sub-agent and skill events

| Event | Purpose |
| --- | --- |
| `subagent.started` / `subagent.completed` / `subagent.failed` | Sub-agent lifecycle |
| `subagent.selected` / `subagent.deselected` | Agent selection state |
| `skill.invoked` | A skill was loaded or used |

### Other useful events

| Event | Purpose |
| --- | --- |
| `abort` | In-flight work was cancelled |
| `system.message` | Non-user/system message |
| `external_tool.requested` / `external_tool.completed` | External tool bridging |
| `exit_plan_mode.requested` / `exit_plan_mode.completed` | Plan-mode transition |
| `command.queued` / `command.completed` | Custom slash command execution |

## Streaming behavior

- `streaming: true` adds delta events such as `assistant.message_delta`.
- Final events like `assistant.message` still fire even when streaming is enabled.
- Tool partial/progress events are often ephemeral and should be treated as live UI updates, not durable history.

## Data access conventions by language

| Concept | TypeScript | Python | Go | .NET | Java |
| --- | --- | --- | --- | --- | --- |
| Event type | `event.type` | `event.type` or `event.type.value` depending on API surface | `event.Type` | event class or `EventType` | event class |
| Final text | `event.data.content` | `event.data.content` | `*event.Data.Content` | `evt.Data.Content` | `event.getData().content()` |
| Delta text | `event.data.deltaContent` | `event.data.delta_content` | `*event.Data.DeltaContent` | `evt.Data.DeltaContent` | `event.getData().deltaContent()` |
| Nil / null checks | optional chaining | Python `None` | pointer checks required | nullable strings | nullable accessors |

## Practical guidance

1. Use `assistant.message_delta` for live rendering.
2. Use `assistant.message` for the final canonical text.
3. Use `session.idle` to know when a turn is done.
4. Use `assistant.usage` for per-call accounting and `session.usage_info` for session totals.
5. If you need every detail for audits or replay, store the full event stream from `getMessages()`.
