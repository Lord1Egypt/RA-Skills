# Accessibility and Events in Blazor ListBox

## Table of Contents
- [Keyboard Navigation](#keyboard-navigation)
- [ARIA Attributes](#aria-attributes)
- [Accessibility Best Practices](#accessibility-best-practices)
- [Event Binding](#event-binding)
- [Event Handling Patterns](#event-handling-patterns)
- [Debugging Events](#debugging-events)

## Keyboard Navigation

The ListBox supports full keyboard navigation for accessibility.

### Built-in Keyboard Support

The ListBox automatically supports these keyboard shortcuts:

| Key | Action |
|-----|--------|
| **Arrow Down** | Move to next item |
| **Arrow Up** | Move to previous item |
| **Space** | Select/deselect current item (Multiple mode) |
| **Ctrl + A** | Select all items |
| **Shift + Click** | Range selection |
| **Ctrl + Click** | Toggle individual items |
| **Home** | Go to first item |
| **End** | Go to last item |
| **Page Up** | Page up in list |
| **Page Down** | Page down in list |

### Example with Keyboard Navigation

```razor
@using Syncfusion.Blazor.DropDowns

<div>
    <h3>Select Skills (Use arrow keys and space)</h3>
    <p style="color: #666; font-size: 12px;">
        Tip: Use Arrow keys to navigate, Space to select/deselect
    </p>
    
    <SfListBox TValue="string[]" 
               DataSource="@Skills" 
               TItem="string"
               Height="250px"
               Enabled="true">
    </SfListBox>
</div>

@code {
    public string[] Skills = new string[]
    {
        "C#",
        "Blazor",
        "JavaScript",
        "React",
        "Angular",
        "Vue.js",
        "SQL",
        "Python"
    };
}
```

### Filtering Accessible

When filtering is enabled, keyboard navigation still works:

```razor
<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="string"
           AllowFiltering="true"
           FilterPlaceholder="Type to search..."
           Height="300px">
</SfListBox>

@code {
    public string[] Items = new string[] 
    { 
        "Apple", "Apricot", "Banana", "Blueberry", 
        "Cherry", "Cranberry", "Date", "Dragonfruit" 
    };
}
```

## ARIA Attributes

ARIA attributes help screen readers understand the ListBox structure and behavior.

### Automatic ARIA Attributes

The ListBox automatically includes:
- `role="listbox"` - Identifies as a listbox widget
- `role="option"` - Identifies list items
- `aria-selected="true|false"` - Indicates selection state
- `aria-disabled="true|false"` - Indicates disabled state
- `aria-label` / `aria-labelledby` - Provides accessible name

### Adding Custom ARIA Labels

```razor
@using Syncfusion.Blazor.DropDowns

<div>
    <label id="skills-label">Select your technical skills:</label>
    <SfListBox TValue="string[]" 
               DataSource="@Skills" 
               TItem="string"
               Height="250px"
               Enabled="true">
    </SfListBox>
</div>

@code {
    public string[] Skills = new string[]
    {
        "C#", "Blazor", "JavaScript", "React", "SQL"
    };
}
```

### ARIA-Live Regions for Dynamic Updates

```razor
@using Syncfusion.Blazor.DropDowns

<div>
    <SfListBox TValue="string[]" 
               DataSource="@Items" 
               TItem="string">
        <ListBoxEvents ValueChange="@OnSelectionChanged"></ListBoxEvents>
    </SfListBox>
    
    <div aria-live="polite" aria-atomic="true" role="status">
        <p>@SelectionStatus</p>
    </div>
</div>

@code {
    private string SelectionStatus = "No items selected";

    private void OnSelectionChanged(ChangeEventArgs args)
    {
        var selected = args.Value as string[];
        int count = selected?.Length ?? 0;
        SelectionStatus = count > 0 
            ? $"{count} item(s) selected: {string.Join(", ", selected)}"
            : "No items selected";
    }

    public string[] Items = new string[] { "Item 1", "Item 2", "Item 3" };
}
```

## Accessibility Best Practices

### 1. Always Provide Labels

```razor
<!-- GOOD: Clear label -->
<label for="status-listbox">Select Status:</label>
<SfListBox TValue="string[]" 
           DataSource="@Statuses" 
           TItem="string"
           Id="status-listbox">
</SfListBox>

<!-- BAD: No context -->
<SfListBox TValue="string[]" DataSource="@Statuses" TItem="string">
</SfListBox>
```

### 2. Sufficient Color Contrast

```razor
<style>
    .accessible-listbox .e-list-item {
        /* WCAG AA: Minimum 4.5:1 contrast ratio for text */
        background-color: white;
        color: #333333; /* Dark gray on white */
    }

    .accessible-listbox .e-list-item.e-active {
        background-color: #1976d2; /* Blue background */
        color: white;
    }
</style>
```

### 3. Visible Focus Indicators

```razor
<style>
    .accessible-listbox .e-list-item {
        outline-offset: -2px;
    }

    .accessible-listbox .e-list-item:focus {
        outline: 3px solid #0066cc;
    }

    .accessible-listbox .e-list-item.e-active:focus {
        outline: 3px solid white;
    }
</style>
```

### 4. Support Keyboard-Only Navigation

```razor
<!-- Always support keyboard navigation -->
<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="string"
           Enabled="true">
</SfListBox>

<!-- Test: Use only keyboard (Tab, Arrow Keys, Space, Enter) -->
```

### 5. Clear Error Messages

```razor
@using Syncfusion.Blazor.DropDowns

<div>
    <SfListBox TValue="string[]" 
               DataSource="@Items" 
               TItem="string"
               @bind-Value="@SelectedValues">
        <ListBoxEvents ValueChange="@ValidateSelection"></ListBoxEvents>
    </SfListBox>
    
    @if (!string.IsNullOrEmpty(ErrorMessage))
    {
        <div role="alert" style="color: #d32f2f; margin-top: 10px;">
            @ErrorMessage
        </div>
    }
</div>

@code {
    private string[] SelectedValues;
    private string ErrorMessage;
    private string[] Items = new string[] { "Item 1", "Item 2", "Item 3" };

    private void ValidateSelection(ChangeEventArgs args)
    {
        var selected = args.Value as string[];
        if (selected == null || selected.Length == 0)
        {
            ErrorMessage = "Please select at least one item.";
        }
        else if (selected.Length > 2)
        {
            ErrorMessage = "You can select up to 2 items only.";
        }
        else
        {
            ErrorMessage = "";
        }
    }
}
```

## Event Binding

### ValueChange Event

Fires when the selected values change:

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="string">
    <ListBoxEvents ValueChange="@OnValueChanged"></ListBoxEvents>
</SfListBox>

<p>@EventLog</p>

@code {
    private string EventLog = "";

    private void OnValueChanged(ChangeEventArgs args)
    {
        var selected = args.Value as string[];
        EventLog = selected != null 
            ? $"Selected: {string.Join(", ", selected)}"
            : "No selection";
    }

    public string[] Items = new string[] { "Apple", "Banana", "Orange", "Mango" };
}
```

## Event Handling Patterns

### Multi-Event Handler

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="string">
    <ListBoxEvents ValueChange="@HandleEvent" ></ListBoxEvents>
</SfListBox>

<div style="margin-top: 20px;">
    <h4>Event Log</h4>
    @foreach(var log in EventLogs.TakeLast(5).Reverse())
    {
        <p>@log</p>
    }
</div>

@code {
    private List<string> EventLogs = new List<string>();

    private void HandleEvent(ChangeEventArgs args)
    {
        AddLog($"[ValueChange] Values: {string.Join(", ", args.Value as string[] ?? new string[] { })}");
    }

    
    private void AddLog(string message)
    {
        EventLogs.Add($"[{DateTime.Now:HH:mm:ss.fff}] {message}");
    }

    public string[] Items = new string[] { "Item 1", "Item 2", "Item 3" };
}
```

### Async Event Handling

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="ItemData">
    <ListBoxFieldSettings Text="Name" Value="Id" />
    <ListBoxEvents ValueChange="@OnSelectionChangedAsync"></ListBoxEvents>
</SfListBox>

<p>Status: @LoadingStatus</p>

@code {
    private string LoadingStatus = "Ready";
    private int[] SelectedIds;

    private async Task OnSelectionChangedAsync(ChangeEventArgs args)
    {
        LoadingStatus = "Processing...";

        var selected = args.Value as string[];
        SelectedIds = selected?.Select(int.Parse).ToArray() ?? new int[] { };

        // Simulate async operation
        await Task.Delay(500);

        LoadingStatus = $"Processed {SelectedIds.Length} item(s)";
    }

    public List<ItemData> Items = new List<ItemData>
    {
        new ItemData { Id = "1", Name = "Item 1" },
        new ItemData { Id = "2", Name = "Item 2" }
    };

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
    }
}
```

### Conditional Event Handling

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="ItemData">
    <ListBoxFieldSettings Text="Name" Value="Id" />
    <ListBoxEvents ValueChange="@OnSelectionChanged"></ListBoxEvents>
</SfListBox>

@code {
    private void OnSelectionChanged(ChangeEventArgs args)
    {
        var selected = args.Value as string[];

        // Only process if valid selection
        if (selected == null || selected.Length == 0)
        {
            Console.WriteLine("No selection");
            return;
        }

        // Conditional logic
        if (selected.Length > 3)
        {
            Console.WriteLine("Too many selections");
        }
        else if (selected.Contains("1"))
        {
            Console.WriteLine("Item 1 is selected");
        }
    }

    public List<ItemData> Items = new List<ItemData>
    {
        new ItemData { Id = "1", Name = "Item 1" },
        new ItemData { Id = "2", Name = "Item 2" },
        new ItemData { Id = "3", Name = "Item 3" }
    };

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
    }
}
```

## Debugging Events

### Event Logger Component

```razor
@using Syncfusion.Blazor.DropDowns

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
    <div>
        <h4>ListBox</h4>
        <SfListBox TValue="string[]" 
                   DataSource="@Items" 
                   TItem="string">
            <ListBoxEvents ValueChange="@LogEvent"></ListBoxEvents>
        </SfListBox>
    </div>
    
    <div>
        <h4>Event Log</h4>
        <div style="border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: auto;">
            @foreach(var log in EventLogs)
            {
                <div style="font-size: 12px; font-family: monospace;">
                    @log
                </div>
            }
        </div>
        <button @onclick="ClearLogs">Clear</button>
    </div>
</div>

@code {
    private List<string> EventLogs = new List<string>();
    private int EventCount = 0;

    private void LogEvent(ChangeEventArgs args)
    {
        EventCount++;
        var timestamp = DateTime.Now.ToString("HH:mm:ss.fff");
        var eventType = "ValueChange";
        var value = string.Join(", ", args.Value as string[] ?? new string[] { });
        
        EventLogs.Add($"[{EventCount}] {timestamp} - {eventType}: [{value}]");
        
        if (EventLogs.Count > 50)
        {
            EventLogs.RemoveAt(0);
        }
    }

    private void ClearLogs()
    {
        EventLogs.Clear();
        EventCount = 0;
    }

    public string[] Items = new string[] { "Item 1", "Item 2", "Item 3" };
}
```

### Console Logging

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="string"
           ValueChange="@OnValueChanged">
</SfListBox>

@code {
    private void OnValueChanged(ChangeEventArgs args)
    {
        var selected = args.Value as string[];
        
        Console.WriteLine("=== ValueChange Event ===");
        Console.WriteLine($"Event Type: ValueChange");
        Console.WriteLine($"Timestamp: {DateTime.Now:O}");
        Console.WriteLine($"Selected Items: {(selected != null ? string.Join(", ", selected) : "None")}");
        Console.WriteLine($"Selection Count: {selected?.Length ?? 0}");
        Console.WriteLine("========================");
    }

    public string[] Items = new string[] { "Item 1", "Item 2", "Item 3" };
}
```

### Performance Monitoring

```razor
@using Syncfusion.Blazor.DropDowns

@code {
    private DateTime LastEventTime = DateTime.Now;
    private int EventCount = 0;

    private void OnValueChanged(ChangeEventArgs args)
    {
        EventCount++;
        var now = DateTime.Now;
        var timeSinceLastEvent = (now - LastEventTime).TotalMilliseconds;
        
        Console.WriteLine($"Event #{EventCount} | Time since last: {timeSinceLastEvent:F2}ms");
        
        LastEventTime = now;
    }
}
```
