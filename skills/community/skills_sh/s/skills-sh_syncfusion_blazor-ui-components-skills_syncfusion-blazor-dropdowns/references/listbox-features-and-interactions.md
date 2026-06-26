# Features and Interactions in Blazor ListBox

## Table of Contents
- [Filtering and Search](#filtering-and-search)
- [Drag and Drop](#drag-and-drop)
- [Icons and Templates](#icons-and-templates)
- [Sorting and Grouping](#sorting-and-grouping)
- [Dual ListBox Pattern](#dual-listbox-pattern)
- [Enable/Disable Items](#enabledisable-items)
- [Advanced Interactions](#advanced-interactions)

## Filtering and Search

Enable users to search and filter items in the ListBox. This is useful for large data sets.

### Basic Filtering

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Vehicles" 
           TItem="VehicleData"
           AllowFiltering="true">
    <ListBoxFieldSettings Text="Text" Value="Id" />
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

**Features:**
- Search input appears at the top of ListBox
- Filters items as user types
- Default filter type: "Contains"

### Filter Type Options

```razor
<SfListBox TValue="string[]" 
           DataSource="@Vehicles" 
           TItem="VehicleData"
           AllowFiltering="true"
           FilterType="FilterType.StartsWith">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>
```

**Available Filter Types:**
- `FilterType.StartsWith` - Match beginning of text (e.g., "Hen" matches "Hennessey")
- `FilterType.Contains` - Match anywhere in text (default, e.g., "enness" matches "Hennessey")
- `FilterType.EndsWith` - Match end of text

### Custom Filter Placeholder

```razor
<SfListBox TValue="string[]" 
           DataSource="@Vehicles" 
           TItem="VehicleData"
           AllowFiltering="true"
           FilterPlaceholder="Search for a vehicle...">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>
```

## Drag and Drop

Allow users to reorder items by dragging and dropping. Useful for priority lists or custom ordering.

### Enable Drag and Drop

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Tasks" 
           TItem="TaskData"
           AllowDragging="true">
    <ListBoxFieldSettings Text="Name" Value="Id" />
</SfListBox>

@code {
    public List<TaskData> Tasks = new List<TaskData>
    {
        new TaskData { Id = "Task-01", Name = "Design UI Mockup" },
        new TaskData { Id = "Task-02", Name = "Develop Backend API" },
        new TaskData { Id = "Task-03", Name = "Create Documentation" },
        new TaskData { Id = "Task-04", Name = "Test Application" },
        new TaskData { Id = "Task-05", Name = "Deploy to Production" }
    };

    public class TaskData
    {
        public string Id { get; set; }
        public string Name { get; set; }
    }
}
```

**Behavior:**
- Click and drag items to reorder
- Visual feedback during drag (highlighted border)
- New order persists in the component

### Drag Between Two ListBoxes

```razor
@using Syncfusion.Blazor.DropDowns

<div style="display: flex; gap: 30px;">
    <div>
        <h4>Available Items</h4>
        <SfListBox TValue="string[]" 
                   DataSource="@Available" 
                   TItem="ItemData"
                   AllowDragging="true">
            <ListBoxFieldSettings Text="Name" Value="Id" />
        </SfListBox>
    </div>

    <div>
        <h4>Drag Here</h4>
        <SfListBox TValue="string[]" 
                   DataSource="@Selected" 
                   TItem="ItemData"
                   AllowDragging="true">
            <ListBoxFieldSettings Text="Name" Value="Id" />
        </SfListBox>
    </div>
</div>

@code {
    public List<ItemData> Available = new List<ItemData>
    {
        new ItemData { Id = "Item-01", Name = "Item 1" },
        new ItemData { Id = "Item-02", Name = "Item 2" },
        new ItemData { Id = "Item-03", Name = "Item 3" }
    };

    public List<ItemData> Selected = new List<ItemData>();

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
    }
}
```

**Note:** Current implementation allows reordering within the same ListBox. For moving between ListBoxes, implement custom event handlers.

## Icons and Templates

Add icons to list items and create custom item templates for rich formatting.

### Using Icons

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="ItemData">
    <ListBoxFieldSettings Text="Name" Value="Id" IconCss="Icon" />
</SfListBox>

@code {
    public List<ItemData> Items = new List<ItemData>
    {
        new ItemData { Id = "item-01", Name = "Home", Icon = "e-icons e-home" },
        new ItemData { Id = "item-02", Name = "Settings", Icon = "e-icons e-settings" },
        new ItemData { Id = "item-03", Name = "Download", Icon = "e-icons e-download" },
        new ItemData { Id = "item-04", Name = "Favorite", Icon = "e-icons e-star" }
    };

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Icon { get; set; }
    }
}
```

**Result:** Each item displays an icon next to the text

### Custom Item Templates

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Employees" 
           TItem="EmployeeData">
    <ListBoxFieldSettings Text="Name" Value="Id" />
    <ListBoxTemplates>
        <ItemTemplate>
            @{
                var item = context as EmployeeData;
            }
            <div style="display: flex; gap: 10px; align-items: center;">
                <img src="@item.Avatar" style="width: 30px; height: 30px; border-radius: 50%;" />
                <div>
                    <div><strong>@item.Name</strong></div>
                    <small style="color: gray;">@item.Title</small>
                </div>
            </div>
        </ItemTemplate>
    </ListBoxTemplates>
</SfListBox>

@code {
    public List<EmployeeData> Employees = new List<EmployeeData>
    {
        new EmployeeData { Id = "emp-01", Name = "John Doe", Title = "Manager", Avatar = "/images/john.jpg" },
        new EmployeeData { Id = "emp-02", Name = "Jane Smith", Title = "Developer", Avatar = "/images/jane.jpg" },
        new EmployeeData { Id = "emp-03", Name = "Mike Johnson", Title = "Designer", Avatar = "/images/mike.jpg" }
    };

    public class EmployeeData
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Title { get; set; }
        public string Avatar { get; set; }
    }
}
```

**Template Features:**
- Access current item via `context`
- Display custom HTML and Blazor components
- Each item renders the template

## Sorting and Grouping

Organize items by sorting and grouping.

### Sorting

```razor
@using Syncfusion.Blazor.DropDowns
@using System.Linq

<SfListBox TValue="string[]" 
           DataSource="@SortedVehicles" 
           TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>

<button @onclick="SortByName">Sort A-Z</button>
<button @onclick="SortByName_Desc">Sort Z-A</button>

@code {
    private List<VehicleData> _vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-02" },
        new VehicleData { Text = "McLaren F1", Id = "Vehicle-03" },
        new VehicleData { Text = "Ferrari Enzo", Id = "Vehicle-04" }
    };

    public List<VehicleData> SortedVehicles { get; set; }

    protected override void OnInitialized()
    {
        SortedVehicles = new List<VehicleData>(_vehicles);
    }

    private void SortByName()
    {
        SortedVehicles = _vehicles.OrderBy(v => v.Text).ToList();
        StateHasChanged();
    }

    private void SortByName_Desc()
    {
        SortedVehicles = _vehicles.OrderByDescending(v => v.Text).ToList();
        StateHasChanged();
    }

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
    }
}
```

### Grouping

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Vehicles" 
           TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" GroupBy="Category" />
</SfListBox>

@code {
    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01", Category = "High Performance" },
        new VehicleData { Text = "Tesla Model 3", Id = "Vehicle-02", Category = "Electric" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-03", Category = "High Performance" },
        new VehicleData { Text = "Nissan Leaf", Id = "Vehicle-04", Category = "Electric" },
        new VehicleData { Text = "BMW i8", Id = "Vehicle-05", Category = "Hybrid" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
        public string Category { get; set; }
    }
}
```

**Result:** Items are grouped by category with collapsible headers

## Dual ListBox Pattern

Create a source-target ListBox pattern for data transfer between two lists.

```razor
@using Syncfusion.Blazor.DropDowns

<div style="display: flex; gap: 20px;">
    <div>
        <h4>Available Skills</h4>
        <SfListBox TValue="string[]" 
                   DataSource="@AvailableSkills" 
                   TItem="SkillData"
                   @ref="SourceListBox">
            <ListBoxFieldSettings Text="Name" Value="Id" />
            <ListBoxSelectionSettings ShowCheckbox="true"></ListBoxSelectionSettings>
        </SfListBox>
    </div>

    <div style="display: flex; flex-direction: column; justify-content: center; gap: 10px;">
        <button @onclick="MoveToRequired">Add →</button>
        <button @onclick="RemoveFromRequired">← Remove</button>
    </div>

    <div>
        <h4>Required Skills</h4>
        <SfListBox TValue="string[]" 
                   DataSource="@RequiredSkills" 
                   TItem="SkillData"
                   @ref="TargetListBox">
            <ListBoxFieldSettings Text="Name" Value="Id" />
            <ListBoxSelectionSettings ShowCheckbox="true"></ListBoxSelectionSettings>
        </SfListBox>
    </div>
</div>

@code {
    private SfListBox<string[], SkillData> SourceListBox;
    private SfListBox<string[], SkillData> TargetListBox;

    private List<SkillData> AvailableSkills = new List<SkillData>
    {
        new SkillData { Id = "skill-01", Name = "C#" },
        new SkillData { Id = "skill-02", Name = "Blazor" },
        new SkillData { Id = "skill-03", Name = "JavaScript" },
        new SkillData { Id = "skill-04", Name = "React" },
        new SkillData { Id = "skill-05", Name = "SQL" }
    };

    private List<SkillData> RequiredSkills = new List<SkillData>();

    private void MoveToRequired()
    {
        var selected = SourceListBox?.Value;
        if (selected != null && selected.Length > 0)
        {
            var itemsToMove = AvailableSkills
                .Where(s => selected.Contains(s.Id))
                .ToList();

            foreach (var item in itemsToMove)
            {
                AvailableSkills.Remove(item);
                RequiredSkills.Add(item);
            }

            StateHasChanged();
        }
    }

    private void RemoveFromRequired()
    {
        var selected = TargetListBox?.Value;
        if (selected != null && selected.Length > 0)
        {
            var itemsToMove = RequiredSkills
                .Where(s => selected.Contains(s.Id))
                .ToList();

            foreach (var item in itemsToMove)
            {
                RequiredSkills.Remove(item);
                AvailableSkills.Add(item);
            }

            StateHasChanged();
        }
    }

    public class SkillData
    {
        public string Id { get; set; }
        public string Name { get; set; }
    }
}
```

## Enable/Disable Items

Selectively disable certain items while keeping others available.

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="ItemData">
    <ListBoxFieldSettings Text="Name" Value="Id" />
</SfListBox>

<button @onclick="ToggleItemState">Toggle Item 2 State</button>

@code {
    public List<ItemData> Items = new List<ItemData>
    {
        new ItemData { Id = "item-01", Name = "Item 1", IsEnabled = true },
        new ItemData { Id = "item-02", Name = "Item 2", IsEnabled = false },
        new ItemData { Id = "item-03", Name = "Item 3", IsEnabled = true },
        new ItemData { Id = "item-04", Name = "Item 4", IsEnabled = false }
    };

    private void ToggleItemState()
    {
        var item = Items.FirstOrDefault(i => i.Id == "item-02");
        if (item != null)
        {
            item.IsEnabled = !item.IsEnabled;
            StateHasChanged();
        }
    }

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public bool IsEnabled { get; set; }
    }
}
```

**Note:** Display disabled state using custom templates with CSS classes.

## Advanced Interactions

### Searchable Grouped List

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@FilteredItems" 
           TItem="ItemData"
           AllowFiltering="true"
           FilterType="FilterType.Contains">
    <ListBoxFieldSettings Text="Name" Value="Id" GroupBy="Category" />
</SfListBox>

@code {
    private List<ItemData> _allItems = new List<ItemData>
    {
        new ItemData { Id = "item-01", Name = "Apple", Category = "Fruit" },
        new ItemData { Id = "item-02", Name = "Banana", Category = "Fruit" },
        new ItemData { Id = "item-03", Name = "Carrot", Category = "Vegetable" },
        new ItemData { Id = "item-04", Name = "Broccoli", Category = "Vegetable" }
    };

    public List<ItemData> FilteredItems
    {
        get => new List<ItemData>(_allItems);
    }

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Category { get; set; }
    }
}
```

### Virtual Scrolling for Large Lists

```razor
<!-- For large datasets, consider limiting DataSource to visible items -->
<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="ItemData"
           Height="300px">
    <ListBoxFieldSettings Text="Name" Value="Id" />
</SfListBox>

@code {
    public List<ItemData> Items = Enumerable.Range(1, 1000)
        .Select(i => new ItemData { Id = $"item-{i:D4}", Name = $"Item {i}" })
        .ToList();

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
    }
}
```

### Event Logging

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="ItemData"
           ValueChange="@OnValueChanged">
    <ListBoxFieldSettings Text="Name" Value="Id" />
</SfListBox>

<div>
    <h4>Event Log</h4>
    @foreach(var log in EventLog.TakeLast(5))
    {
        <p>@log</p>
    }
</div>

@code {
    public List<string> EventLog = new List<string>();

    private void OnValueChanged(ChangeEventArgs args)
    {
        var timestamp = DateTime.Now.ToString("HH:mm:ss");
        var selected = args.Value as string[];
        var count = selected?.Length ?? 0;
        EventLog.Add($"[{timestamp}] Selection changed - {count} items selected");
    }

    public List<ItemData> Items = new List<ItemData>
    {
        new ItemData { Id = "item-01", Name = "Item 1" },
        new ItemData { Id = "item-02", Name = "Item 2" }
    };

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
    }
}
```
