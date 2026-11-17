# Runtime and stream contract

Read this reference when building the agent loop, provider adapter, Stop behavior, or renderer state. The executable event union is [contracts/events.schema.json](contracts/events.schema.json), the pure state machine is [runtime/stream-reducer.mjs](runtime/stream-reducer.mjs), and complete replay cases are in [fixtures/turns.json](fixtures/turns.json).

## Boundary

Keep four components separate:

1. The provider adapter translates a model provider's native stream into internal progress.
2. The host resolves tools, validates canvases, owns credentials, and emits renderer events.
3. The renderer consumes only the six versioned host events below.
4. The snapshot store supplies the same normalized observations to widgets and `read_screen`.

The renderer must not consume provider events directly. Provider formats can change without changing the renderer contract.

Every public host event has `schemaVersion: "2.0"`, one `turnId`, and a contiguous integer `seq` beginning at zero. The host chooses `shape: "text"` or `shape: "canvas"` before visible output and includes it in `turn_start`.

| Event | Required payload | Renderer effect |
|---|---|---|
| `turn_start` | `shape` | Create one pending turn. |
| `text_delta` | `text` | Append to a text turn, or buffer privately for a canvas turn. |
| `tool_call` | `callId`, `toolId`, `argSummary` | Add one pending, human-readable chip. |
| `tool_result` | `callId`, `status`, `summary` | Settle the matching chip from the actual resolver result. |
| `artifact` | `artifactId`, `kind: "canvas"`, validated `body` AST | Atomically commit one canvas. |
| `turn_end` | `status`, optional `fallbackText` | Make the turn terminal. |

The wire contains no raw tool arguments, partial JSON, API response bodies, credentials, or source XML. Keep source XML in the host's saved artifact record. The renderer receives only the validated AST.

## Bounded loop

Route the request first. Resolve company names or ambiguous intent before choosing a canvas. Use text when clarification is needed.

For each accepted turn:

1. Emit `turn_start` at `seq: 0` with the chosen shape.
2. Ask the model for the next response step using only registered tool schemas.
3. Convert complete tool requests into safe `tool_call` chips, run independent handlers in parallel, and emit `tool_result` only when each handler settles.
4. Feed normalized successes and typed failures back to the model. Limit the overall tool loop to six rounds.
5. For text shape, stream visible text and finish. For canvas shape, buffer model prose, parse complete XML, validate the AST, and commit one artifact.
6. If canvas validation fails, return the typed validation error to the model for at most one repair within the same turn budget. If repair fails, emit `turn_end` with `status: "error"` and a concise `fallbackText`.

Never stream incomplete XML into a parser or renderer. A rejected artifact does not advance reducer state, so a corrected artifact retries the same sequence number. Preserve the last good canvas in history while a new canvas is being prepared.

## Provider adapter mapping

A provider adapter may expose five kinds of progress. They are adapter inputs, not a second UI protocol.

| Provider progress | Host behavior |
|---|---|
| `thinking` | Keep it private. The host can show a generic busy state from the active turn. |
| `tool_start` | Start accumulating the tool request. Emit nothing until the host has a complete call ID, registered tool ID, and safe summary. |
| `tool_input_delta` | Append to host-private argument JSON. Never forward partial JSON. |
| `tool_end` | Finish tool input only. It does not mean the resolver ran or succeeded. |
| `text_delta` | Emit for text shape. Buffer for canvas shape until artifact validation settles. |

Resolver completion, timeout, rate limit, preview result, or handler error produces the host `tool_result`. A provider `tool_end` can never settle a chip.

Generate `argSummary` from an allowlisted formatter for each tool, such as `$NVDA` or `dashboard`. Truncate the formatted label to at most 96 JavaScript UTF-16 code units before emitting it; a longer label is rejected with `INVALID_FIELD` and breaks the turn. Never format or truncate serialized raw arguments into a label. A short result summary can name a success, preview, or typed failure, but must not copy a raw response.

## Shape rules

A text turn may emit text and tool events, then one terminal event. It cannot emit an artifact or fallback text. A canvas turn may emit tool events and buffered text. Apply these terminal outcomes exactly:

| Shape | Artifact state | `turn_end.status` | `fallbackText` | Result |
|---|---|---|---|---|
| Text | None | `success`, `error`, or `stopped` | Forbidden | End the text turn. An error or stop interrupts pending chips. |
| Canvas | Committed | `success` | Forbidden | Keep the artifact. All tool chips must already be settled. |
| Canvas | None | `success` | Forbidden | Reject with `MISSING_ARTIFACT`. |
| Canvas | None | `error` | Required | End with the concise fallback after repair is exhausted. |
| Canvas | Committed | `error` | Forbidden | Preserve the artifact and end in error. |
| Canvas | None or committed | `stopped` | Forbidden | Preserve any committed artifact and interrupt pending chips. |

`fallbackText` is valid only for an errored canvas turn with no artifact. A successful turn of either shape cannot end with a pending tool call. Error and stopped endings convert pending chips to interrupted.

