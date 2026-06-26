# Events and API Reference

## Table of Contents
- [Event Reference](#event-reference)
- [Event Handling](#event-handling)
- [API Methods](#api-methods)
- [Properties](#properties)
- [Reactive Patterns](#reactive-patterns)

## Event Reference

### Complete Event List

| Event | When Fired | Arguments |
|-------|-----------|-----------|
| `ValueChange` | Selection changed | `MultiSelectChangeEventArgs<TValue>` |
| `Focus` | Component focused | `object` |
| `Blur` | Component loses focus | `object` |
| `Opened` | Popup opened | `PopupEventArgs` |
| `Closed` | Popup closed | `ClosedEventArgs` |
| `OnOpen` | Before popup opens | `BeforeOpenEventArgs` |
| `OnClose` | Before popup closes | `PopupEventArgs` |
| `Filtering` | Filter text entered | `FilteringEventArgs` |
| `CustomValueSpecifier` | Custom value entered | `CustomValueEventArgs<TItem>` |
| `OnValueSelect` | Before item selected | `SelectEventArgs<TItem>` |
| `OnValueRemove` | Before item removed | `RemoveEventArgs<TItem>` |
| `ValueRemoved` | After item removed | `RemoveEventArgs<TItem>` |
| `ChipSelected` | Chip/tag selected | `ChipSelectedEventArgs<TItem>` |
| `OnChipTag` | Before item set as chip | `TaggingEventArgs<TItem>` |
| `Cleared` | All items cleared | `MouseEventArgs` |
| `SelectingAll` | Before select all starts | `SelectingAllEventArgs<TItem>` |
| `SelectedAll` | After select all completes | `SelectAllEventArgs<TItem>` |
| `OnActionBegin` | Before async action starts | `ActionBeginEventArgs` |
| `OnActionComplete` | After async action completes | `ActionCompleteEventArgs<TItem>` |
| `OnActionFailure` | When async action fails | `Exception` |
| `DataBound` | After data binding completes | `DataBoundEventArgs` |
| `OnResizeStart` | Popup resize begins | `object` |
| `OnResizeStop` | Popup resize completes | `object` |
| `Created` | After component created | `object` |
| `Destroyed` | Before component destroyed | `object` |

### ValueChange Event

Fired when user selects or deselects items:

```csharp
@page "/events-change"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Placeholder="Select items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       ValueChange="OnSelectionChange">
    </MultiSelectEvents>
</SfMultiSelect>

<p>@EventLog</p>

@code {
    private List<Item> Items { get; set; } = new();
    private string EventLog { get; set; } = "";

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Item 1" },
            new Item { ID = "2", Name = "Item 2" }
        };
    }

    private void OnSelectionChange(MultiSelectChangeEventArgs<string[]> args)
    {
        EventLog = $"Selected: {string.Join(", ", args.Value ?? Array.Empty<string>())}";
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

**Arguments:**
```csharp
public class MultiSelectChangeEventArgs<TValue>
{
    public TValue Value { get; set; }        // Current selected values
    public TValue PreviousValue { get; set; } // Previous selected values
    public bool IsInteracted { get; set; }  // True if user-triggered
}
```

### Focus and Blur Events

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       Focus="OnFocus"
                       Blur="OnBlur">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private void OnFocus(FocusEventArgs args)
    {
        Console.WriteLine("Component focused");
    }

    private void OnBlur(FocusEventArgs args)
    {
        Console.WriteLine("Component lost focus");
    }

    private List<Item> Items { get; set; } = new();
}
```

### Opened and Closed Events

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       Opened="OnOpened"
                       Closed="OnClosed">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private bool IsPopupOpen { get; set; } = false;

    private void OnOpened(PopupEventArgs args)
    {
        IsPopupOpen = true;
        Console.WriteLine("Popup opened");
    }

    private void OnClosed(PopupEventArgs args)
    {
        IsPopupOpen = false;
        Console.WriteLine("Popup closed");
    }

    private List<Item> Items { get; set; } = new();
}
```

**Note:** Event names are `Opened` and `Closed` (past tense), not `Open` and `Close`.

### Filtering Event

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@FilteredItems"
               AllowFiltering="true">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       Filtering="OnFiltering">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private List<Item> AllItems { get; set; } = new();
    private List<Item> FilteredItems { get; set; } = new();

    private void OnFiltering(FilteringEventArgs args)
    {
        args.PreventDefaultAction = true;  // Custom filtering

        FilteredItems = AllItems
            .Where(x => x.Name.Contains(args.Text, StringComparison.OrdinalIgnoreCase))
            .ToList();
    }

    private List<Item> Items { get; set; } = new();
}
```

### Custom Value Event

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               AllowCustomValue="true">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       CustomValueSpecifier="OnCustomValue">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private void OnCustomValue(CustomValueEventArgs<Item> args)
    {
        // Handle custom value - args.Text contains the user input
        Console.WriteLine($"Custom value: {args.Text}");
        
        // Create and return a new item
        args.NewData = new Item 
        { 
            ID = Guid.NewGuid().ToString(), 
            Name = args.Text 
        };
        
        // Optionally add to data source
        Items.Add(args.NewData);
    }

    private List<Item> Items { get; set; } = new();
}
```

**Note:** Event is `CustomValueSpecifier` (not `CustomValueSelection`). Use `args.Text` for input and set `args.NewData` with the created object.

### OnValueSelect and OnValueRemove Events

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       OnValueSelect="OnSelect"
                       OnValueRemove="OnRemove"
                       ValueRemoved="OnRemoved">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private void OnSelect(SelectEventArgs<Item> args)
    {
        // Called before item is selected
        Console.WriteLine($"Selecting: {args.ItemData.Name}");
        
        // Cancel selection if needed
        if (args.ItemData.ID == "restricted")
            args.Cancel = true;
    }

    private void OnRemove(RemoveEventArgs<Item> args)
    {
        // Called before item is removed
        Console.WriteLine($"Removing: {args.ItemData.Name}");
        
        // Cancel removal if needed
        args.Cancel = false;
    }

    private void OnRemoved(RemoveEventArgs<Item> args)
    {
        // Called after item is removed
        Console.WriteLine($"Removed: {args.ItemData.Name}");
    }

    private List<Item> Items { get; set; } = new();
}
```

### ChipSelected and OnChipTag Events

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Mode="VisualMode.Box">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       OnChipTag="OnTagging"
                       ChipSelected="OnChipSelect">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private void OnTagging(TaggingEventArgs<Item> args)
    {
        // Called before item is displayed as a chip
        Console.WriteLine($"Tagging: {args.ItemData.Name}");
        
        // Customize chip display if needed
        args.SetClass = "custom-chip-class";
    }

    private void OnChipSelect(ChipSelectedEventArgs<Item> args)
    {
        // Called when a chip is clicked/selected
        Console.WriteLine($"Chip selected: {args.Data.Name}");
    }

    private List<Item> Items { get; set; } = new();
}
```

### Cleared Event

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               ShowClearButton="true">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       Cleared="OnCleared">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private void OnCleared(MouseEventArgs args)
    {
        // Called after clear button is clicked and all items are cleared
        Console.WriteLine("All selections cleared");
    }

    private List<Item> Items { get; set; } = new();
}
```

### SelectingAll and SelectedAll Events

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Mode="VisualMode.CheckBox"
               ShowSelectAll="true">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       SelectingAll="OnSelectingAll"
                       SelectedAll="OnSelectedAll">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private void OnSelectingAll(SelectingAllEventArgs<Item> args)
    {
        // Called before select all operation
        Console.WriteLine($"Selecting all: {args.Items.Count} items");
        
        // Cancel select all if needed
        args.Cancel = false;
        
        // Suppress individual OnValueSelect/OnValueRemove events during select all
        args.SuppressItemEvents = true;
    }

    private void OnSelectedAll(SelectAllEventArgs<Item> args)
    {
        // Called after select all operation completes
        Console.WriteLine($"Selected all: {args.Items.Count} items");
    }

    private List<Item> Items { get; set; } = new();
}
```

### OnOpen and OnClose Events

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       OnOpen="OnBeforeOpen"
                       OnClose="OnBeforeClose">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private void OnBeforeOpen(BeforeOpenEventArgs args)
    {
        // Called before popup opens
        Console.WriteLine("Popup opening...");
        
        // Cancel popup open if needed
        args.Cancel = false;
    }

    private void OnBeforeClose(PopupEventArgs args)
    {
        // Called before popup closes
        Console.WriteLine("Popup closing...");
        
        // Cancel popup close if needed
        args.Cancel = false;
    }

    private List<Item> Items { get; set; } = new();
}
```

### OnResizeStart and OnResizeStop Events

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               AllowResize="true">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       OnResizeStart="OnResizeBegin"
                       OnResizeStop="OnResizeEnd">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private void OnResizeBegin(object args)
    {
        // Called when popup resize starts
        Console.WriteLine("Popup resize started");
    }

    private void OnResizeEnd(object args)
    {
        // Called when popup resize completes
        Console.WriteLine("Popup resize completed");
    }

    private List<Item> Items { get; set; } = new();
}
```

## Event Handling

### Async Event Handlers

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item"
                       ValueChange="OnSelectionChangeAsync">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private async Task OnSelectionChangeAsync(MultiSelectChangeEventArgs<string[]> args)
    {
        // Async operations like API calls
        var result = await FetchDataAsync(args.Value);
        Console.WriteLine($"Result: {result}");
    }

    private async Task<string> FetchDataAsync(string[] values)
    {
        // Simulate API call
        await Task.Delay(1000);
        return $"Processed {values?.Length ?? 0} items";
    }

    private List<Item> Items { get; set; } = new();
}
```

