# Selection Modes in Blazor ListBox

## Table of Contents
- [Single Selection](#single-selection)
- [Multiple Selection](#multiple-selection)
- [Checkbox Selection](#checkbox-selection)
- [Getting Selected Values](#getting-selected-values)
- [Handling Selection Events](#handling-selection-events)
- [Selection Constraints](#selection-constraints)
- [Advanced Patterns](#advanced-patterns)

## Single Selection

Enable single selection mode to allow users to select only one item at a time.

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" />
    <ListBoxSelectionSettings Mode="Syncfusion.Blazor.DropDowns.SelectionMode.Single"></ListBoxSelectionSettings>
</SfListBox>

@code {
    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-02" },
        new VehicleData { Text = "McLaren F1", Id = "Vehicle-03" },
        new VehicleData { Text = "Ferrari Enzo", Id = "Vehicle-04" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
    }
}
```

**Behavior:**
- User can click only one item to select it
- Clicking another item deselects the previous one
- `Value` will contain single item in array

## Multiple Selection

Multiple selection (default) allows selecting many items. Users can use Shift+Click for range selection and Ctrl+Click for individual items.

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" />
    <ListBoxSelectionSettings Mode="Syncfusion.Blazor.DropDowns.SelectionMode.Multiple"></ListBoxSelectionSettings>
</SfListBox>

@code {
    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-02" },
        new VehicleData { Text = "McLaren F1", Id = "Vehicle-03" },
        new VehicleData { Text = "Ferrari Enzo", Id = "Vehicle-04" },
        new VehicleData { Text = "Koenigsegg CCR", Id = "Vehicle-05" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
    }
}
```

**Keyboard Shortcuts (Multiple Mode):**
- **Click** - Select single item
- **Shift + Click** - Select range of items
- **Ctrl + Click** - Toggle individual items
- **Arrow Keys** - Navigate items
- **Space** - Select/deselect current item

**Note:** Multiple selection is the default mode if you don't specify `Mode`.

## Checkbox Selection

Enable checkboxes for explicit multi-selection. This provides a clear visual indicator of selected items.

### Basic Checkbox Selection

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" />
    <ListBoxSelectionSettings ShowCheckbox="true"></ListBoxSelectionSettings>
</SfListBox>

@code {
    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-02" },
        new VehicleData { Text = "McLaren F1", Id = "Vehicle-03" },
        new VehicleData { Text = "Ferrari Enzo", Id = "Vehicle-04" },
        new VehicleData { Text = "Koenigsegg CCR", Id = "Vehicle-05" },
        new VehicleData { Text = "Aston Martin One-77", Id = "Vehicle-06" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
    }
}
```

**Result:**
- Each item displays a checkbox
- Clicking checkbox toggles selection
- Visual feedback with checked/unchecked states

### With Select All Functionality

```razor
<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" />
    <ListBoxSelectionSettings ShowCheckbox="true" ShowSelectAll="true"></ListBoxSelectionSettings>
</SfListBox>
```

**Features:**
- Additional "Select All" checkbox at the top
- Click to select/deselect all items at once
- Individual checkboxes still work independently
- Partial selection state if some items are selected

## Getting Selected Values

### Two-Way Binding

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData" @bind-Value="@SelectedVehicleIds">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>

<p>Selected: @string.Join(", ", SelectedVehicleIds ?? new string[] { })</p>

@code {
    public string[] SelectedVehicleIds { get; set; }

    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-02" },
        new VehicleData { Text = "McLaren F1", Id = "Vehicle-03" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
    }
}
```

**How It Works:**
- `@bind-Value="@SelectedVehicleIds"` - Two-way binding
- `SelectedVehicleIds` always contains current selected values
- Values update automatically when user selects items

### Getting Values Programmatically

```razor
@ref="ListBoxRef"
<button @onclick="GetSelected">Get Selected</button>

@code {
    private SfListBox<string[], VehicleData> ListBoxRef;

    private void GetSelected()
    {
        var selected = ListBoxRef.Value;
        if (selected != null && selected.Length > 0)
        {
            Console.WriteLine($"Selected IDs: {string.Join(", ", selected)}");
        }
    }
}
```

### Finding Display Text for Selected Values

```razor
@code {
    private void ShowSelectedTexts()
    {
        var selectedIds = ListBoxRef.Value;
        var selectedTexts = Vehicles
            .Where(v => selectedIds.Contains(v.Id))
            .Select(v => v.Text)
            .ToList();

        Console.WriteLine($"Selected Vehicles: {string.Join(", ", selectedTexts)}");
    }
}
```

## Handling Selection Events

### Change Event

Fires when selection changes (user selects/deselects item):

```razor
<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData" ValueChange="@OnSelectionChanged">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>

<p>Last changed: @LastChanged</p>

@code {
    private string LastChanged = "None";

    private void OnSelectionChanged(ChangeEventArgs args)
    {
        var selected = args.Value as string[];
        LastChanged = selected != null && selected.Length > 0 
            ? string.Join(", ", selected) 
            : "None";
    }

    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-02" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
    }
}
```
### Event Handler with Logging

```razor
@code {
    private List<string> SelectionHistory = new List<string>();

    private void OnSelectionChanged(ChangeEventArgs args)
    {
        var selected = args.Value as string[];
        var timestamp = DateTime.Now.ToString("HH:mm:ss");
        var log = $"[{timestamp}] Selected: {string.Join(", ", selected ?? new string[] { })}";
        
        SelectionHistory.Add(log);
        
        // Log to console
        Console.WriteLine(log);
    }
}
```

## Selection Constraints

### Maximum Selection Length

Limit the number of items users can select:

```razor
<SfListBox TValue="string[]" 
           DataSource="@Vehicles" 
           TItem="VehicleData"
           MaximumSelectionLength="3">
    <ListBoxFieldSettings Text="Text" Value="Id" />
    <ListBoxSelectionSettings ShowCheckbox="true"></ListBoxSelectionSettings>
</SfListBox>

<p>You can select up to 3 vehicles</p>

@code {
    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-02" },
        new VehicleData { Text = "McLaren F1", Id = "Vehicle-03" },
        new VehicleData { Text = "Ferrari Enzo", Id = "Vehicle-04" },
        new VehicleData { Text = "Koenigsegg CCR", Id = "Vehicle-05" },
        new VehicleData { Text = "Aston Martin One-77", Id = "Vehicle-06" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
    }
}
```

**Behavior:**
- Checkboxes become disabled after reaching limit
- Users cannot select more items
- Default limit is 500

### Initial Selection

Set pre-selected values when component initializes:

```razor
<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData" @bind-Value="@PreselectedVehicles">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>

@code {
    public string[] PreselectedVehicles = new string[] { "Vehicle-02", "Vehicle-04" };

    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-02" },
        new VehicleData { Text = "McLaren F1", Id = "Vehicle-03" },
        new VehicleData { Text = "Ferrari Enzo", Id = "Vehicle-04" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
    }
}
```

**Result:** "Bugatti Chiron" and "Ferrari Enzo" are pre-selected

## Advanced Patterns

### Filtering Selection Results

```razor
@code {
    private void FilterSelections()
    {
        var selected = ListBoxRef.Value;
        var luxuryVehicles = Vehicles
            .Where(v => selected.Contains(v.Id) && v.Category == "Luxury")
            .ToList();
    }
}
```

### Cascading Selection

```razor
@using Syncfusion.Blazor.DropDowns

<!-- First ListBox: Select Category -->
<SfListBox TValue="string[]" DataSource="@Categories" TItem="string" @bind-Value="@SelectedCategories">
</SfListBox>

<!-- Second ListBox: Show items in selected category -->
<SfListBox TValue="string[]" DataSource="@FilteredItems" TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>

@code {
    private string[] SelectedCategories;
    private List<string> Categories = new List<string> { "Luxury", "Sport", "Electric" };

    private List<VehicleData> FilteredItems
    {
        get
        {
            if (SelectedCategories == null || SelectedCategories.Length == 0)
                return new List<VehicleData>();

            return AllVehicles
                .Where(v => SelectedCategories.Contains(v.Category))
                .ToList();
        }
    }

    private List<VehicleData> AllVehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-01", Category = "Luxury" },
        new VehicleData { Text = "Tesla Model S", Id = "Vehicle-02", Category = "Electric" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
        public string Category { get; set; }
    }
}
```

### Transfer Between ListBoxes

```razor
@using Syncfusion.Blazor.DropDowns

<div style="display: flex; gap: 20px;">
    <div>
        <h4>Available</h4>
        <SfListBox TValue="string[]" DataSource="@Available" TItem="ItemData" @ref="SourceListBox">
            <ListBoxFieldSettings Text="Name" Value="Id" />
            <ListBoxSelectionSettings ShowCheckbox="true"></ListBoxSelectionSettings>
        </SfListBox>
    </div>

    <div style="display: flex; gap: 10px; flex-direction: column; justify-content: center;">
        <button @onclick="MoveToSelected">→</button>
        <button @onclick="MoveToAvailable">←</button>
    </div>

    <div>
        <h4>Selected</h4>
        <SfListBox TValue="string[]" DataSource="@Selected" TItem="ItemData" @ref="TargetListBox">
            <ListBoxFieldSettings Text="Name" Value="Id" />
            <ListBoxSelectionSettings ShowCheckbox="true"></ListBoxSelectionSettings>
        </SfListBox>
    </div>
</div>

@code {
    private SfListBox<string[], ItemData> SourceListBox;
    private SfListBox<string[], ItemData> TargetListBox;

    private List<ItemData> Available = new List<ItemData>
    {
        new ItemData { Id = "1", Name = "Item 1" },
        new ItemData { Id = "2", Name = "Item 2" },
        new ItemData { Id = "3", Name = "Item 3" }
    };

    private List<ItemData> Selected = new List<ItemData>();

    private void MoveToSelected()
    {
        var selectedIds = SourceListBox?.Value;
        if (selectedIds != null)
        {
            var itemsToMove = Available.Where(a => selectedIds.Contains(a.Id)).ToList();
            foreach (var item in itemsToMove)
            {
                Available.Remove(item);
                Selected.Add(item);
            }
            StateHasChanged();
        }
    }

    private void MoveToAvailable()
    {
        var selectedIds = TargetListBox?.Value;
        if (selectedIds != null)
        {
            var itemsToMove = Selected.Where(s => selectedIds.Contains(s.Id)).ToList();
            foreach (var item in itemsToMove)
            {
                Selected.Remove(item);
                Available.Add(item);
            }
            StateHasChanged();
        }
    }

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
    }
}
```

### Validation: Require Selection

```razor
@code {
    private bool IsValid()
    {
        var selected = ListBoxRef.Value;
        return selected != null && selected.Length > 0;
    }

    private void Submit()
    {
        if (!IsValid())
        {
            Console.WriteLine("Please select at least one item");
            return;
        }
        // Process submission
    }
}
```
