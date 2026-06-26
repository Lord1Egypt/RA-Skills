# Serialization in Blazor Diagram

Serialization is saving and loading the persistent state of a diagram (nodes, connectors, layout, styles) as a JSON string.

---

## Requirements: Two-Way Binding

**Always** use two-way binding (`@bind-`) for `Nodes` and `Connectors` when serialization is needed. Without `@bind-`, loaded data will not reflect in the UI:

```razor
<SfDiagramComponent @ref="_diagram"
                    @bind-Nodes="_nodes"
                    @bind-Connectors="_connectors" />
```

---

## Save Diagram to JSON String

```csharp
private SfDiagramComponent _diagram;

private string SaveDiagram()
{
    string json = _diagram.SaveDiagram();
    return json; // store in DB, localStorage, file, etc.
}
```

---

## Load Diagram from JSON String

```csharp
private async Task LoadDiagram(string json)
{
    await _diagram.LoadDiagramAsync(json);
}
```

---

## Save and Load via File Download/Upload

To let users download the diagram as a `.json` file and upload it back:

**C# side:**
```csharp
@inject IJSRuntime jsRuntime

private async Task SaveToFile()
{
    string data = _diagram.SaveDiagram();
    // Invoke JS to trigger browser download
    await jsRuntime.InvokeAsync<object>("saveDiagram", data, "my-diagram");
}

private async Task LoadFromFile()
{
    _diagram.BeginUpdate();
    // Invoke JS to open file picker; file content flows back via a JS interop callback
    await jsRuntime.InvokeAsync<object>("click");
    await _diagram.EndUpdateAsync();
}
```

**JavaScript side (in wwwroot or _Host):**
```javascript
function saveDiagram(data, fileName) {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(data);
    const a = document.createElement('a');
    a.href = dataStr;
    a.download = fileName + '.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
}

function click() {
    document.getElementById('UploadFiles').click();
}
```

---

## Load Classic SfDiagram JSON into SfDiagramComponent

When migrating from the legacy `SfDiagram` component, load its serialized JSON with `isClassicData = true`:

```csharp
// Old SfDiagram serialized string:
string classicJson = legacyDiagram.SaveDiagram();

// Load into new SfDiagramComponent:
await _diagram.LoadDiagramAsync(classicJson, isClassicData: true);
```

---

## Mermaid Syntax (Flowchart, MindMap, Sequence)

The diagram can serialize/deserialize to Mermaid syntax for flowcharts, mind maps, and sequence diagrams.

### Save as Mermaid

```csharp
string mermaidStr = _diagram.SaveDiagramAsMermaid();
```

### Load from Mermaid

```csharp
await _diagram.LoadDiagramFromMermaidAsync(mermaidStr);
```

> **Note:** Mermaid serialization only works with `HierarchicalTree` (flowchart), `MindMap`, and sequence diagram layouts. Regular diagrams with free-form nodes will not serialize correctly to Mermaid.

---

## Common Gotchas

- **Missing `@bind-`** on `Nodes`/`Connectors` causes `LoadDiagramAsync` to load data but the UI won't update
- **`BeginUpdate()` / `EndUpdateAsync()`** wrap file-based loads to prevent intermediate re-renders
- **Custom data on nodes** — if `node.Data` is a custom object, it must be JSON-serializable; complex types with circular references will cause exceptions
- **Mermaid is layout-specific** — only flowchart, mind map, and sequence diagram layouts support Mermaid serialization
- **`LoadDiagramAsync` replaces all current content** — save current state before loading if needed
- **Classic `SfDiagram` migration** — always pass `isClassicData: true` when loading legacy diagram JSON; omitting it causes a parsing error