### Preventing Default Behavior

```csharp
private void OnFiltering(FilteringEventArgs args)
{
    args.PreventDefaultAction = true;  // Skip default filter
    // Implement custom filtering logic
}
```

## API Methods

### Open and Close Popup

```csharp
@page "/api-methods"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect @ref="MultiSelectRef"
               TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Placeholder="See buttons below">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

<button @onclick="OpenPopup">Open</button>
<button @onclick="ClosePopup">Close</button>
<button @onclick="FocusComponent">Focus</button>
<button @onclick="ClearSelection">Clear</button>

@code {
    private SfMultiSelect<string[], Item> MultiSelectRef;
    private List<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Item 1" },
            new Item { ID = "2", Name = "Item 2" }
        };
    }

    private async Task OpenPopup()
    {
        if (MultiSelectRef != null)
            await MultiSelectRef.ShowPopupAsync();
    }

    private async Task ClosePopup()
    {
        if (MultiSelectRef != null)
            await MultiSelectRef.HidePopupAsync();
    }

    private async Task FocusComponent()
    {
        if (MultiSelectRef != null)
            await MultiSelectRef.FocusAsync();
    }

    private async Task ClearSelection()
    {
        if (MultiSelectRef != null)
            await MultiSelectRef.ClearAsync();
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

### Refresh Data

```csharp
private async Task RefreshData()
{
    // Update data source
    Items = new List<Item>
    {
        new Item { ID = "1", Name = "Updated Item 1" },
        new Item { ID = "2", Name = "Updated Item 2" }
    };

    // Refresh component
    if (MultiSelectRef != null)
        await MultiSelectRef.RefreshDataAsync();
}
```

**Note:** Use `RefreshDataAsync()` method (not `Refresh()`).

## Properties

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `Value` | `TValue` | Currently selected values (array type) |
| `DataSource` | `IEnumerable<TItem>` | Items to display |
| `Enabled` | `bool` | Enable/disable component (default: true) |
| `Readonly` | `bool` | Read-only mode |
| `AllowFiltering` | `bool` | Enable filtering |
| `Mode` | `VisualMode` | Display mode (Default, Box, CheckBox, Delimiter) |
| `Placeholder` | `string` | Placeholder text |
| `PopupHeight` | `string` | Popup height |
| `PopupWidth` | `string` | Popup width |
| `AllowCustomValue` | `bool` | Allow custom values |
| `ShowClearButton` | `bool` | Show clear button |
| `ShowDropDownIcon` | `bool` | Show dropdown icon |
| `MaximumSelectionLength` | `int` | Maximum selection limit |

**Note:** Grouping is enabled via `GroupBy` in `MultiSelectFieldSettings` (no `AllowGrouping` or `ShowCheckbox` properties).

### Accessing Properties

```csharp
@page "/properties"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect @ref="MultiSelectRef"
               TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedValues">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

