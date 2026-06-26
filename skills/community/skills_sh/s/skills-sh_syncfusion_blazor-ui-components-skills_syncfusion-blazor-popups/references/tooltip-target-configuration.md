# Tooltip Target Configuration

This guide covers how to configure tooltip targets, including single elements, multiple elements, and dynamic elements added after initialization.

## Overview

The `Target` property specifies which elements should trigger tooltips using CSS selectors. The Tooltip component supports:
- **Single target**: One specific element
- **Multiple targets**: Multiple elements with one tooltip configuration
- **Dynamic targets**: Elements added after component initialization
- **CSS selectors**: IDs, classes, attributes, and complex selectors

## Target Property

The `Target` property accepts any valid CSS selector string to identify target elements.

### Single Target by ID

Target a specific element using its ID:

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Content="Let's go green to save the planet!!" Target="#btn">
    <SfButton ID="btn" Content="Show Tooltip"></SfButton>
</SfTooltip>
```

**Selector pattern:** `#elementId`

### Single Target by Class

Target an element using its class:

```razor
<SfTooltip Content="Class-based tooltip" Target=".tooltip-trigger">
    <button class="tooltip-trigger">Button</button>
</SfTooltip>
```

**Selector pattern:** `.className`

### Multiple Targets by Class

One tooltip configuration for multiple elements:

```razor
@using Syncfusion.Blazor.Buttons
@using Syncfusion.Blazor.Popups

<SfTooltip Target=".action-button" Content="Perform action">
    <div class="toolbar">
        <SfButton CssClass="action-button" Content="Save"></SfButton>
        <SfButton CssClass="action-button" Content="Delete"></SfButton>
        <SfButton CssClass="action-button" Content="Export"></SfButton>
    </div>
</SfTooltip>
```

**When to use:**
- Uniform tooltip behavior across multiple elements
- Reducing code duplication
- Dynamic element sets
- Toolbar buttons with same tooltip pattern

### Multiple Targets with Attribute Selector

Target all elements with a specific attribute:

```razor
<SfTooltip Target="[data-tooltip='true']" Content="Tooltip content">
    <div>
        <button data-tooltip="true">Button 1</button>
        <button data-tooltip="true">Button 2</button>
        <button data-tooltip="true">Button 3</button>
    </div>
</SfTooltip>
```

**When to use:**
- Semantic HTML markup
- Filtering elements by data attributes
- Progressive enhancement
- Framework integration

### Using Class Selectors for Multiple Elements

Target multiple elements with a shared class name and provide explicit content. Title attributes can remain on elements for semantic HTML, but should not be used as the selector:

```razor
@using Syncfusion.Blazor.Buttons
@using Syncfusion.Blazor.Popups

<SfTooltip ID="Tooltip" Target=".action-item" Content="Click to perform action">
    <div id="container">
        <SfButton ID="btn1" CssClass="action-item" Content="Save" title="Save your changes"></SfButton>
        <SfButton ID="btn2" CssClass="action-item" Content="Cancel" title="Discard changes"></SfButton>
        <button class="action-item" title="Recycle to reduce waste">Recycle Tips</button>
        <a href="#" class="action-item" title="Switch to renewable energy">Renewable Energy</a>
    </div>
</SfTooltip>
```

**How it works:**
- Add class names to elements that should show tooltips
- Set `Target=".action-item"` to select all elements with the class (use class/ID selectors, NOT `[title]`)
- Set explicit `Content` with the tooltip text
- Title attributes on elements provide semantic markup and browser fallback
- Works with any HTML element
- Provides consistent styled Syncfusion tooltips

## Complex Selectors

### Descendant Selector

Target elements within a specific container:

```razor
<!-- All buttons inside #toolbar -->
<SfTooltip Target="#toolbar button" Content="Toolbar action">
    <div id="toolbar">
        <button>Action 1</button>
        <button>Action 2</button>
        <div class="group">
            <button>Action 3</button>
        </div>
    </div>
</SfTooltip>
```

### Child Selector

Target direct children only:

```razor
<!-- Only direct child buttons of #menu -->
<SfTooltip Target="#menu > button" Content="Menu item">
    <div id="menu">
        <button>Direct Child</button>
        <div>
            <button>Not a direct child</button>
        </div>
    </div>
</SfTooltip>
```

### Multiple Selector

Target multiple different selectors:

```razor
<!-- Target buttons AND links -->
<SfTooltip Target="#container button, #container a" Content="Interactive element">
    <div id="container">
        <button>Button</button>
        <a href="#">Link</a>
        <span>Not targeted</span>
    </div>
</SfTooltip>
```

### Pseudo-class Selector

Target elements based on state or position:

```razor
<!-- First button in container -->
<SfTooltip Target="#container button:first-child" Content="First button">
    <div id="container">
        <button>First (targeted)</button>
        <button>Second (not targeted)</button>
    </div>
</SfTooltip>

<!-- All disabled buttons -->
<SfTooltip Target="button:disabled" Content="This action is currently unavailable">
    <button disabled>Disabled Button</button>
</SfTooltip>
```

## Dynamic Targets

