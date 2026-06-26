# Traces & Logs

Traces and logs are the primary debugging interface for ADK agents. Every conversation turn, tool call, LLM reasoning step, and error is recorded as a trace with spans. The CLI provides structured access to all of it.

## CLI Debugging Tools

Most commands support `--format json` for structured output — **always use it** when consuming output programmatically. The exception is `adk dev`, which has no `--format` flag: use `adk dev --non-interactive` to get a structured NDJSON event stream instead.

| Command                                 | Purpose                                                                                         | Options / tokens                                                                                                                  |
| --------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `adk check --format json`               | Offline project validation — catches config/schema issues before runtime                        | —                                                                                                                                 |
| `adk logs --format json`                | Browse or stream log entries                                                                    | `--follow`, `--summary`, level filters (`error`, `warning`)                                                                       |
| `adk traces --format json`              | Query traces with span details — filter by workflow, action, trigger, conversation, error, time | `workflow=`, `action=`, `trigger=`, `conversation=`, `trace=`, `error`, `since=`, `until=`, `limit=`, `--follow`, `--include-llm` |
| `adk workflows runs --format json`      | List or inspect durable workflow runs by id, name, or status                                    | `name=`, `status=`, `limit=`, `nextToken=`, `<wrkflow_id>`                                                                        |
| `adk chat --single "msg" --format json` | Send a test message and get structured response                                                 | `--conversation-id`                                                                                                               |
| `adk dev --non-interactive`             | Start dev server with structured NDJSON event stream (no TUI)                                   | —                                                                                                                                 |

## Querying Logs

Logs give a high-level view of what happened. Start here before diving into traces.

```bash
adk logs --format json                          # last 50 entries
adk logs error --format json                    # errors only
adk logs warning --format json                  # warnings and above
adk logs warning since=1h --format json         # warnings from the last hour
adk logs error limit=10 --format json           # last 10 errors
adk logs --follow --format json                 # stream live as NDJSON
adk logs --summary --format json                # single snapshot summary
```

### When to use logs vs traces

- **Logs** — quick error scanning, startup issues, integration failures, deployment problems
- **Traces** — detailed per-conversation analysis, tool call inspection, LLM reasoning review

## Querying Traces

Traces provide the full picture of a conversation turn: every span in order. The command takes positional filter tokens (not flags) for slicing the trace store.

```bash
adk traces --format json                                    # recent traces (default limit 20)
adk traces error --format json                              # error traces only
adk traces workflow=<name> --format json                    # traces for a workflow
adk traces conversation=<id> --format json                  # traces for a conversation
adk traces trace=<id> --include-llm --format json           # drill into one trace with LLM content
adk traces since=1h limit=50 --format json                  # last hour, up to 50
adk traces error --follow --format json                     # stream errors live (NDJSON)
```

Combine tokens freely (`adk traces error workflow=onboarding since=1h`). `--format` only accepts `json`; omit it for the default text output.

### Trace Structure

A trace represents one unit of agent activity. Each trace contains:

- **Trace ID** — unique identifier
- **Timestamp** — when the trace was recorded
- **Conversation ID** — which conversation it belongs to
- **Type** — the kind of activity
- **Spans** — ordered list of sub-events within the trace

### Span Types

Spans are the atomic units inside a trace. Each span has a `type` field:

| Span Type                  | Key Fields                                         | What It Means                                                         |
| -------------------------- | -------------------------------------------------- | --------------------------------------------------------------------- |
| `tool_call`                | `tool_name`, `input`, `output`, `success`, `error` | A tool was invoked. Check `success` to see if it worked.              |
| `code_execution_exception` | `message`, `stackTrace`                            | Code error in the LLMz sandbox. Read `stackTrace` to find the source. |
| `think`                    | `content`                                          | LLM reasoning step — shows why the model made a decision.             |
| `end`                      | —                                                  | Conversation turn completed.                                          |

### Reading a Trace

When analyzing a trace:

1. Look at spans in chronological order
2. Find where behavior diverges from expected
3. For `tool_call` spans: check `success`, read `error` if false, verify `input` matches expectations
4. For `think` spans: understand model reasoning before a tool call
5. For `code_execution_exception`: read the stack trace, correlate with source code

