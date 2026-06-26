# Toolbar — Syncfusion Blazor DataGrid

## Table of Contents
- [Built-in Toolbar Items](#built-in-toolbar-items)
- [Custom Toolbar Items](#custom-toolbar-items)
- [Mixed Built-in and Custom Items](#mixed-built-in-and-custom-items)
- [Enable / Disable Toolbar Items Dynamically](#enable--disable-toolbar-items-dynamically)
- [Custom Toolbar Template](#custom-toolbar-template)
- [OnToolbarClick Event](#ontoolbarclick-event)
- [Show Only Icons in Built-in Toolbar Items](#show-only-icons-in-built-in-toolbar-items)
- [Customize Built-in Toolbar Items](#customize-built-in-toolbar-items)
- [Custom Toolbar Items in a Specific Position](#custom-toolbar-items-in-a-specific-position)
- [Custom Items with Same Text as Built-in Items](#custom-items-with-same-text-as-built-in-items)
- [Customize Toolbar Items Tooltip Text](#customize-toolbar-items-tooltip-text)
- [Enable / Disable Toolbar Items Based on Selected Row](#enable--disable-toolbar-items-based-on-selected-row)
- [Customize Toolbar Buttons Using CSS](#customize-toolbar-buttons-using-css)

## Built-in Toolbar Items

Pass a `List<string>` to the `Toolbar` property:

```razor
<SfGrid DataSource="@Orders"
        Toolbar="@(new List<string>{ "Add","Edit","Delete","Update","Cancel" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true">
    </GridEditSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

**All built-in toolbar item strings:**

| Item String | Action |
|---|---|
| `"Add"` | Add new row |
| `"Edit"` | Edit selected row |
| `"Delete"` | Delete selected row |
| `"Update"` | Save current edit |
| `"Cancel"` | Cancel current edit |
| `"Search"` | Show search input |
| `"Print"` | Print the grid |
| `"ExcelExport"` | Export to Excel |
| `"CsvExport"` | Export to CSV |
| `"PdfExport"` | Export to PDF |
| `"ColumnChooser"` | Open column chooser |
| `"Expand"` | Expand all groups |
| `"Collapse"` | Collapse all groups |

## Custom Toolbar Items

Use `ItemModel` objects for custom buttons:

```razor
@using Syncfusion.Blazor.Navigations

<SfGrid DataSource="@Orders" @ref="Grid"
        Toolbar="@ToolbarItems">
    <GridEvents OnToolbarClick="ToolbarClickHandler" TValue="Order"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    List<ItemModel> ToolbarItems = new()
    {
        new ItemModel { Text = "Refresh", TooltipText = "Refresh data", Id = "refresh",
                        PrefixIcon = "e-icons e-refresh" },
        new ItemModel { Text = "Export", TooltipText = "Export to Excel", Id = "export",
                        PrefixIcon = "e-icons e-export-excel" }
    };

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        switch (args.Item.Id)
        {
            case "refresh":
                await Grid.Refresh();
                break;
            case "export":
                await Grid.ExportToExcelAsync();
                break;
        }
    }
}
```

## Mixed Built-in and Custom Items

```razor
<SfGrid DataSource="@Orders"
        Toolbar="@(new List<object>{ "Add","Edit","Delete","Update","Cancel",
            new ItemModel { Text = "Refresh", Id = "refresh" } })">
    <GridEvents OnToolbarClick="OnToolbarClick" TValue="Order"></GridEvents>
    ...
</SfGrid>
```

## Enable / Disable Toolbar Items Dynamically

Built-in items generate IDs as `{GridID}_{ItemName}` (e.g., `Grid_Add`). Custom items use the `Id` you set:

```razor
<SfGrid id="Grid" DataSource="@Orders" @ref="Grid" Toolbar="@ToolbarItems">
    ...
</SfGrid>

@code {
    SfGrid<Order> Grid;
    List<string> ToolbarItems = new() { "Add", "Edit", "Delete" };

    // Disable Edit and Delete
    async Task DisableEditDelete()
    {
        await Grid.EnableToolbarItemsAsync(new List<string> { "Grid_Edit", "Grid_Delete" }, false);
    }

    // Re-enable them
    async Task EnableEditDelete()
    {
        await Grid.EnableToolbarItemsAsync(new List<string> { "Grid_Edit", "Grid_Delete" }, true);
    }
}
```

## Custom Toolbar Template

Replace the entire toolbar with a `ToolbarTemplate`:

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true" @ref="Grid">
    <GridTemplates>
        <ToolbarTemplate>
            <SfToolbar>
                <ToolbarEvents Clicked="ToolbarClickHandler"></ToolbarEvents>
                <ToolbarItems>
                    <ToolbarItem Type="ItemType.Button" Id="expandAll"
                                 Text="Expand All"
                                 PrefixIcon="e-icons e-chevron-down">
                    </ToolbarItem>
                    <ToolbarItem Type="ItemType.Button" Id="collapseAll"
                                 Text="Collapse All"
                                 PrefixIcon="e-icons e-chevron-up">
                    </ToolbarItem>
                </ToolbarItems>
            </SfToolbar>
        </ToolbarTemplate>
    </GridTemplates>
    <GridGroupSettings Columns="@(new string[]{ "CustomerID" })"></GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "expandAll")
            await Grid.ExpandAllGroupAsync();
        else if (args.Item.Id == "collapseAll")
            await Grid.CollapseAllGroupAsync();
    }
}
```

## OnToolbarClick Event

Handle toolbar item clicks (built-in or custom). Prefer checking `args.Item.Id` over `args.Item.Text` for reliability — IDs are stable and unaffected by localization:

```razor
<GridEvents TValue="Order" OnToolbarClick="OnToolbarClick"></GridEvents>

@code {
    async Task OnToolbarClick(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        // Prefer args.Item.Id — stable, not affected by localization
        // args.Item.Text is also available but may vary with locale
        if (args.Item.Id == "Grid_excelexport")
        {
            await Grid.ExportToExcelAsync();
        }
        else if (args.Item.Id == "Grid_pdfexport")
        {
            await Grid.ExportToPdfAsync();
        }
        else if (args.Item.Id == "Grid_csvexport")
        {
            await Grid.ExportToCsvAsync();
        }
    }
}
```

## Show Only Icons in Built-in Toolbar Items

Hide the text label using CSS for a compact toolbar layout. Always set `TooltipText` or `aria-label` for accessibility:

```razor
<SfGrid @ref="Grid" DataSource="@Orders" Toolbar="@(new string[]{ "Add","Edit","Delete","Update","Cancel" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"></GridEditSettings>
    <GridColumns>...</GridColumns>
</SfGrid>

<style>
    .e-grid .e-toolbar .e-tbar-btn-text,
    .e-grid .e-toolbar .e-toolbar-items .e-toolbar-item .e-tbar-btn-text {
        display: none;
    }
</style>
```

## Customize Built-in Toolbar Items

Intercept built-in toolbar actions via `OnToolbarClick`. Set `args.Cancel = true` to prevent the default action and execute custom logic. Use `args.Item.Id` (not `args.Item.Text`) for reliable detection:

```razor
<SfGrid ID="Grid" @ref="Grid" DataSource="@Orders" AllowPaging="true"
        Toolbar="@(new List<string>{ "Add","Edit","Delete","Cancel","Update" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"></GridEditSettings>
    <GridEvents OnToolbarClick="ToolbarClickHandler" TValue="OrderData"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<OrderData> Grid;

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_add")
        {
            args.Cancel = true; // prevent default add action
            var newRecord = new OrderData(10247, "TOMSP", "Hanari Carnes", "Lyon");
            await Grid.AddRecordAsync(newRecord);
        }
    }
}
```

## Custom Toolbar Items in a Specific Position

Use the `Align` property of `ItemModel` to position custom items. Default is `Left`; also supports `Center` and `Right`:

```razor
@using Syncfusion.Blazor.Navigations

<SfGrid DataSource="@Orders" @ref="Grid" AllowGrouping="true"
        Toolbar="@Toolbaritems">
    <GridEvents OnToolbarClick="ToolbarClickHandler" TValue="OrderData"></GridEvents>
    <GridGroupSettings Columns="@(new string[]{ "CustomerID" })"></GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<OrderData> Grid;

    List<object> Toolbaritems = new()
    {
        "Search",
        new ItemModel { Text = "Expand all",  TooltipText = "Expand all",
                        PrefixIcon = "e-expand",  Align = ItemAlign.Left },
        new ItemModel { Text = "Collapse all", TooltipText = "Collapse all",
                        PrefixIcon = "e-collapse", Align = ItemAlign.Right }
    };

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Text == "Expand all")
            await Grid.ExpandAllGroupAsync();
        else if (args.Item.Text == "Collapse all")
            await Grid.CollapseAllGroupAsync();
    }
}
```

## Custom Items with Same Text as Built-in Items

When a custom `ItemModel` has the same `Text` as a built-in item (e.g., `"Add"`, `"Edit"`), the grid may treat it as a built-in item and disable it at unexpected times. Fix: assign unique `Id` values that match the built-in IDs you want to map to, and handle actions manually:

```razor
@using Syncfusion.Blazor.Navigations

<SfGrid @ref="Grid" DataSource="@Orders" AllowPaging="true" Toolbar="@ToolbarItems">
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"></GridEditSettings>
    <GridEvents OnToolbarClick="ToolbarClickHandler" TValue="OrderData"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<OrderData> Grid;

    List<ItemModel> ToolbarItems = new()
    {
        new ItemModel { Text = "Add",    PrefixIcon = "e-add",    Id = "Grid_add" },
        new ItemModel { Text = "Edit",   PrefixIcon = "e-edit",   Id = "Grid_edit" },
        new ItemModel { Text = "Delete", PrefixIcon = "e-delete", Id = "Grid_delete" },
        new ItemModel { Text = "Update", PrefixIcon = "e-update", Id = "Grid_update" },
        new ItemModel { Text = "Cancel", PrefixIcon = "e-cancel", Id = "Grid_cancel" }
    };

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_add")    await Grid.AddRecordAsync();
        if (args.Item.Id == "Grid_edit")   await Grid.StartEditAsync();
        if (args.Item.Id == "Grid_delete") await Grid.DeleteRecordAsync();
        if (args.Item.Id == "Grid_update") await Grid.EndEditAsync();
        if (args.Item.Id == "Grid_cancel") await Grid.CloseEditAsync();
    }
}
```

## Customize Toolbar Items Tooltip Text

Set `ItemModel.TooltipText` to give each toolbar button a descriptive tooltip. Tooltips improve accessibility when icons are shown without text:

```razor
@using Syncfusion.Blazor.Navigations

<SfGrid ID="Grid" @ref="Grid" DataSource="@Orders" AllowPaging="true"
        AllowExcelExport="true" AllowPdfExport="true"
        Toolbar="@ToolbarItems">
    <GridEvents OnToolbarClick="ToolbarClickHandler" TValue="OrderData"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<OrderData> Grid;

    List<object> ToolbarItems = new()
    {
        new ItemModel { Text = "Excel", TooltipText = "Export to Excel",
                        PrefixIcon = "e-excelexport", Id = "Grid_excelexport" },
        new ItemModel { Text = "Pdf",   TooltipText = "Export to PDF",
                        PrefixIcon = "e-pdfexport",   Id = "Grid_pdfexport" },
        new ItemModel { Text = "CSV",   TooltipText = "Export to CSV",
                        PrefixIcon = "e-csvexport",   Id = "Grid_csvexport" }
    };

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_excelexport") await Grid.ExportToExcelAsync();
        else if (args.Item.Id == "Grid_pdfexport")  await Grid.ExportToPdfAsync();
        else if (args.Item.Id == "Grid_csvexport")  await Grid.ExportToCsvAsync();
    }
}
```

## Enable / Disable Toolbar Items Based on Selected Row

Use the `RowSelecting` event with `EnableToolbarItemsAsync` to toggle toolbar items depending on the selected row's data:

```razor
<SfGrid ID="Grid" @ref="Grid" DataSource="@Orders" AllowPaging="true"
        Toolbar="@(new List<string>{ "Add","Edit","Delete","Cancel","Update" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"></GridEditSettings>
    <GridEvents RowSelecting="RowSelectingHandler" TValue="OrderData"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<OrderData> Grid;

    async Task RowSelectingHandler(RowSelectingEventArgs<OrderData> args)
    {
        // Disable Add/Edit/Delete for specific rows
        bool enable = !(args.Data.OrderID == 10249 ||
                        args.Data.OrderID == 10252 ||
                        args.Data.OrderID == 10256);

        await Grid.EnableToolbarItemsAsync(
            new List<string> { "Grid_add", "Grid_edit", "Grid_delete" }, enable);
    }
}
```

## Customize Toolbar Buttons Using CSS

Override built-in toolbar button styles using the `.e-grid .e-toolbar` selectors. Maintain sufficient color contrast and preserve focus indicators for accessibility.

Change the background color of toolbar buttons:

```css
.e-grid .e-toolbar .e-tbar-btn .e-icons,
.e-grid .e-toolbar .e-toolbar-items .e-toolbar-item .e-tbar-btn {
    background: #add8e6;
}
```

Full example:

```razor
<SfGrid DataSource="@Orders" AllowPaging="true"
        Toolbar="@(new string[]{ "Add","Edit","Delete","Update","Cancel" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"></GridEditSettings>
    <GridColumns>...</GridColumns>
</SfGrid>

<style>
    .e-grid .e-toolbar .e-tbar-btn .e-icons,
    .e-grid .e-toolbar .e-toolbar-items .e-toolbar-item .e-tbar-btn {
        background: #add8e6;
    }
</style>
```

> **Tip:** When using CSS isolation, place styles in the component's `.razor.css` file and use the `::deep` selector to target inner elements. Also consider hover, active, focus-visible, and disabled states, plus high-contrast themes for accessibility.
