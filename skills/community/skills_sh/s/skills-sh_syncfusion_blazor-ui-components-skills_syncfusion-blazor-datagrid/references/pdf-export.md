# PDF Export — Syncfusion Blazor DataGrid

## Table of Contents
- [Enable and Trigger Export](#enable-and-trigger-export)
- [PdfExportProperties](#pdfexportproperties)
- [Export Current Page Only](#export-current-page-only)
- [Export Selected Records](#export-selected-records)
- [Export Filtered Records](#export-filtered-records)
- [Export with Custom Data Source](#export-with-custom-data-source)
- [Export with Custom Aggregate](#export-with-custom-aggregate)
- [Export with Custom Date Format](#export-with-custom-date-format)
- [Page Settings](#page-settings)
- [Customize Columns on Export](#customize-columns-on-export)
- [Enable Horizontal Overflow](#enable-horizontal-overflow)
- [Add Header and Footer](#add-header-and-footer)
- [Apply Theme](#apply-theme)
- [Show Spinner During Export](#show-spinner-during-export)
- [Export as Memory Stream](#export-as-memory-stream)
- [PDF Export Events](#pdf-export-events)

## Enable and Trigger Export

```razor
<SfGrid ID="Grid" @ref="Grid" DataSource="@Orders" AllowPdfExport="true"
        Toolbar="@(new List<string>{ "PdfExport" })">
    <GridEvents OnToolbarClick="ToolbarClickHandler" TValue="Order"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_pdfexport")  // Grid ID + itemname
            await Grid.ExportToPdfAsync();
    }
}
```

## PdfExportProperties

```razor
@code {
    async Task ExportToPdf()
    {
        var props = new PdfExportProperties
        {
            FileName = "Orders.pdf",
            ExportType = ExportType.AllPages,     // or ExportType.CurrentPage
            IncludeHiddenColumn = true
        };
        await Grid.ExportToPdfAsync(props);
    }
}
```

| Property | Description |
|---|---|
| `FileName` | Output file name |
| `ExportType` | `AllPages` or `CurrentPage` |
| `IncludeHiddenColumn` | Include hidden columns |
| `DataSource` | Custom data source for export |
| `Query` | Filter rows via Query |
| `PageOrientation` | `Portrait` or `Landscape` |
| `PageSize` | PDF page size (e.g., `PdfPageSize.A4`) |
| `AllowHorizontalOverflow` | Fit all columns on a single page without wrapping |
| `DisableAutoFitWidth` | Disable auto column width fitting; use with `Columns` to set explicit widths |
| `Columns` | List of `GridColumn` objects to override exported columns/headers |
| `Theme` | Apply font, color, and border styling via `PdfTheme` |
| `IsRepeatHeader` | Repeat column headers on each page of the exported PDF |

## Export Current Page Only

```razor
var props = new PdfExportProperties
{
    ExportType = ExportType.CurrentPage
};
await Grid.ExportToPdfAsync(props);
```

## Export Selected Records

```razor
var selected = await Grid.GetSelectedRecordsAsync();
var props = new PdfExportProperties { DataSource = selected };
await Grid.ExportToPdfAsync(props);
```

## Export Filtered Records

Retrieve active filter results using `GetFilteredRecordsAsync()` and pass as `DataSource`.

```razor
<SfGrid ID="Grid" @ref="Grid" DataSource="@Orders" AllowFiltering="true"
        AllowPdfExport="true" Toolbar="@(new List<string>() { "PdfExport" })">
    <GridEvents OnToolbarClick="ToolbarClickHandler" TValue="OrderData"></GridEvents>
</SfGrid>

@code {
    SfGrid<OrderData> Grid;

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_pdfexport")
        {
            var filteredRecords = await Grid.GetFilteredRecordsAsync();
            var props = new PdfExportProperties { DataSource = filteredRecords };
            await Grid.ExportToPdfAsync(props);
        }
    }
}
```

## Export with Custom Data Source

```razor
var filtered = Orders.Where(o => o.Freight > 100).ToList();
var props = new PdfExportProperties { DataSource = filtered };
await Grid.ExportToPdfAsync(props);
```

## Export with Custom Aggregate

Set `Type="AggregateType.Custom"` on the aggregate column and handle the `PdfAggregateTemplateInfo` event to inject calculated values into the exported PDF.

```razor
<SfGrid ID="Grid" @ref="Grid" DataSource="@Orders" AllowPdfExport="true"
        Toolbar="@(new List<string>() { "PdfExport" })">
    <GridEvents TValue="OrderDetails"
                OnToolbarClick="ToolbarClickHandler"
                PdfAggregateTemplateInfo="PdfAggregateTemplateInfoHandler">
    </GridEvents>
    <GridAggregates>
        <GridAggregate>
            <GridAggregateColumns>
                <GridAggregateColumn Field="Freight" Type="AggregateType.Custom">
                    <FooterTemplate>Custom Total</FooterTemplate>
                </GridAggregateColumn>
            </GridAggregateColumns>
        </GridAggregate>
    </GridAggregates>
</SfGrid>

@code {
    SfGrid<OrderDetails> Grid;

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_pdfexport")
            await Grid.ExportToPdfAsync();
    }

    void PdfAggregateTemplateInfoHandler(PdfAggregateEventArgs args)
    {
        // Inject the custom calculated value into the exported PDF
        args.Value = Orders.Sum(o => o.Freight).ToString("C2");
    }
}
```

## Export with Custom Date Format

Apply a .NET date format string via the column's `Format` property. The format is respected during PDF export.

```razor
<GridColumn Field="OrderDate" HeaderText="Order Date"
            Format="dd/MM/yyyy" Type="ColumnType.Date"
            TextAlign="TextAlign.Right" Width="130" />
```

## Page Settings

```razor
var props = new PdfExportProperties
{
    PageOrientation = PageOrientation.Landscape,
    PageSize = PdfPageSize.A4,
    FileName = "landscape-report.pdf"
};
await Grid.ExportToPdfAsync(props);
```

## Customize Columns on Export

Override which columns appear in the PDF by providing a `List<GridColumn>` to `PdfExportProperties.Columns`. Use `DisableAutoFitWidth = true` to apply explicit column widths.

```razor
@code {
    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_pdfexport")
        {
            var exportColumns = new List<GridColumn>
            {
                new GridColumn { Field = "OrderID",    HeaderText = "Order Number",   TextAlign = TextAlign.Left },
                new GridColumn { Field = "CustomerID", HeaderText = "Customer Name",  TextAlign = TextAlign.Left },
                new GridColumn { Field = "Freight",    HeaderText = "Freight Amount", Format = "C2",
                                 TextAlign = TextAlign.Center, Width = "120" }
            };

            var props = new PdfExportProperties
            {
                Columns = exportColumns,
                DisableAutoFitWidth = true   // honour explicit Width values above
            };
            await Grid.ExportToPdfAsync(props);
        }
    }
}
```

## Enable Horizontal Overflow

Forces all columns onto a single page width instead of wrapping to a new page.

```razor
var props = new PdfExportProperties { AllowHorizontalOverflow = true };
await Grid.ExportToPdfAsync(props);
```

## Add Header and Footer

```razor
var props = new PdfExportProperties
{
    Header = new PdfHeader
    {
        FromTop = 0,
        Height = 130,
        Contents = new List<PdfHeaderFooterContent>
        {
            new PdfHeaderFooterContent
            {
                Type = ContentType.Text,
                Value = "Order Report",
                Position = new PdfPosition { X = 280, Y = 0 },
                Style = new PdfContentStyle { TextBrushColor = "#000000", FontSize = 16 }
            }
        }
    },
    Footer = new PdfFooter
    {
        FromBottom = 160,
        Height = 150,
        Contents = new List<PdfHeaderFooterContent>
        {
            new PdfHeaderFooterContent
            {
                Type = ContentType.PageNumber,
                PageNumberType = PdfPageNumberType.Arabic,
                Format = "Page {$current} of {$total}",
                Position = new PdfPosition { X = 0, Y = 25 },
                Style = new PdfContentStyle { TextBrushColor = "#0078d4", FontSize = 12 }
            }
        }
    }
};
await Grid.ExportToPdfAsync(props);
```

## Apply Theme

```razor
var props = new PdfExportProperties
{
    Theme = new PdfTheme
    {
        Header = new PdfThemeStyle
        {
            FontColor = "#ffffff",
            FontName = "Calibri",
            FontSize = 10,
            Bold = true,
            BackgroundColor = "#0078d4"
        },
        Record = new PdfThemeStyle
        {
            FontColor = "#333333",
            FontSize = 9
        },
        Caption = new PdfThemeStyle
        {
            FontColor = "#0078d4",
            Bold = true,
            FontSize = 10
        }
    }
};
await Grid.ExportToPdfAsync(props);
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
        if (args.Item.Id == "Grid_pdfexport")
        {
            await Grid.ShowSpinnerAsync();
            await Grid.ExportToPdfAsync();
        }
    }

    async Task OnExportComplete(object args)
    {
        await Grid.HideSpinnerAsync();
    }
}
```

## Export as Memory Stream

Pass `asMemoryStream: true` to receive a `MemoryStream` instead of triggering a direct browser download. Use JavaScript interop to download, or write to a `FileStream` on the server.

```razor
@inject IJSRuntime JSRuntime

@code {
    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_pdfexport")
        {
            // Returns MemoryStream instead of auto-downloading
            MemoryStream stream = await Grid.ExportToPdfAsync(asMemoryStream: true);

            // Trigger browser download via JS interop
            await JSRuntime.InvokeVoidAsync("saveAsFile",
                "Export.pdf", Convert.ToBase64String(stream.ToArray()), true);
        }
    }
}
```

**JavaScript helper** (`wwwroot/saveAsFile.js`):

```js
function saveAsFile(filename, bytesBase64) {
    var link = document.createElement('a');
    link.download = filename;
    link.href = "data:application/octet-stream;base64," + bytesBase64;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
```

### Merge Two PDF Memory Streams

Export two streams and combine them into one PDF using `PdfDocument.Merge`.

```razor
@code {
    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_pdfexport")
        {
            var finalDoc    = new Syncfusion.Pdf.PdfDocument();
            var stream1     = await Grid.ExportToPdfAsync(asMemoryStream: true);
            var stream2     = await Grid.ExportToPdfAsync(asMemoryStream: true, customProps);

            Stream[] streams = { new MemoryStream(stream1.ToArray()),
                                  new MemoryStream(stream2.ToArray()) };
            Syncfusion.Pdf.PdfDocument.Merge(finalDoc, streams);

            var merged = new MemoryStream();
            finalDoc.Save(merged);
            await JSRuntime.InvokeVoidAsync("saveAsFile",
                "Merged.pdf", Convert.ToBase64String(merged.ToArray()), true);
        }
    }
}
```

## PDF Export Events

| Event | Description |
|---|---|
| `PdfExportInit` | Fires before PDF export begins |
| `PdfQueryCellInfo` | Fires per cell during export; customize value/style |
| `PdfHeaderQueryCellInfo` | Fires per header cell during export |
| `PdfHeaderQueryCellInfoEvent` | Fires per header cell; also used to adjust header row height (e.g., for rotated text) |
| `PdfAggregateQueryCellInfo` | Fires per aggregate cell |
| `PdfAggregateTemplateInfo` | Fires for custom-type aggregate columns; inject calculated value into exported PDF |
| `ExportComplete` | Fires after export is complete; use to hide spinner or reset query |