## Reproducing Issues with `adk chat`

Use `adk chat` to send test messages and generate fresh traces:

```bash
# Single message with structured output
adk chat --single "Hello" --format json

# Continue an existing conversation
adk chat --single "Follow-up message" --conversation-id <id> --format json
```

The JSON output includes the bot's response and conversation ID, which you can use to query traces for that specific conversation and send subsequent messages.

## Programmatic Trace Access: `onTrace` Hook

For monitoring traces in code, use the `onTrace` hook in conversation handlers. This is useful for custom logging, performance monitoring, and automated error detection. The Botpress ADK also has an OTLP endpoint that can be enabled with the `--otlp` flag on `adk dev`, if the current environment is setup for OTLP traces.

### Basic Trace Logging

```typescript
// src/conversations/extensions/logging.ts
import { Autonomous } from '@botpress/runtime'

export const onTraceLogging: Autonomous.Hooks['onTrace'] = ({ trace, iteration }) => {
  if (trace.type === 'code_execution_exception') {
    console.error(`Code Execution Error: ${trace.message}`, trace.stackTrace)
  }

  if (trace.type === 'tool_call' && !trace.success) {
    console.error(
      `Error during tool call to "${trace.tool_name}" with input "${JSON.stringify(trace.input)}":`,
      trace.error
    )
  }
}
```

### Comprehensive Trace Logging

```typescript
export const onTraceLogging: Autonomous.Hooks['onTrace'] = ({ trace, iteration }) => {
  switch (trace.type) {
    case 'code_execution_exception':
      console.error(`[CODE ERROR] ${trace.message}`, trace.stackTrace)
      break
    case 'tool_call':
      if (trace.success) {
        console.log(`[TOOL SUCCESS] ${trace.tool_name}`, trace.output)
      } else {
        console.error(`[TOOL ERROR] ${trace.tool_name}`, trace.error)
      }
      break
    case 'think':
      console.debug(`[THINK] ${trace.content}`)
      break
    default:
      console.log(`[TRACE] ${trace.type}`, trace)
  }
}
```

### Using in a Conversation

```typescript
import { Conversation } from '@botpress/runtime'
import { onTraceLogging } from './extensions/logging'

export default new Conversation({
  channel: '*',
  handler: async ({ execute }) => {
    await execute({
      instructions: `You are a helpful assistant...`,
      hooks: {
        onTrace: (props) => onTraceLogging!(props),
      },
    })
  },
})
```

### Performance Monitoring

```typescript
export const makePerformanceMonitor = () => {
  const startTime = Date.now()
  const toolStartTimes = new Map<string, number>()
  const toolMetrics = new Map<string, number[]>()

  const onBeforeTool: Autonomous.Hooks['onBeforeTool'] = async ({ tool }) => {
    toolStartTimes.set(tool.name, Date.now())
  }

  const onAfterTool: Autonomous.Hooks['onAfterTool'] = async ({ tool }) => {
    const start = toolStartTimes.get(tool.name)
    const duration = start ? Date.now() - start : 0
    const metrics = toolMetrics.get(tool.name) || []
    metrics.push(duration)
    toolMetrics.set(tool.name, metrics)
    console.log(`[PERF] ${tool.name}: ${duration}ms`)
  }

  const onTrace: Autonomous.Hooks['onTrace'] = ({ trace }) => {
    if (trace.type === 'end') {
      console.log(`[PERF] Total conversation: ${Date.now() - startTime}ms`)
      console.log(`[PERF] Tool metrics:`, Object.fromEntries(toolMetrics))
    }
  }

  return { onBeforeTool, onAfterTool, onTrace }
}
```

### Hook Reference

| Hook           | Parameters                               | When It Fires         |
| -------------- | ---------------------------------------- | --------------------- |
| `onBeforeTool` | `{ iteration, tool, input, controller }` | Before each tool call |
| `onAfterTool`  | `{ tool, output }`                       | After each tool call  |
| `onTrace`      | `{ trace, iteration }`                   | On every trace event  |
