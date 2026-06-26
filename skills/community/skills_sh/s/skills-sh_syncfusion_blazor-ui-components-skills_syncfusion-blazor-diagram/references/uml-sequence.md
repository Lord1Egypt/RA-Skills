# UML Sequence Diagram in Blazor Diagram

A UML sequence diagram shows how objects communicate in a time-ordered sequence. Use `UmlSequenceDiagramModel` instead of manually creating nodes/connectors.

---

## Basic Setup

```razor
@using Syncfusion.Blazor.Diagram

<SfDiagramComponent @ref="_diagram" Height="600px" Model="@_model" />

@code {
    private SfDiagramComponent _diagram;
    private UmlSequenceDiagramModel _model;

    protected override void OnInitialized()
    {
        _model = new UmlSequenceDiagramModel
        {
            SpaceBetweenParticipants = 200,
            Participants = new List<UmlSequenceParticipant>
            {
                new UmlSequenceParticipant { ID = "User", Content = "User", IsActor = true },
                new UmlSequenceParticipant { ID = "System", Content = "System", IsActor = false }
            },
            Messages = new List<UmlSequenceMessage>
            {
                new UmlSequenceMessage
                {
                    ID = "MSG1", Content = "Login Request",
                    FromParticipantID = "User", ToParticipantID = "System",
                    MessageType = UmlSequenceMessageType.Synchronous
                },
                new UmlSequenceMessage
                {
                    ID = "MSG2", Content = "Login Response",
                    FromParticipantID = "System", ToParticipantID = "User",
                    MessageType = UmlSequenceMessageType.Reply
                }
            }
        };
    }
}
```

---

## Participants (Lifelines)

| Property | Type | Description |
|----------|------|-------------|
| `ID` | string | Unique identifier |
| `Content` | string | Display name |
| `IsActor` | bool | `true` = stick figure (actor); `false` = box (object/system) |
| `ShowDestructionMarker` | bool | Show X at the end of the lifeline |
| `ActivationBoxes` | `IEnumerable<UmlSequenceActivationBox>` | Active execution periods |

---

## Message Types

| `UmlSequenceMessageType` | Description |
|--------------------------|-------------|
| `Synchronous` | Solid arrow — sender waits for response |
| `Asynchronous` | Open arrow — sender continues immediately |
| `Reply` | Dashed arrow — response to a previous message |
| `Create` | Creates a new participant instance |
| `Delete` | Terminates a participant |
| `Self` | Arrow from participant to itself |

**UmlSequenceMessage properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | string | Unique identifier |
| `Content` | string | Label shown on the arrow |
| `FromParticipantID` | string | Sender participant ID |
| `ToParticipantID` | string | Receiver participant ID |
| `MessageType` | `UmlSequenceMessageType` | Arrow style and semantics |

---

## Activation Boxes

Show when a participant is actively processing (thin rectangle on lifeline):

```csharp
new UmlSequenceParticipant
{
    ID = "System",
    Content = "System",
    ActivationBoxes = new List<UmlSequenceActivationBox>
    {
        new UmlSequenceActivationBox
        {
            ID = "Act1",
            StartMessageID = "MSG1",  // activation starts when MSG1 is received
            EndMessageID = "MSG2"     // activation ends when MSG2 is sent
        }
    }
}
```

---

## Fragments (Alt / Loop / Opt)

Fragments group messages under conditional or looping constructs:

```csharp
Fragments = new List<UmlSequenceFragment>
{
    new UmlSequenceFragment
    {
        ID = "Frag1",
        FragmentType = UmlSequenceFragmentType.Alternative,
        Conditions = new List<UmlSequenceFragmentCondition>
        {
            new UmlSequenceFragmentCondition
            {
                Content = "if payment succeeds",
                MessageIds = new List<string> { "MSG3", "MSG4" }
            },
            new UmlSequenceFragmentCondition
            {
                Content = "if payment fails",
                MessageIds = new List<string> { "MSG5" }
            }
        }
    }
}
```

### Fragment types:

| `UmlSequenceFragmentType` | Description |
|---------------------------|-------------|
| `Optional` | `opt` — executes only if condition is met |
| `Alternative` | `alt` — if/else branches |
| `Loop` | `loop` — repeating block |

### Nested fragments:

Use `Conditions[n].Fragments` to nest fragments inside a condition:

```csharp
new UmlSequenceFragmentCondition
{
    Content = "while retries < 3",
    Fragments = new List<UmlSequenceFragment> { innerFragment }
}
```

---

## Participant Spacing

```csharp
_model = new UmlSequenceDiagramModel
{
    SpaceBetweenParticipants = 300,  // default is 100
    // ...
};
```

---

## Updating the Diagram After Model Changes (UpdateFromModelAsync)

After programmatically modifying the `UmlSequenceDiagramModel` (adding participants, messages, or fragments) at runtime, call `UpdateFromModelAsync()` to synchronize the diagram UI with the updated model:

```csharp
private async Task AddNewMessage()
{
    // Modify the model — add a new message
    _model.Messages.Add(new UmlSequenceMessage
    {
        ID = "MSG4",
        Content = "New interaction",
        FromParticipantID = "Client",
        ToParticipantID = "Server",
        MessageType = UmlSequenceMessageType.Synchronous
    });

    // Tell the diagram to refresh its visual representation
    await _diagram.UpdateFromModelAsync();
}

private async Task AddNewParticipant()
{
    _model.Participants.Add(new UmlSequenceParticipant
    {
        ID = "Database",
        Content = "Database",
        IsActor = false
    });

    await _diagram.UpdateFromModelAsync();
}
```

> **Note:** `UpdateFromModelAsync()` is required any time the `UmlSequenceDiagramModel` is changed at runtime — the diagram does NOT automatically re-render when you mutate the model object. Always `await` it.

---

## Common Gotchas

- **Set `Model` property** on `SfDiagramComponent` — do not use `Nodes`/`Connectors` for sequence diagrams
- **IDs must be unique** across participants and messages — duplicate IDs cause rendering issues
- **Message order matters** — messages are displayed top-to-bottom in the order they appear in `Messages`
- **`StartMessageID`/`EndMessageID`** on activation boxes must reference valid message IDs — mismatches silently fail
- **Fragments reference messages by ID** — a message can only belong to one fragment condition; cross-condition references are not supported
- **`SpaceBetweenParticipants`** should be increased when participant names or message labels are long
- **Serialization** — sequence diagram models created via `UmlSequenceDiagramModel` can be saved/loaded with `SaveDiagramAsMermaid` / `LoadDiagramFromMermaidAsync`
