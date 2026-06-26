# Data Binding in Syncfusion Blazor AutoComplete

## Table of Contents
- [Overview](#overview)
- [Binding Local Data](#binding-local-data)
  - [Primitive Types](#primitive-types)
  - [Object Collections](#object-collections)
  - [ObservableCollection](#observablecollection)
  - [Dynamic Objects](#dynamic-objects)
- [Remote Data](#remote-data)
  - [Web API](#web-api)
  - [OData Services](#odata-services)
  - [Custom Adaptor](#custom-adaptor)
- [DataBound Event](#databound-event)

## Overview

The AutoComplete component loads data through the **DataSource** property. It supports multiple data source types:
- Arrays and Lists of primitives (string, int, etc.)
- Collections of objects
- Remote services (Web APIs, OData)
- Dynamic objects (ExpandoObject, DynamicObject)
- ObservableCollection for real-time updates

## Binding Local Data

### Primitive Types

Bind arrays or lists of simple data types like strings and integers.

**String Array:**
```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                Placeholder="Select a country">
</SfAutoComplete>

@code {
    private List<string> Countries = new()
    {
        "Austria",
        "Brazil", 
        "Canada",
        "Denmark",
        "Egypt",
        "Finland"
    };
}
```

**Integer Array:**
```blazor
<SfAutoComplete TValue="int" TItem="int" 
                DataSource="@Numbers"
                Placeholder="Select a number">
</SfAutoComplete>

@code {
    private List<int> Numbers = new() { 10, 20, 30, 40, 50 };
}
```

### Object Collections

Map object properties to AutoComplete fields using **AutoCompleteFieldSettings**.

**Basic Object Binding:**
```blazor
<SfAutoComplete TValue="string" TItem="Country" 
                DataSource="@Countries"
                Placeholder="Select a country">
    <AutoCompleteFieldSettings Value="CountryName"></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Country
    {
        public string CountryName { get; set; }
        public string Code { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { CountryName = "Austria", Code = "AT" },
        new Country { CountryName = "Brazil", Code = "BR" },
        new Country { CountryName = "Canada", Code = "CA" }
    };
}
```

**Complex Object with Display Text:**
```blazor
<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees"
                Placeholder="Select an employee">
    <AutoCompleteFieldSettings Value="EmployeeName" >
    </AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public string Department { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, EmployeeName = "John Smith", Department = "IT" },
        new Employee { EmployeeId = 2, EmployeeName = "Jane Doe", Department = "HR" },
        new Employee { EmployeeId = 3, EmployeeName = "Bob Wilson", Department = "Sales" }
    };
}
```

### ObservableCollection

Use **ObservableCollection** when you need to dynamically add or remove items and have the UI update automatically.

```blazor
@using Syncfusion.Blazor.DropDowns
@using System.Collections.ObjectModel

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                Placeholder="Select a country">
</SfAutoComplete>

<button @onclick="AddCountry">Add Country</button>

@code {
    private ObservableCollection<string> Countries = new()
    {
        "Austria",
        "Brazil",
        "Canada"
    };

    private void AddCountry()
    {
        Countries.Add("Denmark");
    }
}
```

### Dynamic Objects

**ExpandoObject:**
```blazor
@using Syncfusion.Blazor.DropDowns
@using System.Dynamic

<SfAutoComplete TValue="string" TItem="dynamic" 
                DataSource="@DynamicCountries"
                Placeholder="Select a country">
    <AutoCompleteFieldSettings Value="CountryName"></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    private List<dynamic> DynamicCountries = new();

    protected override void OnInitialized()
    {
        DynamicCountries = new()
        {
            CreateDynamic("Austria", "AT"),
            CreateDynamic("Brazil", "BR"),
            CreateDynamic("Canada", "CA")
        };
    }

    private dynamic CreateDynamic(string name, string code)
    {
        dynamic obj = new ExpandoObject();
        obj.CountryName = name;
        obj.CountryCode = code;
        return obj;
    }
}
```

## Remote Data

### Web API

Fetch data from a Web API endpoint using **SfDataManager**:

```blazor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfAutoComplete TValue="string" TItem="Product" 
                AllowFiltering="true"
                DebounceDelay="300">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
                   Adaptor="Syncfusion.Blazor.Adaptors.UrlAdaptor">
    </SfDataManager>
    <AutoCompleteFieldSettings Value="ProductName" ></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal Price { get; set; }
    }
}
```

### OData Services

Connect to OData endpoints like SharePoint or Azure Data Services:

```blazor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfAutoComplete TValue="string" TItem="Order" 
                AllowFiltering="true"
                DebounceDelay="300">
    <SfDataManager Url="YOUR_ODATA_SERVICE_URL" 
                   Adaptor="Syncfusion.Blazor.Adaptors.ODataAdaptor">
    </SfDataManager>
    <AutoCompleteFieldSettings Value="CustomerID"></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Order
    {
        public int OrderID { get; set; }
        public string CustomerID { get; set; }
        public DateTime OrderDate { get; set; }
    }
}
```

**With Query Filter:**
```blazor
<SfAutoComplete TValue="string" TItem="Order" 
                AllowFiltering="true">
    <SfDataManager Url="YOUR_ODATA_SERVICE_URL" 
                   Adaptor="Syncfusion.Blazor.Adaptors.ODataAdaptor">
        <SfDataManagerRequest PageSize="10"></SfDataManagerRequest>
    </SfDataManager>
</SfAutoComplete>
```

### Custom Adaptor

For custom data sources or business logic:

```blazor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfAutoComplete TValue="string" TItem="Product" 
                AllowFiltering="true">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)">
    </SfDataManager>
</SfAutoComplete>

@code {
    public class CustomAdaptor : DataAdaptor
    {
        public override async Task<Object> Read(DataManagerRequest dm, string key = null)
        {
            // Call your API or database here
            var products = await GetProductsAsync();
            
            // Handle filtering if dm.Search contains search text
            if (dm.Search != null && dm.Search.Count > 0)
            {
                var searchKey = dm.Search[0];
                products = products.Where(p => p.ProductName.Contains(searchKey)).ToList();
            }
            
            return products;
        }

        private async Task<List<Product>> GetProductsAsync()
        {
            // Fetch from your API
            return new() { /* ... */ };
        }
    }

    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
    }
}
```

## DataBound Event

The **DataBound** event fires after data is loaded into the AutoComplete. Use it to perform post-processing or notifications:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries">
    <AutoCompleteEvents TValue="string" TItem="string"
                        DataBound="@OnDataBound">
    </AutoCompleteEvents>
</SfAutoComplete>

<p>@LoadMessage</p>

@code {
    private List<string> Countries = new() { "Austria", "Brazil", "Canada" };
    private string LoadMessage = "";

    private void OnDataBound(DataBoundEventArgs args)
    {
        LoadMessage = "Data loaded successfully";
    }
}
```

## Best Practices

1. **Use DebounceDelay for Remote Data:** Reduce server requests by adding a delay before filter requests
2. **Lazy Load Large Datasets:** Use pagination or virtualization instead of loading all data at once
3. **Map Fields Explicitly:** Always use AutoCompleteFieldSettings to clarify which property is the display value
4. **Handle Null Values:** Check for null before accessing nested properties in complex objects
5. **Use ObservableCollection for Dynamic Updates:** When items change after initial load, use ObservableCollection for automatic UI updates

## Related Topics

- [Filtering & Search](filtering-and-search.md)
- [Templates & Styling](templates-and-styling.md)
- [Advanced Features](advanced-features.md)
