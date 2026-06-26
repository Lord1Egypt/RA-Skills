# Adaptive UI Layout

## Table of Contents
- [Overview](#overview)
- [Render Adaptive Dialogs](#render-adaptive-dialogs)
- [Vertical Row Rendering](#vertical-row-rendering)
- [Limit Adaptive Layout to Mobile Only](#limit-adaptive-layout-to-mobile-only)
- [Supported Features in Vertical Mode](#supported-features-in-vertical-mode)
- [Key Properties](#key-properties)

## Overview

The Syncfusion Blazor DataGrid includes an adaptive UI designed for small screens. When `EnableAdaptiveUI="true"`, the grid renders filter, sort, column chooser, column menu, and edit dialogs in a full-screen mobile-friendly layout. Rows can optionally render vertically for improved readability on narrow viewports.

**When to use this reference:**
- Building mobile-responsive Blazor apps with DataGrid
- Rendering filter/sort/edit dialogs in full-screen on small devices
- Switching row layout to vertical mode for narrow screens
- Limiting adaptive behavior to mobile screen sizes only

## Render Adaptive Dialogs

Set `EnableAdaptiveUI="true"` to activate mobile-optimized full-screen dialogs for filter, sort, and edit operations:

```razor
@using Syncfusion.Blazor.Grids

<div class="content-wrapper e-bigger e-adaptive-demo">
    <div class="e-mobile-layout">
        <div class="e-mobile-content">
            <SfGrid DataSource="@AdaptiveData"
                    AllowPaging="true"
                    AllowSorting="true"
                    AllowFiltering="true"
                    EnableAdaptiveUI="true"
                    Toolbar="@(new List<string>() { "Add", "Edit", "Delete", "Cancel", "Update", "Search" })"
                    Height="100%">
                <GridFilterSettings Type="FilterType.Excel"></GridFilterSettings>
                <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"
                                  Mode="EditMode.Dialog"></GridEditSettings>
                <GridColumns>
                    <GridColumn Field="SNO" HeaderText="S NO" IsPrimaryKey="true" Width="150"
                                ValidationRules="@(new ValidationRules{ Required=true })"></GridColumn>
                    <GridColumn Field="Model" HeaderText="Model" Width="200"
                                ValidationRules="@(new ValidationRules{ Required=true })"></GridColumn>
                    <GridColumn Field="Developer" HeaderText="Developer" Width="200"></GridColumn>
                    <GridColumn Field="ReleaseDate" HeaderText="Released Date"
                                EditType="EditType.DatePickerEdit" Format="yyyyMMM" Width="200"></GridColumn>
                    <GridColumn Field="AndroidVersion" HeaderText="Android Version" Width="200"></GridColumn>
                </GridColumns>
            </SfGrid>
        </div>
    </div>
</div>

@code {
    public List<AdaptiveDetails> AdaptiveData { get; set; }

    protected override void OnInitialized()
    {
        AdaptiveData = AdaptiveDetails.GetAllModels();
    }
}
```

> Use `EditMode.Dialog` with `EnableAdaptiveUI` so edit forms render as full-screen dialogs on mobile.

## Vertical Row Rendering

Set `RowRenderingMode="RowDirection.Vertical"` to display each row's fields stacked vertically. This improves data readability on narrow screens.

> `EnableAdaptiveUI="true"` must be set for vertical row rendering to work. The default is `RowDirection.Horizontal`.

```razor
@using Syncfusion.Blazor.Grids
@using Syncfusion.Blazor.DropDowns

<SfDropDownList TValue="RowDirection" TItem="DropDownOrder" DataSource="@DropDownValue" Width="120px">
    <DropDownListFieldSettings Text="Text" Value="Value"></DropDownListFieldSettings>
    <DropDownListEvents ValueChange="OnChange" TValue="RowDirection" TItem="DropDownOrder"></DropDownListEvents>
</SfDropDownList>

<SfGrid @ref="Grid"
        DataSource="@AdaptiveData"
        AllowPaging="true"
        AllowSorting="true"
        AllowFiltering="true"
        EnableAdaptiveUI="true"
        RowRenderingMode="@RowDirectionValue"
        Toolbar="@(new List<string>() { "Add", "Edit", "Delete", "Cancel", "Update", "Search" })"
        Height="100%">
    <GridFilterSettings Type="FilterType.Excel"></GridFilterSettings>
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"
                      Mode="EditMode.Dialog"></GridEditSettings>
    <GridColumns>
        <GridColumn Field="SNO" HeaderText="S NO" IsPrimaryKey="true" Width="150"></GridColumn>
        <GridColumn Field="Model" HeaderText="Model" Width="200"></GridColumn>
        <GridColumn Field="Developer" HeaderText="Developer" Width="200"></GridColumn>
        <GridColumn Field="ReleaseDate" HeaderText="Released Date"
                    EditType="EditType.DatePickerEdit" Format="yyyyMMM" Width="200"></GridColumn>
        <GridColumn Field="AndroidVersion" HeaderText="Android Version" Width="200"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    private SfGrid<AdaptiveDetails> Grid;
    public RowDirection RowDirectionValue { get; set; } = RowDirection.Horizontal;
    public List<AdaptiveDetails> AdaptiveData { get; set; }

    protected override void OnInitialized()
    {
        AdaptiveData = AdaptiveDetails.GetAllModels();
    }

    public class DropDownOrder
    {
        public string Text { get; set; }
        public RowDirection Value { get; set; }
    }

    List<DropDownOrder> DropDownValue = new List<DropDownOrder>
    {
        new DropDownOrder() { Text = "Horizontal", Value = RowDirection.Horizontal },
        new DropDownOrder() { Text = "Vertical",   Value = RowDirection.Vertical },
    };

    public void OnChange(ChangeEventArgs<RowDirection, DropDownOrder> args)
    {
        RowDirectionValue = args.Value;
    }
}
```

## Limit Adaptive Layout to Mobile Only

By default, `EnableAdaptiveUI="true"` applies the adaptive layout on both mobile and desktop. To restrict it to mobile screen sizes only, set `AdaptiveUIMode="AdaptiveMode.Mobile"`:

```razor
<SfGrid @ref="Grid"
        ID="Grid"
        DataSource="@Orders"
        EnableAdaptiveUI="true"
        RowRenderingMode="RowDirection.Horizontal"
        AdaptiveUIMode="AdaptiveMode.Mobile"
        AllowPaging="true"
        AllowSorting="true"
        AllowGrouping="true"
        AllowSelection="true"
        AllowFiltering="true"
        AllowExcelExport="true"
        AllowPdfExport="true"
        ShowColumnChooser="true"
        Toolbar="@(new List<string>() { "Add", "Edit", "Delete", "Cancel", "Update", "Search",
                                        "ColumnChooser", "ExcelExport", "PdfExport" })"
        Height="100%">
    <GridEvents OnToolbarClick="ToolbarClickHandler" TValue="OrderData"></GridEvents>
    <GridFilterSettings Type="FilterType.Excel"></GridFilterSettings>
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"
                      Mode="EditMode.Dialog"></GridEditSettings>
    <GridSelectionSettings Type="SelectionType.Multiple"></GridSelectionSettings>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true" Width="130"
                    ValidationRules="@(new ValidationRules{ Required=true })"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="200"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" EditType="EditType.NumericEdit"
                    Format="C2" Width="160"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Format="MM/dd/yyyy hh:mm tt"
                    Type="ColumnType.DateTime" EditType="EditType.DateTimePickerEdit" Width="200"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="170"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    private SfGrid<OrderData> Grid;
    public List<OrderData> Orders { get; set; }

    protected override void OnInitialized()
    {
        Orders = OrderData.GetAllRecords();
    }

    public async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "Grid_pdfexport")
            await Grid.ExportToPdfAsync();
        if (args.Item.Id == "Grid_excelexport")
            await Grid.ExportToExcelAsync();
    }
}
```

**`AdaptiveUIMode` values:**

| Value | Description |
|---|---|
| `AdaptiveMode.Both` | Adaptive layout on mobile and desktop (default) |
| `AdaptiveMode.Mobile` | Adaptive layout on mobile screen sizes only |

> The `RowRenderingMode` applied depends on the `AdaptiveUIMode` configuration.

## Supported Features in Vertical Mode

When `RowRenderingMode="RowDirection.Vertical"`, the following features are supported:

- Paging (including page size dropdown)
- Sorting
- Filtering
- Selection
- Dialog editing
- Aggregates
- Infinite scrolling
- Toolbar: **Add**, **Filter**, **Sort**, **Edit**, **Delete**, **Search**, toolbar template
  - Overflow menu (three-dot icon) shows: **ColumnChooser**, **Print**, **PdfExport**, **ExcelExport**, **CsvExport**

> The **Column Menu** feature (grouping, sorting, autofit, filter, column chooser) is only supported when `RowRenderingMode` is **Horizontal**.

## Key Properties

| Property | Type | Description |
|---|---|---|
| `EnableAdaptiveUI` | `bool` | Enables adaptive mobile-friendly layout |
| `RowRenderingMode` | `RowDirection` | `Horizontal` (default) or `Vertical` row layout |
| `AdaptiveUIMode` | `AdaptiveMode` | `Both` (default) or `Mobile` — controls where adaptive layout applies |

## Mobile Layout CSS (Optional)

Use this CSS shell to simulate a mobile device frame in demos or previews:

```css
.e-mobile-layout {
    position: relative;
    width: 360px;
    height: 640px;
    margin: auto;
    border: 16px solid #f4f4f4;
    border-top-width: 60px;
    border-bottom-width: 60px;
    border-radius: 36px;
    box-shadow: 0 0px 2px rgb(144,144,144), 0 0px 10px rgba(0,0,0,0.16);
}

.e-mobile-layout .e-mobile-content {
    overflow-x: hidden;
    height: 100%;
    background: white;
}

/* Simplified adaptive pager */
.e-adaptive-demo .e-pager .e-pagesizes,
.e-adaptive-demo .e-pager .e-pagecountmsg,
.e-adaptive-demo .e-pager .e-pagercontainer {
    display: none;
}
```
