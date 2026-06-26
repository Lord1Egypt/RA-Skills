# Styling and Appearance in Blazor ListBox

## Table of Contents
- [Themes](#themes)
- [CSS Customization](#css-customization)
- [Sizing and Layout](#sizing-and-layout)
- [Custom Templates](#custom-templates)
- [Dark Mode](#dark-mode)
- [Responsive Design](#responsive-design)
- [Advanced Styling](#advanced-styling)

## Themes

Syncfusion provides built-in themes. Apply a theme by including the stylesheet in `index.html`.

### Available Themes

Add the theme stylesheet to your `index.html` `<head>` section:

```html
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
```

**Theme Options:**

| Theme | CSS File | Description |
|-------|----------|-------------|
| Bootstrap 5 | `bootstrap5.css` | Modern, clean, responsive design |
| Material | `material.css` | Google Material Design |
| Fluent | `fluent.css` | Microsoft Fluent UI design |
| Tailwind | `tailwind.css` | Tailwind CSS styling |
| Fabric | `fabric.css` | Microsoft Office Fabric design |
| Bootstrap Dark | `bootstrap5-dark.css` | Bootstrap 5 with dark background |
| Material Dark | `material-dark.css` | Material Design dark mode |

### Switching Themes

```html
<!-- Bootstrap 5 (Default) -->
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />

<!-- OR Material Design -->
<link href="_content/Syncfusion.Blazor.Themes/material.css" rel="stylesheet" />

<!-- OR Fluent UI -->
<link href="_content/Syncfusion.Blazor.Themes/fluent.css" rel="stylesheet" />
```

**Note:** Only include one theme stylesheet at a time.

## CSS Customization

### Custom CSS Classes

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="ItemData"
           CssClass="my-listbox">
    <ListBoxFieldSettings Text="Name" Value="Id" />
</SfListBox>

<style>
    .my-listbox {
        border: 2px solid #007bff;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .my-listbox .e-list-item {
        padding: 12px;
        font-size: 14px;
    }

    .my-listbox .e-list-item:hover {
        background-color: #e3f2fd;
    }

    .my-listbox .e-list-item.e-item-focus,
    .my-listbox .e-list-item.e-active {
        background-color: #2196F3;
        color: white;
    }
</style>

@code {
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

### Styling List Items

```razor
<style>
    /* Default item style */
    .e-listbox .e-list-item {
        padding: 10px 15px;
        border-bottom: 1px solid #f0f0f0;
    }

    /* Hover state */
    .e-listbox .e-list-item:hover {
        background-color: #f5f5f5;
        cursor: pointer;
    }

    /* Focus state (keyboard navigation) */
    .e-listbox .e-list-item:focus {
        outline: 2px solid #007bff;
    }

    /* Selected/Active state */
    .e-listbox .e-list-item.e-active {
        background-color: #007bff;
        color: white;
        font-weight: 500;
    }

    /* Checkbox styling */
    .e-listbox .e-list-item.e-checked {
        background-color: #e8f5e9;
    }
</style>
```

### Height and Width Control

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="string"
           Height="250px"
           Width="300px">
</SfListBox>

@code {
    public string[] Items = new string[] { "Apple", "Banana", "Orange", "Mango" };
}
```

## Sizing and Layout

### Full Width

```razor
<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="string"
           Width="100%"
           Height="300px">
</SfListBox>
```

### Container Responsive

```razor
<div style="width: 100%; max-width: 500px; height: 300px;">
    <SfListBox TValue="string[]" 
               DataSource="@Items" 
               TItem="string"
               Width="100%"
               Height="100%">
    </SfListBox>
</div>

@code {
    public string[] Items = new string[] 
    { 
        "Apple", "Banana", "Orange", "Mango", "Grape", 
        "Kiwi", "Pineapple", "Papaya", "Watermelon" 
    };
}
```

### Multi-Column Layout

```razor
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
    <div>
        <h4>Column 1</h4>
        <SfListBox TValue="string[]" DataSource="@Items1" TItem="string" Height="250px">
        </SfListBox>
    </div>
    <div>
        <h4>Column 2</h4>
        <SfListBox TValue="string[]" DataSource="@Items2" TItem="string" Height="250px">
        </SfListBox>
    </div>
</div>

@code {
    public string[] Items1 = new string[] { "Item 1", "Item 2", "Item 3" };
    public string[] Items2 = new string[] { "Item 4", "Item 5", "Item 6" };
}
```

## Custom Templates

### Item Template with Styling

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="ItemData">
    <ListBoxFieldSettings Text="Name" Value="Id" />
    <ListBoxTemplates>
        <ItemTemplate>
            @{
                var item = context as ItemData;
            }
            <div style="display: flex; align-items: center; gap: 12px; padding: 8px 0;">
                <span style="width: 24px; height: 24px; 
                             background-color: @item.Color; 
                             border-radius: 4px;">
                </span>
                <div>
                    <strong>@item.Name</strong>
                    <br />
                    <small style="color: #999;">@item.Category</small>
                </div>
            </div>
        </ItemTemplate>
    </ListBoxTemplates>
</SfListBox>

@code {
    public List<ItemData> Items = new List<ItemData>
    {
        new ItemData { Id = "1", Name = "Red Color", Category = "Primary", Color = "#FF5252" },
        new ItemData { Id = "2", Name = "Green Color", Category = "Primary", Color = "#00E676" },
        new ItemData { Id = "3", Name = "Blue Color", Category = "Primary", Color = "#2979F0" }
    };

    public class ItemData
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Category { get; set; }
        public string Color { get; set; }
    }
}
```

### Rich Content Template

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Products" 
           TItem="ProductData">
    <ListBoxFieldSettings Text="Name" Value="Id" />
    <ListBoxTemplates>
        <ItemTemplate>
            @{
                var product = context as ProductData;
            }
            <div style="display: flex; justify-content: space-between; 
                        padding: 10px; border-bottom: 1px solid #eee;">
                <div>
                    <strong>@product.Name</strong>
                    <div style="font-size: 12px; color: #666;">
                        @product.Description
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: bold; color: #2196F3;">
                        $@product.Price.ToString("F2")
                    </div>
                    <div style="font-size: 12px; color: #999;">
                        Stock: @product.Stock
                    </div>
                </div>
            </div>
        </ItemTemplate>
    </ListBoxTemplates>
</SfListBox>

@code {
    public List<ProductData> Products = new List<ProductData>
    {
        new ProductData { Id = "1", Name = "Laptop", Description = "High-performance device", Price = 1299.99m, Stock = 5 },
        new ProductData { Id = "2", Name = "Mouse", Description = "Wireless mouse", Price = 29.99m, Stock = 50 },
        new ProductData { Id = "3", Name = "Keyboard", Description = "Mechanical keyboard", Price = 129.99m, Stock = 15 }
    };

    public class ProductData
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public decimal Price { get; set; }
        public int Stock { get; set; }
    }
}
```

## Dark Mode

### Bootstrap 5 Dark Theme

```html
<!-- In index.html, replace the theme stylesheet -->
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5-dark.css" rel="stylesheet" />
```

### Material Dark Theme

```html
<link href="_content/Syncfusion.Blazor.Themes/material-dark.css" rel="stylesheet" />
```

### Custom Dark Mode Toggle

```razor
@using Syncfusion.Blazor.DropDowns

<div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
    <h3>Dark Mode Example</h3>
    <button @onclick="ToggleDarkMode">Toggle Dark Mode</button>
</div>

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="string"
           CssClass="@(IsDarkMode ? "dark-mode" : "light-mode")">
</SfListBox>

<style>
    .light-mode {
        background-color: white;
        color: #333;
    }

    .dark-mode {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }

    .dark-mode .e-list-item {
        background-color: #2a2a2a;
        color: #e0e0e0;
    }

    .dark-mode .e-list-item:hover {
        background-color: #383838;
    }

    .dark-mode .e-list-item.e-active {
        background-color: #1976d2;
    }
</style>

@code {
    private bool IsDarkMode = false;
    public string[] Items = new string[] { "Item 1", "Item 2", "Item 3", "Item 4" };

    private void ToggleDarkMode()
    {
        IsDarkMode = !IsDarkMode;
    }
}
```

## Responsive Design

### Mobile-Friendly ListBox

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" 
           DataSource="@Items" 
           TItem="string"
           CssClass="responsive-listbox">
</SfListBox>

<style>
    .responsive-listbox {
        width: 100%;
        max-width: 600px;
    }

    @media (max-width: 768px)
    {
        .responsive-listbox {
            height: 250px;
        }

        .responsive-listbox .e-list-item {
            padding: 15px;
            font-size: 14px;
        }
    }

    @media (max-width: 480px)
    {
        .responsive-listbox {
            height: 200px;
        }

        .responsive-listbox .e-list-item {
            padding: 12px;
            font-size: 13px;
        }
    }
</style>

@code {
    public string[] Items = new string[] 
    { 
        "Option 1", "Option 2", "Option 3", "Option 4", "Option 5" 
    };
}
```

### Flexible Grid Layout

```razor
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
    @for (int i = 1; i <= 3; i++)
    {
        <div>
            <h4>List @i</h4>
            <SfListBox TValue="string[]" DataSource="@GetItems(i)" TItem="string" Height="300px">
            </SfListBox>
        </div>
    }
</div>

@code {
    private string[] GetItems(int listNum)
    {
        return new string[] 
        { 
            $"Item {listNum}-1", 
            $"Item {listNum}-2", 
            $"Item {listNum}-3", 
            $"Item {listNum}-4" 
        };
    }
}
```

## Advanced Styling

### Gradient Background

```razor
<style>
    .gradient-listbox {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px;
        padding: 2px;
    }

    .gradient-listbox .e-listbox {
        background: white;
        border-radius: 6px;
    }
</style>

<div class="gradient-listbox">
    <SfListBox TValue="string[]" DataSource="@Items" TItem="string">
    </SfListBox>
</div>

@code {
    public string[] Items = new string[] { "Item 1", "Item 2", "Item 3" };
}
```

### Shadow and Border Styling

```razor
<style>
    .styled-listbox {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .styled-listbox .e-list-item {
        border-left: 4px solid transparent;
        padding: 12px 15px;
        transition: all 0.2s ease;
    }

    .styled-listbox .e-list-item:hover {
        border-left-color: #2196F3;
        background-color: #f5f5f5;
        padding-left: 18px;
    }

    .styled-listbox .e-list-item.e-active {
        border-left-color: #2196F3;
        background-color: #e3f2fd;
        color: #1976d2;
    }
</style>

<SfListBox TValue="string[]" DataSource="@Items" TItem="string" CssClass="styled-listbox">
</SfListBox>

@code {
    public string[] Items = new string[] { "Item 1", "Item 2", "Item 3" };
}
```

### Animation Effects

```razor
<style>
    .animated-listbox .e-list-item {
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .animated-listbox .e-list-item:hover {
        animation: pulse 0.3s ease-out;
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.02);
        }
    }
</style>

<SfListBox TValue="string[]" DataSource="@Items" TItem="string" CssClass="animated-listbox">
</SfListBox>

@code {
    public string[] Items = new string[] { "Item 1", "Item 2", "Item 3" };
}
```

## Accessibility Styling

### High Contrast Mode

```razor
<style>
    .high-contrast-listbox {
        border: 2px solid #000;
    }

    .high-contrast-listbox .e-list-item {
        background: white;
        color: black;
        padding: 12px;
        font-size: 16px;
    }

    .high-contrast-listbox .e-list-item:focus {
        outline: 3px solid #0066cc;
        outline-offset: 2px;
    }

    .high-contrast-listbox .e-list-item.e-active {
        background: #0066cc;
        color: white;
        font-weight: bold;
    }
</style>
```

### Focus Indicators

```razor
<style>
    .accessible-listbox .e-list-item {
        focus-visible: outline 3px solid #0066cc;
    }

    .accessible-listbox .e-list-item:focus-visible {
        outline: 3px solid #0066cc;
        outline-offset: -3px;
    }
</style>
```