### TargetContainer Property

The `TargetContainer` property specifies the container selector where target elements will be automatically registered for tooltips, including elements added to the DOM after initialization.

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip ID="BasicTooltip" Target=".tooltip-item" TargetContainer=".tooltip-container" Content="Helpful information">
</SfTooltip>

<div class="tooltip-container">
    <span class="tooltip-item" title="This is a static element">Static Element</span>
    <SfButton @onclick="AddElement">Add Dynamic Element</SfButton>
    @if (ShowElement)
    {
        <span class="tooltip-item" title="This was added dynamically">Dynamic Element</span>
    }
</div>

@code {
    private bool ShowElement = false;
    
    private void AddElement()
    {
        ShowElement = true;
    }
}
```

### How TargetContainer Works

1. **Set container selector**: `TargetContainer=".tooltip-container"`
2. **Set target selector**: `Target=".tooltip-item"` (use class/ID selectors, NOT `[title]`)
3. **Set content**: Provide explicit `Content` property with tooltip text
4. **Title attributes**: Can be added to elements for semantic markup
5. **Automatic registration**: New elements matching Target inside TargetContainer automatically get tooltips
6. **No manual refresh**: Component handles changes automatically

### When to Use TargetContainer

**Good for:**
- Dynamic lists or grids
- Elements added via user actions
- AJAX/API-loaded content
- Conditional rendering in Blazor
- Real-time data displays

**Example scenarios:**
- Adding rows to a table
- Loading products from API
- Chat messages appearing
- Notification items
- Search results

### Dynamic List Example

```razor
<SfTooltip Target=".list-item" TargetContainer="#dynamic-list" Content="Item in list">
</SfTooltip>

<div id="dynamic-list">
    @foreach (var item in items)
    {
        <div class="list-item" title="@item.Description">
            @item.Name
        </div>
    }
</div>

<SfButton @onclick="AddItem">Add Item</SfButton>

@code {
    private List<Item> items = new()
    {
        new Item { Name = "Item 1", Description = "Description 1" }
    };
    
    private int counter = 2;
    
    private void AddItem()
    {
        items.Add(new Item 
        { 
            Name = $"Item {counter}", 
            Description = $"Description {counter}" 
        });
        counter++;
    }
    
    class Item
    {
        public string Name { get; set; }
        public string Description { get; set; }
    }
}
```

### Dynamic Table Rows

```razor
<SfTooltip Target=".status-cell" TargetContainer="#data-table" Content="@StatusContent">
</SfTooltip>

<SfTooltip Target=".action-btn" TargetContainer="#data-table" Content="@ActionContent">
</SfTooltip>

<table id="data-table">
    <thead>
        <tr>
            <th>Name</th>
            <th>Status</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        @foreach (var row in dataRows)
        {
            <tr class="data-row">
                <td>@row.Name</td>
                <td class="status-cell" title="@row.StatusDetails">@row.Status</td>
                <td>
                    <button class="action-btn" title="Edit @row.Name">✏️</button>
                    <button class="action-btn" title="Delete @row.Name">🗑️</button>
                </td>
            </tr>
        }
    </tbody>
</table>

<button @onclick="AddRow">Add Row</button>

@code {
    private string StatusContent = "Status of the item";
    private string ActionContent = "Perform action on row";
    private List<DataRow> dataRows = new();
    
    private void AddRow()
    {
        dataRows.Add(new DataRow 
        { 
            Name = $"Item {dataRows.Count + 1}",
            Status = "Active",
            StatusDetails = "Currently active and operational"
        });
    }
    
    class DataRow
    {
        public string Name { get; set; }
        public string Status { get; set; }
        public string StatusDetails { get; set; }
    }
}
```

## GUID ID Limitations

⚠️ **Important**: The Tooltip component cannot recognize target IDs that start with a digit.

### The Problem

When using GUIDs as element IDs, tooltips may not work if the GUID starts with a number:

```razor
<!-- ❌ Won't work if GUID starts with digit -->
<SfTooltip Target="#@Guid.NewGuid()" Content="Tooltip">
    <button id="@Guid.NewGuid()">Button</button>
</SfTooltip>

<!-- Example problematic ID: -->
<!-- id="123abc-def-456-ghi-789" -->
```

### The Solution

Prefix GUID IDs with a letter:

```razor
<!-- ✅ Works -->
@{
    var buttonId = $"btn-{Guid.NewGuid()}";
}

<SfTooltip Target="#@buttonId" Content="Tooltip">
    <button id="@buttonId">Button</button>
</SfTooltip>

<!-- Example valid ID: -->
<!-- id="btn-abc123-def-456-ghi-789" -->
```

### Alternative: Use Class Names

Instead of IDs, use class names with GUIDs:

```razor
@{
    var uniqueClass = $"tooltip-target-{Guid.NewGuid()}";
}

<SfTooltip Target=".@uniqueClass" Content="Tooltip">
    <button class="@uniqueClass">Button</button>
