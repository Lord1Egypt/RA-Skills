# Features and Selection

## Table of Contents
- [Selection Modes](#selection-modes)
- [Single vs Multiple Selection](#single-vs-multiple-selection)
- [Select and Deselect All](#select-and-deselect-all)
- [Programmatic Selection](#programmatic-selection)
- [Custom Values](#custom-values)
- [Default Values](#default-values)
- [Disabled Items](#disabled-items)
- [Virtualization](#virtualization)

## Selection Modes

### Checkbox Mode

Display checkboxes for explicit selection:

```csharp
@page "/selection-checkbox"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedItems"
               Mode="VisualMode.CheckBox"
               Placeholder="Select with checkboxes">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

<p>Selected: @string.Join(", ", SelectedItems ?? Array.Empty<string>())</p>

@code {
    private string[] SelectedItems { get; set; } = Array.Empty<string>();
    private List<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Option 1" },
            new Item { ID = "2", Name = "Option 2" },
            new Item { ID = "3", Name = "Option 3" }
        };
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

**Best for:** 
- Clarity: Visually explicit which items are selected
- Accessibility: Easier for screen readers
- Forms: Professional appearance in forms

### Delimiter Mode

Display selected items as comma-separated values:

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedItems"
               Mode="VisualMode.Delimiter"
               Placeholder="Select items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>
```

**Best for:**
- Space-constrained UIs
- Compact display
- Simple lists

### Box Mode

Display selected items as removable chips/boxes:

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedItems"
               Mode="VisualMode.Box"
               Placeholder="Select items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>
```

**Best for:**
- Modern UIs
- Easy deselection (click X on chip)
- Visual grouping of selections

### Default Mode

No special formatting:

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Mode="VisualMode.Default">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>
```

## Single vs Multiple Selection

### Multiple Selection (Default)

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Placeholder="Select multiple">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<Item> Items { get; set; } = new();
}
```

**Returns:** `string[]` with all selected values

### Restricting to Single Selection (No Multi-Select)

For single-item selection, use the standard Dropdown List component instead:

```csharp
<SfDropDownList DataSource="@Items" 
                @bind-Value="SelectedItem"
                TValue="string"
                TItem="Item"
                Placeholder="Select one">
    <DropDownListFieldSettings Text="Name" Value="ID"></DropDownListFieldSettings>
</SfDropDownList>

@code {
    private string SelectedItem { get; set; }
}
```

**Why:** MultiSelect always allows multiple selections by design. Use DropDownList for single selection.

## Select and Deselect All

### Enable Select/Deselect All

```csharp
@page "/select-all-demo"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedItems"
               Mode="VisualMode.CheckBox"
               ShowSelectAll="true"
               Placeholder="Select items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

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

**Behavior:**
- Checkbox at top of dropdown
- Click to select/deselect all items
- Checkbox shows indeterminate state if partially selected

### Customize Select All Text

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Mode="VisualMode.CheckBox"
               ShowSelectAll="true"
               SelectAllText="Check All Items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>
```

## Programmatic Selection

### Set Selected Values Manually

```csharp
@page "/programmatic-selection"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect @ref="MultiSelectRef"
               TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedItems">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

<button @onclick="SelectFirst">Select First Item</button>
<button @onclick="ClearSelection">Clear All</button>

@code {
    private SfMultiSelect<string[], Item> MultiSelectRef;
    private string[] SelectedItems { get; set; } = Array.Empty<string>();
    private List<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Item 1" },
            new Item { ID = "2", Name = "Item 2" }
        };
    }

    private async Task SelectFirst()
    {
        SelectedItems = new string[] { "1" };
        await MultiSelectRef.RefreshDataAsync();
    }

    private async Task ClearSelection()
    {
        await MultiSelectRef.ClearAsync();
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

### Add Items to Selection

```csharp
private async Task AddToSelection(string itemID)
{
    if (!SelectedItems.Contains(itemID))
    {
        var newSelection = SelectedItems.ToList();
        newSelection.Add(itemID);
        SelectedItems = newSelection.ToArray();
        await MultiSelectRef.RefreshDataAsync();
    }
}
```

### Remove Item from Selection

```csharp
private async Task RemoveFromSelection(string itemID)
{
    if (SelectedItems.Contains(itemID))
    {
        SelectedItems = SelectedItems.Where(x => x != itemID).ToArray();
        await MultiSelectRef.RefreshDataAsync();
    }
}
```

## Custom Values

### Allow Custom Value Input

Users can type custom values not in the data source:

```csharp
@page "/custom-values"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedItems"
               AllowCustomValue="true"
               Placeholder="Type or select">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

<p>Selected: @string.Join(", ", SelectedItems ?? Array.Empty<string>())</p>

@code {
    private string[] SelectedItems { get; set; } = Array.Empty<string>();
    private List<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Tag 1" },
            new Item { ID = "2", Name = "Tag 2" }
        };
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

**Use cases:**
- Tag/label input
- Custom category creation
- Free-form selections

### Custom Value Event

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedItems"
               AllowCustomValue="true">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="Item" 
                       CustomValueSpecifier="OnCustomValueSelected">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private void OnCustomValueSelected(CustomValueEventArgs<Item> args)
    {
        // Handle custom value
        Console.WriteLine($"Custom value entered: {args.Text}");
        
        // Add to data source if needed
        Items.Add(new Item { ID = Guid.NewGuid().ToString(), Name = args.Text });
    }
}
```

## Default Values

### Set Initial Selection

```csharp
@page "/default-values"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedItems"
               Placeholder="Default items selected">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

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

        // Set initial selection
        SelectedItems = new string[] { "1", "2" };
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

## Disabled Items

### Disable Specific Items

```csharp
@page "/disabled-items"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Placeholder="Some items are disabled">
    <MultiSelectFieldSettings Text="Name" Value="ID" Disabled="Disabled"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Available Item", Disabled = false },
            new Item { ID = "2", Name = "Disabled Item", Disabled = true },
            new Item { ID = "3", Name = "Another Available", Disabled = false }
        };
    }

    public class Item 
    { 
        public string ID { get; set; } 
        public string Name { get; set; } 
        public bool Disabled { get; set; }
    }
}
```

### Disable Entire Component

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Enabled="false"
               Placeholder="Disabled dropdown">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>
```

## Virtualization

### Enable Virtual Scrolling

For large datasets (100+ items), use virtualization:

```csharp
@page "/virtualization"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@LargeDataSet"
               EnableVirtualization="true"
               PopupHeight="300px"
               Placeholder="Virtual scrolling enabled">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<Item> LargeDataSet { get; set; } = new();

    protected override void OnInitialized()
    {
        // Generate 10,000 items
        LargeDataSet = Enumerable.Range(1, 10000)
            .Select(i => new Item { ID = i.ToString(), Name = $"Item {i}" })
            .ToList();
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

**Properties:**
- `EnableVirtualization="true"` - Enable virtual scrolling
- `PopupHeight="300px"` - Height of visible area (determines how many items to render)

**Performance benefit:** Only renders visible items, handles 10,000+ items smoothly.

**Note:** The `ItemsCount` property is obsolete. The number of items displayed is now determined based on the popup's height.

## Key Takeaways

✅ Use `Mode="VisualMode.CheckBox"` for explicit selection with checkboxes  
✅ `Mode="VisualMode.Box"` for modern chip-based display  
✅ Enable `ShowSelectAll="true"` with CheckBox mode for bulk selection  
✅ Use `EnableVirtualization="true"` for datasets over 500 items  
✅ Set disabled field in data to prevent item selection  
✅ Available modes: Default, Box, Delimiter, CheckBox  

## Next Steps

- **Add filtering** → See [Filtering and Grouping](filtering-and-grouping.md)
- **Handle events** → See [Events and API Reference](events-and-api.md)
- **Customize styling** → See [Customization and Styling](customization-and-styling.md)
