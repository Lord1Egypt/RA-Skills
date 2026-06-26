# Data Binding in Blazor ListBox

## Table of Contents
- [Binding Array of Strings](#binding-array-of-strings)
- [Binding Array of Objects](#binding-array-of-objects)
- [Binding Complex Objects](#binding-complex-objects)
- [Remote Data (DataManager)](#remote-data-datamanager)
- [Dynamic Data Updates](#dynamic-data-updates)
- [Field Settings Reference](#field-settings-reference)
- [Best Practices](#best-practices)

## Binding Array of Strings

The simplest form of data binding uses an array of strings. Both the display text and the value resolve to the same string.

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@Games" TItem="string"></SfListBox>

@code {
    public string[] Games = new string[] 
    { 
        "Badminton", 
        "Cricket", 
        "Football", 
        "Golf", 
        "Tennis", 
        "Basket Ball", 
        "Base Ball", 
        "Hockey", 
        "Volley Ball" 
    };
}
```

**When to Use:**
- Simple lists where display text equals the value
- Categories, tags, or enumerations
- No need to map display vs. internal IDs
- Quick prototyping

**Result:**
- Display: "Badminton"
- Selected Value: "Badminton"

## Binding Array of Objects

Most real-world scenarios use objects where one property displays while another stores the value. Use `ListBoxFieldSettings` to map these properties.

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>

@code {
    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-02" },
        new VehicleData { Text = "Bugatti Veyron Super Sport", Id = "Vehicle-03" },
        new VehicleData { Text = "SSC Ultimate Aero", Id = "Vehicle-04" },
        new VehicleData { Text = "Koenigsegg CCR", Id = "Vehicle-05" },
        new VehicleData { Text = "McLaren F1", Id = "Vehicle-06" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
    }
}
```

**Field Settings:**
- `Text="Text"` - Property to display in the list
- `Value="Id"` - Property to use as the selected value

**Accessing Selected Values:**

```razor
<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData" @bind-Value="@SelectedIds">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>

<p>Selected IDs: @string.Join(", ", SelectedIds ?? new string[] { })</p>

@code {
    public string[] SelectedIds { get; set; }
    
    // ... Vehicles list ...
}
```

**Display: "Hennessey Venom" → Selected Value: "Vehicle-01"**

## Binding Complex Objects

For nested or complex object structures, map the properties using dot notation.

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@SportsDetails" TItem="SportsData">
    <ListBoxFieldSettings Text="Sports.Name" Value="Id" />
</SfListBox>

@code {
    public List<SportsData> SportsDetails = new List<SportsData>
    {
        new SportsData { Id = "game0", Sports = new GameData { Name = "Badminton" } },
        new SportsData { Id = "game1", Sports = new GameData { Name = "Cricket" } },
        new SportsData { Id = "game2", Sports = new GameData { Name = "Football" } },
        new SportsData { Id = "game3", Sports = new GameData { Name = "Golf" } },
        new SportsData { Id = "game4", Sports = new GameData { Name = "Tennis" } },
        new SportsData { Id = "game5", Sports = new GameData { Name = "Basket Ball" } }
    };

    public class GameData
    {
        public string Name { get; set; }
    }

    public class SportsData
    {
        public string Id { get; set; }
        public GameData Sports { get; set; }
    }
}
```

**Nested Mapping:**
- `Text="Sports.Name"` - Maps to nested `Sports.Name` property
- `Value="Id"` - Top-level `Id` property

**Important:** Ensure nested properties are not null to avoid binding errors.

## Remote Data (DataManager)

Fetch data from remote APIs or OData services using `SfDataManager`.

### REST API Example

```razor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfListBox TValue="string[]" TItem="OrderDetails" Query="@RemoteDataQuery">
    <SfDataManager Url="YOUR_ODATA_SERVICE_URL" 
                   CrossDomain="true" 
                   Adaptor="Syncfusion.Blazor.Adaptors.ODataAdaptor">
    </SfDataManager>
    <ListBoxFieldSettings Text="CustomerID" Value="OrderID" />
</SfListBox>

@code {
    public Query RemoteDataQuery = new Query().Select(new List<string> { "CustomerID", "OrderID" }).Take(6);

    public class OrderDetails
    {
        public int OrderID { get; set; }
        public string CustomerID { get; set; }
        public int EmployeeID { get; set; }
        public double Freight { get; set; }
        public string ShipCity { get; set; }
        public DateTime OrderDate { get; set; }
    }
}
```

### Custom API with JSON Adaptor

```razor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfListBox TValue="string[]" TItem="ProductData" Query="@ApiQuery">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
                   Adaptor="Syncfusion.Blazor.Adaptors.JsonAdaptor">
    </SfDataManager>
    <ListBoxFieldSettings Text="Name" Value="Id" />
</SfListBox>

@code {
    public Query ApiQuery = new Query().Select(new List<string> { "Id", "Name", "Category" }).Take(10);

    public class ProductData
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Category { get; set; }
    }
}
```

**DataManager Features:**
- `Url` - API endpoint
- `CrossDomain="true"` - Enable CORS
- `Adaptor` - Data format (ODataAdaptor, JsonAdaptor, UrlAdaptor, etc.)
- `Query` - Filter, select, and limit results

**Query Methods:**
- `.Select(new List<string> { "field1", "field2" })` - Choose specific fields
- `.Take(n)` - Limit to n records
- `.Skip(n)` - Skip first n records
- `.Where("field", "equal", "value")` - Filter data
- `.RequiresCount()` - Include total count

## Dynamic Data Updates

Update the ListBox data at runtime by modifying the data source.

### Adding Items

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@Items" TItem="ItemData">
    <ListBoxFieldSettings Text="Name" Value="Id" />
</SfListBox>

<button @onclick="AddItem">Add Item</button>

@code {
    public List<ItemData> Items = new List<ItemData>
    {
        new ItemData { Id = "1", Name = "Item 1" },
        new ItemData { Id = "2", Name = "Item 2" }
    };

    private void AddItem()
    {
        Items.Add(new ItemData { Id = "3", Name = "Item 3" });
        StateHasChanged(); // Notify component to re-render
    }

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
    }
}
```

### Removing Items

```razor
<button @onclick="RemoveItem">Remove Selected</button>

@code {
    private void RemoveItem()
    {
        if (Items.Count > 0)
        {
            Items.RemoveAt(0);
            StateHasChanged();
        }
    }
}
```

### Clearing All Items

```razor
<button @onclick="ClearItems">Clear All</button>

@code {
    private void ClearItems()
    {
        Items.Clear();
        StateHasChanged();
    }
}
```

### Real-time Data Binding

```razor
<SfListBox TValue="string[]" DataSource="@Items" @ref="ListBoxRef">
    <ListBoxFieldSettings Text="Name" Value="Id" />
</SfListBox>

<button @onclick="RefreshData">Refresh from API</button>

@code {
    private SfListBox<string[], ItemData> ListBoxRef;

    private async Task RefreshData()
    {
        Items = await FetchDataFromApi();
        await ListBoxRef.Refresh();
    }

    private async Task<List<ItemData>> FetchDataFromApi()
    {
        // Simulate API call
        return new List<ItemData>
        {
            new ItemData { Id = "1", Name = "Updated Item 1" }
        };
    }
}
```

## Field Settings Reference

The `ListBoxFieldSettings` property maps object properties to display and value fields.

**Available Field Mappings:**

| Property | Type | Description |
|----------|------|-------------|
| `Text` | string | Property name for display text |
| `Value` | string | Property name for selected value |
| `GroupBy` | string | Property name for grouping items |
| `IconCss` | string | Property name for icon CSS classes |
| `HtmlAttributes` | string | Property name for HTML attributes object |

### Grouping Example

```razor
<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" GroupBy="Category" />
</SfListBox>

@code {
    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Audi A4", Id = "Vehicle-01", Category = "Luxury" },
        new VehicleData { Text = "Tesla Model 3", Id = "Vehicle-02", Category = "Electric" },
        new VehicleData { Text = "BMW M5", Id = "Vehicle-03", Category = "Luxury" },
        new VehicleData { Text = "Nissan Leaf", Id = "Vehicle-04", Category = "Electric" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
        public string Category { get; set; }
    }
}
```

## Best Practices

### 1. Match Type Parameters Correctly

```razor
<!-- For array of strings -->
<SfListBox TValue="string[]" DataSource="@StringArray" TItem="string"></SfListBox>

<!-- For array of objects -->
<SfListBox TValue="string[]" DataSource="@ObjectList" TItem="MyObject"></SfListBox>
```

### 2. Handle Null Data

```razor
@code {
    public List<VehicleData> Vehicles = new List<VehicleData>();

    protected override async Task OnInitializedAsync()
    {
        try
        {
            Vehicles = await FetchVehicles();
        }
        catch (Exception ex)
        {
            // Log error
        }
    }
}
```

### 3. Use Immutable Updates for Complex Scenarios

```razor
private void AddItem(ItemData newItem)
{
    Items = new List<ItemData>(Items) { newItem };
    StateHasChanged();
}
```

### 4. Cache Remote Data

```razor
private List<VehicleData> _cachedVehicles;

private async Task<List<VehicleData>> GetVehicles()
{
    if (_cachedVehicles == null)
    {
        _cachedVehicles = await FetchFromApi();
    }
    return _cachedVehicles;
}
```

### 5. Validate Data Before Binding

```razor
@code {
    private void BindData(List<VehicleData> data)
    {
        if (data != null && data.Any())
        {
            Vehicles = data;
            StateHasChanged();
        }
    }
}
```

## Common Issues

### Issue: Data Not Displaying

**Cause:** Field names don't match property names

**Solution:**
```razor
<!-- WRONG: Property is "ProductName" but Text="Name" -->
<ListBoxFieldSettings Text="Name" Value="Id" />

<!-- CORRECT: Match actual property name -->
<ListBoxFieldSettings Text="ProductName" Value="Id" />
```

### Issue: Remote Data Takes Too Long

**Cause:** Fetching too many records

**Solution:**
```razor
<!-- Add Take() to limit results -->
public Query RemoteDataQuery = new Query().Take(25);
```

### Issue: Nested Property Not Found

**Cause:** Null parent property

**Solution:**
```razor
@code {
    public List<SportsData> SportsDetails = new List<SportsData>
    {
        // Ensure Sports object is always initialized
        new SportsData { Id = "game1", Sports = new GameData { Name = "Cricket" } }
    };
}
```
