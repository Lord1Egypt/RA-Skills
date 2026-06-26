# Working Examples

## Before you start

- Use an explicit permission handler for real sessions.
- Register streaming/event handlers before `send()`.
- Prefer `disconnect()` over `destroy()`.
- If you want resumable sessions, provide your own `sessionId`.

## Minimal chat examples

### TypeScript / Node.js

```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();

const session = await client.createSession({
  model: "gpt-5",
  streaming: true,
  onPermissionRequest: approveAll,
});

session.on("assistant.message_delta", (event) => {
  process.stdout.write(event.data.deltaContent ?? "");
});

await session.sendAndWait({ prompt: "What is 2+2?" });

await session.disconnect();
await client.stop();
```

### Python

```python
import asyncio
from copilot import CopilotClient
from copilot.session import PermissionHandler

async def main():
    async with CopilotClient() as client:
        session = await client.create_session(
            model="gpt-5",
            streaming=True,
            on_permission_request=PermissionHandler.approve_all,
        )

        def on_event(event):
            if event.type.value == "assistant.message_delta":
                print(event.data.delta_content or "", end="", flush=True)

        session.on(on_event)
        await session.send_and_wait("What is 2+2?")
        await session.disconnect()

asyncio.run(main())
```

### Go

```go
package main

import (
    "context"
    "fmt"
    "log"

    copilot "github.com/github/copilot-sdk/go"
)

func main() {
    ctx := context.Background()
    client := copilot.NewClient(nil)
    if err := client.Start(ctx); err != nil {
        log.Fatal(err)
    }
    defer client.Stop()

    session, err := client.CreateSession(ctx, &copilot.SessionConfig{
        Model:               "gpt-5",
        Streaming:           true,
        OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
    })
    if err != nil {
        log.Fatal(err)
    }
    defer session.Disconnect()

    session.On(func(event copilot.SessionEvent) {
        if event.Type == "assistant.message_delta" && event.Data.DeltaContent != nil {
            fmt.Print(*event.Data.DeltaContent)
        }
    })

    if _, err := session.SendAndWait(ctx, copilot.MessageOptions{
        Prompt: "What is 2+2?",
    }); err != nil {
        log.Fatal(err)
    }
}
```

### .NET

```csharp
using GitHub.Copilot.SDK;

await using var client = new CopilotClient();
await client.StartAsync();

await using var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5",
    Streaming = true,
    OnPermissionRequest = PermissionHandler.ApproveAll,
});

session.On(evt =>
{
    if (evt is AssistantMessageDeltaEvent delta)
    {
        Console.Write(delta.Data.DeltaContent);
    }
});

await session.SendAndWaitAsync(new MessageOptions
{
    Prompt = "What is 2+2?"
});
```

### Java

```java
import com.github.copilot.sdk.CopilotClient;
import com.github.copilot.sdk.events.AssistantMessageDeltaEvent;
import com.github.copilot.sdk.json.MessageOptions;
import com.github.copilot.sdk.json.PermissionHandler;
import com.github.copilot.sdk.json.SessionConfig;

try (var client = new CopilotClient()) {
    client.start().get();

    var session = client.createSession(
        new SessionConfig()
            .setModel("claude-sonnet-4.5")
            .setStreaming(true)
            .setOnPermissionRequest(PermissionHandler.APPROVE_ALL)
    ).get();

    session.on(AssistantMessageDeltaEvent.class, event ->
        System.out.print(event.getData().deltaContent())
    );

    session.sendAndWait(new MessageOptions().setPrompt("What is 2+2?")).get();
}
```

## Custom tool examples

### TypeScript

```typescript
import { z } from "zod";
import { CopilotClient, approveAll, defineTool } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();

const session = await client.createSession({
  model: "gpt-5",
  onPermissionRequest: approveAll,
  tools: [
    defineTool("lookup_issue", {
      description: "Fetch issue details from our tracker",
      parameters: z.object({
        id: z.string().describe("Issue identifier"),
      }),
      handler: async ({ id }) => ({ id, status: "open" }),
    }),
  ],
});
```

### Python

```python
from pydantic import BaseModel, Field
from copilot import define_tool

class IssueParams(BaseModel):
    id: str = Field(description="Issue identifier")

@define_tool(description="Fetch issue details from our tracker")
async def lookup_issue(params: IssueParams) -> dict:
    return {"id": params.id, "status": "open"}
```

### Go

```go
type IssueParams struct {
    ID string `json:"id" jsonschema:"Issue identifier"`
}

lookupIssue := copilot.DefineTool(
    "lookup_issue",
    "Fetch issue details from our tracker",
    func(params IssueParams, inv copilot.ToolInvocation) (any, error) {
        return map[string]string{"id": params.ID, "status": "open"}, nil
    },
)
```

### .NET

```csharp
using Microsoft.Extensions.AI;

var lookupIssue = AIFunctionFactory.Create(
    (string id) => new { Id = id, Status = "open" },
    "lookup_issue",
    "Fetch issue details from our tracker"
);
```

### Java

```java
// Java SDK support lives in github/copilot-sdk-java.
// Follow its current documentation for tool wiring and event classes:
// https://github.com/github/copilot-sdk-java
```

## Resume example

### TypeScript

```typescript
const session = await client.createSession({
  sessionId: "user-123-review-42",
  model: "gpt-5.2-codex",
  onPermissionRequest: approveAll,
});

await session.sendAndWait({ prompt: "Review the repository" });
await session.disconnect();

const resumed = await client.resumeSession("user-123-review-42", {
  onPermissionRequest: approveAll,
});

await resumed.sendAndWait({ prompt: "Continue from where you left off" });
```

### Important resume note for BYOK

If the session uses a custom `provider`, pass that provider again when resuming. API keys and bearer tokens are not persisted to disk.

## Small but important current rules

### Overriding a built-in tool requires explicit opt-in

**TypeScript**

```typescript
import { z } from "zod";
import { defineTool } from "@github/copilot-sdk";

defineTool("edit_file", {
  description: "Custom editor",
  parameters: z.object({ path: z.string(), content: z.string() }),
  overridesBuiltInTool: true,
  handler: async () => "ok",
});
```

**Python**

```python
from pydantic import BaseModel, Field
from copilot import define_tool

class EditFileParams(BaseModel):
    path: str = Field(description="File path")
    content: str = Field(description="New file content")

@define_tool(
    name="edit_file",
    description="Custom editor",
    overrides_built_in_tool=True,
)
async def edit_file(params: EditFileParams) -> str:
    return "ok"
```

**Go**

```go
type EditFileParams struct {
    Path string `json:"path" jsonschema:"File path"`
    Content string `json:"content" jsonschema:"New file content"`
}

editFile := copilot.DefineTool("edit_file", "Custom editor",
    func(params EditFileParams, inv copilot.ToolInvocation) (any, error) {
        return "ok", nil
    })
editFile.OverridesBuiltInTool = true
```

**.NET**

```csharp
using Microsoft.Extensions.AI;
using System.Collections.Generic;

var editFile = AIFunctionFactory.Create(
    (string path, string content) => "ok",
    "edit_file",
    "Custom editor",
    new AIFunctionFactoryOptions
    {
        AdditionalProperties = new Dictionary<string, object?> { ["is_override"] = true }
    }
);
```

### Other advanced patterns worth remembering

- Image input supports file and blob attachments; vision-capable models are required.
- Mid-turn steering uses `mode: "immediate"` and queueing uses `mode: "enqueue"`.
- Telemetry uses `TelemetryConfig` and can export to OTLP or file.