</SfTooltip>
```

### Why This Happens

HTML ID selectors in CSS require IDs to start with a letter or certain special characters, not digits. While HTML5 allows digit-starting IDs, CSS selector engines (which Tooltip uses internally) do not.

## Practical Examples

### Icon Toolbar

```razor
<SfTooltip Target=".toolbar-icon" Content="Click toolbar action">
    <div class="toolbar">
        <button class="toolbar-icon" data-action="save" title="Save">💾</button>
        <button class="toolbar-icon" data-action="copy" title="Copy">📋</button>
        <button class="toolbar-icon" data-action="delete" title="Delete">🗑️</button>
        <button class="toolbar-icon" data-action="share" title="Share">🔗</button>
    </div>
</SfTooltip>
```

### Form Fields with Help

```razor
<SfTooltip Target=".form-help" OpensOn="Focus" Content="Enter valid input">
    <div class="form">
        <div class="form-group">
            <label>Email:</label>
            <input class="form-help" type="email" title="Enter a valid email address" placeholder="name@example.com" />
        </div>
        <div class="form-group">
            <label>Password:</label>
            <input class="form-help" type="password" title="Minimum 8 characters, including numbers and symbols" placeholder="Min 8 chars with numbers and symbols" />
        </div>
        <div class="form-group">
            <label>Phone:</label>
            <input class="form-help" type="tel" title="Format: (555) 123-4567" placeholder="(555) 123-4567" />
        </div>
    </div>
</SfTooltip>
```

### Status Indicators

```razor
<SfTooltip Target=".status-indicator" TargetContainer="#status-panel" Content="Service status">
</SfTooltip>

<div id="status-panel">
    @foreach (var service in services)
    {
        <div class="status-item">
            <span class="status-indicator" title="@service.StatusMessage">
                @(service.IsOnline ? "🟢" : "🔴")
            </span>
            <span>@service.Name</span>
        </div>
    }
</div>

@code {
    private List<Service> services = new()
    {
        new Service { Name = "API Server", IsOnline = true, StatusMessage = "All systems operational" },
        new Service { Name = "Database", IsOnline = true, StatusMessage = "Connected and responsive" },
        new Service { Name = "Cache", IsOnline = false, StatusMessage = "Connection timeout" }
    };
    
    class Service
    {
        public string Name { get; set; }
        public bool IsOnline { get; set; }
        public string StatusMessage { get; set; }
    }
}
```

### Navigation Menu

```razor
<SfTooltip Target=".nav-link" Position="Position.RightCenter" Content="Navigate to page">
    <nav id="nav-menu" class="sidebar">
        <a href="/dashboard" class="nav-link" title="View your dashboard">
            <span class="icon">📊</span>
        </a>
        <a href="/reports" class="nav-link" title="Generate reports">
            <span class="icon">📈</span>
        </a>
        <a href="/settings" class="nav-link" title="Configure settings">
            <span class="icon">⚙️</span>
        </a>
        <a href="/profile" class="nav-link" title="Edit your profile">
            <span class="icon">👤</span>
        </a>
    </nav>
</SfTooltip>
```

## Best Practices

### Selector Specificity

**Be specific enough to target intended elements:**

✅ **Good:**
```razor
Target="#toolbar .action-button"
```

❌ **Too broad:**
```razor
Target="button"  <!-- Targets ALL buttons on page -->
```

### Performance

- **Avoid overly broad selectors**: Target specific containers
- **Use IDs when possible**: Fastest selector performance
- **Limit dynamic containers**: One TargetContainer per logical section
- **Use classes over complex selectors**: Better performance

### Maintainability

- **Use semantic class names**: `.help-icon` vs `.tooltip-1`
- **Document selector patterns**: Comment complex selectors
- **Consistent naming**: Follow a naming convention
- **Avoid inline selectors**: Define in constants or configuration

### Accessibility

- **Use title attributes**: Screen readers announce them
- **Provide alternative access**: Don't rely solely on tooltips
- **Keyboard accessible targets**: Ensure targets are focusable
- **Logical tab order**: Tooltips follow document order

### Dynamic Content

- **Always use TargetContainer** for elements added after init
- **Set container at parent level**: Not too broad, not too narrow
- **Test add/remove scenarios**: Verify tooltips work after DOM changes
- **Consider memory**: Remove unused tooltips/containers

### Testing

Always test target configuration with:
- Single and multiple targets
- Dynamic addition/removal of elements
- Various selector types
- Different browsers
- Edge cases (empty containers, no matches)

## Troubleshooting

**Tooltip doesn't appear:**
- Verify Target selector matches element
- Check element exists in DOM when tooltip initializes
- Ensure element is visible (not `display: none`)
- Test selector in browser console: `document.querySelector(selector)`

**Dynamic elements don't show tooltips:**
- Add `TargetContainer` property
- Verify container selector is correct
- Check that Target selector matches new elements
- Ensure TargetContainer exists when component initializes

**GUID IDs don't work:**
- Prefix IDs with letter: `btn-{guid}`
- Or use class names instead
- Or use data attributes: `[data-id='{guid}']`

**Multiple tooltips conflict:**
- Check for overlapping Target selectors
- Use more specific selectors
- Verify CssClass differentiation
- Test with browser dev tools
