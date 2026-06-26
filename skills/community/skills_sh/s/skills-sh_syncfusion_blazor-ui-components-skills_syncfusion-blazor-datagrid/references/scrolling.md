# Scrolling — Syncfusion Blazor DataGrid

## Table of Contents
- [Fixed Dimensions (Enable Scrollbars)](#fixed-dimensions-enable-scrollbars)
- [Responsive with Parent Container](#responsive-with-parent-container)
- [Sticky Header](#sticky-header)
- [Scroll to Specific Row](#scroll-to-specific-row)
- [Custom Scrollbar Styling](#custom-scrollbar-styling)

## Fixed Dimensions (Enable Scrollbars)

```razor
<SfGrid DataSource="@Orders" Height="315" Width="400">
    <GridColumns>...</GridColumns>
</SfGrid>
```

Without explicit `Height`/`Width`, content expands to fit (`auto` default). Scrollbars appear when:
- **Vertical**: total row height exceeds Grid `Height`
- **Horizontal**: total column width exceeds Grid `Width`

## Responsive with Parent Container

```razor
<div style="height:400px; width:100%;">
    <SfGrid DataSource="@Orders" Height="100%" Width="100%">
        <GridColumns>...</GridColumns>
    </SfGrid>
</div>
```

> Parent container must have explicit height for `Height="100%"` to work.

## Sticky Header

Header row stays fixed while scrolling through content:

```razor
<SfGrid DataSource="@Orders" Height="400" EnableStickyHeader="true">
    <GridColumns>...</GridColumns>
</SfGrid>
```

> Requires explicit container height. Compatible with virtual scrolling.

## Scroll to Specific Row

`ScrollIntoViewAsync` brings a row (and optionally a column) into the viewport.

**Signature:** `ScrollIntoViewAsync(rowIndex, columnIndex?, hierarchyIndex?)`

```razor
<SfGrid @ref="Grid" DataSource="@Orders" Height="315">...</SfGrid>
@code {
    SfGrid<Order> Grid;

    // Scroll to row index 15
    await Grid.ScrollIntoViewAsync(15);

    // Scroll to row 15, column index 3
    await Grid.ScrollIntoViewAsync(15, 3);
}
```

**Select and scroll to a row in combination** — requires `PreventRender(false)` in `RowSelected` to update the UI:

```razor
<SfGrid @ref="Grid" DataSource="@Orders" Height="315">
    <GridEvents RowSelected="RowSelectedHandler" TValue="Order"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    async Task ScrollToRow(int rowIndex)
    {
        await Grid.SelectRowAsync(rowIndex);
        await Grid.ScrollIntoViewAsync(rowIndex);
    }

    void RowSelectedHandler(RowSelectEventArgs<Order> args)
    {
        Grid.PreventRender(false); // required for UI refresh
    }
}
```

## Custom Scrollbar Styling

Uses native browser scrollbars. Customizable via CSS — browser-dependent (Chrome/Edge/Safari). Consider accessibility: ensure keyboard scrolling and focus visuals remain usable.

```css
/* Global selectors — add to wwwroot/css/app.css */
::-webkit-scrollbar { background-color: white; }
::-webkit-scrollbar-thumb { background-color: #888; border-radius: 10px; }
::-webkit-scrollbar-button { background-color: #bbbbbb; }
```

Or scope to the grid content only:

```css
.e-grid .e-content::-webkit-scrollbar { width: 10px; height: 10px; }
.e-grid .e-content::-webkit-scrollbar-thumb { background-color: #888; border-radius: 5px; }
.e-grid .e-content::-webkit-scrollbar-button { display: none; }

