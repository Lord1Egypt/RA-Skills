# Collaborative Editing in Blazor Diagram

Collaborative editing enables multiple users to edit the same diagram simultaneously in real time.

---

## Architecture

- **SignalR** handles real-time communication between the browser and server
- **Redis** (optional) acts as a shared temporary store for multi-server deployments
- Changes that trigger `HistoryChanged` are propagated to all connected clients
- **`GetDiagramUpdates(HistoryChangedEventArgs)`** — serializes the diagram change from `HistoryChangedEventArgs` into a `List<string>` for transmission
- **`SetDiagramUpdatesAsync(List<string>)`** — applies received serialized changes from other clients to the local diagram

---

## Setup Overview

Collaborative editing requires two parts:

1. **ASP.NET Core SignalR Hub** — receives and broadcasts diagram changes
2. **Blazor App** — connects to the hub and syncs the diagram component

---

## Step 1: Create the SignalR Hub (Server Project)

```csharp
// DiagramHub.cs
using Microsoft.AspNetCore.SignalR;

public class DiagramHub : Hub
{
    private readonly IDiagramStateService _stateService;

    public DiagramHub(IDiagramStateService stateService)
    {
        _stateService = stateService;
    }

    public async Task BroadcastDiagramAction(string action, string data)
    {
        // Broadcast to all OTHER connected clients (not the sender)
        await Clients.Others.SendAsync("ReceiveDiagramAction", action, data);
        // Store state (e.g., in Redis or in-memory)
        await _stateService.SaveAsync(action, data);
    }

    public async Task<string> GetCurrentState()
    {
        return await _stateService.GetAsync();
    }
}
```

**Register in `Program.cs`:**
```csharp
builder.Services.AddSignalR();
// ...
app.MapHub<DiagramHub>("/diagramhub");
```

---

## Step 2: Connect the Blazor App to the Hub

```razor
@using Microsoft.AspNetCore.SignalR.Client
@using Syncfusion.Blazor.Diagram
@implements IAsyncDisposable

<SfDiagramComponent @ref="_diagram"
                    @bind-Nodes="_nodes"
                    @bind-Connectors="_connectors"
                    HistoryChanged="OnHistoryChanged" />

@code {
    private SfDiagramComponent _diagram;
    private DiagramObjectCollection<Node> _nodes = new();
    private DiagramObjectCollection<Connector> _connectors = new();
    private HubConnection _hubConnection;

    protected override async Task OnInitializedAsync()
    {
        _hubConnection = new HubConnectionBuilder()
            .WithUrl(Navigation.ToAbsoluteUri("/diagramhub"))
            .Build();

        // Receive changes from other clients
        _hubConnection.On<string, string>("ReceiveDiagramAction", async (action, data) =>
        {
            await _diagram.LoadDiagramAsync(data);
            await InvokeAsync(StateHasChanged);
        });

        await _hubConnection.StartAsync();

        // Load current diagram state on join
        var state = await _hubConnection.InvokeAsync<string>("GetCurrentState");
        if (!string.IsNullOrEmpty(state))
            await _diagram.LoadDiagramAsync(state);
    }

    private async void OnHistoryChanged(HistoryChangedEventArgs args)
    {
        // Broadcast current state after each change
        string currentState = _diagram.SaveDiagram();
        await _hubConnection.SendAsync("BroadcastDiagramAction", args.Action.ToString(), currentState);
    }

    public async ValueTask DisposeAsync()
    {
        await _hubConnection.DisposeAsync();
    }
}
```

---

## Optimized Sync with GetDiagramUpdates / SetDiagramUpdatesAsync

Instead of sending the full `SaveDiagram()` JSON on every change, use the optimized delta-based API:

- **`GetDiagramUpdates(HistoryChangedEventArgs)`** — serializes only the change described by the history event into a compact `List<string>`
- **`SetDiagramUpdatesAsync(List<string>)`** — applies a received delta update to the local diagram without a full reload

This approach is more efficient for real-time collaboration because it transmits only what changed, not the entire diagram state.

```razor
<SfDiagramComponent @ref="_diagram"
                    @bind-Nodes="_nodes"
                    @bind-Connectors="_connectors"
                    HistoryChanged="OnHistoryChanged" />

@code {
    private SfDiagramComponent _diagram;
    private HubConnection _hubConnection;

    protected override async Task OnInitializedAsync()
    {
        _hubConnection = new HubConnectionBuilder()
            .WithUrl(Navigation.ToAbsoluteUri("/diagramhub"))
            .Build();

        // Receive delta updates from other clients and apply them
        _hubConnection.On<List<string>>("ReceiveDiagramUpdates", async (updates) =>
        {
            await _diagram.SetDiagramUpdatesAsync(updates);
            await InvokeAsync(StateHasChanged);
        });

        await _hubConnection.StartAsync();
    }

    private async void OnHistoryChanged(HistoryChangedEventArgs args)
    {
        // Serialize only the delta change (not the whole diagram)
        List<string> updates = _diagram.GetDiagramUpdates(args);

        // Broadcast the compact delta to other clients
        await _hubConnection.SendAsync("BroadcastDiagramUpdates", updates);
    }
}
```

**Hub method for delta broadcast:**
```csharp
public async Task BroadcastDiagramUpdates(List<string> updates)
{
    // Forward delta to all other connected clients
    await Clients.Others.SendAsync("ReceiveDiagramUpdates", updates);
}
```

> **Tip:** Use the delta-based `GetDiagramUpdates`/`SetDiagramUpdatesAsync` pattern for production collaboration. The full `SaveDiagram`/`LoadDiagramAsync` approach is simpler but sends much larger payloads, causing higher latency for complex diagrams.

---

## Multi-Server (Scale-Out) Setup

For deployments with multiple server instances, configure a SignalR backplane so all nodes share messages:

```csharp
// In Program.cs — add Redis backplane
builder.Services.AddSignalR()
    .AddStackExchangeRedis("localhost:6379");
```

Store shared diagram state in Redis instead of in-memory:
```csharp
// Use IConnectionMultiplexer to store/retrieve diagram JSON in Redis
```

---

## Limitations

The following settings are **NOT** synchronized across clients — they are local only:

| Unsynchronized Setting |
|------------------------|
| `PageSettings` |
| `ContextMenu` |
| `DiagramHistoryManager` |
| `SnapSettings` |
| `Rulers` |
| `UmlSequenceDiagram` model |
| `Layout` |
| `ScrollSettings` (zoom/pan) |

Zoom and pan are per-user and not broadcast.

---

## Common Gotchas

- **Only `HistoryChanged`-tracked actions are propagated** — programmatic changes that bypass undo/redo history are not broadcast
- **Two-way binding required** — use `@bind-Nodes` and `@bind-Connectors` so `LoadDiagramAsync` correctly updates the UI
- **Race conditions** — if two users edit simultaneously, the last broadcast wins; implement optimistic locking or versioning in the hub for conflict resolution
- **Single server works without Redis** — add Redis only for load-balanced multi-instance deployments
- **Complete working sample** available at: https://github.com/syncfusion/blazor-showcase-diagram-collaborative-editing
