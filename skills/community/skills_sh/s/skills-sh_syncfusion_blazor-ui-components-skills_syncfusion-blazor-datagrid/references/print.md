# Print — Syncfusion Blazor DataGrid

## Table of Contents
- [Toolbar Print Button](#toolbar-print-button)
- [Programmatic Print](#programmatic-print)
- [PrintMode — Control Which Pages Are Printed](#printmode--control-which-pages-are-printed)
- [Print Behavior](#print-behavior)
- [Printing a Large Number of Columns](#printing-a-large-number-of-columns)
- [BeforePrint / AfterPrint Events](#beforeprint--afterprint-events)
- [Limitations of Printing Large Data](#limitations-of-printing-large-data)

## Toolbar Print Button

Add `"Print"` to the toolbar:

```razor
<SfGrid DataSource="@Orders" Toolbar="@(new List<string>{ "Print" })">
    <GridColumns>...</GridColumns>
</SfGrid>
```

Clicking **Print** opens the browser's print dialog with the current grid state (visible columns, sorting, filtering applied).

## Programmatic Print

Trigger print from external UI:

```razor
<SfButton OnClick="PrintGrid">Print Grid</SfButton>
<SfGrid @ref="Grid" DataSource="@Orders">
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    async Task PrintGrid()
    {
        await Grid.PrintAsync();
    }
}
```

## PrintMode — Control Which Pages Are Printed

Use the `PrintMode` property to control whether all pages or only the current page are printed.

| Value | Behavior |
|---|---|
| `PrintMode.AllPages` | Prints the entire dataset across all pages (**default**) |
| `PrintMode.CurrentPage` | Prints only the data visible on the current page |

```razor
<SfGrid DataSource="@Orders" Toolbar="@(new List<string>{ "Print" })"
        PrintMode="PrintMode.CurrentPage" AllowPaging="true">
    <GridPageSettings PageSize="6"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

> `PrintMode.CurrentPage` requires `AllowPaging="true"` to be effective.

## Print Behavior

- Reflects the grid's **current state** — visible columns, applied filters, sort order
- Hidden columns are excluded from the print output
- Page setup (paper size, margins, headers, footers, scaling) is controlled by the **browser's print dialog**, not the application
- Browser-specific print settings:
  - Chrome: `chrome://settings/print`
  - Firefox: File → Print → Page Setup
  - Safari: File → Print → Show Details

## Printing a Large Number of Columns

When the grid has many columns, the browser's default page size (e.g. A4) may not be wide enough to show all of them. Some columns may be cut off in the print preview or output.

To fit all columns in the printed output:
- Switch to **landscape orientation** in the browser's print dialog.
- Reduce the **scale** setting to shrink content, fitting more columns per page.

These adjustments are made in the browser's print dialog — they cannot be configured through application code.

## BeforePrint / AfterPrint Events

```razor
<GridEvents TValue="Order"
            BeforePrint="OnBeforePrint"
            PrintComplete="OnPrintComplete">
</GridEvents>

@code {
    void OnBeforePrint(PrintEventArgs args)
    {
        // Customize before print dialog opens
        // args.Cancel = true; to cancel
    }

    void OnPrintComplete(object args)
    {
        // After print completes
    }
}
```

## Limitations of Printing Large Data

Printing large volumes of data in a single page can cause **browser performance issues** — the page may slow down or become unresponsive.

- The DataGrid uses **virtualization** for on-screen rendering to handle large datasets efficiently.
- Virtualization is **not applied during printing** — all rows and columns are rendered at once, increasing browser load.

**Recommended alternative for large datasets**: Export to a file format and print using a desktop application, which offers better layout control and performance:

| Format | Feature |
|---|---|
| Excel / CSV | Spreadsheet applications handle large data efficiently |
| PDF | Full layout control, suitable for large column grids |

> The printed output always reflects the grid's **current state** — visible columns, applied sort order, and active filters at the time printing is initiated.