Do not show buffered canvas prose beside the committed canvas. It often repeats the same claims. Status and tool chips remain visible. A host error after an artifact commit keeps that validated artifact and ends the turn with error status.

`artifactId` must equal `body.id`. Reopening history uses that stable ID and the saved AST. Manual refresh changes only an ephemeral host view binding to a new snapshot, never the saved AST.
The renderer and `read_screen` use the same effective binding; history reopens with its original evidence.
See [app-shell.md](app-shell.md) for the refresh IPC boundary. A new authored analysis requires a new turn and artifact.

## Sequence and transition handling

Start every new turn at sequence zero. Accept only the next integer for that turn. Reject a gap, duplicate sequence, unknown turn, duplicate call ID, orphan result, second result, shape mismatch, second artifact, invalid canvas, or incompatible contract version without mutating state.

Once `turn_end` is accepted, ignore every later event for that turn ID, including a tool result or artifact with an otherwise invalid payload. Do not retain ignored event bodies. A subsequent user request gets a new turn ID. A successful turn cannot end with a pending tool call. Error and stopped endings mark pending chips as interrupted so the UI does not leave a permanent spinner.

The reducer returns one of these forms:

```js
{ state: nextState, accepted: true }
{ state: originalState, accepted: false, error: { code, message, path? } }
{ state: originalState, accepted: false, ignoredReason: "turn_already_terminal" }
```

Use it as a pure reducer:

```js
import { createStreamState, reduceStreamEvent } from "./runtime/stream-reducer.mjs";

let state = createStreamState();
for await (const event of hostEvents) {
  const result = reduceStreamEvent(state, event);
  if (result.accepted) state = result.state;
  else if (result.error) recordContractError(result.error);
}
```

The reducer bounds each event to 64 KiB, a text delta to 8,192 JavaScript UTF-16 code units, cumulative turn text to 262,144 code units, tool chips to 64, argument summaries to 96 code units, and summaries or fallback text to 2,048 code units. Apply smaller product limits when appropriate.

## Stop and cancellation

When the user selects Stop:

1. Ask the provider adapter to abort if it supports abort.
2. Cancel or detach outstanding host resolvers where safe.
3. Emit the next valid sequence as `turn_end` with `status: "stopped"`.
4. Discard every later provider delta and resolver completion for that turn.

Do not claim that provider billing stopped. Some adapters cannot cancel work already accepted upstream. Stop guarantees only that the local host stops rendering and accepting results.

## Replay inventory

[fixtures/turns.json](fixtures/turns.json) contains complete, deterministic event arrays and expected reducer outcomes for:

- A successful text answer.
- A successful canvas with buffered prose and one atomic artifact.
- A failed tool whose typed failure still permits a text answer.
- A malformed canvas, one repair at the same sequence, and then success.
- A malformed canvas whose repair is exhausted and releases fallback text.
- A successful canvas ending rejected before any artifact, followed by a valid error fallback at the same sequence.
- A stopped canvas ending with fallback text rejected, followed by a valid stopped ending at the same sequence.
- A stopped turn followed by ignored late text, tool result, and artifact events.

Run these replays through the reducer rather than copying event snippets into application code. Validate every accepted event against the event schema as a separate gate. Runtime transition validity and JSON Schema validity answer different questions.

### Standalone reducer replay

From the emitted `stock-terminal/references/` directory, save this temporary check as `verify-stream.mjs`, run `node verify-stream.mjs`, and remove the temporary file after it prints the replay count. Node is used only for this check. The reducer itself uses browser-standard JavaScript APIs.

```js
import { readFile } from "node:fs/promises";
import { createStreamState, reduceStreamEvent } from "./runtime/stream-reducer.mjs";

const fixture = JSON.parse(await readFile("./fixtures/turns.json", "utf8"));
for (const replay of fixture.replays) {
  let state = createStreamState();
  const errors = [];
  const ignored = [];
  let accepted = 0;
  for (const event of replay.events) {
    const result = reduceStreamEvent(state, event);
    if (result.accepted) {
      state = result.state;
      accepted += 1;
    } else if (result.error) errors.push(result.error.code);
    else ignored.push(result.ignoredReason);
  }
  const turn = state.turns[replay.events[0].turnId];
  if (accepted !== replay.expected.accepted
      || JSON.stringify(errors) !== JSON.stringify(replay.expected.errors)
      || JSON.stringify(ignored) !== JSON.stringify(replay.expected.ignored)
      || turn.status !== replay.expected.status) {
    throw new Error(`Replay failed: ${replay.name}`);
  }
}
console.log(`stream replays passed: ${fixture.replays.length}`);
```

## Host security checks

Read credentials only in the host process inside allowlisted request handlers. They must never enter model messages, tool schemas, event objects, logs, fixture data, or renderer state. Add a distinctive fake secret to a test handler and assert that it is absent from every serialized public event and final reducer state.

Reject unexpected event properties. In particular, `rawArgs`, `arguments`, `sourceXml`, and arbitrary provider fields are not part of any event. Treat `argSummary`, `summary`, `fallbackText`, and canvas narrative as untrusted display text and escape them in native components. Do not render them as HTML.
