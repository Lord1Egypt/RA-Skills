# Clipboard, AutoFill & Paste — Syncfusion Blazor DataGrid

## Table of Contents
- [Overview](#overview)
- [Clipboard — Copy Selected Rows or Cells](#clipboard--copy-selected-rows-or-cells)
- [Programmatic Copy via External Button](#programmatic-copy-via-external-button)
- [AutoFill](#autofill)
- [AutoFill Limitations](#autofill-limitations)
- [Paste](#paste)
- [Paste Limitations](#paste-limitations)

## Overview

The clipboard feature allows copying selected rows or cells to the clipboard using keyboard shortcuts or programmatic methods. AutoFill lets users drag a handle to fill adjacent cells. Paste lets users copy cells and paste them to a different range within the grid.

---

## Clipboard — Copy Selected Rows or Cells

Enable selection and focus the grid to use keyboard shortcuts:

| Windows | Mac | Action |
|---|---|---|
| `Ctrl + C` | `Command + C` | Copy selected rows or cells |
| `Ctrl + Shift + H` | `Command + Shift + H` | Copy with column headers |

If `Mode` is `Row`, entire rows are copied. If `Mode` is `Cell`, only highlighted cells are copied.

```razor
<SfGrid DataSource="@Orders" Height="348">
    <GridSelectionSettings Type="SelectionType.Multiple"></GridSelectionSettings>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true" Width="120" />
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="150" />
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="150" />
        <GridColumn Field="ShipName" HeaderText="Ship Name" Width="150" />
    </GridColumns>
</SfGrid>
```

## Programmatic Copy via External Button

Use `CopyAsync()` to trigger clipboard copy programmatically:

```razor
<SfButton OnClick="Copy">Copy</SfButton>
<SfButton OnClick="CopyHeader">Copy With Header</SfButton>

<SfGrid @ref="Grid" DataSource="@Orders" Height="348">
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    async Task Copy() => await Grid.CopyAsync();

    // Pass true to include column headers in copied content
    async Task CopyHeader() => await Grid.CopyAsync(true);
}
```

---

## AutoFill

AutoFill lets users copy values from selected cells and drag a handle to fill adjacent cells.

**Requirements:**
- `EnableAutoFill="true"` on the grid
- Cell selection: `Mode="SelectionMode.Cell"`, `CellSelectionMode="CellSelectionMode.Box"`, `Type="SelectionType.Multiple"`
- Batch editing enabled: `Mode="EditMode.Batch"`

```razor
<SfGrid DataSource="@Orders" EnableAutoFill="true" AllowSelection="true"
        Toolbar="@(new List<string> { "Add", "Update", "Cancel" })" Height="348">
    <GridSelectionSettings CellSelectionMode="CellSelectionMode.Box"
                           Mode="SelectionMode.Cell"
                           Type="SelectionType.Multiple">
    </GridSelectionSettings>
    <GridEditSettings AllowAdding="true" AllowDeleting="true"
                      AllowEditing="true" Mode="EditMode.Batch">
    </GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID" IsPrimaryKey="true" Width="120" />
        <GridColumn Field="CustomerID" Width="150" />
        <GridColumn Field="ShipCity" Width="150" />
    </GridColumns>
</SfGrid>
```

**Usage:**
1. Select the source cells.
2. Hover over the bottom-right corner to reveal the autofill handle.
3. Drag the handle to the target cells and release.

### AutoFill Limitations

| Limitation | Detail |
|---|---|
| Data type conversion | Strings into numeric/date cells produce `NaN` or empty |
| Sequential series | Copies values directly — no series generation |
| Virtualization | Not supported with virtual or column virtualization |
| Infinite scrolling | Only applies to cells within the current viewport |

> AutoFill is not compatible with `AllowDragSelection`.

---

## Paste

Paste copies selected cells to a new range using `Ctrl + C` / `Ctrl + V`.

**Requirements:** Same as AutoFill — cell selection with Box mode and Batch editing.

```razor
<SfGrid DataSource="@Orders" EnableAutoFill="true" AllowSelection="true"
        Toolbar="@(new List<string> { "Add", "Update", "Cancel" })" Height="348">
    <GridSelectionSettings CellSelectionMode="CellSelectionMode.Box"
                           Mode="SelectionMode.Cell"
                           Type="SelectionType.Multiple">
    </GridSelectionSettings>
    <GridEditSettings AllowAdding="true" AllowDeleting="true"
                      AllowEditing="true" Mode="EditMode.Batch">
    </GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID" IsPrimaryKey="true" Visible="false" Width="120" />
        <GridColumn Field="CustomerID" Width="150" />
        <GridColumn Field="ShipCity" Width="150" />
    </GridColumns>
</SfGrid>
```

**Steps:**
1. Select cells to copy → `Ctrl + C`
2. Select target cells → `Ctrl + V`

### Paste Limitations

- Pasting strings into numeric cells results in `NaN`; into date cells results in an empty cell.
- Ensure pasted values are compatible with the target column's data type.
