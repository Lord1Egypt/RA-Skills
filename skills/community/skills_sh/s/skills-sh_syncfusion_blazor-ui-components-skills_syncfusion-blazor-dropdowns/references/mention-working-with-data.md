# Working with Data in Blazor Mention Component

## Table of Contents
- [Overview](#overview)
- [Local Data Binding](#local-data-binding)
- [Primitive Data Types](#primitive-data-types)
- [Complex Data Objects](#complex-data-objects)
- [ExpandoObject Binding](#expandoobject-binding)
- [Enum Data Binding](#enum-data-binding)
- [Remote Data Binding](#remote-data-binding)
- [Data Events](#data-events)
- [Error Handling](#error-handling)

---

## Overview

The Mention component uses the `DataSource` property to populate mention suggestions. You can bind data from:
- **Local sources:** Collections in C# code
- **Remote services:** APIs using DataManager with adaptors
- **Enums:** Predefined enumeration values
- **Dynamic objects:** ExpandoObject for flexible data

Each data type supports the `TItem` generic parameter and `MentionFieldSettings` for mapping display and value fields.

---

## Local Data Binding

### Basic Local List

```razor
<SfMention TItem="PersonData" DataSource="@Persons">
    <TargetComponent>
        <div id="mention" contenteditable="true" placeholder="Type @..."></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class PersonData
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }

    List<PersonData> Persons = new()
    {
        new() { Id = 1, Name = "Alice" },
        new() { Id = 2, Name = "Bob" },
        new() { Id = 3, Name = "Carol" }
    };
}
```

**Key Points:**
- `DataSource` accepts `IEnumerable<TItem>`
- `MentionFieldSettings.Text` specifies display field
- `MentionFieldSettings.Value` specifies internal value (optional)

### Dynamic Data Loading

```razor
@code {
    List<PersonData> LocalData;

    protected override void OnInitialized()
    {
        // Load data from database, file, or service
        LocalData = FetchPersonsFromDatabase();
    }

    private List<PersonData> FetchPersonsFromDatabase()
    {
        // Simulated database fetch
        return new()
        {
            new() { Id = 1, Name = "Alice", Email = "alice@company.com" },
            new() { Id = 2, Name = "Bob", Email = "bob@company.com" }
        };
    }
}
```

---

## Primitive Data Types

### String Array

```razor
<SfMention TItem="string" DataSource="@EmailList">
    <TargetComponent>
        <div id="emailMention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text=""></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<string> EmailList = new()
    {
        "alice@company.com",
        "bob@company.com",
        "carol@company.com"
    };
}
```

### Integer Array

```razor
<SfMention TItem="int" DataSource="@ProjectIds">
    <TargetComponent>
        <input id="projectMention" type="text" placeholder="Type @ for project IDs..." />
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text=""></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<int> ProjectIds = new() { 101, 102, 103, 104, 105 };
}
```

---

## Complex Data Objects

### Multiple Field Mapping

```razor
<SfMention TItem="EmployeeData" DataSource="@Employees">
    <TargetComponent>
        <div id="empMention" contenteditable="true" placeholder="Type @..."></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings 
            Text="EmployeeName" 
            Value="EmployeeId">
        </MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class EmployeeData
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public string Department { get; set; }
        public string Email { get; set; }
    }

    List<EmployeeData> Employees = new()
    {
        new() { EmployeeId = 1, EmployeeName = "Alice Johnson", Department = "Engineering", Email = "alice@company.com" },
        new() { EmployeeId = 2, EmployeeName = "Bob Smith", Department = "Marketing", Email = "bob@company.com" },
        new() { EmployeeId = 3, EmployeeName = "Carol White", Department = "Sales", Email = "carol@company.com" }
    };
}
```

**Field Mappings:**
- `Text`: Displayed in suggestions and inserted as mention text
- `Value`: Internal identifier (accessible in events, not displayed)
- Other properties: Can be accessed in templates

### Nested Object Access

```razor
@code {
    public class DepartmentInfo
    {
        public int DeptId { get; set; }
        public string DeptName { get; set; }
    }

    public class EmployeeWithDept
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public DepartmentInfo Department { get; set; }
    }

    // Note: For nested properties, flatten during data preparation
    List<EmployeeWithDept> FlattenedEmployees = new()
    {
        new() { Id = 1, Name = "Alice", Department = new() { DeptId = 1, DeptName = "Engineering" } }
    };
}
```

---

## ExpandoObject Binding

### Dynamic Properties at Runtime

```razor
<SfMention TItem="dynamic" DataSource="@DynamicUsers">
    <TargetComponent>
        <div id="dynamicMention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="UserName"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    using System.Dynamic;

    List<ExpandoObject> DynamicUsers = CreateDynamicUsers();

    static List<ExpandoObject> CreateDynamicUsers()
    {
        var users = new List<ExpandoObject>();

        dynamic user1 = new ExpandoObject();
        user1.UserId = 1;
        user1.UserName = "Alice";
        user1.Role = "Admin";
        users.Add(user1);

        dynamic user2 = new ExpandoObject();
        user2.UserId = 2;
        user2.UserName = "Bob";
        user2.Role = "User";
        users.Add(user2);

        return users;
    }
}
```

**Use Cases:**
- Schema-less data from external APIs
- Adding properties dynamically without class definition
- Flexible response handling from different services

---

## Enum Data Binding

### Using Enumeration Values

```razor
<SfMention TItem="Priority" DataSource="@PriorityList">
    <TargetComponent>
        <input id="priorityMention" type="text" placeholder="Type @ for priority..." />
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text=""></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public enum Priority
    {
        Low,
        Medium,
        High,
        Critical
    }

    List<Priority> PriorityList = Enum.GetValues(typeof(Priority))
        .Cast<Priority>()
        .ToList();
}
```

### Enum with Display Names

```razor
<SfMention TItem="PriorityData" DataSource="@PriorityOptions">
    <TargetComponent>
        <div id="enumMention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="DisplayName" Value="PriorityValue"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class PriorityData
    {
        public Priority PriorityValue { get; set; }
        public string DisplayName { get; set; }
    }

    public enum Priority
    {
        Low,
        Medium,
        High
    }

    List<PriorityData> PriorityOptions = new()
    {
        new() { PriorityValue = Priority.Low, DisplayName = "🟢 Low Priority" },
        new() { PriorityValue = Priority.Medium, DisplayName = "🟡 Medium Priority" },
        new() { PriorityValue = Priority.High, DisplayName = "🔴 High Priority" }
    };
}
```

---

## Remote Data Binding

### OData v4 Service

```razor
<SfMention TItem="CustomerData">
    <TargetComponent>
        <div id="odataMention" contenteditable="true" placeholder="Type @..."></div>
    </TargetComponent>
    <ChildContent>
        <SfDataManager Url="YOUR_ODATA_SERVICE_URL" 
                       Adaptor="Adaptors.ODataV4Adaptor">
        </SfDataManager>
        <MentionFieldSettings Text="ContactName"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class CustomerData
    {
        public string CustomerID { get; set; }
        public string ContactName { get; set; }
        public string CompanyName { get; set; }
    }
}
```

**Result:** Fetches customer names from public Northwind OData service.

### Web API Adaptor

```razor
<SfMention TItem="UserData">
    <TargetComponent>
        <input id="apiMention" type="text" placeholder="Search users..." />
    </TargetComponent>
    <ChildContent>
        <SfDataManager Url="YOUR_API_ENDPOINT" 
                       Adaptor="Adaptors.WebApiAdaptor">
        </SfDataManager>
        <MentionFieldSettings Text="Name" Value="UserId"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class UserData
    {
        public int UserId { get; set; }
        public string Name { get; set; }
        public string Email { get; set; }
    }
}
```

**Endpoint Format:**
```
GET /api/users?$top=25&$skip=0&$filter=Name startswith 'alice'
```

### Offline Mode (Caching)

```razor
<SfMention TItem="ProductData">
    <TargetComponent>
        <div id="offlineMention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <SfDataManager Url="YOUR_API_ENDPOINT" 
                       Adaptor="Adaptors.ODataV4Adaptor"
                       Offline="true">
        </SfDataManager>
        <MentionFieldSettings Text="ProductName"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class ProductData
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
    }
}
```

**Benefits:**
- First fetch caches data locally
- Subsequent requests use cache (faster)
- Server fallback if cache unavailable
- Reduces API calls

---

## Data Events

### OnActionBegin

Triggered when data fetch starts (e.g., on first `@` keypress):

```razor
<SfMention TItem="PersonData" 
           DataSource="@Persons"
           OnActionBegin="ActionBegin">
    <!-- Component content -->
</SfMention>

@code {
    async Task ActionBegin(ActionBeginEventArgs Args)
    {
        Console.WriteLine($"Data fetch started. Action: {Args.RequestType}");
        // Log event, show loading indicator, etc.
    }
}
```

### OnActionComplete

Triggered after data successfully fetches:

```razor
<SfMention TItem="PersonData" 
           DataSource="@Persons"
           OnActionComplete="ActionComplete">
    <!-- Component content -->
</SfMention>

@code {
    async Task ActionComplete(ActionCompleteEventArgs<PersonData> Args)
    {
        Console.WriteLine($"Data loaded: {Args.Result?.Count()} items");
        // Process loaded data, update UI, etc.
    }
}
```

### OnActionFailure

Triggered when data fetch fails:

```razor
<SfMention TItem="PersonData"
           OnActionFailure="ActionFailure">
    <TargetComponent>
        <div id="mention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <SfDataManager Url="YOUR_API_ENDPOINT" 
                       Adaptor="Adaptors.WebApiAdaptor">
        </SfDataManager>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    void ActionFailure(FailureEventArgs Args)
    {
        Console.WriteLine($"Error: {Args.Error}");
        // Show error message to user
    }
}
```

---

## Error Handling

### Null or Empty Data

```razor
@code {
    List<PersonData> SafeData = GetDataWithFallback();

    private List<PersonData> GetDataWithFallback()
    {
        try
        {
            var data = FetchFromAPI();
            return data ?? new List<PersonData>(); // Fallback to empty
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Data fetch failed: {ex.Message}");
            return new List<PersonData>(); // Return empty instead of null
        }
    }
}
```

### Validate Data Before Binding

```razor
@code {
    List<PersonData> ValidateAndBind(List<PersonData> rawData)
    {
        if (rawData == null || rawData.Count == 0)
        {
            Console.WriteLine("Warning: Empty data source");
            return new List<PersonData>();
        }

        // Remove invalid entries
        return rawData.Where(p => !string.IsNullOrEmpty(p.Name)).ToList();
    }
}
```

---

## Next Steps

- **Enhance filtering:** See [Filtering & Search](../filtering-and-search.md)
- **Customize display:** Explore [Templates](../templates.md)
- **Fine-tune behavior:** Check [Customization](../customization.md)
