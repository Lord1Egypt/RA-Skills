# Cascading ComboBox

Cascading ComboBox creates dependent dropdown chains where child ComboBox options depend on the parent's selection.

## Basic Cascading Pattern

Create a two-level cascade (Country → State):

```razor
@using Syncfusion.Blazor.DropDowns

<div class="form-group">
    <label>Country:</label>
    <SfComboBox TItem="Country" TValue="int"
        Placeholder="Select a country"
        DataSource="@Countries"
        @bind-Value="@SelectedCountry">
        <ComboBoxEvents TItem="Country" TValue="int"
            ValueChange="@OnCountryChange"></ComboBoxEvents>
        <ComboBoxFieldSettings Text="CountryName" Value="CountryId"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

<div class="form-group" style="margin-top: 20px;">
    <label>State:</label>
    <SfComboBox TItem="State" TValue="int"
        Placeholder="Select a state"
        DataSource="@States"
        @bind-Value="@SelectedState"
        Enabled="@(SelectedCountry > 0)">
        <ComboBoxFieldSettings Text="StateName" Value="StateId"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

@code {
    private int SelectedCountry = 0;
    private int SelectedState = 0;
    private List<State> States = new();

    public class Country
    {
        public int CountryId { get; set; }
        public string CountryName { get; set; }
    }

    public class State
    {
        public int StateId { get; set; }
        public string StateName { get; set; }
        public int CountryId { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { CountryId = 1, CountryName = "United States" },
        new Country { CountryId = 2, CountryName = "Canada" },
        new Country { CountryId = 3, CountryName = "Mexico" }
    };

    private List<State> AllStates = new()
    {
        new State { StateId = 1, StateName = "California", CountryId = 1 },
        new State { StateId = 2, StateName = "Texas", CountryId = 1 },
        new State { StateId = 3, StateName = "New York", CountryId = 1 },
        new State { StateId = 4, StateName = "Ontario", CountryId = 2 },
        new State { StateId = 5, StateName = "Quebec", CountryId = 2 },
        new State { StateId = 6, StateName = "Jalisco", CountryId = 3 }
    };

    private void OnCountryChange(ChangeEventArgs<int, Country> args)
    {
        // Filter states based on selected country
        States = AllStates.Where(s => s.CountryId == args.Value).ToList();
        
        // Reset state selection
        SelectedState = 0;
    }
}
```

---

## Three-Level Cascading

Create a three-level cascade (Country → State → City):

```razor
@using Syncfusion.Blazor.DropDowns

<div class="form-group">
    <label>Country:</label>
    <SfComboBox TItem="Country" TValue="int"
        Placeholder="Select a country"
        DataSource="@Countries"
        @bind-Value="@SelectedCountry">
        <ComboBoxEvents TItem="Country" TValue="int"
            ValueChange="@OnCountryChange"></ComboBoxEvents>
        <ComboBoxFieldSettings Text="CountryName" Value="CountryId"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

<div class="form-group">
    <label>State:</label>
    <SfComboBox TItem="State" TValue="int"
        Placeholder="Select a state"
        DataSource="@States"
        @bind-Value="@SelectedState"
        Enabled="@(SelectedCountry > 0)">
        <ComboBoxEvents TItem="State" TValue="int"
            ValueChange="@OnStateChange"></ComboBoxEvents>
        <ComboBoxFieldSettings Text="StateName" Value="StateId"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

<div class="form-group">
    <label>City:</label>
    <SfComboBox TItem="City" TValue="int"
        Placeholder="Select a city"
        DataSource="@Cities"
        @bind-Value="@SelectedCity"
        Enabled="@(SelectedState > 0)">
        <ComboBoxFieldSettings Text="CityName" Value="CityId"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

@code {
    private int SelectedCountry = 0;
    private int SelectedState = 0;
    private int SelectedCity = 0;
    private List<State> States = new();
    private List<City> Cities = new();

    public class Country
    {
        public int CountryId { get; set; }
        public string CountryName { get; set; }
    }

    public class State
    {
        public int StateId { get; set; }
        public string StateName { get; set; }
        public int CountryId { get; set; }
    }

    public class City
    {
        public int CityId { get; set; }
        public string CityName { get; set; }
        public int StateId { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { CountryId = 1, CountryName = "United States" },
        new Country { CountryId = 2, CountryName = "Canada" }
    };

    private List<State> AllStates = new()
    {
        new State { StateId = 1, StateName = "California", CountryId = 1 },
        new State { StateId = 2, StateName = "Texas", CountryId = 1 },
        new State { StateId = 3, StateName = "Ontario", CountryId = 2 }
    };

    private List<City> AllCities = new()
    {
        new City { CityId = 1, CityName = "Los Angeles", StateId = 1 },
        new City { CityId = 2, CityName = "San Francisco", StateId = 1 },
        new City { CityId = 3, CityName = "Houston", StateId = 2 },
        new City { CityId = 4, CityName = "Toronto", StateId = 3 }
    };

    private void OnCountryChange(ChangeEventArgs<int, Country> args)
    {
        States = AllStates.Where(s => s.CountryId == args.Value).ToList();
        SelectedState = 0;
        Cities = new();
        SelectedCity = 0;
    }

    private void OnStateChange(ChangeEventArgs<int, State> args)
    {
        Cities = AllCities.Where(c => c.StateId == args.Value).ToList();
        SelectedCity = 0;
    }
}
```

