# Cell — Syncfusion Blazor DataGrid

## Table of Contents
- [QueryCellInfo Event](#querycellinfo-event)
- [Custom Attributes](#custom-attributes)
- [ClipMode](#clipmode)
- [Autowrap the Grid Content](#autowrap-the-grid-content)
- [GridLines](#gridlines)
- [Disable HTML Encoding](#disable-html-encoding)
- [Tooltip](#tooltip)
- [Tooltip Template](#tooltip-template)
- [Custom Tooltip for Columns](#custom-tooltip-for-columns)
- [Row Height](#row-height)

## QueryCellInfo Event

Customize individual cell rendering at runtime:

```razor
<SfGrid DataSource="@Orders">
    <GridEvents TValue="Order" QueryCellInfo="CellHandler"></GridEvents>
    <GridColumns>
        <GridColumn Field="Freight" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    void CellHandler(QueryCellInfoEventArgs<Order> args)
    {
        // Change background color for high freight values
        if (args.Column.Field == "Freight" && args.Data.Freight > 100)
        {
            args.Cell.AddStyle(new string[] { "background-color:lightcoral" });
        }
    }
}
```

## Custom Attributes

Apply CSS classes or HTML attributes to columns:

```razor
<GridColumn Field="OrderID" CustomAttributes="@(new Dictionary<string,object>{ {\"class\",\"custom-cell\"} })"></GridColumn>
```

### Inline Styles in CustomAttributes

Apply inline styles directly to cells using the `CustomAttributes` property:

```razor
<GridColumn Field="ShipCity" 
            HeaderText="Ship City" 
            CustomAttributes="@(new Dictionary<string, object>(){ { \"style\", \"background: #d7f0f4; font-style: italic; color: navy\" }})" 
            Width="100">
</GridColumn>
```

**Recommendation:** While inline styles work, using CSS classes is preferred for maintainability. Define styles in a `<style>` block:

```html
<style>
    .custom-cell-style {
        background: #d7f0f4;
        font-style: italic;
        color: navy;
    }
</style>
```

Then apply via class:

```razor
<GridColumn Field="ShipCity" 
            HeaderText="Ship City" 
            CustomAttributes="@(new Dictionary<string, object>(){ { \"class\", \"custom-cell-style\" }})" 
            Width="100">
</GridColumn>
```

## ClipMode

Control text overflow behavior:

| `ClipMode` | Behavior |
|---|---|
| `Clip` | Content clipped at cell boundary |
| `Ellipsis` | Shows `...` when content overflows |
| `EllipsisWithTooltip` | Shows `...` with full value on hover |

```razor
<GridColumn Field="ShipName" ClipMode="ClipMode.EllipsisWithTooltip" Width="150"></GridColumn>
```

## Autowrap the Grid Content

Enable automatic text wrapping in cells to display multi-line content within defined column widths:

```razor
<SfGrid DataSource="@Orders" AllowTextWrap="true" Height="315">
    <GridTextWrapSettings WrapMode="WrapMode.Content"></GridTextWrapSettings>
    <GridColumns>
        <GridColumn Field="Name" HeaderText="Name" Width="70"></GridColumn>
        <GridColumn Field="Description" HeaderText="Description" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

**WrapMode Options:**

| Mode | Description |
|------|-------------|
| `Both` | Wraps text in both header and content cells (default) |
| `Header` | Wraps text only in header cells |
| `Content` | Wraps text only in content cells |

**Key Points:**
- Set `AllowTextWrap` to **true** to enable wrapping
- Define column widths to control wrap boundaries
- Use `TextWrapSettings.WrapMode` to customize wrapping behavior
- HTML content may interfere with wrapping; use templates for complex content

## GridLines

Control cell border visibility:

```razor
<SfGrid DataSource="@Orders" GridLines="GridLine.Both">
    ...
</SfGrid>
```

`GridLine` values: `Default`, `Both`, `None`, `Horizontal`, `Vertical`.

## Disable HTML Encoding

Render raw HTML in cells (use with trusted data only):

```razor
<GridColumn Field="Description" DisableHtmlEncode="false"></GridColumn>
```

> **Warning:** Only disable HTML encoding for trusted data sources to avoid XSS vulnerabilities.

## Tooltip

Display tooltips on cell hover showing the cell value:

```razor
<SfGrid DataSource="@Orders" ShowTooltip="true">
    <GridColumns>
        <GridColumn Field="ShipName" HeaderText="Ship Name" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

> Use the grid-level `ShowTooltip` property to enable tooltips for all cells. For advanced tooltip customization with custom content, use the `TooltipTemplate` property within `GridTemplates`.

## Tooltip Template

Customize tooltip content for header and content cells using the `TooltipTemplate` property:

```razor
<SfGrid DataSource="@Orders" ShowTooltip="true" Width="700">
    <GridTemplates>
        <TooltipTemplate>
            @{
                var tooltip = context as TooltipTemplateContext;
                var order = tooltip?.Data as OrderData;
                if (tooltip?.RowIndex == -1)
                {
                    // Header cell tooltip
                    <span><strong>@tooltip.Value</strong>: Column information</span>
                }
                else
                {
                    // Content cell tooltip
                    var fieldName = tooltip?.Column?.Field;
                    if (fieldName == nameof(OrderData.Freight))
                    {
                        <p><strong>Freight Cost: </strong>$@order.Freight</p>
                    }
                    else if (fieldName == nameof(OrderData.ShipCity))
                    {
                        <p><strong>Destination: </strong>@order.ShipCity, @order.ShipCountry</p>
                    }
                    else
                    {
                        <span>@tooltip.Value</span>
                    }
                }
            }
        </TooltipTemplate>
    </GridTemplates>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="90"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="90"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="80"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>
```

**TooltipTemplateContext Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `Value` | string | Cell content (column name for header, cell value for content) |
| `RowIndex` | int | Row index (-1 for header cells) |
| `ColumnIndex` | int | Column index |
| `Data` | object | Complete row data (null for header cells) |
| `Column` | GridColumn | Column metadata including field name |

## Custom Tooltip for Columns

Display custom tooltips using the `SfTooltip` component within column templates:

```razor
@using Syncfusion.Blazor.Grids
@using Syncfusion.Blazor.Popups

<SfGrid DataSource="@Orders">
    <GridColumns>
        <GridColumn Field="EmployeeID" HeaderText="Employee ID" TextAlign="TextAlign.Right" Width="120"></GridColumn>
        <GridColumn Field="FirstName" HeaderText="First Name" Width="130">
            <Template>
                @{
                    var employee = (context as EmployeeData);
                    <SfTooltip Position="Position.BottomLeft">
                        <ContentTemplate>
                            <span>Employee: @employee.FirstName @employee.LastName</span>
                        </ContentTemplate>
                        <ChildContent>
                            <span>@employee.FirstName</span>
                        </ChildContent>
                    </SfTooltip>
                }
            </Template>
        </GridColumn>
        <GridColumn Field="Title" HeaderText="Title" Width="120"></GridColumn>
        <GridColumn Field="HireDate" HeaderText="Hire Date" Format="d" TextAlign="TextAlign.Right" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    public List<EmployeeData> Orders { get; set; }

    protected override void OnInitialized()
    {
        Orders = EmployeeData.GetAllRecords();
    }
}
```

**Key Advantages:**
- Rich HTML content support in tooltips
- Flexible positioning with `Position` property
- Multiple templates per column possible
- Can display complex data relationships
- Better user experience for detailed information

## Row Height

Control default row height at grid level or per-row:

```razor
<SfGrid DataSource="@Orders" RowHeight="40">
    ...
</SfGrid>
```

Per-row height via `RowDataBound`:

```razor
<GridEvents TValue="Order" RowDataBound="RowBound"></GridEvents>
@code {
    void RowBound(RowDataBoundEventArgs<Order> args)
    {
        if (args.Data.Freight > 100)
            args.Row.AddStyle(new string[] { "height:60px" });
    }
}
