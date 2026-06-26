# Export and Print in Blazor Diagram

---

## Export

The diagram can be exported as JPEG, PNG, SVG, or PDF.

### Basic Export (Download File)

```csharp
private SfDiagramComponent _diagram;

private async Task ExportAsPng()
{
    DiagramExportSettings settings = new DiagramExportSettings();
    // Downloads "diagram.png" to the user's machine
    await _diagram.ExportAsync("diagram", DiagramExportFormat.PNG, settings);
}
```

### Export as Base64 String (for PDF or custom handling)

```csharp
private async Task ExportAsBase64()
{
    DiagramExportSettings settings = new DiagramExportSettings();
    string[] pages = await _diagram.ExportAsync(DiagramExportFormat.PNG, settings);
    // pages[0] is a base64-encoded image string
}
```

---

## Export Format Options

| Format | `DiagramExportFormat` value |
|--------|----------------------------|
| JPEG | `DiagramExportFormat.JPEG` |
| PNG | `DiagramExportFormat.PNG` |
| SVG | `DiagramExportFormat.SVG` |
| PDF | Export as base64 then convert (see below) |

---

## DiagramExportSettings Properties

| Property | Type | Description |
|----------|------|-------------|
| `Region` | `DiagramPrintExportRegion` | Area to export: `PageSettings`, `Content`, or `ClipBounds` |
| `PageWidth` | `double` | Output width in pixels (default 1123) |
| `PageHeight` | `double` | Output height in pixels (default 794) |
| `Margin` | `DiagramThickness` | Margin around exported content |
| `FitToPage` | `bool` | `true` = single page; `false` = multiple pages |
| `Orientation` | `PageOrientation` | `Landscape` (default) or `Portrait` |
| `ClipBounds` | `DiagramRect` | Custom clip region (only with `Region = ClipBounds`) |

### Export a Specific Region

```csharp
private async Task ExportRegion()
{
    var settings = new DiagramExportSettings
    {
        Region = DiagramPrintExportRegion.ClipBounds,
        ClipBounds = new DiagramRect { X = 0, Y = 0, Width = 500, Height = 400 },
        Margin = new DiagramThickness { Left = 10, Top = 10, Right = 10, Bottom = 10 }
    };
    await _diagram.ExportAsync("region", DiagramExportFormat.PNG, settings);
}
```

### Fit All Content to Single Page

```csharp
var settings = new DiagramExportSettings
{
    Region = DiagramPrintExportRegion.Content,
    FitToPage = true,
    Orientation = PageOrientation.Landscape
};
await _diagram.ExportAsync("full-diagram", DiagramExportFormat.PNG, settings);
```

---

## Export to PDF

The diagram has no built-in PDF export, but you can:
1. Export to base64 PNG
2. Use `Syncfusion.PdfExport` to create a PDF document
3. Download via JS interop

```csharp
@using Syncfusion.PdfExport
@inject IJSRuntime JS

private async Task ExportAsPdf()
{
    var exportSettings = new DiagramExportSettings
    {
        Region = DiagramPrintExportRegion.Content,
        FitToPage = true,
        Orientation = PageOrientation.Landscape
    };

    // Get base64 image pages
    string[] images = await _diagram.ExportAsync(DiagramExportFormat.PNG, exportSettings);

    // Build PDF
    PdfDocument doc = new PdfDocument();
    doc.PageSettings.Orientation = PdfPageOrientation.Landscape;
    doc.PageSettings.Margins = new PdfMargins { Left = 0, Right = 0, Top = 0, Bottom = 0 };

    foreach (string base64 in images)
    {
        using var stream = new MemoryStream(Convert.FromBase64String(base64.Split("base64,")[1]));
        PdfPage page = doc.Pages.Add();
        PdfBitmap img = new PdfBitmap(stream);
        page.Graphics.DrawImage(img, 0, 0);
    }

    using var ms = new MemoryStream();
    doc.Save(ms);
    string pdfBase64 = Convert.ToBase64String(ms.ToArray());
    await JS.InvokeAsync<string>("downloadPdf", pdfBase64, "diagram");
    doc.Dispose();
}
```

**Required NuGet:** `Syncfusion.PdfExport.Net.Core`

---

## Print

### Basic Print

```csharp
private async Task PrintDiagram()
{
    DiagramPrintSettings print = new DiagramPrintSettings
    {
        Region = DiagramPrintExportRegion.PageSettings,
        FitToPage = true,
        Orientation = PageOrientation.Portrait,
        Margin = new DiagramThickness { Left = 10, Top = 10, Right = 10, Bottom = 10 }
    };
    await _diagram.PrintAsync(print);
}
```

### DiagramPrintSettings Properties

`DiagramPrintSettings` has the same properties as `DiagramExportSettings`:

| Property | Description |
|----------|-------------|
| `Region` | `PageSettings`, `Content`, or `ClipBounds` |
| `PageWidth` / `PageHeight` | Page dimensions |
| `Margin` | Margin around printed content |
| `FitToPage` | Single vs. multiple pages |
| `Orientation` | `Portrait` or `Landscape` |
| `ClipBounds` | Custom print region |

### Print a Specific Region (ClipBounds)

```csharp
var print = new DiagramPrintSettings
{
    Region = DiagramPrintExportRegion.ClipBounds,
    ClipBounds = new DiagramRect { X = 300, Y = 200, Width = 500, Height = 300 },
    Orientation = PageOrientation.Landscape
};
await _diagram.PrintAsync(print);
```

---

## PageSettings Component

Configure the visible page area in the diagram canvas:

```razor
<SfDiagramComponent>
    <PageSettings Width="816" Height="1054"
                  MultiplePage="true"
                  Orientation="PageOrientation.Portrait"
                  ShowPageBreaks="true">
        <PageMargin Left="10" Right="10" Top="10" Bottom="10" />
    </PageSettings>
</SfDiagramComponent>
```

---

## Common Gotchas

- **No built-in PDF export** — must use `Syncfusion.PdfExport` NuGet and JS interop to download the PDF
- **`ExportAsync` with 2 args returns `string[]`** (base64 per page); **with 3 args triggers a file download** (returns void)
- **`Region = ClipBounds`** requires `ClipBounds` to be set — otherwise the export is empty
- **HTML/Native nodes** are not rendered to image during export — use a server-side rendering workaround for those shapes
- **Page margins in the browser print dialog** may override `DiagramPrintSettings.Margin` — instruct users to set margins in the browser Page Setup dialog
- **SVG export** preserves vector quality but may not render all CSS-styled shapes perfectly
