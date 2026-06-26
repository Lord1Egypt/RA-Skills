# Column Chooser — Syncfusion Blazor DataGrid

## Table of Contents
1. [Enable Column Chooser](#enable-column-chooser)
2. [Hide Column in Chooser](#hide-column-in-chooser)
3. [Open Chooser Programmatically](#open-chooser-programmatically)
4. [Customize Chooser Dialog](#customize-chooser-dialog)
5. [Search Operator](#search-operator)

---

## Enable Column Chooser

Enable the column chooser feature by setting `ShowColumnChooser` to **true**:

```razor
<SfGrid DataSource="@Orders" ShowColumnChooser="true" 
        Toolbar="@(new List<string>() { "ColumnChooser" })">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Format="d" Width="130"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="120"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="120"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Visible="false" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Features:
- Dialog displays column names
- Show/hide columns dynamically
- Search functionality to find columns
- Header text displayed as column name

> The column chooser dialog displays the header text of each column by default. If HeaderText is not defined, the Field name is shown instead.

---

## Hide Column in Chooser

Prevent specific columns from appearing in the column chooser using `ShowInColumnChooser`:

```razor
<SfGrid DataSource="@Orders" ShowColumnChooser="true" 
        Toolbar="@(new List<string>() { "ColumnChooser" })">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" 
                  ShowInColumnChooser="false" Width="120"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Format="d" Width="130"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="120"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Use cases:
- Keep primary key columns visible
- Prevent accidental column hiding
- Simplify dialog for users
- Hide system/internal columns

---

## Open Chooser Programmatically

Open the column chooser dialog using code via the `OpenColumnChooserAsync` method:

```razor
<SfButton OnClick="Show">Open Column Chooser</SfButton>

<SfGrid @ref="Grid" DataSource="@Orders" ShowColumnChooser="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Width="130"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Width="120"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    private SfGrid<OrderData> Grid;
    
    public void Show()
    {
        // Open at position (100, 40)
        Grid.OpenColumnChooserAsync(100, 40);
    }
}
```

Method parameters:
- **x** (double): Horizontal position
- **y** (double): Vertical position

---

## Customize Chooser Dialog

Customize the column chooser dialog size and appearance using CSS:

```razor
<SfGrid DataSource="@Orders" ShowColumnChooser="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Width="130"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

<style>
    .e-grid .e-dialog.e-ccdlg {
        max-height: 600px !important;
        width: 300px !important;
    }
    
    .e-grid .e-ccdlg .e-cc-contentdiv {
        height: 250px !important;
        width: 250px !important;
    }
</style>
```

Customizable selectors:
- `.e-dialog.e-ccdlg`: Main dialog container
- `.e-cc-contentdiv`: Dialog content area
- Use `!important` to override default styles

---

## Search Operator

Change the default search operator in the column chooser using `GridColumnChooserSettings`:

```razor
<SfGrid DataSource="@Orders" ShowColumnChooser="true" 
        Toolbar="@(new List<string>() { "ColumnChooser" })">
    <GridColumnChooserSettings Operator="Syncfusion.Blazor.Operator.Contains"></GridColumnChooserSettings>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Width="130"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Width="120"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Available operators:
- **StartsWith**: Match columns beginning with search text (default)
- **EndsWith**: Match columns ending with search text
- **Contains**: Match columns containing search text
- **Equal**: Match exact column names

Default behavior:
- Search uses **StartsWith** operator
- Users can find columns by typing column names
- Real-time filtering of column list

