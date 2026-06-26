# Style and Appearance

## Table of Contents
- [Overview](#overview)
- [Customize the Grid Root Element](#customize-the-grid-root-element)
- [Customize the Header](#customize-the-header)
- [Customize Grid Lines](#customize-grid-lines)
- [Customize Alternate Rows with Frozen Columns](#customize-alternate-rows-with-frozen-columns)
- [Customize Aggregate Elements](#customize-aggregate-elements)
- [Using Theme Studio](#using-theme-studio)
- [CSS Class Reference](#css-class-reference)

## Overview

The Syncfusion Blazor DataGrid supports visual customization using CSS overrides and Syncfusion Theme Studio. Use browser developer tools to inspect rendered HTML and identify CSS selectors. Prefer specificity over `!important` to maintain consistent styling control.

**When to use this reference:**
- Customize header background, colors, fonts
- Style rows, alternate rows, hover and selection states
- Adjust grid line color and thickness
- Style footer aggregates
- Hide the header
- Apply consistent theme using Theme Studio

## Customize the Grid Root Element

The `.e-grid` class targets the root container. Apply CSS to change font, background, and row-level appearance:

```razor
<SfGrid DataSource="@Orders" Height="315" AllowPaging="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" TextAlign="TextAlign.Right" Width="140"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="120"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" TextAlign="TextAlign.Right" Width="100"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>

<style>
    .e-grid {
        font-family: cursive;
    }

    /* Hover state — prefer specificity over !important */
    .e-grid .e-content .e-row:hover .e-rowcell {
        background-color: rgb(204, 229, 255);
    }

    /* Selected row */
    .e-grid .e-rowcell.e-selectionbackground {
        background-color: rgb(230, 230, 250);
    }

    /* Alternate rows */
    .e-grid .e-row.e-altrow {
        background-color: rgb(150, 212, 212);
    }

    /* Normal rows */
    .e-grid .e-row {
        background-color: rgb(180, 180, 180);
    }

    /* Keyboard focus visibility */
    .e-grid .e-row:focus-visible .e-rowcell {
        outline: 2px solid #005a9e;
        outline-offset: -2px;
    }
</style>
```

**Key selectors:**

| Selector | Targets |
|---|---|
| `.e-grid` | Root grid container |
| `.e-grid .e-row` | All data rows |
| `.e-grid .e-row.e-altrow` | Alternate rows |
| `.e-grid .e-content .e-row:hover .e-rowcell` | Hovered row cells |
| `.e-grid .e-rowcell.e-selectionbackground` | Selected row cells |

## Customize the Header

Use `.e-gridheader`, `.e-headercell`, and `.e-headercelldiv` to style the header area:

```razor
<SfGrid DataSource="@Orders" Height="315" AllowPaging="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" TextAlign="TextAlign.Right" Width="140"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="120"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" TextAlign="TextAlign.Right" Width="120"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Format="d" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>

<style>
    /* Header container border */
    .e-grid .e-gridheader {
        border: 2px solid green;
    }

    /* Individual header cell background and text color */
    .e-grid .e-headercell {
        background-color: #1ea8bd;
        color: #ffffff;
    }

    /* Header text size and weight */
    .e-grid .e-headercelldiv {
        font-size: 15px;
        font-weight: bold;
        color: darkblue;
    }
</style>
```

**Hide the header:**

```css
/* Hide header globally */
.e-grid .e-gridheader .e-columnheader {
    display: none;
}

/* Hide header for a specific grid by ID */
#MyGrid.e-grid .e-gridheader .e-columnheader {
    display: none;
}
```

> Hiding the header removes sorting arrows, filter icons, and column menu buttons. Provide `aria-label` or `aria-labelledby` for accessibility.

**Header CSS selectors:**

| Selector | Targets |
|---|---|
| `.e-grid .e-gridheader` | Header container |
| `.e-grid .e-headercell` | Individual header cells |
| `.e-grid .e-headercelldiv` | Header text inner container |
| `.e-grid .e-gridheader .e-columnheader` | Column header row (hide to remove header) |

## Customize Grid Lines

Use the `GridLines` property to control border visibility, then apply CSS to customize color and thickness:

```razor
<SfGrid DataSource="@Orders" Height="315" GridLines="GridLine.Both">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" TextAlign="TextAlign.Right" Width="90"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="150"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" TextAlign="TextAlign.Right" Width="130"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Format="d" Type="ColumnType.Date" Width="130"></GridColumn>
    </GridColumns>
</SfGrid>

<style>
    .e-grid .e-gridheader,
    .e-grid .e-headercell,
    .e-grid .e-rowcell,
    .e-grid {
        border-color: yellow;
        border-style: solid;
        border-width: 2px;
    }

    /* Ensure header divider lines are visible */
    .e-grid .e-headercell {
        border-right-width: 2px;
    }
</style>
```

**`GridLines` options:**

| Value | Description |
|---|---|
| `GridLine.Horizontal` | Only horizontal lines between rows |
| `GridLine.Vertical` | Only vertical lines between columns |
| `GridLine.Both` | Both horizontal and vertical lines |
| `GridLine.None` | No grid lines |
| `GridLine.Default` | Default browser rendering |

## Customize Alternate Rows with Frozen Columns

When frozen columns are enabled, use `.e-altrow .e-rowcell` to style alternate rows consistently across both frozen and movable sections:

```razor
<SfGrid DataSource="@Orders" Height="315" AllowPaging="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsFrozen="true" TextAlign="TextAlign.Right" Width="140"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="120"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" TextAlign="TextAlign.Right" Width="100"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>

<style>
    /* Applies to alt rows across frozen and movable sections */
    .e-grid .e-altrow .e-rowcell {
        background-color: #E8EEFA;
    }
</style>
```

> Without `IsFrozen`, use `.e-grid .e-row.e-altrow` for alternate row styling.

## Customize Aggregate Elements

Style the footer aggregate area using `.e-gridfooter`, `.e-summaryrow`, and `.e-summarycell`:

```razor
<SfGrid DataSource="@Orders" Height="315" AllowPaging="true">
    <GridAggregates>
        <GridAggregate>
            <GridAggregateColumns>
                <GridAggregateColumn Field="Freight" Type="AggregateType.Sum">
                    <FooterTemplate>
                        @{ var agg = (context as AggregateTemplateContext); }
                        <div>Sum: @agg.Sum</div>
                    </FooterTemplate>
                </GridAggregateColumn>
            </GridAggregateColumns>
        </GridAggregate>
    </GridAggregates>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

<style>
    /* Footer aggregate container */
    .e-grid .e-gridfooter {
        font-family: cursive;
        background-color: #f5f8fc;
    }

    /* Summary row cells */
    .e-grid .e-summaryrow .e-summarycell {
        background-color: #deecf9;
    }

    /* Focus visibility for accessibility */
    .e-grid .e-summarycell:focus-visible {
        outline: 2px solid #005a9e;
        outline-offset: -2px;
    }
</style>
```

**Aggregate CSS selectors:**

| Selector | Targets |
|---|---|
| `.e-grid .e-gridfooter` | Aggregate footer root container |
| `.e-grid .e-summaryrow` | Summary row |
| `.e-grid .e-summaryrow .e-summarycell` | Individual summary cells |

## Using Theme Studio

Syncfusion Theme Studio lets you customize all Syncfusion components globally, including the DataGrid.

1. Open [Syncfusion Theme Studio](https://blazor.syncfusion.com/themestudio/?theme=material3)
2. Select **Grid** in the left panel
3. Customize colors, typography, spacing, and visual tokens
4. Download the generated CSS
5. Include it in the Blazor project's stylesheet or theme bundle (replace the default theme reference)

> Use Theme Studio for project-wide visual consistency. Use targeted CSS overrides for component-specific changes.

## CSS Class Reference

### Grid Structure

| CSS Class | Element |
|---|---|
| `.e-grid` | Root grid container |
| `.e-gridheader` | Header container |
| `.e-headercell` | Header cell |
| `.e-headercelldiv` | Header text inner element |
| `.e-columnheader` | Column header row |
| `.e-gridcontent` | Content area |
| `.e-rowcell` | Data row cell |
| `.e-gridfooter` | Footer/aggregate container |

### Row States

| CSS Class | Element |
|---|---|
| `.e-row` | Normal data row |
| `.e-row.e-altrow` | Alternate row |
| `.e-row:hover .e-rowcell` | Hovered row cell |
| `.e-rowcell.e-selectionbackground` | Selected row cell |
| `.e-row.e-focused` | Focused row |

### Feature-Specific

| CSS Class | Element |
|---|---|
| `.e-summaryrow .e-summarycell` | Aggregate summary cells |
| `.e-groupcaptionrow` | Group caption row |
| `.e-altrow .e-rowcell` | Alternate row cells (frozen column support) |
| `.e-filterbarcell` | Filter bar input cell |
| `.e-filtermenudiv` | Filter menu icon container |
