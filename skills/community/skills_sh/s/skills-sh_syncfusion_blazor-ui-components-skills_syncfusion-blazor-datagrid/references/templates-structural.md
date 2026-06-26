# Templates — Column, Row & Detail — Syncfusion Blazor DataGrid

> *See also: [templates-interactive.md](./templates-interactive.md) for Edit, Toolbar, Caption & Pager templates.*

## Table of Contents
- [Column Template](#column-template)
- [Header Template](#header-template)
- [Row Template](#row-template)
- [Row Template with Formatting](#row-template-with-formatting)
- [Detail Template](#detail-template)
  - [Expand/Collapse Detail Row APIs](#expandcollapse-detail-row-apis)
  - [Expand Detail Row Initially (on DataBound)](#expand-detail-row-initially-on-databound)
  - [Hide Expand Icon When No Child Records](#hide-expand-icon-when-no-child-records)
  - [Customize Expand/Collapse Icon via CSS](#customize-expandcollapse-icon-via-css)
  - [Hierarchical Nested Grid (Detail Template)](#hierarchical-nested-grid-detail-template)

## Column Template

Render custom content in a column cell instead of the default field value:

```razor
<GridColumn HeaderText="Employee Image" Width="120">
    <Template>
        @{
            var emp = context as Employee;
        }
        <img src="@($"images/{emp.EmployeeID}.png")" alt="@emp.EmployeeID"
             style="height:55px; width:55px; border-radius:50%;" />
    </Template>
</GridColumn>
```

**Hyperlink in column:**

```razor
<GridColumn Field="CustomerID" HeaderText="Customer" Width="150">
    <Template>
        @{
            var order = context as Order;
        }
        <a href="/customer/@order.CustomerID">@order.CustomerID</a>
    </Template>
</GridColumn>
```

**Boolean as checkbox (read-only display):**

```razor
<GridColumn Field="IsActive" HeaderText="Active" Width="100">
    <Template>
        @{
            var order = context as Order;
        }
        <SfCheckBox Checked="@order.IsActive" Disabled="true"></SfCheckBox>
    </Template>
</GridColumn>
```

> Define `Field` property even on template columns if sorting, filtering, or editing on that column is needed.

**Syncfusion component inside a column template:**

Render any Syncfusion component (e.g., `SfChip`, `SfProgressBar`) inside `<Template>`:

```razor
<GridColumn HeaderText="Status" Width="150">
    <Template>
        @{
            var order = context as Order;
        }
        <SfChip>
            <ChipItems>
                <ChipItem Text="@order.Status"></ChipItem>
            </ChipItems>
        </SfChip>
    </Template>
</GridColumn>
```

> The `context` inside `<Template>` is typed as `object` — always cast it to your model type before accessing properties.

## Header Template

Customize the column header:

```razor
<GridColumn Field="Freight" HeaderText="Freight" Width="120">
    <HeaderTemplate>
        <div>
            <span class="e-icons e-money"></span> Freight
        </div>
    </HeaderTemplate>
</GridColumn>
```

> `HeaderTemplate` replaces only the header cell content. The sort icon is rendered **separately** by the Grid and will still appear alongside the custom content when `AllowSorting="true"` is set on the column.

## Row Template

Replace the entire row layout with a custom template (must match column count with `<td>` elements):

```razor
<SfGrid DataSource="@Employees" Height="315px">
    <GridTemplates>
        <RowTemplate Context="emp">
            @{
                var employee = emp as Employee;
            }
            <td>
                <img src="@($"images/{employee.EmployeeID}.png")" alt="@employee.FirstName" />
            </td>
            <td>
                <table>
                    <tr><td><b>@employee.FirstName @employee.LastName</b></td></tr>
                    <tr><td>@employee.Title</td></tr>
                    <tr><td>@employee.City, @employee.Country</td></tr>
                </table>
            </td>
        </RowTemplate>
    </GridTemplates>
    <GridColumns>
        <GridColumn HeaderText="Photo" Width="200"></GridColumn>
        <GridColumn HeaderText="Details" Width="350"></GridColumn>
    </GridColumns>
</SfGrid>
```

> `RowTemplate` is not compatible with the following Grid features: Filtering, Paging, Sorting, Searching, RTL, Export, Context Menu, State Persistence, Selection, Grouping, Editing, Frozen rows & columns, Virtual & Infinite scrolling, Column chooser, Column menu, Detail Row, Foreign key column, Resizing, Reordering, Aggregates, Clipboard, and Adaptive view.

## Row Template with Formatting

The `Columns.Format` property does **not** apply to values rendered inside a `RowTemplate`. Format values manually inside the template using .NET format strings:

```razor
<RowTemplate Context="emp">
    @{
        var employee = emp as Employee;
    }
    <td>@employee.FirstName</td>
    <td>@employee.HireDate.ToString("MM/dd/yyyy")</td>
    <td>@employee.Salary.ToString("C2")</td>
</RowTemplate>
```

> Use `.ToString("format")` or custom helper methods to produce the desired date, currency, or custom text output within a `RowTemplate`.

## Detail Template

Show expanded details when a row is expanded:

```razor
<SfGrid DataSource="@Employees" Height="400px">
    <GridTemplates>
        <DetailTemplate>
            @{
                var emp = context as Employee;
            }
            <div style="padding: 10px;">
                <p><b>Bio:</b> @emp.Notes</p>
                <p><b>Phone:</b> @emp.HomePhone</p>
            </div>
        </DetailTemplate>
    </GridTemplates>
    <GridColumns>
        <GridColumn Field="EmployeeID" HeaderText="ID" Width="80"></GridColumn>
        <GridColumn Field="FirstName" HeaderText="Name" Width="150"></GridColumn>
        <GridColumn Field="Title" HeaderText="Title" Width="200"></GridColumn>
    </GridColumns>
</SfGrid>
```

### Expand/Collapse Detail Row APIs

Use the following methods on `SfGrid<T>` to control detail row expansion programmatically:

| Method | Description |
|--------|-------------|
| `ExpandCollapseDetailRowAsync("FieldName", value)` | Expands or collapses the detail row matching the given field/value pair |
| `ExpandCollapseDetailRowAsync(rowDataObject)` | Expands or collapses the detail row for the provided row data object |
| `ExpandAllDetailRowAsync()` | Expands all detail rows |

```csharp
// Expand by field + value
await Grid.ExpandCollapseDetailRowAsync("EmployeeID", 1);

// Expand by row data object
await Grid.ExpandCollapseDetailRowAsync(Employees[0]);

// Expand all rows
await Grid.ExpandAllDetailRowAsync();
```

### Expand Detail Row Initially (on DataBound)

To expand a specific detail row on initial load, invoke `ExpandCollapseDetailRowAsync` inside the `DataBound` event:

```razor
<SfGrid @ref="grid" DataSource="@Employees">
    <GridEvents DataBound="DataBoundHandler" TValue="Employee"></GridEvents>
    <GridTemplates>
        <DetailTemplate>...</DetailTemplate>
    </GridTemplates>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Employee> grid;

    public async Task DataBoundHandler()
    {
        // Expand the detail row where EmployeeID == 1
        await grid.ExpandCollapseDetailRowAsync("EmployeeID", 1);
    }
}
```

> To expand **all** rows at initial load, call `ExpandAllDetailRowAsync()` inside the `DataBound` event instead.

### Hide Expand Icon When No Child Records

By default every row shows the expand icon regardless of whether child data exists. Use `RowDataBound` to hide the icon for rows with no children:

```razor
<SfGrid DataSource="@Employees" @ref="Grid">
    <GridEvents TValue="Employee" RowDataBound="RowDataBoundHandler"></GridEvents>
    <GridTemplates>
        <DetailTemplate>...</DetailTemplate>
    </GridTemplates>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    void RowDataBoundHandler(RowDataBoundEventArgs<Employee> args)
    {
        // Hide the expand icon when the employee has no orders
        if (!Orders.Any(o => o.EmployeeID == args.Data.EmployeeID))
        {
            args.Row.AddClass(new[] { "e-detail-hide" });
        }
    }
}
```

Add the following CSS to hide the expand cell for marked rows:

```css
.e-grid .e-detail-hide .e-detailrowcollapse {
    visibility: hidden;
    pointer-events: none;
}
```

> The class `e-detail-hide` is a custom class — choose any name and match it in the CSS selector.

### Customize Expand/Collapse Icon via CSS

Override the default expand/collapse icons in detail rows using CSS icon classes:

```css
/* Replace the default expand icon */
.e-grid .e-detailrowcollapse .e-icons::before {
    content: "\e7f9"; /* custom icon code from Syncfusion icon font */
}

/* Replace the default collapse icon */
.e-grid .e-detailrowexpand .e-icons::before {
    content: "\e825";
}
```

> Find available icon codes in the [Syncfusion Icon Demo](https://ej2.syncfusion.com/demos/#/icons). Use `font-family: 'e-icons'` if the icon font is not inherited automatically.

### Hierarchical Nested Grid (Detail Template)

Embed a child `SfGrid` inside the `<DetailTemplate>` to create a master-detail (hierarchical) layout:

```razor
<SfGrid DataSource="@Employees" Height="400px">
    <GridTemplates>
        <DetailTemplate>
            @{
                var emp = context as Employee;
                var childOrders = Orders.Where(o => o.EmployeeID == emp.EmployeeID).ToList();
            }
            <SfGrid DataSource="@childOrders" AllowPaging="true">
                <GridPageSettings PageSize="5"></GridPageSettings>
                <GridColumns>
                    <GridColumn Field="OrderID"    HeaderText="Order ID"   Width="120"></GridColumn>
                    <GridColumn Field="CustomerID" HeaderText="Customer"   Width="150"></GridColumn>
                    <GridColumn Field="Freight"    HeaderText="Freight"    Width="120" Format="C2"></GridColumn>
                    <GridColumn Field="ShipCity"   HeaderText="Ship City"  Width="150"></GridColumn>
                </GridColumns>
            </SfGrid>
        </DetailTemplate>
    </GridTemplates>
    <GridColumns>
        <GridColumn Field="EmployeeID" HeaderText="ID"    Width="80"></GridColumn>
        <GridColumn Field="FirstName"  HeaderText="Name"  Width="150"></GridColumn>
        <GridColumn Field="Title"      HeaderText="Title" Width="200"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    List<Employee> Employees = ...;
    List<Order>    Orders    = ...;
}
```

> Filter child data per parent row inside the template using LINQ. Each expanded row creates its own independent child Grid instance. Avoid heavy data operations in the template to prevent performance issues on expand.