<button @onclick="GetInfo">Get Info</button>
<p>@Info</p>

@code {
    private SfMultiSelect<string[], Item> MultiSelectRef;
    private string[] SelectedValues { get; set; } = Array.Empty<string>();
    private List<Item> Items { get; set; } = new();
    private string Info { get; set; } = "";

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Item 1" },
            new Item { ID = "2", Name = "Item 2" }
        };
    }

    private void GetInfo()
    {
        Info = $"Selected: {SelectedValues.Length}, Total: {Items.Count}";
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

## Reactive Patterns

### Binding and State Management

```csharp
@page "/reactive-state"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedItems"
               Placeholder="Select items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

<div>
    <h4>Selected Items: @SelectedItems.Length</h4>
    <ul>
        @foreach (var item in SelectedItems)
        {
            <li>@item</li>
        }
    </ul>
</div>

@code {
    private string[] SelectedItems { get; set; } = Array.Empty<string>();
    private List<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Item 1" },
            new Item { ID = "2", Name = "Item 2" },
            new Item { ID = "3", Name = "Item 3" }
        };
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

### Cascading Updates

```csharp
@page "/cascading"
@using Syncfusion.Blazor.DropDowns

<p>Department: @SelectedDepartment</p>
<SfMultiSelect TValue="string[]"
               TItem="string"
               DataSource="@Departments"
               @bind-Value="SelectedDepartments"
               Placeholder="Select department">
</SfMultiSelect>

<p>Employees in selected departments:</p>
<SfMultiSelect TValue="string[]"
               TItem="Employee"
               DataSource="@FilteredEmployees"
               @bind-Value="SelectedEmployees"
               Placeholder="Select employees">
    <MultiSelectFieldSettings Text="Name" Value="EmployeeID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private string[] SelectedDepartments { get; set; } = new[] { "IT" };
    private string SelectedDepartment => SelectedDepartments?.FirstOrDefault() ?? "IT";
    private string[] SelectedEmployees { get; set; } = Array.Empty<string>();
    
    private List<string> Departments { get; set; } = new() { "IT", "HR", "Finance" };
    private List<Employee> AllEmployees { get; set; } = new();
    private List<Employee> FilteredEmployees { get; set; } = new();

    protected override void OnInitialized()
    {
        AllEmployees = new List<Employee>
        {
            new Employee { EmployeeID = "1", Name = "Alice", Department = "IT" },
            new Employee { EmployeeID = "2", Name = "Bob", Department = "HR" },
            new Employee { EmployeeID = "3", Name = "Charlie", Department = "IT" }
        };
        
        UpdateEmployeeList();
    }

    protected override void OnParametersSet()
    {
        UpdateEmployeeList();
    }

    private void UpdateEmployeeList()
    {
        FilteredEmployees = AllEmployees
            .Where(x => x.Department == SelectedDepartment)
            .ToList();
    }

    public class Employee
    {
        public string EmployeeID { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

## Key Takeaways

✅ `ValueChange` event fires on selection updates (not `Change`)  
✅ Use `Opened`/`Closed` events after popup state changes  
✅ Use `OnOpen`/`OnClose` events before popup state changes (cancellable)  
✅ `CustomValueSpecifier` for custom values (use `args.NewData` not `args.Item`)  
✅ `OnValueSelect`/`OnValueRemove` fire before item selection/removal (cancellable)  
✅ `ValueRemoved` fires after item is removed (not cancellable)  
✅ `ChipSelected` fires when clicking a chip in Box mode  
✅ `OnChipTag` fires before item is rendered as chip (customize display)  
✅ `Cleared` fires when clear button removes all items  
✅ `SelectingAll`/`SelectedAll` for select all operations in CheckBox mode  
✅ Use `args.Cancel` to prevent default behavior in `On*` events  
✅ Use `RefreshDataAsync()` method (not `Refresh()`)  
✅ Use async handlers for API calls  
✅ `PreventDefaultAction` for custom filtering behavior  
✅ Reference component for API method calls (e.g., `ShowPopupAsync()`, `HidePopupAsync()`, `FocusAsync()`)  
✅ Binding provides real-time state sync  
✅ Cascading updates enable dependent selectors  
✅ `OnResizeStart`/`OnResizeStop` for popup resize handling (requires `AllowResize="true"`)  
✅ Use `args.SuppressItemEvents` in `SelectingAll` to prevent individual item events  

## Next Steps

- **Advanced usage** → See [Advanced Scenarios](advanced-scenarios.md)
- **Form validation** → See [Advanced Scenarios](advanced-scenarios.md#form-validation)
- **Performance tips** → See [Data Binding](data-binding.md#performance-considerations)