---

## Cascading with Form Field Population

Populate other form fields based on ComboBox selection:

```razor
@using Syncfusion.Blazor.DropDowns

<div class="form-group">
    <label>Select Country:</label>
    <SfComboBox TItem="Country" TValue="int"
        Placeholder="Choose a country"
        DataSource="@Countries"
        @bind-Value="@SelectedCountry">
        <ComboBoxEvents TItem="Country" TValue="int"
            ValueChange="@OnCountryChange"></ComboBoxEvents>
        <ComboBoxFieldSettings Text="Name" Value="CountryId"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

<div style="margin-top: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 4px;">
    <h4>Country Details</h4>
    @if (SelectedCountryData != null)
    {
        <div class="form-group">
            <label>Country Code:</label>
            <input type="text" class="form-control" value="@SelectedCountryData.Code" readonly />
        </div>
        <div class="form-group">
            <label>Capital:</label>
            <input type="text" class="form-control" value="@SelectedCountryData.Capital" readonly />
        </div>
        <div class="form-group">
            <label>Continent:</label>
            <input type="text" class="form-control" value="@SelectedCountryData.Continent" readonly />
        </div>
        <div class="form-group">
            <label>Population:</label>
            <input type="text" class="form-control" value="@SelectedCountryData.Population" readonly />
        </div>
    }
    else
    {
        <p>Select a country to view details</p>
    }
</div>

@code {
    private int SelectedCountry = 0;
    private Country SelectedCountryData;

    public class Country
    {
        public int CountryId { get; set; }
        public string Name { get; set; }
        public string Code { get; set; }
        public string Capital { get; set; }
        public string Continent { get; set; }
        public long Population { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country 
        { 
            CountryId = 1, 
            Name = "United States", 
            Code = "USA", 
            Capital = "Washington DC", 
            Continent = "North America",
            Population = 331000000
        },
        new Country 
        { 
            CountryId = 2, 
            Name = "Canada", 
            Code = "CA", 
            Capital = "Ottawa", 
            Continent = "North America",
            Population = 38250000
        },
        new Country 
        { 
            CountryId = 3, 
            Name = "Mexico", 
            Code = "MX", 
            Capital = "Mexico City", 
            Continent = "North America",
            Population = 128000000
        }
    };

    private void OnCountryChange(ChangeEventArgs<int, Country> args)
    {
        SelectedCountryData = args.ItemData;
    }
}
```

---

## Dynamic Data Loading from API

Cascade ComboBox with data loaded from a remote API:

```razor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<div class="form-group">
    <label>Category:</label>
    <SfComboBox TItem="Category" TValue="int"
        Placeholder="Select a category"
        AllowFiltering="true"
        DataSource="@Categories"
        @bind-Value="@SelectedCategory">
        <ComboBoxEvents TItem="Category" TValue="int"
            ValueChange="@OnCategoryChange"></ComboBoxEvents>
        <ComboBoxFieldSettings Text="CategoryName" Value="CategoryId"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

<div class="form-group" style="margin-top: 20px;">
    <label>Product:</label>
    <SfComboBox TItem="Product" TValue="int"
        Placeholder="Select a product"
        AllowFiltering="true"
        Enabled="@(SelectedCategory > 0)">
        <SfDataManager Url="@ProductApiUrl" 
            Adaptor="Syncfusion.Blazor.Adaptors.UrlAdaptor"></SfDataManager>
        <ComboBoxFieldSettings Text="ProductName" Value="ProductId"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

@code {
    private int SelectedCategory = 0;
    private string ProductApiUrl = "";

    public class Category
    {
        public int CategoryId { get; set; }
        public string CategoryName { get; set; }
    }

    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal Price { get; set; }
    }

    private List<Category> Categories = new()
    {
        new Category { CategoryId = 1, CategoryName = "Electronics" },
        new Category { CategoryId = 2, CategoryName = "Clothing" },
        new Category { CategoryId = 3, CategoryName = "Books" }
    };

    private void OnCategoryChange(ChangeEventArgs<int, Category> args)
    {
        SelectedCategory = args.Value;
        // Build API URL with category filter
        ProductApiUrl = $"YOUR_API_ENDPOINT";
    }
}
```

---

## Best Practices

1. **Always Filter Child Data**
   - Clear child data when parent selection changes
   - Reset child selection to 0

2. **Disable Child ComboBox Until Parent is Selected**
   ```razor
   Enabled="@(SelectedCountry > 0)"
   ```

3. **Use OnInitializedAsync for Initial Data**
   ```razor
   protected override async Task OnInitializedAsync()
   {
       Countries = await LoadCountries();
   }
   ```

4. **Handle No Data Scenario**
   - Show "No items available" message
   - Disable empty ComboBox

5. **Use ValueChange Event for Updates**
   - More reliable than Index binding
   - Gets full ItemData

---

## Common Issues

**Problem: Child ComboBox not updating**
- Ensure `ValueChange` event calls filter logic
- Verify StateHasChanged() or re-assignment triggers UI update

**Problem: Selection persists when parent changes**
- Explicitly reset child value: `SelectedChild = 0`
- Rebuild child data list

**Problem: API calls on every render**
- Use local caching
- Only fetch when parent selection changes

---

*See also: [Data Binding](data-binding.md), [Selection & Value](selection-and-value.md), [Events & Validation](events-and-validation.md)*
