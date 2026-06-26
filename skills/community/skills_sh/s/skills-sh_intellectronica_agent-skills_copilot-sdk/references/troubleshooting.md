# Troubleshooting

## Fast checklist

1. Confirm which SDK and version you are using.
2. Confirm whether the session is using normal Copilot auth or BYOK.
3. Confirm whether the client is spawning the CLI or connecting via `cliUrl`.
4. Turn on debug logging.
5. Check permission handling before debugging anything else.

## Common failures

| Problem | Likely cause | Fix |
| --- | --- | --- |
| CLI not found | CLI missing from PATH, or the app did not point the SDK at its CLI binary | Install `copilot`, set `cliPath` / `CLIPath`, or use the Go bundler workflow for embedded CLI distribution |
| Not authenticated | No CLI login, no token, or wrong auth path | Run `copilot auth login`, pass `githubToken`, or configure BYOK |
| Tool requests never run | No permission handler, or handler denies them | Provide explicit permission handler |
| Streaming output missing | Handler attached after `send()` | Subscribe before sending |
| Content appears empty | Reading wrong field | Use `event.data.content` / `deltaContent` |
| Resume fails | Session ID not stable or not found | Create sessions with your own `sessionId` |
| BYOK resume fails | Provider config not re-supplied | Pass `provider` again on resume |
| MCP server starts but tools do not show up | `tools` filtered them out, or server init failed | Check `tools`, command, args, URL, and auth |
| Session cleanup confusion | Using deprecated lifecycle docs | Prefer `disconnect()`, not `destroy()` |

## Permission handling

This is one of the most common sources of confusion.

- Treat permission handling as required for real application sessions.
- The SDK is deny-by-default for tool execution.
- A session can appear healthy while silently refusing the work you expected it to do.

### Examples

**TypeScript**

```typescript
const session = await client.createSession({
  onPermissionRequest: approveAll,
});
```

**Python**

```python
session = await client.create_session(
    on_permission_request=PermissionHandler.approve_all,
)
```

## Authentication issues

### Standard Copilot auth

Supported paths include:

- Stored Copilot CLI login
- Explicit `githubToken`
- Environment variables such as `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN`

### BYOK

Use a custom `provider` when supplying your own model credentials.

Important BYOK rules:

- `model` is required.
- API keys are not persisted.
- Resume requires the provider config again.
- `type: "azure"` and `type: "openai"` are not interchangeable.
- Azure Managed Identity / Entra is a documented pattern via short-lived `bearerToken` / `bearer_token` values generated outside the SDK (for example with `DefaultAzureCredential`).

## Debug logging

### Enable SDK debug logging

**TypeScript**

```typescript
const client = new CopilotClient({
  logLevel: "debug",
});
```

**Python**

```python
client = CopilotClient({"log_level": "debug"})
```

**Go**

```go
client := copilot.NewClient(&copilot.ClientOptions{
    LogLevel: "debug",
})
```

**.NET**

```csharp
var client = new CopilotClient(new CopilotClientOptions
{
    LogLevel = "debug"
});
```

### CLI log directory

- Node.js and .NET can pass CLI args such as `--log-dir`.
- Python can pass CLI flags via `SubprocessConfig(..., cli_args=[...])`.
- Go and Java are more limited here; use a separately managed headless CLI if you need custom CLI logging.

## Transport issues

The default transport is stdio. If you are debugging startup or sharing a server, switch mentally to the headless/TCP model.

### Start a headless CLI

```bash
copilot --headless --port 4321
```

### Connect to it

```typescript
const client = new CopilotClient({
  cliUrl: "localhost:4321",
});
```

If `cliUrl` is wrong, you will get connection failures that look unrelated to your app logic.

## Event handling mistakes

- `assistant.message` is the final assistant output.
- `assistant.message_delta` is only a chunk.
- `session.idle` is the cleanest completion signal.
- Usage lives in `assistant.usage` and `session.usage_info`, not just the final message.

## Resume and persistence mistakes

- If you do not supply a meaningful `sessionId`, operational resume is clumsy.
- `disconnect()` preserves session state on disk.
- `deleteSession()` removes it permanently.
- Resumable state lives under `~/.copilot/session-state/` unless config overrides it.

## MCP debugging hints

1. Run the MCP server command independently first.
2. Check whether the server supports the expected transport.
3. Verify auth headers or environment variables.
4. Set `tools: ["*"]` while debugging.
5. Watch for permission denials after the tool appears.

## Platform-specific notes

### macOS

- GUI applications may not inherit your shell PATH; set `cliPath` explicitly if needed.

### Windows

- Use explicit executable paths if PATH resolution is inconsistent.

### Linux

- Verify execute permissions and shared-library dependencies if the CLI fails to launch.

## Packaging note for Go

The Go SDK also supports bundling the CLI with `go get -tool github.com/github/copilot-sdk/go/cmd/bundler` followed by `go tool bundler`. If your Go app is distributed rather than run only on developer machines, do not assume a global `copilot` install is the only option.

## Good default debugging sequence

1. Enable debug logging.
2. Swap to a trivial prompt like `What is 2+2?`.
3. Use `approveAll` temporarily.
4. Remove MCP and custom tools until the base session works.
5. Add features back one by one.
