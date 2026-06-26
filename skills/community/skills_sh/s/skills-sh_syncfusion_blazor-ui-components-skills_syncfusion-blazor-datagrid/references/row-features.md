# Row Features — Syncfusion Blazor DataGrid

## Table of Contents
- [Row Height](#row-height)
- [Row Styles](#row-styles)
- [Row Hover](#row-hover)
- [Frozen Rows (Row Pinning)](#frozen-rows-row-pinning)
- [Row Template](#row-template)
  - [Row Template — Formatting & Embedded Controls](#row-template--formatting--embedded-controls)
  - [Row Template Limitations](#row-template-limitations)
- [Detail Template](#detail-template)
  - [Hierarchical DataGrid (Nested Grid in Detail Template)](#hierarchical-datagrid-nested-grid-in-detail-template)
  - [Template Column in Detail DataGrid](#template-column-in-detail-datagrid)
- [Row Drag and Drop](#row-drag-and-drop)
- [Row Spanning](#row-spanning)
  - [AutoSpanMode Enum](#autospanmode-enum)
  - [Disable Spanning for a Specific Column](#disable-spanning-for-a-specific-column)
  - [Programmatic Cell Merging — `MergeCellsAsync`](#programmatic-cell-merging--mergecellesasync)
- [Row Events](#row-events)

## Row Height

Set a uniform height (default 42px) for all rows including header and footer:

```razor
<SfGrid DataSource="@Orders" RowHeight="60" Height="400">...</SfGrid>
```

**Set row height conditionally via `RowDataBound`:**

```razor
<GridEvents TValue="Order" RowDataBound="OnRowDataBound"></GridEvents>
<style> .tall-row { height: 80px; } </style>
@code {
    void OnRowDataBound(RowDataBoundEventArgs<Order> args)
    {
        if (args.Data.Freight > 100)
            args.Row.AddClass(new string[] { "tall-row" });
    }
}
```

## Row Styles

**Via `RowDataBound` (conditional CSS classes):**

```razor
<GridEvents TValue="Order" RowDataBound="OnRowDataBound"></GridEvents>
<style>
    .below-30 { background-color: rgb(211, 225, 248); }
    .below-80 { background-color: rgb(163, 236, 217); }
    .above-80 { background-color: rgb(220, 248, 177); }
</style>
@code {
    void OnRowDataBound(RowDataBoundEventArgs<Order> args)
    {
        if (args.Data.Freight < 30) args.Row.AddClass(new[] { "below-30" });
        else if (args.Data.Freight < 80) args.Row.AddClass(new[] { "below-80" });
        else args.Row.AddClass(new[] { "above-80" });
    }
}
```

**Alternate rows / selected row via CSS:**

```css
.e-grid .e-altrow { background-color: #aaf1eb; }              /* alternate rows */
#CustomGrid .e-selectionbackground { background-color: #f9920b; } /* selected row */
```

```razor
<SfGrid ID="CustomGrid" DataSource="@Orders">...</SfGrid>
```

## Row Hover

Enabled by default. Disable: `<SfGrid EnableHover="false">`.

## Frozen Rows (Row Pinning)

```razor
<SfGrid DataSource="@Orders" FrozenRows="2" Height="315px" AllowSelection="false" EnableHover="false">
    <GridColumns>...</GridColumns>
</SfGrid>
```

```css
.e-grid .e-frozenrow-border { background-color: rgb(5, 114, 47); }
```

> `FrozenColumns` and `FrozenRows` can be used together.

## Row Template

Replace the entire row layout with a custom template. Number of `<td>` elements must match column count.

```razor
<SfGrid DataSource="@Employees" Height="315px">
    <GridTemplates>
        <RowTemplate Context="emp">
            @{ var employee = emp as Employee; }
            <td><img src="@($"images/{employee.EmployeeID}.png")" alt="@employee.FirstName" /></td>
            <td>
                <div><strong>@employee.FirstName @employee.LastName</strong></div>
                <div>@employee.Title</div>
            </td>
        </RowTemplate>
    </GridTemplates>
    <GridColumns>
        <GridColumn HeaderText="Employee Image" Width="250"></GridColumn>
        <GridColumn HeaderText="Employee Details" Width="300"></GridColumn>
    </GridColumns>
</SfGrid>
```

### Row Template — Formatting & Embedded Controls

`Columns.Format` does **not** apply inside `RowTemplate`. Use `.ToString()` directly:

```razor
<td>@employee.HireDate.ToString("MMM dd, yyyy")</td>
<td>@employee.Salary.ToString("C2")</td>
```

Syncfusion components can be embedded inside `RowTemplate`:

```razor
<RowTemplate Context="row">
    @{ var order = row as OrderData; }
    <td><SfChip><ChipItems><ChipItem Text="@order.OrderID.ToString()"></ChipItem></ChipItems></SfChip></td>
    <td><SfNumericTextBox Value="@order.Quantity"></SfNumericTextBox></td>
    <td><SfDatePicker Value="@order.OrderDate"></SfDatePicker></td>
    <td><SfDropDownList DataSource="@StatusList" Value="@order.OrderStatus"></SfDropDownList></td>
</RowTemplate>
```

### Row Template Limitations

The following Grid features are **incompatible** with `RowTemplate`:

- Filtering, Sorting, Searching
- Paging
- Editing
- Grouping
- Aggregates
- Export (Excel / PDF)
- Context Menu
- Selection
- Frozen rows & columns
- Virtual & Infinite scrolling
- Column Chooser / Column Menu
- Detail Row
- Foreign key column
- Resizing / Reordering
- Clipboard
- Adaptive view
- RTL
- State Persistence

## Detail Template

Expand rows to show additional information inside `<DetailTemplate>`:

```razor
<SfGrid DataSource="@Employees" Height="315px">
    <GridTemplates>
        <DetailTemplate>
            @{ var employee = context as Employee; }
            <p><b>Bio:</b> @employee.Notes</p>
            <p><b>City:</b> @employee.City</p>
        </DetailTemplate>
    </GridTemplates>
    <GridColumns>...</GridColumns>
</SfGrid>
```

**Expand specific row on load** — call `ExpandCollapseDetailRowAsync` in `DataBound`:

```razor
<GridEvents DataBound="DataBoundHandler" TValue="EmployeeData"></GridEvents>
@code {
    async Task DataBoundHandler() =>
        await grid.ExpandCollapseDetailRowAsync("EmployeeID", 1);
}
```

**Expand all rows via button** — call `ExpandAllDetailRowAsync`:

```razor
<SfButton Content="Expand All" OnClick="@(async () => await Grid.ExpandAllDetailRowAsync())"></SfButton>
```

### Hierarchical DataGrid (Nested Grid in Detail Template)

Nest an `SfGrid` inside `DetailTemplate` to create parent-child layouts. DataGrid has no built-in hierarchical mode.

```razor
<DetailTemplate>
    @{ var emp = context as EmployeeData; }
    <SfGrid DataSource="@(Orders.Where(o => o.EmployeeID == emp.EmployeeID).ToList())">
        <GridColumns>
            <GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
            <GridColumn Field="ShipCity" HeaderText="Ship City" Width="150"></GridColumn>
        </GridColumns>
    </SfGrid>
</DetailTemplate>
```

### Template Column in Detail DataGrid

Use the `Template` property on a column inside the detail grid:

```razor
<GridColumn HeaderText="Photo" Width="100">
    <Template>
        @{ var order = context as OrderData; }
        <img src="images/@(order.OrderID).png" height="55px" />
    </Template>
</GridColumn>
```

## Row Drag and Drop

> Row selection must be enabled. Use `SelectionType.Multiple` to drag multiple rows.

**Within same grid:**

```razor
<SfGrid ID="Grid" AllowRowDragAndDrop="true" AllowSelection="true">
    <GridSelectionSettings Type="SelectionType.Multiple"></GridSelectionSettings>
</SfGrid>
```

**Cross-grid:**

```razor
<SfGrid ID="SourceGrid" AllowRowDragAndDrop="true" AllowSelection="true">
    <GridRowDropSettings TargetID="DestGrid"></GridRowDropSettings>
    <GridSelectionSettings Type="SelectionType.Multiple"></GridSelectionSettings>
</SfGrid>
<SfGrid ID="DestGrid" AllowRowDragAndDrop="true" AllowSelection="true">
    <GridRowDropSettings TargetID="SourceGrid"></GridRowDropSettings>
    <GridSelectionSettings Type="SelectionType.Multiple"></GridSelectionSettings>
</SfGrid>
```

**`AllowEmptyAreaDrop`** (default: `true`) — rows dropped in empty space append to end. Set `false` to restrict drops to existing rows only:

```razor
<GridRowDropSettings AllowEmptyAreaDrop="false" TargetID="DestGrid"></GridRowDropSettings>
```

**Drop to custom component** (e.g., `SfTreeGrid`) — set `TargetID` and handle `RowDropped`:

```razor
<SfGrid @ref="grid" ID="Grid" AllowRowDragAndDrop="true" AllowSelection="true">
    <GridRowDropSettings TargetID="DestGrid"></GridRowDropSettings>
    <GridEvents TValue="OrderData" RowDropped="RowDroppedHandler"></GridEvents>
</SfGrid>
<SfTreeGrid ID="DestGrid" AllowRowDragAndDrop="true" IdMapping="TaskID" ChildMapping="Subtasks">
</SfTreeGrid>
@code {
    async Task RowDroppedHandler(RowDroppedEventArgs<OrderData> args)
    {
        foreach (var row in args.Data)
            TreeGridData.Add(new WrapData { TaskID = row.OrderID, TaskName = row.ShipCity });
        GridData.RemoveAll(r => args.Data.Contains(r));
        await grid.Refresh();
    }
}
```

## Row Spanning

The `AutoSpan` property controls automatic cell merging. Set it on `SfGrid` using the `AutoSpanMode` enum.

### AutoSpanMode Enum

| Value | Description |
|---|---|
| `AutoSpanMode.None` | Disables all spanning (default) |
| `AutoSpanMode.Row` | Horizontal merging across columns within the same row |
| `AutoSpanMode.Column` | Vertical merging of identical values in the same column |
| `AutoSpanMode.HorizontalAndVertical` | Both row and column spanning (row merging applied first) |

**Enable row spanning (horizontal merge):**

```razor
<SfGrid DataSource="@TeleCastDataList" GridLines="GridLine.Both"
        AutoSpan="AutoSpanMode.Row" AllowSelection="false" EnableHover="false">
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Disable Spanning for a Specific Column

Use `GridColumn.AutoSpan="AutoSpanMode.None"` to opt out a column from grid-level spanning:

```razor
<SfGrid AutoSpan="AutoSpanMode.Row">
    <GridColumns>
        <GridColumn Field="Channel" AutoSpan="AutoSpanMode.None"></GridColumn>
        <GridColumn Field="Program"></GridColumn>
    </GridColumns>
</SfGrid>
```

**Combination Matrix (Grid-level vs Column-level):**

| Grid AutoSpan | Column AutoSpan | Effective Behavior |
|---|---|---|
| `None` | `None` | No spanning |
| `Row` | `None` | No spanning — column explicitly disables |
| `Row` | `Row` | Row spanning only |
| `Row` | `HorizontalAndVertical` | Row spanning only — grid limits to Row |
| `Column` | `Column` | Column spanning only |
| `HorizontalAndVertical` | `Row` | Row spanning only — column narrows scope |
| `HorizontalAndVertical` | `Column` | Column spanning only — column narrows scope |
| `HorizontalAndVertical` | `HorizontalAndVertical` | Full row and column spanning |

### Programmatic Cell Merging — `MergeCellsAsync`

Manually merge rectangular cell regions. Supports single and batch (`IEnumerable<MergeCellInfo>`) overloads.

```razor
@code {
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            await Grid.MergeCellsAsync(new MergeCellInfo { RowIndex = 0, ColumnIndex = 1, RowSpan = 2, ColSpan = 3 });
            await Grid.MergeCellsAsync(new List<MergeCellInfo>
            {
                new() { RowIndex = 0, ColumnIndex = 0, RowSpan = 2, ColSpan = 1 },
                new() { RowIndex = 3, ColumnIndex = 2, RowSpan = 1, ColSpan = 2 }
            });
        }
    }
}
```

`MergeCellInfo`: `RowIndex`, `ColumnIndex` (zero-based start), `RowSpan`, `ColSpan`.

## Row Events

| Event | Args | Description |
|---|---|---|
| `RowDataBound` | `RowDataBoundEventArgs<T>` | Fires when a row is data-bound; used for styling |
| `RowCreating` | `RowCreatingEventArgs<T>` | Fires before new record is saved (editing) |
| `RowCreated` | `RowCreatedEventArgs<T>` | Fires after new record is saved |
| `RowUpdating` | `RowUpdatingEventArgs<T>` | Fires before an edit is saved |
| `RowUpdated` | `RowUpdatedEventArgs<T>` | Fires after an edit is saved |
| `RowDeleting` | `RowDeletingEventArgs<T>` | Fires before a row is deleted |
| `RowDeleted` | `RowDeletedEventArgs<T>` | Fires after a row is deleted |
| `RowDragStarting` | `RowDragStartingEventArgs<T>` | Fires when row drag begins |
| `RowDropping` | `RowDroppingEventArgs<T>` | Fires while rows are being dropped; can be canceled |
| `RowDropped` | `RowDroppedEventArgs<T>` | Fires after rows are dropped on target |
