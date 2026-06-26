# Context Menu — Syncfusion Blazor DataGrid

## Table of Contents
- [Enable Context Menu](#enable-context-menu)
- [Default Context Menu Items](#default-context-menu-items)
- [Custom Context Menu Items](#custom-context-menu-items)
- [Mixed Built-in + Custom Items](#mixed-built-in--custom-items)
- [Sub-menu Items](#sub-menu-items)
- [ContextMenuItemModel Properties](#contextmenuitemmodel-properties)
- [Context Menu Events](#context-menu-events)
- [Disable Context Menu for Specific Columns](#disable-context-menu-for-specific-columns)
- [Enable or Disable Context Menu Items Dynamically](#enable-or-disable-context-menu-items-dynamically)
- [Show or Hide Context Menu Items Dynamically](#show-or-hide-context-menu-items-dynamically)
- [Access Specific Row Details on Context Menu Click](#access-specific-row-details-on-context-menu-click)

## Enable Context Menu

Set `ContextMenuItems` on `SfGrid` with built-in string keys. Requires `AllowSorting`, `AllowGrouping`, `AllowPaging`, export flags, and `GridEditSettings` for the relevant items to appear.

```razor
<SfGrid DataSource="@Orders" AllowSorting="true" AllowPaging="true" AllowGrouping="true"
        AllowExcelExport="true" AllowPdfExport="true" ContextMenuItems="@ContextMenuItems">
    <GridEditSettings AllowEditing="true" AllowDeleting="true"></GridEditSettings>
    ...
</SfGrid>

@code {
    List<object> ContextMenuItems = new()
    {
        "AutoFit", "AutoFitAll", "SortAscending", "SortDescending",
        "Copy", "Edit", "Delete", "Save", "Cancel",
        "PdfExport", "ExcelExport", "CsvExport",
        "FirstPage", "PrevPage", "LastPage", "NextPage", "Group", "Ungroup"
    };
}
```

## Default Context Menu Items

**Header area:**

| Item | Description |
|---|---|
| `"AutoFit"` | Auto-fit current column width |
| `"AutoFitAll"` | Auto-fit all column widths |
| `"Group"` | Group by current column |
| `"Ungroup"` | Remove group on current column |
| `"SortAscending"` | Sort column ascending |
| `"SortDescending"` | Sort column descending |

**Content area:**

| Item | Description |
|---|---|
| `"Edit"` | Edit selected row |
| `"Delete"` | Delete selected row |
| `"Save"` | Save current edit |
| `"Cancel"` | Cancel current edit |
| `"Copy"` | Copy selected rows |
| `"PdfExport"` | Export to PDF |
| `"ExcelExport"` | Export to Excel |
| `"CsvExport"` | Export to CSV |

**Pager area:**

| Item | Description |
|---|---|
| `"FirstPage"` | Go to first page |
| `"PrevPage"` | Go to previous page |
| `"LastPage"` | Go to last page |
| `"NextPage"` | Go to next page |

## Custom Context Menu Items

```razor
<SfGrid @ref="Grid" DataSource="@Employees" AllowPaging="true"
        ContextMenuItems="@CustomMenuItems">
    <GridEvents ContextMenuItemClicked="OnContextMenuClick" TValue="Employee"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Employee> Grid;

    List<ContextMenuItemModel> CustomMenuItems = new()
    {
        new ContextMenuItemModel
        {
            Text = "Copy with headers",
            Target = ".e-content",
            Id = "copywithheader"
        }
    };

    async Task OnContextMenuClick(ContextMenuClickEventArgs<Employee> args)
    {
        if (args.Item.Id == "copywithheader")
        {
            await Grid.CopyAsync(true); // copy with headers
        }
    }
}
```

## Mixed Built-in + Custom Items

```razor
<SfGrid DataSource="@Orders"
        ContextMenuItems="@(new List<object>
        {
            "Copy",
            new ContextMenuItemModel { Text = "Copy with headers", Target = ".e-content", Id = "copywithheader" }
        })">
    <GridEvents ContextMenuItemClicked="OnContextMenuClick" TValue="Order"></GridEvents>
    ...
</SfGrid>
```

## Sub-menu Items

Sub-items must use `List<Syncfusion.Blazor.Navigations.MenuItem>` (not `List<ContextMenuItemModel>`) for the `Items` property.

```razor
@code {
    List<ContextMenuItemModel> ContextMenuItems = new()
    {
        new ContextMenuItemModel
        {
            Text = "Clipboard", Target = ".e-content", Id = "clipboard",
            Items = new List<Syncfusion.Blazor.Navigations.MenuItem>
            {
                new Syncfusion.Blazor.Navigations.MenuItem { Text = "Copy", Id = "copy" },
                new Syncfusion.Blazor.Navigations.MenuItem { Text = "Copy With Header", Id = "copywithheader" }
            }
        }
    };

    async Task OnContextMenuClick(ContextMenuClickEventArgs<OrderData> args)
    {
        if (args.Item.Id == "copy") await Grid.CopyAsync(false);
        else if (args.Item.Id == "copywithheader") await Grid.CopyAsync(true);
    }
}
```

## ContextMenuItemModel Properties

| Property | Type | Description |
|---|---|---|
| `Text` | `string` | Display text of the menu item |
| `Id` | `string` | Unique identifier for handling clicks |
| `Target` | `string` | CSS selector for where the item appears (`.e-headercell`, `.e-content`, `.e-pager`) |
| `IconCss` | `string` | CSS icon class |
| `Items` | `List<Syncfusion.Blazor.Navigations.MenuItem>` | Sub-menu items (use `MenuItem`, not `ContextMenuItemModel`) |
| `Disabled` | `bool` | Disables the menu item so it cannot be clicked |
| `Hidden` | `bool` | Hides the menu item from view |

## Context Menu Events

| Event | Args Type | Description |
|---|---|---|
| `ContextMenuItemClicked` | `ContextMenuClickEventArgs<T>` | Fires when a context menu item is clicked; use `args.Item.Id` and `args.RowInfo.RowData` |
| `ContextMenuOpen` | `ContextMenuOpenEventArgs<T>` | Fires before context menu opens; use `args.Cancel`, `args.Column.Field`, `args.ContextMenu.Items` |

### ContextMenuOpenEventArgs key members

| Member | Description |
|---|---|
| `args.Cancel` | Set to `true` to prevent the context menu from opening |
| `args.Column.Field` | The field name of the column where right-click occurred |
| `args.ContextMenu.Items` | Collection of menu items; set `item.Disabled` or `item.Hidden` per item |

### ContextMenuClickEventArgs key members

| Member | Description |
|---|---|
| `args.Item.Id` | The `Id` of the clicked menu item |
| `args.RowInfo.RowData` | The full data object of the row that was right-clicked |

## Disable Context Menu for Specific Columns

Use the `ContextMenuOpen` event and set `args.Cancel = true` to prevent the context menu from opening on a particular column.

```razor
@code {
    void OnContextMenuOpen(ContextMenuOpenEventArgs<OrderData> args)
    {
        if (args.Column.Field == "Freight")
            args.Cancel = true; // suppress context menu for this column
    }
}
```

## Enable or Disable Context Menu Items Dynamically

Use `args.ContextMenu.Items` inside `ContextMenuOpen` to set `item.Disabled = true/false` per column or row condition.

```razor
@code {
    // Disable "Copy" only when right-clicking the ShipCity column
    void OnContextMenuOpen(ContextMenuOpenEventArgs<OrderData> args)
    {
        foreach (var item in args.ContextMenu.Items)
        {
            item.Disabled = item.Text == "Copy" && args.Column.Field == nameof(OrderData.ShipCity);
        }
    }
}
```

## Show or Hide Context Menu Items Dynamically

Use `item.Hidden = true/false` inside `ContextMenuOpen` to show or hide individual items.

> **Note:** The display text for the built-in `"Edit"` item is `"Edit Record"` at runtime. Use `item.Text == "Edit Record"` when matching by text inside `ContextMenuOpen`.

```razor
@code {
    // Hide "Edit Record" item when right-clicking the CustomerID column
    void OnContextMenuOpen(ContextMenuOpenEventArgs<OrderData> args)
    {
        foreach (var item in args.ContextMenu.Items)
        {
            if (item.Text == "Edit Record" && args.Column.Field == nameof(OrderData.CustomerID))
                item.Hidden = true;
        }
    }
}
```

## Access Specific Row Details on Context Menu Click

Use `args.RowInfo.RowData` in the `ContextMenuItemClicked` event to retrieve the full data object of the right-clicked row.

```razor
@code {
    OrderData selectedRow;

    void OnContextMenuClick(ContextMenuClickEventArgs<OrderData> args)
    {
        if (args.Item.Id == "fetchdata")
            selectedRow = args.RowInfo.RowData; // full row object
    }
}

