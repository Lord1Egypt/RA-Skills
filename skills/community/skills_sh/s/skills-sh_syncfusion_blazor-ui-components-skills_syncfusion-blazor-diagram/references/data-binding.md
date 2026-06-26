# Data Binding in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Local Data Binding](#local-data-binding)
- [Hierarchical Data Binding](#hierarchical-data-binding)
- [Accessing Custom Data in NodeCreating](#accessing-custom-data-in-nodecreating)
- [Remote Data Binding](#remote-data-binding)
- [Runtime Data CRUD Operations](#runtime-data-crud-operations)
- [Common Gotchas](#common-gotchas)

---

## Overview

Instead of manually defining every node and connector, the diagram can auto-generate them from a data source. Define a model class with `ID` and `ParentID` fields, pass it to `DataSourceSettings`, and let the layout engine handle placement.

**When to use data binding:**
- Loading org chart data from a database
- Rendering hierarchical trees from API data
- Building diagrams from any collection of objects with parent-child relationships

---

## Local Data Binding

Bind a flat list to automatically generate a hierarchical diagram:

```razor
@using Syncfusion.Blazor.Diagram

<SfDiagramComponent Height="600px"
                    NodeCreating="OnNodeCreating"
                    ConnectorCreating="OnConnectorCreating">
    <DataSourceSettings ID="Id" ParentID="ParentId" DataSource="@data" />
    <Layout Type="LayoutType.HierarchicalTree"
            HorizontalSpacing="40" VerticalSpacing="40" />
</SfDiagramComponent>

@code {
    public class OrgData
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Role { get; set; }
        public string ParentId { get; set; }   // empty = root
    }

    List<OrgData> data = new()
    {
        new OrgData { Id = "1", Name = "CEO",        Role = "Director",  ParentId = "" },
        new OrgData { Id = "2", Name = "CTO",        Role = "Manager",   ParentId = "1" },
        new OrgData { Id = "3", Name = "CFO",        Role = "Manager",   ParentId = "1" },
        new OrgData { Id = "4", Name = "Dev Lead",   Role = "Lead",      ParentId = "2" },
        new OrgData { Id = "5", Name = "Designer",   Role = "Creative",  ParentId = "3" },
    };

    private void OnNodeCreating(IDiagramObject obj)
    {
        var node = obj as Node;
        node.Width = 120; node.Height = 50;
        node.Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" };
    }

    private void OnConnectorCreating(IDiagramObject obj)
    {
        (obj as Connector).Type = ConnectorSegmentType.Orthogonal;
    }
}
```

**Key `DataSourceSettings` properties:**

| Property | Description |
|----------|-------------|
| `ID` | Name of the unique identifier field in your data class |
| `ParentID` | Name of the parent reference field |
| `DataSource` | The collection of data objects |
| `Root` | Optional: specify the ID of the root node (when multiple root candidates exist) |

---

## Hierarchical Data Binding

For multi-root or complex hierarchies:

```razor
<DataSourceSettings ID="Id" ParentID="ParentId" DataSource="@data" Root="root1" />
```

Set `Root` to the ID of the node you want as the top-level root when the layout has multiple nodes with empty `ParentId`.

---

## Accessing Custom Data in NodeCreating

The `NodeCreating` callback receives the raw data object — cast it to access your model's fields:

```csharp
private void OnNodeCreating(IDiagramObject obj)
{
    var node = obj as Node;
    node.Width = 120;
    node.Height = 50;

    // Access your data model
    if (node.Data is OrgData data)
    {
        // Apply styling based on data
        node.Style = new ShapeStyle
        {
            Fill = data.Role == "Director" ? "#E74C3C" :
                   data.Role == "Manager"  ? "#3498DB" : "#2ECC71",
            StrokeColor = "white"
        };

        // The annotation content is usually auto-set from data,
        // but you can customize it:
        if (node.Annotations.Count > 0)
            node.Annotations[0].Content = $"{data.Name}\n({data.Role})";
    }
}
```

---

## Remote Data Binding

Fetch data from an API and bind after loading:

```razor
<SfDiagramComponent @ref="_diagram" Height="600px"
                    NodeCreating="OnNodeCreating"
                    ConnectorCreating="OnConnectorCreating">
    <DataSourceSettings ID="Id" ParentID="ParentId" DataSource="@data" />
    <Layout Type="LayoutType.OrganizationalChart"
            HorizontalSpacing="40" VerticalSpacing="40" />
</SfDiagramComponent>

@code {
    List<OrgData> data = new();

    protected override async Task OnInitializedAsync()
    {
        // Fetch from API
        data = await Http.GetFromJsonAsync<List<OrgData>>("api/org-chart");
    }

    private void OnNodeCreating(IDiagramObject obj)
    {
        var node = obj as Node;
        node.Width = 120; node.Height = 50;
        node.Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" };
    }

    private void OnConnectorCreating(IDiagramObject obj)
    {
        (obj as Connector).Type = ConnectorSegmentType.Orthogonal;
    }
}
```

---

## Runtime Data CRUD Operations

When using a remote data source (`SfDataManager`), use these async methods to perform CRUD operations on the bound data source. The diagram automatically refreshes its layout after each operation.

### Setup — Remote Data with WebAPI

```razor
<SfDiagramComponent ID="diagram" @ref="@_diagram" Width="100%" Height="690px"
                    ConnectorCreating="@ConnectorCreating"
                    NodeCreating="@NodeCreating">
    <DataSourceSettings ID="EmployeeID" ParentID="ReportsTo">
        <SfDataManager Url="api/Data" Adaptor="Syncfusion.Blazor.Adaptors.WebApiAdaptor" />
    </DataSourceSettings>
    <Layout Type="LayoutType.HierarchicalTree" VerticalSpacing="75" HorizontalSpacing="75" />
</SfDiagramComponent>
```

### Read Data

Fetch records from the data source based on an optional query:

```csharp
// Read all data
List<object> records = (List<object>)await _diagram.ReadDataAsync();

// Read with a query filter
Query query = new Query().Where("ReportsTo", "equal", "1");
List<object> filtered = (List<object>)await _diagram.ReadDataAsync(query);
```

### Insert Data

Add a new record to the data source. The diagram layout updates automatically:

```csharp
var newEmployee = new EmployeeDetails
{
    EmployeeID = 10,
    Name = "Alice",
    Designation = "Developer",
    ReportsTo = "3",
    Colour = "Blue"
};
await _diagram.InsertDataAsync(newEmployee);

// Insert with explicit table name and position
await _diagram.InsertDataAsync(newEmployee, tableName: "Employees", position: 0);
```

### Update Data

Modify an existing record identified by a key field:

```csharp
var updatedEmployee = new EmployeeDetails
{
    EmployeeID = 6,
    Name = "Michael",
    Designation = "Product Manager",
    ReportsTo = "1",
    Colour = "Green"
};
await _diagram.UpdateDataAsync("EmployeeID", updatedEmployee);

// Update with table name and original data (for delta updates)
await _diagram.UpdateDataAsync("EmployeeID", updatedEmployee, tableName: "Employees", original: originalEmployee);
```

### Delete Data

Remove a record by key field and value:

```csharp
// Delete the record where EmployeeID = 6
await _diagram.DeleteDataAsync("EmployeeID", 6);

// Delete with explicit table name
await _diagram.DeleteDataAsync("EmployeeID", 6, tableName: "Employees");
```

### Refresh Data Source

`RefreshDataSourceAsync()` dynamically updates the diagram layout to reflect changes made to the underlying `DataSource` object. It rebuilds the entire diagram from the new data — use it when you replace or mutate the data collection bound to `DataSourceSettings.DataSource`.

**Example — MindMap with runtime data refresh:**

```razor
@using Syncfusion.Blazor.Diagram
@using Syncfusion.Blazor.Buttons

<SfDiagramComponent @ref="_diagram" Height="600px"
                    NodeCreating="@OnNodeCreating"
                    ConnectorCreating="@OnConnectorCreating">
    <DataSourceSettings ID="Id" ParentID="ParentId" DataSource="@_dataSource" />
    <Layout Type="LayoutType.MindMap">
        <LayoutMargin Top="20" Left="20" />
    </Layout>
</SfDiagramComponent>

<SfButton Content="Refresh Data Source" OnClick="@RefreshData" />

@code {
    private SfDiagramComponent _diagram;

    private void OnNodeCreating(IDiagramObject obj)
    {
        Node node = obj as Node;
        node.Height = 25;
        node.Width = 25;
        node.Style = new ShapeStyle { Fill = "#6495ED", StrokeWidth = 1, StrokeColor = "white" };
        node.Shape = new BasicShape { Type = NodeShapes.Basic };
    }

    private void OnConnectorCreating(IDiagramObject obj)
    {
        Connector connector = obj as Connector;
        connector.Type = ConnectorSegmentType.Bezier;
        connector.Style = new ShapeStyle { StrokeColor = "#6495ED", StrokeWidth = 2 };
        connector.TargetDecorator = new DecoratorSettings { Shape = DecoratorShape.None };
    }

    public class MindMapDetails
    {
        public string Id      { get; set; }
        public string Label   { get; set; }
        public string ParentId { get; set; }
        public string Branch  { get; set; }
    }

    // Initial data source — full tree
    public object _dataSource = new List<object>()
    {
        new MindMapDetails { Id = "1",  Label = "Creativity",     ParentId = "",  Branch = "Root" },
        new MindMapDetails { Id = "2",  Label = "Brainstorming",  ParentId = "1", Branch = "Right" },
        new MindMapDetails { Id = "3",  Label = "Complementing",  ParentId = "1", Branch = "Left" },
        new MindMapDetails { Id = "4",  Label = "Sessions",       ParentId = "2", Branch = "subRight" },
        new MindMapDetails { Id = "5",  Label = "Complementing",  ParentId = "2", Branch = "subRight" },
        new MindMapDetails { Id = "6",  Label = "Local",          ParentId = "3", Branch = "subRight" },
        new MindMapDetails { Id = "7",  Label = "Remote",         ParentId = "3", Branch = "subRight" },
        new MindMapDetails { Id = "8",  Label = "Individual",     ParentId = "3", Branch = "subRight" },
        new MindMapDetails { Id = "9",  Label = "Teams",          ParentId = "3", Branch = "subRight" },
        new MindMapDetails { Id = "10", Label = "Ideas",          ParentId = "5", Branch = "subRight" },
        new MindMapDetails { Id = "11", Label = "Engagement",     ParentId = "5", Branch = "subRight" },
    };

    // Replace the data source with a trimmed set, then call RefreshDataSourceAsync
    private async Task RefreshData()
    {
        _dataSource = new List<object>()
        {
            new MindMapDetails { Id = "1", Label = "Creativity",    ParentId = "",  Branch = "Root" },
            new MindMapDetails { Id = "2", Label = "Brainstorming", ParentId = "1", Branch = "Right" },
            new MindMapDetails { Id = "3", Label = "Complementing", ParentId = "1", Branch = "Left" },
            new MindMapDetails { Id = "4", Label = "Sessions",      ParentId = "2", Branch = "subRight" },
            new MindMapDetails { Id = "5", Label = "Complementing", ParentId = "2", Branch = "subRight" },
        };

        // Rebuild the diagram layout from the new data
        await _diagram.RefreshDataSourceAsync();
    }
}
```

> **Note:** `RefreshDataSourceAsync()` rebuilds the entire diagram from the current `DataSource` value. Always assign the new data to the field **before** calling this method so the diagram reads the updated collection.  
> Use `DoLayoutAsync()` instead when working with manual node/connector collections (without `DataSourceSettings`).

### Method Signatures Reference

| Method | Signature | Description |
|--------|-----------|-------------|
| `ReadDataAsync` | `Task<IEnumerable<object>> ReadDataAsync(Query? query = null)` | Read records from data source |
| `InsertDataAsync` | `Task InsertDataAsync(object data, string? tableName = null, Query? query = null, int position = 0)` | Add a new record |
| `UpdateDataAsync` | `Task UpdateDataAsync(string keyField, object data, string? tableName = null, Query? query = null, object? original = null, IDictionary<string, object>? updateProperties = null)` | Modify an existing record |
| `DeleteDataAsync` | `Task DeleteDataAsync(string keyField, object value, string? tableName = null, Query? query = null)` | Remove a record |
| `RefreshDataSourceAsync` | `Task RefreshDataSourceAsync()` | Reload all data and rebuild layout |

---

## Common Gotchas

- **Root node must have an empty `ParentId`** (empty string `""`, not `null`) — otherwise it won't be recognized as root
- **`ID` and `ParentID` in `DataSourceSettings` are field name strings** — they must exactly match your model's property names (case-sensitive)
- **`NodeCreating` is required** — without it, the auto-generated nodes have no size and won't be visible
- **`DataSource` + `Layout` go together** — data binding without a layout type results in all nodes stacked at (0, 0)
- **`node.Data`** in `NodeCreating` holds your original data object — cast it to your model type to access custom fields
- **Do NOT set `Nodes`/`Connectors` collections when using data binding** — the diagram generates them automatically from the data source
