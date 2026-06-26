# Excel Export — Syncfusion Blazor DataGrid

## Table of Contents
- [Enable and Trigger Export](#enable-and-trigger-export)
- [ExcelExportProperties](#excelexportproperties)
- [Export Current Page Only](#export-current-page-only)
- [Export Selected Records](#export-selected-records)
- [Export with Custom Data Source](#export-with-custom-data-source)
- [Add Header and Footer](#add-header-and-footer)
- [Apply Theme](#apply-theme)
- [CSV Export](#csv-export)
- [Show Spinner During Export](#show-spinner-during-export)
- [Export Events](#export-events)
- [Export Grouped Records](#export-grouped-records)
- [Export with Hidden Columns](#export-with-hidden-columns)
- [Show or Hide Columns While Exporting](#show-or-hide-columns-while-exporting)
- [Define File Name](#define-file-name)
- [Customize Export Columns](#customize-export-columns)
- [Background Color Customization](#background-color-customization)
- [Conditional Cell Formatting](#conditional-cell-formatting)
- [Exporting with Custom Aggregate](#exporting-with-custom-aggregate)
- [Exporting with Custom Date Format](#exporting-with-custom-date-format)
- [Passing Additional Parameters to the Server](#passing-additional-parameters-to-the-server)
- [Add Additional Worksheets](#add-additional-worksheets)
- [Export as Memory Stream](#export-as-memory-stream)

## Enable and Trigger Export

```razor
<SfGrid ID="Grid" @ref="Grid" DataSource="@Orders" AllowExcelExport="true"
        Toolbar="@(new List<string>{ "ExcelExport","CsvExport" })">
    <GridEvents OnToolbarClick="ToolbarClickHandler" TValue="Order"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        // Grid ID + item name forms the button ID
        if (args.Item.Id == "Grid_excelexport")
            await Grid.ExportToExcelAsync();
        else if (args.Item.Id == "Grid_csvexport")
            await Grid.ExportToCsvAsync();
    }
}
```

## ExcelExportProperties

Pass `ExcelExportProperties` to customize the export:

```razor
@code {
    async Task ExportToExcel()
    {
        var props = new ExcelExportProperties
        {
            FileName = "Orders.xlsx",
            ExportType = ExportType.AllPages,     // or ExportType.CurrentPage
            IncludeHiddenColumn = true,
            IsAutoFit = true
        };
        await Grid.ExportToExcelAsync(props);
    }
}
```

| Property | Description |
|---|---|
| `FileName` | Output file name |
| `ExportType` | `AllPages` or `CurrentPage` |
| `IncludeHiddenColumn` | Include hidden columns |
| `IsAutoFit` | Auto-fit column widths |
| `DataSource` | Custom data source for export |
| `Query` | Filter rows via Query |
| `EnableFilter` | Show filter dropdowns in header row |

## Export Current Page Only

```razor
var props = new ExcelExportProperties
{
    ExportType = ExportType.CurrentPage
};
await Grid.ExportToExcelAsync(props);
```

## Export Selected Records

```razor
var selectedData = await Grid.GetSelectedRecordsAsync();
var props = new ExcelExportProperties
{
    DataSource = selectedData
};
await Grid.ExportToExcelAsync(props);
```

## Export with Custom Data Source

```razor
var filtered = Orders.Where(o => o.Freight > 100).ToList();
var props = new ExcelExportProperties { DataSource = filtered };
await Grid.ExportToExcelAsync(props);
```

## Add Header and Footer

> Use `ExcelHorizontalAlign` (not `ExcelHAlign`) for horizontal alignment in `ExcelStyle`.

```razor
var props = new ExcelExportProperties
{
    Header = new ExcelHeader
    {
        HeaderRows = 2,
        Rows = new List<ExcelRow>
        {
            new ExcelRow { Cells = new List<ExcelCell>
            {
                new ExcelCell { Value = "Order Report", ColSpan = 4,
                    Style = new ExcelStyle { FontSize = 16, Bold = true, HAlign = ExcelHorizontalAlign.Center }
                }
            }},
            new ExcelRow { Cells = new List<ExcelCell>
            {
                new ExcelCell { Value = DateTime.Now.ToString("MMMM dd, yyyy"), ColSpan = 4,
                    Style = new ExcelStyle { HAlign = ExcelHorizontalAlign.Center }
                }
            }}
        }
    },
    Footer = new ExcelFooter
    {
        FooterRows = 1,
        Rows = new List<ExcelRow>
        {
            new ExcelRow { Cells = new List<ExcelCell>
            {
                new ExcelCell { Value = "Confidential", ColSpan = 4,
                    Style = new ExcelStyle { HAlign = ExcelHorizontalAlign.Center }
                }
            }}
        }
    }
};
await Grid.ExportToExcelAsync(props);
```

## Apply Theme

```razor
var props = new ExcelExportProperties
{
    Theme = new ExcelTheme
    {
        Header = new ExcelStyle { FontColor = "#ffffff", BackColor = "#0078d4", Bold = true },
        Record = new ExcelStyle { FontColor = "#333333", BackColor = "#f3f3f3" },
        Caption = new ExcelStyle { FontColor = "#0078d4", Bold = true }
    }
};
await Grid.ExportToExcelAsync(props);
```

## CSV Export

```razor
// Simple
await Grid.ExportToCsvAsync();

// With options (asMemoryStream: false = direct download)
var props = new ExcelExportProperties
{
    FileName = "orders.csv",
    ExportType = ExportType.AllPages
};
await Grid.ExportToCsvAsync(asMemoryStream: false, props);
```

## Show Spinner During Export

```razor
<GridEvents TValue="Order"
            OnToolbarClick="ToolbarClickHandler"
            ExportComplete="OnExportComplete">
</GridEvents>

@code {
    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_excelexport")
        {
            await Grid.ShowSpinnerAsync();
            await Grid.ExportToExcelAsync();
        }
    }

    async Task OnExportComplete(object args)
    {
        await Grid.HideSpinnerAsync();
    }
}
```

## Export Events

| Event | Description |
|---|---|
| `ExcelExportInit` | Fires before Excel export begins |
| `ExcelQueryCellInfoEvent` | Fires per data cell during export; customize cell value/style |
| `ExcelHeaderQueryCellInfo` | Fires per header cell during export |
| `ExcelAggregateTemplateInfo` | Fires per aggregate cell during export; use `args.Cell.Value` to set custom aggregate value |
| `ExportComplete` | Fires after export is complete |

## Export Grouped Records

Set `AllowGrouping="true"` and configure `GridGroupSettings`. Grouped rows export with Excel outline formatting (max 7 levels).

```razor
<SfGrid AllowGrouping="true" AllowExcelExport="true" ...>
    <GridGroupSettings Columns="@(new string[] { "CustomerID" })"></GridGroupSettings>
    <GridEvents OnToolbarClick="ToolbarClickHandler" TValue="OrderData"></GridEvents>
</SfGrid>

@code {
    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_excelexport")
            await Grid.ExportToExcelAsync();
    }
}
```

> **Limitation:** Excel supports a maximum of 7 nested outline levels. Grouping beyond this will not include outline structure in the export.

## Export with Hidden Columns

Set `IncludeHiddenColumn = true` to include columns with `Visible="false"` in the export.

```razor
var props = new ExcelExportProperties { IncludeHiddenColumn = true };
await Grid.ExportToExcelAsync(props);
```

## Show or Hide Columns While Exporting

Toggle column `Visible` state before export and restore it in `ExportComplete`.

```razor
<GridEvents OnToolbarClick="ToolbarClickHandler" ExportComplete="ExportCompleteHandler" TValue="OrderData"></GridEvents>

@code {
    bool isCustomerIDVisible = false;
    bool isShipCityVisible = true;

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_excelexport")
        {
            isCustomerIDVisible = true;   // show during export
            isShipCityVisible = false;    // hide during export
            await Grid.ExportToExcelAsync();
        }
    }

    void ExportCompleteHandler(object args)
    {
        isCustomerIDVisible = false;  // restore
        isShipCityVisible = true;
    }
}
```

## Define File Name

```razor
var props = new ExcelExportProperties { FileName = "OrderReport.xlsx" };
await Grid.ExportToExcelAsync(props);
```

## Customize Export Columns

Override column definitions (field, header, format, alignment) for export only without affecting the Grid UI.

```razor
var exportColumns = new List<GridColumn>
{
    new GridColumn { Field = "OrderID",    HeaderText = "Order Number", Width = "120" },
    new GridColumn { Field = "CustomerID", HeaderText = "Customer Name", Width = "120" },
    new GridColumn { Field = "Freight",    HeaderText = "Freight", Format = "C2",
                     TextAlign = TextAlign.Center, Width = "120" }
};
var props = new ExcelExportProperties { Columns = exportColumns };
await Grid.ExportToExcelAsync(props);
```

> By default, the exported Excel document uses the **Material** theme styling.

## Background Color Customization

Use `BackColor` on `ExcelStyle` to set background colors for header, record, and caption rows.

```razor
var props = new ExcelExportProperties
{
    Theme = new ExcelTheme
    {
        Header = new ExcelStyle { BackColor = "#0078d4", FontColor = "#ffffff", Bold = true },
        Record = new ExcelStyle { BackColor = "#f3f3f3" },
        Caption = new ExcelStyle { BackColor = "#e0e0e0" }
    }
};
await Grid.ExportToExcelAsync(props);
```

## Conditional Cell Formatting

Handle `ExcelQueryCellInfoEvent` to apply per-cell styles during export based on data values.

```razor
<GridEvents ExcelQueryCellInfoEvent="ExcelQueryCellInfoHandler" TValue="OrderData"></GridEvents>

@code {
    void ExcelQueryCellInfoHandler(ExcelQueryCellInfoEventArgs<OrderData> args)
    {
        if (args.Column.Field == "Freight")
        {
            if (args.Data.Freight < 30)      args.Style.BackColor = "#99ffcc";
            else if (args.Data.Freight < 60) args.Style.BackColor = "#ffffb3";
            else                             args.Style.BackColor = "#ff704d";
        }
    }
}
```

## Exporting with Custom Aggregate

Set aggregate `Type="AggregateType.Custom"` and handle `ExcelAggregateTemplateInfo` to supply the value for export.

```razor
<GridAggregates>
    <GridAggregate>
        <GridAggregateColumns>
            <GridAggregateColumn Field="ShipCountry" Type="AggregateType.Custom"
                CustomAggregate="@CustomAggregateFunction">
                <FooterTemplate>Count: @(context as AggregateTemplateContext).Custom</FooterTemplate>
            </GridAggregateColumn>
        </GridAggregateColumns>
    </GridAggregate>
</GridAggregates>
<GridEvents ExcelAggregateTemplateInfo="ExcelAggregateHandler" TValue="OrderData"></GridEvents>

@code {
    int CustomAggregateFunction() => Orders.Count(x => x.ShipCountry == "Brazil");

    void ExcelAggregateHandler(ExcelAggregateEventArgs args)
    {
        if (args.Column.Field == "ShipCountry")
            args.Cell.Value = CustomAggregateFunction();
    }
}
```

## Exporting with Custom Date Format

Set `Type="ColumnType.Date"` and `Format` on the column; the format is applied in the exported file automatically.

```razor
<GridColumn Field="OrderDate" HeaderText="Order Date"
            Type="ColumnType.Date" Format="yyyy-MM-dd" Width="150" />
```

## Passing Additional Parameters to the Server

Use `Grid.Query.AddParams()` before export to pass custom parameters with the data request, then restore the original query in `ExportComplete`.

```razor
<GridEvents OnToolbarClick="ToolbarClickHandler" ExportComplete="ExportCompleteHandler" TValue="OrderData"></GridEvents>

@code {
    Query queryClone;

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_excelexport")
        {
            queryClone = Grid.Query;
            Grid.Query = new Query().AddParams("exportParam", "value");
            await Grid.ExportToExcelAsync();
        }
    }

    void ExportCompleteHandler(object args)
    {
        if (queryClone != null) Grid.Query = queryClone;
    }
}
```

## Add Additional Worksheets

Use `ExcelExportProperties.Workbook` to inject extra worksheets; set `GridSheetIndex` to control where Grid data lands.

```razor
@using Syncfusion.ExcelExport

@code {
    async Task ExportWithExtraSheets()
    {
        var props = new ExcelExportProperties
        {
            Workbook = new Workbook(),
            GridSheetIndex = 0   // Grid data goes to sheet index 0
        };
        props.Workbook.Worksheets.Add(); // extra blank sheet 1
        props.Workbook.Worksheets.Add(); // extra blank sheet 2
        await Grid.ExportToExcelAsync(props);
    }
}
```

## Export as Memory Stream

Pass `asMemoryStream: true` to get a `MemoryStream` instead of a direct browser download, then send bytes via JS interop.

```razor
@inject IJSRuntime JSRuntime

@code {
    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_excelexport")
        {
            MemoryStream stream = await Grid.ExportToExcelAsync(asMemoryStream: true);
            await JSRuntime.InvokeVoidAsync("saveAsFile", "Export.xlsx",
                Convert.ToBase64String(stream.ToArray()));
        }
    }
}
```

**JS helper (`wwwroot/saveAsFile.js`):**
```js
function saveAsFile(filename, bytesBase64) {
    var link = document.createElement('a');
    link.download = filename;
    link.href = "data:application/octet-stream;base64," + bytesBase64;
    document.body.appendChild(link); link.click(); document.body.removeChild(link);
}

