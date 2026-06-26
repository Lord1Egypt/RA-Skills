# Filtering — Syncfusion Blazor DataGrid

## Table of Contents
1. [Enable Filtering](#enable-filtering)
2. [Filter Types](#filter-types)
3. [Filter Bar](#filter-bar)
4. [Filter Menu](#filter-menu)
5. [Excel-Like Filter](#excel-like-filter)
6. [Checkbox Filter](#checkbox-filter)
7. [Filter Operators](#filter-operators)
8. [WildCard and Like Operator Filter](#wildcard-and-like-operator-filter)
9. [Filtering with Case Sensitivity](#filtering-with-case-sensitivity)
10. [Enable Different Filter for a Column](#enable-different-filter-for-a-column)
11. [Change Default Filter Operator for a Column](#change-default-filter-operator-for-a-column)
12. [Programmatic Filtering](#programmatic-filtering)
13. [Get Filtered Records](#get-filtered-records)
14. [Initial Filter State](#initial-filter-state)
15. [FilterTemplate (Custom Components)](#filtertemplate-custom-components)
16. [Filtering Events](#filtering-events)
17. [Filter Enum Column](#filter-enum-column)

---

## Enable Filtering

Set `AllowFiltering="true"` on the grid. Set `AllowFiltering="false"` on a `GridColumn` to disable for a specific column.

```razor
<SfGrid DataSource="@Orders" AllowFiltering="true">
    <GridFilterSettings Type="FilterType.FilterBar"></GridFilterSettings>
    <GridColumns>
        <GridColumn Field="OrderID"    AllowFiltering="true"  Width="120"></GridColumn>
        <GridColumn Field="CustomerID" AllowFiltering="false" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

---

## Filter Types

| `FilterType` | Description |
|---|---|
| `FilterBar` | Text inputs below column headers (default) |
| `Menu` | Popup dialog per column with operators |
| `Excel` | Excel-like dialog with checkbox list + search |
| `CheckBox` | Checkbox-only filter dialog |

---

## Filter Bar

```razor
<GridFilterSettings Type="FilterType.FilterBar" Mode="FilterBarMode.Immediate" ShowFilterBarStatus="true">
</GridFilterSettings>
```

- `Mode`: `OnEnter` (filter on Enter key) or `Immediate` (filter as you type)
- `ShowFilterBarStatus`: Shows active filter info in pager

**Custom Filter Bar Template** — Use `FilterTemplate` to replace the default text input (supports `SfDatePicker`, `SfNumericTextBox`, `SfComboBox`, `SfMultiSelect`):

```razor
<GridColumn Field="OrderDate" HeaderText="Order Date">
    <FilterTemplate>
        <SfDatePicker TValue="DateTime?" @bind-Value="@DateValue">
            <DatePickerEvents TValue="DateTime?" ValueChange="DatePickerValueChange"></DatePickerEvents>
        </SfDatePicker>
    </FilterTemplate>
</GridColumn>
@code {
    public DateTime? DateValue { get; set; }
    public async Task DatePickerValueChange(Syncfusion.Blazor.Calendars.ChangedEventArgs<DateTime?> args)
    {
        if (args.Value == null) await Grid.ClearFilteringAsync();
        else await Grid.FilterByColumnAsync("OrderDate", "equal", args.Value);
    }
}
```

**Hide Filter Bar for Template Column** — Use `FilterTemplate` with empty `<span>`:

```razor
<GridColumn HeaderText="Action">
    <Template><SfButton>Action</SfButton></Template>
    <FilterTemplate><span></span></FilterTemplate>
</GridColumn>
```

---

## Filter Menu

```razor
<GridFilterSettings Type="FilterType.Menu"></GridFilterSettings>
```

Per-column override: `FilterSettings="@(new FilterSettings { Type = FilterType.Menu })"` on `GridColumn`.

Default editors: **String** → `AutoComplete` | **Number** → `NumericTextBox` | **Boolean** → `DropDownList` | **Date** → `DatePicker` | **DateTime** → `DateTimePicker`

**Customize Operators** — Assign `List<Syncfusion.Blazor.Grids.IFilterOperator>` to `args.FilterOperators` in `FilterDialogOpening`. Implement `IFilterOperator` with `Value` and `Text` properties:

```razor
<GridEvents TValue="OrderData" FilterDialogOpening="FilterDialogOpeningHandler"></GridEvents>
@code {
    public class Operators : Syncfusion.Blazor.Grids.IFilterOperator
    {
        public string Value { get; set; }
        public string Text  { get; set; }
    }
    List<Syncfusion.Blazor.Grids.IFilterOperator> StringOperator = new List<Syncfusion.Blazor.Grids.IFilterOperator>
    {
        new Operators() { Value = "startswith", Text = "Starts With" },
        new Operators() { Value = "endswith",   Text = "Ends With"   },
        new Operators() { Value = "contains",   Text = "Contains"    },
        new Operators() { Value = "equal",      Text = "Equal"       },
        new Operators() { Value = "notequal",   Text = "Not Equal"   }
    };
    List<Syncfusion.Blazor.Grids.IFilterOperator> NumberOperator = new List<Syncfusion.Blazor.Grids.IFilterOperator>
    {
        new Operators() { Value = "equal", Text = "Equal" }, new Operators() { Value = "notequal", Text = "Not Equal" },
        new Operators() { Value = "greaterthan", Text = "Greater Than" }, new Operators() { Value = "lessthan", Text = "Less Than" }
    };
    List<Syncfusion.Blazor.Grids.IFilterOperator> DateOperator = new List<Syncfusion.Blazor.Grids.IFilterOperator>
    {
        new Operators() { Value = "equal", Text = "Equal" }, new Operators() { Value = "notequal", Text = "Not Equal" },
        new Operators() { Value = "greaterthan", Text = "After" }, new Operators() { Value = "lessthan", Text = "Before" }
    };
    List<Syncfusion.Blazor.Grids.IFilterOperator> BooleanOperator = new List<Syncfusion.Blazor.Grids.IFilterOperator>
    {
        new Operators() { Value = "equal", Text = "Equal" }, new Operators() { Value = "notequal", Text = "Not Equal" }
    };
    public async Task FilterDialogOpeningHandler(FilterDialogOpeningEventArgs args)
    {
        if (args.ColumnName == "CustomerID" || args.ColumnName == "ShipName") args.FilterOperators = StringOperator;
        else if (args.ColumnName == "OrderID")   args.FilterOperators = NumberOperator;
        else if (args.ColumnName == "OrderDate") args.FilterOperators = DateOperator;
        else if (args.ColumnName == "Verified")  args.FilterOperators = BooleanOperator;
    }
}
```

**FilterEditorSettings** — Customize built-in filter dialog editors (applies to both Menu and Excel dialogs):

```razor
<GridColumn Field="Freight" FilterSettings="@(new FilterSettings { Type = FilterType.Menu })"
            FilterEditorSettings="@(new NumericFilterParams { Params = new NumericTextBoxModel<object> { Min = 0, Step = 10 } })">
</GridColumn>
```

---

## Excel-Like Filter

```razor
<GridFilterSettings Type="FilterType.Excel"></GridFilterSettings>
```

**FilterChoiceCount** — Default 1000 items. Override in `FilterDialogOpening`: `args.FilterChoiceCount = 3000;`

> High `FilterChoiceCount` may slow dialog opening.

**FilterItemTemplate** — Customize display text in checkbox list:

```razor
<GridColumn Field="IsVerified" Type="ColumnType.Boolean" DisplayAsCheckBox="true">
    <FilterItemTemplate>
        @{ var item = (FilterItemTemplateContext)context; }
        <span>@(item.Value?.ToString() == "True" ? "Delivered" : "Not Delivered")</span>
    </FilterItemTemplate>
</GridColumn>
```

---

## Checkbox Filter

```razor
<GridFilterSettings Type="FilterType.CheckBox"></GridFilterSettings>
```

---

## Filter Operators

| Operator | Supported Types |
|---|---|
| `StartsWith`, `DoesNotStartWith`, `EndsWith`, `DoesNotEndWith`, `Contains`, `DoesNotContain` | String |
| `Equal`, `NotEqual` | String, Number, Boolean, Date |
| `GreaterThan`, `GreaterThanOrEqual`, `LessThan`, `LessThanOrEqual`, `Between` | Number, Date |
| `IsNull`, `IsNotNull` | String, Number, Date |
| `IsEmpty`, `IsNotEmpty` | String |

> Default `Operator` is `Equal` in `GridFilterSettings.Columns`.

---

## WildCard and Like Operator Filter

**WildCard** (`*` symbol) — Supported in all filter bar search modes:

| Pattern | Description |
|---|---|
| `a*b` | Starts with "a" and ends with "b" |
| `a*` | Starts with "a" |
| `*b` | Ends with "b" |
| `a` | Contains "a" |
| `ab*` | Contains "a", followed by any chars, then "b" |

**Like** (`%` symbol) — Supported in Filter Menu, Filter Bar (via `Operator` property), and Custom Filter of Excel type:

| Pattern | Description |
|---|---|
| `%ab%` | Contains "ab" |
| `ab%` | Ends with "ab" |
| `%ab` | Starts with "ab" |

---

## Filtering with Case Sensitivity

```razor
<GridFilterSettings EnableCaseSensitivity="@isCaseSensitive"></GridFilterSettings>
@code { private bool isCaseSensitive = false; }
```

---

## Enable Different Filter for a Column

```razor
<GridFilterSettings Type="Syncfusion.Blazor.Grids.FilterType.Menu"></GridFilterSettings>
<GridColumns>
    <GridColumn Field="OrderID"    FilterSettings="@(new FilterSettings { Type = FilterType.Menu })"     Width="100"></GridColumn>
    <GridColumn Field="CustomerID" FilterSettings="@(new FilterSettings { Type = FilterType.Excel })"    Width="120"></GridColumn>
    <GridColumn Field="Freight"    FilterSettings="@(new FilterSettings { Type = FilterType.CheckBox })" Width="100"></GridColumn>
</GridColumns>
```

> **Limitation:** `Menu`, `Excel`, and `CheckBox` filter types can be mixed across columns, but **cannot be combined with `FilterBar`**. The `FilterBar` type requires UI-level changes (a visible input row beneath headers) that are incompatible with the icon-based dialogs used by the other filter types. If you need different filter types per column, set the global `GridFilterSettings` type to `Menu`, `Excel`, or `CheckBox` — not `FilterBar`.

---

## Change Default Filter Operator for a Column

Default: `StartsWith` for string, `Equal` for numeric/boolean columns.

```razor
<GridColumn Field="OrderID"    FilterSettings="@(new FilterSettings { Operator = Syncfusion.Blazor.Operator.Equal })"      Width="100"></GridColumn>
<GridColumn Field="CustomerID" FilterSettings="@(new FilterSettings { Operator = Syncfusion.Blazor.Operator.StartsWith })" Width="120"></GridColumn>
<GridColumn Field="ShipCity"   FilterSettings="@(new FilterSettings { Operator = Syncfusion.Blazor.Operator.Contains })"   Width="100"></GridColumn>
```

---

## Programmatic Filtering

```razor
@code {
    await Grid.FilterByColumnAsync("OrderID", "equal", 10248);                                                   // single value
    await Grid.FilterByColumnAsync("CustomerID", "equal", new List<string> { "VINET", "TOMSP", "ERNSH" });       // multiple values
    await Grid.ClearFilteringAsync();                                                                            // clear all filters
    var filteredRecords = Grid.GetFilteredRecordsAsync();                                                        // get filtered (local)
    FilterData = (List<OrderData>)filteredRecords.Result;
    var filteredData = await Grid.GetFilteredRecordsAsync();                                                     // get filtered (remote)
    List<OrderData> filteredList = JsonConvert.DeserializeObject<List<OrderData>>(JsonConvert.SerializeObject(filteredData));
}
```

---

## Initial Filter State

**Declarative** — Define using `GridFilterColumn` inside `GridFilterSettings`:
```razor
<GridFilterSettings>
    <GridFilterColumns>
        <GridFilterColumn Field="ShipCity" MatchCase="false" Operator="Syncfusion.Blazor.Operator.StartsWith" Predicate="and" Value="@ShipCityValue"></GridFilterColumn>
        <GridFilterColumn Field="ShipName" MatchCase="false" Operator="Syncfusion.Blazor.Operator.StartsWith" Predicate="and" Value="@ShipNameValue"></GridFilterColumn>
    </GridFilterColumns>
</GridFilterSettings>
```

**Multiple Values (same/different columns via DataBound)** — Get column `Uid` via `GetColumnsAsync`, add `GridFilterColumn` entries to `Grid.FilterSettings.Columns`, then call `Grid.Refresh()`:
```razor
<GridEvents DataBound="DataBoundHandler" TValue="OrderData"></GridEvents>
@code {
    public bool Initialrender = true;
    public async Task DataBoundHandler()
    {
        var columns = await Grid.GetColumnsAsync();
        if (columns != null && Initialrender)
        {
            Initialrender = false;
            Grid.FilterSettings.Columns ??= new List<GridFilterColumn>();
            string custUid = columns[1].Uid; string orderUid = columns[0].Uid;
            Grid.FilterSettings.Columns.Add(new GridFilterColumn { Field = "CustomerID", Operator = Syncfusion.Blazor.Operator.StartsWith, Predicate = "or",  Value = "VINET", Uid = custUid  });
            Grid.FilterSettings.Columns.Add(new GridFilterColumn { Field = "CustomerID", Operator = Syncfusion.Blazor.Operator.StartsWith, Predicate = "or",  Value = "HANAR", Uid = custUid  });
            Grid.FilterSettings.Columns.Add(new GridFilterColumn { Field = "OrderID",    Operator = Syncfusion.Blazor.Operator.LessThan,   Predicate = "and", Value = 10250,   Uid = orderUid });
            Grid.FilterSettings.Columns.Add(new GridFilterColumn { Field = "OrderID",    Operator = Syncfusion.Blazor.Operator.NotEqual,   Predicate = "and", Value = 10262,   Uid = orderUid });
            Grid.Refresh();
        }
    }
}
```

---

## FilterTemplate (Custom Components)

Replace default filter input with a custom component. Use `FilterByColumnAsync` in the value-change event to trigger filtering.

```razor
<GridColumn Field="ShipCountry" HeaderText="Ship Country">
    <FilterTemplate>
        <SfMultiSelect TItem="string" TValue="string[]" DataSource="@ShipCountryData" Placeholder="Select a country">
            <MultiSelectEvents TItem="string" TValue="string[]" ValueChange="@MultiSelectValueChange"></MultiSelectEvents>
        </SfMultiSelect>
    </FilterTemplate>
</GridColumn>
@code {
    List<string> ShipCountryData = new List<string>() { "France", "Germany", "Brazil", "Belgium" };
    private async Task MultiSelectValueChange(MultiSelectChangeEventArgs<string[]> args)
    {
        if (args.Value == null) await Grid.ClearFilteringAsync();
        else await Grid.FilterByColumnAsync("ShipCountry", "equal", args.Value);
    }
}
```

---

## Filtering Events

| Event | Args Type | Description |
|---|---|---|
| `Filtering` | `FilteringEventArgs` | Before filter applied; `args.Cancel = true` cancels it |
| `Filtered` | `FilteredEventArgs` | After filter applied |
| `FilterDialogOpening` | `FilterDialogOpeningEventArgs` | Before dialog opens (Menu/Excel/CheckBox) |

**`FilteringEventArgs`**: `ColumnName`, `FilterPredicates`, `Cancel`
**`FilteredEventArgs`**: `ColumnName`, `FilterPredicates`
**`FilterDialogOpeningEventArgs`**: `ColumnName`, `FilterOperators`, `FilterChoiceCount`

```razor
<GridEvents TValue="OrderData" Filtering="FilteringHandler" Filtered="FilteredHandler" FilterDialogOpening="FilterDialogOpeningHandler"></GridEvents>
@code {
    void FilteringHandler(FilteringEventArgs args)
    {
        if (args.ColumnName == "ShipCity") args.Cancel = true;
    }
    void FilteredHandler(FilteredEventArgs args)
    {
        var columnName       = args.ColumnName;
        var filterPredicates = args.FilterPredicates;
    }
    void FilterDialogOpeningHandler(FilterDialogOpeningEventArgs args)
    {
        // args.FilterOperators = ...; args.FilterChoiceCount = ...;
    }
}
```

---

## Filter Enum Column

Use `FilterTemplate` with `SfDropDownList` bound to enum values. Apply via `FilterByColumnAsync` in `ValueChange`:

```razor
<GridColumn Field="Type" HeaderText="Type" Type="ColumnType.String" Width="130">
    <FilterTemplate>
        <SfDropDownList Placeholder="Type" ID="Type" Value="@((string)(context as PredicateModel).Value)"
                        DataSource="@FilterDropData" TValue="string" TItem="Data">
            <DropDownListEvents TItem="Data" ValueChange="Change" TValue="string"></DropDownListEvents>
            <DropDownListFieldSettings Value="Type" Text="Type"></DropDownListFieldSettings>
        </SfDropDownList>
    </FilterTemplate>
</GridColumn>
@code {
    List<Data> FilterDropData = new List<Data>
    {
        new Data() { Type = "All" }, new Data() { Type = "Base" },
        new Data() { Type = "Replace" }, new Data() { Type = "Delta" }
    };
    public async Task Change(ChangeEventArgs<string, Data> args)
    {
        if (args.Value == "All") await Grid.ClearFilteringAsync();
        else await Grid.FilterByColumnAsync("Type", "contains", args.Value);
    }
    public class Data { public string Type { get; set; } }
}
```
