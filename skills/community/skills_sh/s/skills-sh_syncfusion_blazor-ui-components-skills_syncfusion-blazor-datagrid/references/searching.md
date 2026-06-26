# Searching — Syncfusion Blazor DataGrid

## Table of Contents
- [Enable Search Toolbar](#enable-search-toolbar)
- [Initial Search Configuration](#initial-search-configuration)
- [Search Operators](#search-operators)
- [Search Specific Columns](#search-specific-columns)
- [Exclude Column from Search](#exclude-column-from-search)
- [Programmatic Search](#programmatic-search)
- [Search by External Button](#search-by-external-button)
- [Search on Keystroke (Custom Toolbar)](#search-on-keystroke-custom-toolbar)
- [Ignore Accents in Search](#ignore-accents-in-search)
- [Clear Search by External Button](#clear-search-by-external-button)
- [Multiple Keyword Search](#multiple-keyword-search)

## Enable Search Toolbar

Add a search box to the toolbar by including `"Search"` in the `Toolbar` property:

```razor
<SfGrid DataSource="@Orders" Toolbar="@(new List<string>() { \"Search\" })">
    <GridColumns>...</GridColumns>
</SfGrid>
```

> The clear icon appears in the grid search box when focused or after typing a character. Selecting the clear icon removes the text and resets the search results.

## Initial Search Configuration

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Grids

<SfGrid DataSource="@Orders" Toolbar="@(new List<string>() { \"Search\" })">
    <GridSearchSettings
        Key="Ha"
        Operator="Syncfusion.Blazor.Operator.Contains"
        IgnoreCase="true"
        IgnoreAccent="false"
        Fields="@(new string[]{ \"CustomerID\", \"ShipCity\" })">
    </GridSearchSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

| Property | Values | Description |
|---|---|---|
| `Key` | string | Initial search value |
| `Operator` | `Contains`, `StartsWith`, `EndsWith`, `Equal` | Match mode |
| `IgnoreCase` | bool | Case-insensitive search |
| `IgnoreAccent` | bool | Ignore diacritics (local data only) |
| `Fields` | string[] | Restrict search to specific columns |

## Search Operators

Search operators define how the search key is compared to data values. Configure the operator using `GridSearchSettings.Operator`. The default is **Contains**.

| Operator     | Description                                              |
|--------------|----------------------------------------------------------|
| `StartsWith` | Checks whether a value begins with the specified value.  |
| `EndsWith`   | Checks whether a value ends with the specified value.    |
| `Contains`   | Checks whether a value contains the specified value.     |
| `Equal`      | Checks whether a value is equal to the specified value.  |

Use a `SfDropDownList` to change the operator dynamically at runtime:

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Grids
@using Syncfusion.Blazor.DropDowns

<SfDropDownList Width="100px" TValue="Operator" TItem="DropDownOrder" Value="@SearchOperator" DataSource="@DropDownData">
    <DropDownListFieldSettings Value="Value" Text="Text"></DropDownListFieldSettings>
    <DropDownListEvents TValue="Operator" TItem="DropDownOrder" ValueChange="OnValueChange"></DropDownListEvents>
</SfDropDownList>

<SfGrid DataSource="@Orders" Toolbar="@ToolbarItems">
    <GridSearchSettings Operator="@SearchOperator"></GridSearchSettings>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    public List<string> ToolbarItems = new List<string>() { "Search" };
    public Operator SearchOperator { get; set; } = Operator.StartsWith;

    public class DropDownOrder
    {
        public string Text { get; set; }
        public Operator Value { get; set; }
    }

    List<DropDownOrder> DropDownData = new List<DropDownOrder>
    {
        new DropDownOrder() { Text = "StartsWith", Value = Operator.StartsWith },
        new DropDownOrder() { Text = "EndsWith",   Value = Operator.EndsWith   },
        new DropDownOrder() { Text = "Contains",   Value = Operator.Contains   },
        new DropDownOrder() { Text = "Equal",      Value = Operator.Equal      }
    };

    public void OnValueChange(ChangeEventArgs<Operator, DropDownOrder> args)
    {
        SearchOperator = args.Value;
    }
}
```

## Search Specific Columns

By default, search scans all visible columns. To restrict search to specific columns, set the field names in `GridSearchSettings.Fields`:

```razor
@using Syncfusion.Blazor.Grids

<SfGrid DataSource="@Orders" Toolbar="@ToolbarItems">
    <GridSearchSettings Fields="@SpecificColumns"></GridSearchSettings>
    <GridColumns>
        <GridColumn Field="OrderID"    HeaderText="Order ID"    Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="150"></GridColumn>
        <GridColumn Field="Freight"    HeaderText="Freight"     Format="C2" Width="150"></GridColumn>
        <GridColumn Field="ShipCity"   HeaderText="Ship City"   Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    public List<string> ToolbarItems = new List<string>() { "Search" };
    public string[] SpecificColumns = new string[] { "CustomerID", "ShipCity" };
}
```

## Exclude Column from Search

```razor
<GridColumn Field="OrderID" AllowSearching="false"></GridColumn>
```

## Programmatic Search

```razor
<SfGrid @ref="Grid" DataSource="@Orders" Toolbar="@(new List<string>() { \"Search\" })">...</SfGrid>
@code {
    SfGrid<Order> Grid;

    // Trigger search
    await Grid.SearchAsync("France");

    // Clear search
    await Grid.SearchAsync("");
}
```

## Search by External Button

```razor
<input @bind="SearchText" />
<button @onclick="Search">Search</button>

<SfGrid @ref="Grid" DataSource="@Orders">...</SfGrid>
@code {
    SfGrid<Order> Grid;
    string SearchText = "";
    async Task Search() => await Grid.SearchAsync(SearchText);
}
```

## Search on Keystroke (Custom Toolbar)

Use an `SfToolbar` with `ToolbarItem` of `Type="ItemType.Input"` and call `SearchAsync` inside the TextBox `Input` event to trigger search on every keystroke:

```razor
@using Syncfusion.Blazor.Data
@using Syncfusion.Blazor.Grids
@using Syncfusion.Blazor.Inputs
@using Syncfusion.Blazor.Navigations

<SfGrid @ref="DefaultGrid" DataSource="@Orders" AllowSorting="true" AllowPaging="true">
    <SfToolbar>
        <ToolbarItems>
            <ToolbarItem Type="ItemType.Input" Align="Syncfusion.Blazor.Navigations.ItemAlign.Right">
                <Template>
                    <SfTextBox Placeholder="Enter values to search" Input="OnInput"></SfTextBox>
                    <span class="e-search-icon e-icons"></span>
                </Template>
            </ToolbarItem>
        </ToolbarItems>
    </SfToolbar>
    <GridColumns>...</GridColumns>
</SfGrid>
@code {
    private SfGrid<OrderData> DefaultGrid;

    public void OnInput(InputEventArgs args)
    {
        this.DefaultGrid.SearchAsync(args.Value);
    }
}
```

## Ignore Accents in Search

By default, the DataGrid does not treat accented and unaccented characters as equivalent. To enable accent-insensitive search, set `GridSearchSettings.IgnoreAccent` to `true`. This is useful when data contains diacritic characters such as `é`, `ñ`, `ü`, etc.

> Accent-insensitive comparison applies to both searching and filtering when using an `IEnumerable` (local) data source only. This feature affects characters outside the ASCII range.

```razor
@using Syncfusion.Blazor.Grids

<SfGrid DataSource="@GridData" Toolbar="@(new List<string>() { \"Search\" })">
    <GridSearchSettings IgnoreAccent="true"></GridSearchSettings>
    <GridColumns>
        <GridColumn Field="Inventor"       HeaderText="Inventor Name"              Width="180"></GridColumn>
        <GridColumn Field="PatentFamilies" HeaderText="Number of Patent Families"  TextAlign="TextAlign.Right" Width="195"></GridColumn>
        <GridColumn Field="Country"        HeaderText="Country"                    Width="120"></GridColumn>
        <GridColumn Field="MainFields"     HeaderText="Main Fields of Invention"   Width="130"></GridColumn>
    </GridColumns>
</SfGrid>
```

## Clear Search by External Button

To programmatically clear an applied search, call `SearchAsync` with an empty string. This removes the search text and resets the grid results:

```razor
@using Syncfusion.Blazor.Buttons
@using Syncfusion.Blazor.Grids

<SfButton Content="Clear Search" OnClick="ClearSearch"></SfButton>

<SfGrid @ref="DefaultGrid" DataSource="@Orders" Toolbar="@ToolbarItems">
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    private SfGrid<OrderData> DefaultGrid;
    public List<string> ToolbarItems = new List<string>() { "Search" };

    public async Task ClearSearch()
    {
        await DefaultGrid.SearchAsync("");
    }
}
```

> You can also clear the search by clicking the clear icon inside the search input field in the toolbar.

## Multiple Keyword Search

Use `WhereFilter` and combine predicates with `WhereFilter.Or` / `WhereFilter.And` to search using multiple criteria. This works for both local and remote data via the grid's `Query` property:

```razor
@using Syncfusion.Blazor.Grids
@using Syncfusion.Blazor.Inputs
@using Syncfusion.Blazor.Buttons
@using Syncfusion.Blazor.Data

<SfTextBox Input="OnInput"></SfTextBox>
<SfRadioButton TChecked="bool" ValueChange="OnRadioButtonChecked" Label="Filter Paid"></SfRadioButton>

<SfGrid @ref="DefaultGrid" DataSource="@Orders" Query="@SearchQuery">
    <GridColumns>
        <GridColumn Field="OrderID"    HeaderText="Order ID"    Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="150"></GridColumn>
        <GridColumn Field="Paid"       HeaderText="Paid"          Width="150"></GridColumn>
        <GridColumn Field="Freight"    HeaderText="Freight"       Format="C2" TextAlign="TextAlign.Right" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    public Query SearchQuery { get; set; }
    private SfGrid<OrderData> DefaultGrid;
    public List<OrderData> Orders { get; set; }

    WhereFilter ColumnPredicate = new WhereFilter();
    List<WhereFilter> Predicate = new List<WhereFilter>();

    // Combine with OR — search by CustomerID text input
    public void OnInput(InputEventArgs args)
    {
        Predicate = new List<WhereFilter>();
        Predicate.Add(new WhereFilter()
        {
            Field = "CustomerID",
            value = args.Value,
            Operator = "contains",
            IgnoreCase = true
        });
        ColumnPredicate = WhereFilter.Or(Predicate);
        SearchQuery = new Query().Where(ColumnPredicate);
    }

    // Combine with AND — additionally filter by Paid status
    public void OnRadioButtonChecked(ChangeArgs<bool> args)
    {
        Predicate.Add(new WhereFilter()
        {
            Field = "Paid",
            value = "Yes",
            Operator = "equal",
            IgnoreCase = true
        });
        ColumnPredicate = WhereFilter.And(Predicate);
        SearchQuery = new Query().Where(ColumnPredicate);
    }

    protected override void OnInitialized()
    {
        Orders = OrderData.GetAllRecords();
    }
}
```

> - Use `WhereFilter.Or` to match any of the conditions (e.g., multiple keywords on the same field).
> - Use `WhereFilter.And` to require all conditions to match simultaneously.
> - This approach works with both local (`IEnumerable`) and remote (`SfDataManager`) data sources.
