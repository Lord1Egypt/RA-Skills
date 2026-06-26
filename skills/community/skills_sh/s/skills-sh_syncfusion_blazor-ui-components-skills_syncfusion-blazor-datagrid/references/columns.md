# Columns — Syncfusion Blazor DataGrid

## Table of Contents
1. [Column Definition](#column-definition)
2. [Column Types & Formatting](#column-types--formatting)
3. [Column Width](#column-width)
4. [Controlling Column-Level Grid Actions](#controlling-column-level-grid-actions)
5. [Render Boolean Values as Checkbox](#render-boolean-values-as-checkbox)
6. [Fixed Columns](#fixed-columns)
7. [Responsive Columns (HideAtMedia)](#responsive-columns-hideatmedia)
8. [Accessing Columns Programmatically](#accessing-columns-programmatically)
9. [Column Headers](#column-headers)
10. [Stacked Headers](#stacked-headers)
11. [Column Visibility](#column-visibility)
12. [Column Reorder](#column-reorder)
13. [Column Resizing](#column-resizing)
14. [Frozen Columns](#frozen-columns)
15. [Column Chooser](#column-chooser)
16. [Column Menu](#column-menu)
17. [Column Spanning](#column-spanning)
18. [Auto-Generated Columns](#auto-generated-columns)

## Related Skills (Detailed Guides)

For in-depth coverage of specific column features, see:

- **[Column Headers](column-headers.md)** — HeaderText, HeaderTemplate, stacked headers, text alignment, text wrapping
- **[Column Template](column-template.md)** — Render custom HTML, images, hyperlinks, charts, and Syncfusion components
- **[Column Resizing](column-resizing.md)** — Enable resizing, set min/max width, prevent resizing, AutoFit columns
- **[Column Reorder](column-reorder.md)** — Drag-and-drop reordering, programmatic column reordering by index or field
- **[Column Spanning](column-spanning.md)** — AutoSpan modes, merge cells vertically and horizontally
- **[Column Rendering](column-rendering.md)** — Manual column definition, auto-generation, primary keys, field binding
- **[Column Chooser](column-chooser.md)** — Show/hide columns, open dialog programmatically, customize search
- **[Column Menu](column-menu.md)** — Context menu operations, custom menu items, event handling
- **[Column Validation](column-validation.md)** — Validation rules, data annotations, custom validators
- **[Foreign Key Column](foreignKey-column.md)** — Display related data from foreign key sources, local/remote binding, custom editors
- **[Frozen Column](frozen-column.md)** — Keep columns visible during scrolling, freeze directions, freeze line moving

---

## Column Definition

```razor
<GridColumn
    Field="OrderID"
    HeaderText="Order ID"
    Width="120"
    TextAlign="TextAlign.Right"
    Format="C2"
    Type="ColumnType.Number"
    IsPrimaryKey="true"
    AllowSorting="true"
    AllowFiltering="true"
    AllowEditing="true"
    AllowGrouping="true"
    AllowSearching="true"
    Visible="true"
    ClipMode="ClipMode.EllipsisWithTooltip">
</GridColumn>
```

---

## Column Types & Formatting

| `ColumnType` | C# Type | Description | Example Format |
|---|---|---|---|
| `String` | string | Text data. Default when `Type` is not set. | — |
| `Integer` | int | Integer numeric values. | `"N0"` |
| `Decimal` | decimal | Decimal numeric values. | `"C2"`, `"N2"` |
| `Double` | double | Double-precision floating-point values. | `"C2"`, `"N2"` |
| `Long` | long | Long integer values. | `"N0"` |
| `Boolean` | bool | Boolean values. Renders as text (true/false) by default; use `DisplayAsCheckBox="true"` to render as checkbox. | — |
| `CheckBox` | — | Renders a checkbox for **row selection**. Activates multiple-selection mode by default. Do not use for boolean data fields — use `Boolean` for that. | — |
| `Date` | DateTime (date only) | Date values with formatting support. | `"d"`, `"MM/dd/yyyy"` |
| `DateTime` | DateTime (with time) | Date and time values. | `"dd/MM/yyyy hh:mm a"` |
| `DateOnly` | DateOnly | .NET 7+ `DateOnly` values. | `"d"` |
| `TimeOnly` | TimeOnly | .NET 7+ `TimeOnly` values. | `"hh:mm"` |
| `None` | — | No specific data type specified. | — |

> **Boolean vs CheckBox:** `ColumnType.Boolean` binds to a boolean data field and supports editing. `ColumnType.CheckBox` is purely for row selection UI and does not bind to data.

```razor
<GridColumn Type="ColumnType.CheckBox" Width="50"></GridColumn>  <!-- row selection -->
<GridColumn Field="OrderID"    Type="ColumnType.Integer"  IsPrimaryKey="true" Width="120"></GridColumn>
<GridColumn Field="Freight"    Type="ColumnType.Double"   Format="C2" TextAlign="TextAlign.Right"></GridColumn>
<GridColumn Field="OrderDate"  Type="ColumnType.Date"     Format="d"  TextAlign="TextAlign.Right"></GridColumn>
<GridColumn Field="IsVerified" Type="ColumnType.Boolean"  DisplayAsCheckBox="true"></GridColumn>
```

---

## Column Width

The `Width` property of `GridColumn` accepts **pixels** (number), **percentages** (`"25%"`), or `"auto"`.

| Width Value | Example | Behavior |
|---|---|---|
| Pixel (number) | `Width="120"` | Fixed pixel width |
| Percentage | `Width="25%"` | Responsive, relative to container |
| Auto | `Width="auto"` | Fit content width |

```razor
<GridColumn Field="OrderID"    Width="120"></GridColumn>       <!-- pixels -->
<GridColumn Field="CustomerID" Width="25%"></GridColumn>       <!-- percentage -->
<GridColumn Field="ShipCity"   Width="auto"></GridColumn>      <!-- auto-fit -->
```

> When `AllowResizing="true"`, columns without a specified width default to **200 pixels**.

---

## Controlling Column-Level Grid Actions

Each column can independently allow or deny grid actions using boolean properties on `GridColumn`:

| Property | Default | Description |
|---|---|---|
| `AllowSorting` | `true` | Enable/disable sorting for this column |
| `AllowFiltering` | `true` | Enable/disable filtering for this column |
| `AllowGrouping` | `true` | Enable/disable grouping for this column |
| `AllowEditing` | `true` | Enable/disable editing for this column |
| `AllowResizing` | `true` | Enable/disable resizing for this column |
| `AllowReordering` | `true` | Enable/disable reordering for this column |
| `AllowSearching` | `true` | Include/exclude column from global search |

```razor
<GridColumn Field="OrderID"    AllowEditing="false"  AllowGrouping="false" IsPrimaryKey="true"></GridColumn>
<GridColumn Field="CustomerID" AllowSorting="false"  AllowFiltering="false"></GridColumn>
<GridColumn Field="Freight"    AllowSearching="false" AllowReordering="false"></GridColumn>
```

---

## Render Boolean Values as Checkbox

Use `DisplayAsCheckBox="true"` to render a boolean column as a visual checkbox (read-only display). Pair with `Type="ColumnType.Boolean"`.

```razor
<GridColumn Field="IsVerified" HeaderText="Verified"
            DisplayAsCheckBox="true"
            Type="ColumnType.Boolean"
            Width="120">
</GridColumn>
```

> For **editing** boolean values, the column's `EditType` automatically uses `EditType.BooleanEdit`. To render a checkbox in edit mode, set `DisplayAsCheckBox="true"`.

---

## Fixed Columns

A fixed column stays at its position regardless of column reordering. Set `FixedColumn="true"`:

```razor
<GridColumn Field="OrderID" IsPrimaryKey="true" FixedColumn="true" Width="120"></GridColumn>
```

> Fixed columns cannot be moved by drag-and-drop reordering.

---

## Responsive Columns (HideAtMedia)

Hide columns on specific screen sizes using the `HideAtMedia` CSS media query property:

```razor
<!-- Hide when viewport is 700px or wider -->
<GridColumn Field="ShipCity"    HideAtMedia="(min-width: 700px)" Width="150"></GridColumn>
<!-- Hide on small screens (below 500px) -->
<GridColumn Field="ShipCountry" HideAtMedia="(max-width: 500px)" Width="150"></GridColumn>
```

> `HideAtMedia` accepts any valid CSS media query string. The column is hidden/shown dynamically as the viewport resizes.

---

## Accessing Columns Programmatically

| Method | Description |
|---|---|
| `GetColumnsAsync()` | Returns all column objects |
| `GetColumnByFieldAsync(field)` | Get column by field name |
| `GetColumnByUidAsync(uid)` | Get column by unique ID |
| `GetVisibleColumnsAsync()` | Get only visible columns |
| `GetForeignKeyColumnsAsync()` | Get all foreign key columns |
| `GetColumnFieldNamesAsync()` | Get array of all field names |
| `RefreshColumnsAsync()` | Re-render columns after dynamic changes |

```razor
@code {
    SfGrid<Order> Grid;

    async Task Example()
    {
        var allCols   = await Grid.GetColumnsAsync();
        var col       = await Grid.GetColumnByFieldAsync("OrderID");
        var visible   = await Grid.GetVisibleColumnsAsync();
        var fields    = await Grid.GetColumnFieldNamesAsync();

        // Dynamically add/change columns then refresh:
        await Grid.RefreshColumnsAsync();
    }
}
```

---

## Column Headers

```razor
<GridColumn Field="CustomerID" HeaderText="Customer Name">
    <HeaderTemplate>
        <div>
            <span class="e-icons e-user" style="font-size:14px"></span>
            Customer
        </div>
    </HeaderTemplate>
</GridColumn>
```

### Text Wrapping

```razor
<SfGrid AllowTextWrap="true">
    <GridTextWrapSettings WrapMode="WrapMode.Header"></GridTextWrapSettings>
    ...
</SfGrid>
```

`WrapMode`: `Header`, `Content`, `Both`.

### Custom Attributes on Header

```razor
<GridColumn Field="OrderID" HeaderText="Order ID"
            CustomAttributes="@(new Dictionary<string,object>{ {"class","custom-header"} })">
</GridColumn>
```

---

## Stacked Headers

Group multiple columns under a common header:

```razor
<GridColumns>
    <GridColumn HeaderText="Order Info">
        <Columns>
            <GridColumn Field="OrderID" HeaderText="ID" Width="100"></GridColumn>
            <GridColumn Field="OrderDate" HeaderText="Date" Width="120"></GridColumn>
        </Columns>
    </GridColumn>
    <GridColumn HeaderText="Ship Info">
        <Columns>
            <GridColumn Field="ShipCity" Width="120"></GridColumn>
            <GridColumn Field="ShipCountry" Width="150"></GridColumn>
        </Columns>
    </GridColumn>
</GridColumns>
```

---

## Column Visibility

### Hide/Show via AllowToggle

```razor
<GridColumn Field="CustomerID" Visible="true"></GridColumn>
<GridColumn Field="InternalNote" Visible="false"></GridColumn>
```

### Programmatic Show/Hide

```razor
<SfGrid @ref="Grid" ...>...</SfGrid>
@code {
    SfGrid<Order> Grid;
    await Grid.HideColumnsAsync(new string[] { "Customer ID" });   // by HeaderText
    await Grid.ShowColumnsAsync(new string[] { "Customer ID" });
    // Or by field:
    await Grid.HideColumnByFieldAsync("CustomerID");
    await Grid.ShowColumnByFieldAsync("CustomerID");
    // Get all columns:
    var cols = await Grid.GetColumnsAsync();
}
```

---

## Column Reorder

```razor
<SfGrid DataSource="@Orders" AllowReordering="true">
    <GridColumns>...</GridColumns>
</SfGrid>
```

Programmatic reorder:

```razor
await Grid.ReorderColumnsAsync(new string[] { "ShipCountry", "OrderDate" }, "Freight");
// Moves ShipCountry and OrderDate before Freight column
```

Events: `ColumnReordering` (cancelable), `ColumnReordered`.

---

## Column Resizing

```razor
<SfGrid DataSource="@Orders" AllowResizing="true">
    <GridColumns>
        <GridColumn Field="OrderID" MinWidth="100" MaxWidth="300" Width="150"></GridColumn>
        <GridColumn Field="CustomerID" AllowResizing="false" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

Events: `OnResizeStart`, `ResizeStopped`.

### AutoFit Columns

```razor
await Grid.AutoFitColumnsAsync();                         // All columns
await Grid.AutoFitColumnsAsync(new string[]{"OrderID"});  // Specific columns
```

---

## Frozen Columns

### Freeze by Count

```razor
<SfGrid DataSource="@Orders" FrozenColumns="2" FrozenRows="2">
    <GridColumns>
        <GridColumn Field="OrderID"   Width="120"></GridColumn>  <!-- Frozen -->
        <GridColumn Field="CustomerID" Width="150"></GridColumn> <!-- Frozen -->
        <GridColumn Field="Freight"   Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

### Freeze Individual Columns

```razor
<GridColumn Field="OrderID"    IsFrozen="true" Freeze="FreezeDirection.Left"  Width="120"></GridColumn>
<GridColumn Field="ShipCountry" IsFrozen="true" Freeze="FreezeDirection.Right" Width="150"></GridColumn>
```

`FreezeDirection`: `Left`, `Right`, `Fixed`.

---

## Column Chooser

Allow users to show/hide columns via a dialog:

```razor
<SfGrid DataSource="@Orders" ShowColumnChooser="true"
        Toolbar="@(new List<string>() { "ColumnChooser" })">
    <GridColumns>
        <GridColumn Field="OrderID"    ShowInColumnChooser="false"></GridColumn> <!-- Always visible -->
        <GridColumn Field="CustomerID"></GridColumn>
        <GridColumn Field="ShipCountry"></GridColumn>
    </GridColumns>
</SfGrid>
```

Programmatic open:

```razor
await Grid.OpenColumnChooserAsync(100, 50); // x, y position
```

Custom column chooser template:

```razor
<SfGrid ShowColumnChooser="true">
    <GridColumnChooserSettings Operator="SearchOperatorType.Contains"></GridColumnChooserSettings>
    ...
</SfGrid>
```

---

## Column Menu

Right-click header for column operations:

```razor
<SfGrid DataSource="@Orders" ShowColumnMenu="true">
    <GridColumnMenuSettings ShowColumnChooser="true"></GridColumnMenuSettings>
    <GridColumns>
        <GridColumn Field="OrderID" ColumnMenuItems="@(new List<string>{"AutoFit"})"></GridColumn>
    </GridColumns>
</SfGrid>
```

Default items: `AutoFit`, `AutoFitAll`, `SortAscending`, `SortDescending`, `Group`, `Ungroup`, `ColumnChooser`, `Filter`.

Custom items:

```razor
<SfGrid ShowColumnMenu="true">
    <GridColumnMenuItems>
        <GridColumnMenuItem Text="Custom Action" Id="customItem"></GridColumnMenuItem>
    </GridColumnMenuItems>
    <GridEvents TValue="Order" ColumnMenuItemClicked="OnMenuItemClicked"></GridEvents>
    ...
</SfGrid>
@code {
    void OnMenuItemClicked(ColumnMenuClickEventArgs args)
    {
        if (args.Item.Id == "customItem") { /* custom logic */ }
    }
}
```

Events: `OnColumnMenuOpen`, `ColumnMenuItemClicked`.

---

## Column Spanning

Merge cells across columns:

```razor
<SfGrid DataSource="@Orders">
    <GridEvents TValue="Order" QueryCellInfo="QueryCellInfoHandler"></GridEvents>
    <GridColumns>
        <GridColumn Field="OrderID" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" Width="150"></GridColumn>
        <GridColumn Field="ShipCity" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    void QueryCellInfoHandler(QueryCellInfoEventArgs<Order> args)
    {
        // Span CustomerID column over next 2 columns for row 0
        if (args.Data.OrderID == 10248 && args.Column.Field == "CustomerID")
        {
            args.ColSpan = 2;
        }
    }
}
```

---

## Auto-Generated Columns

When no `<GridColumns>` is defined, columns are auto-generated from the model:

```razor
<SfGrid DataSource="@Orders">
    <!-- No GridColumns block — columns auto-generated from Order properties -->
</SfGrid>
```

Control auto-generation with `AutoGenerateColumns="true"` (default when no GridColumns defined).

### For ExpandoObject

```razor
<SfGrid DataSource="@DynamicOrders">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer"></GridColumn>
    </GridColumns>
</SfGrid>
```