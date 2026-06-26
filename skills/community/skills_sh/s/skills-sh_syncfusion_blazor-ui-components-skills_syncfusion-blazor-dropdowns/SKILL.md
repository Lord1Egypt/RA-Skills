---
name: syncfusion-blazor-dropdowns
description: Comprehensive guide for implementing Syncfusion Blazor dropdown components including AutoComplete, ComboBox, DropDown List, MultiSelect Dropdown, and ListBox. Use this when building selection interfaces, data binding, filtering, cascading dropdowns, custom templates, and accessible dropdown experiences in Blazor applications. Covers all dropdown components from Syncfusion.Blazor.DropDowns package.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Dropdowns"
---

# Implementing Syncfusion Blazor Dropdowns

## AutoComplete

The AutoComplete component provides intelligent search suggestions as users type, supporting local and remote data sources with advanced filtering, customization, and accessibility features.

### Component Overview

The **SfAutoComplete** component enables:
- **Data Binding:** Local primitives, objects, or remote data sources
- **Filtering:** Real-time search with debounce, filter types (StartsWith, Contains, EndsWith)
- **Organization:** Grouping, sorting, multicolumn display
- **Customization:** Item/group/header/footer templates, styling, placeholders
- **Performance:** Virtualization for large datasets
- **Accessibility:** WCAG compliance, keyboard navigation, ARIA support
- **Interactions:** Events, disabled items, custom values, RTL support

### Documentation Navigation Guide

Choose the reference that matches your current task:

#### Getting Started
📄 **Read:** [references/getting-started.md](references/autocomplete-getting-started.md)
- Installation of NuGet packages
- Project setup (Visual Studio, VS Code, .NET CLI)
- Basic autocomplete implementation
- CSS imports and theme setup
- Initial configuration

#### Data Binding & Sources
📄 **Read:** [references/data-binding.md](references/autocomplete-data-binding.md)
- Binding local data (primitives, objects, ObservableCollection)
- Complex data types (ExpandoObject, DynamicObject)
- Remote data with DataManager
- ODataAdaptor, Web API, and custom adaptors
- DataBound event handling

#### Filtering & Search
📄 **Read:** [references/filtering-and-search.md](references/autocomplete-filtering-and-search.md)
- Enabling and configuring filtering
- Filter types (StartsWith, Contains, EndsWith)
- Local vs. remote data filtering
- DebounceDelay for performance
- Minimum character length
- Highlight search results

#### Data Organization
📄 **Read:** [references/data-organization.md](references/autocomplete-data-organization.md)
- Grouping data by categories
- Sorting list items
- Multicolumn display
- Selection and selection modes
- Value binding and custom values

#### Templates & Styling
📄 **Read:** [references/templates-and-styling.md](references/autocomplete-templates-and-styling.md)
- Item templates (custom list item layout)
- Group templates (group header customization)
- Header, footer, and no-records templates
- CSS class styling
- Placeholder and FloatLabel customization

#### Advanced Features
📄 **Read:** [references/advanced-features.md](references/autocomplete-advanced-features.md)
- Virtualization for large datasets
- Popup settings and positioning
- Disabled items handling
- Custom values support
- Localization and RTL support
- Event handling (ActionBegin, ActionComplete, ValueChange, etc.)

#### Accessibility & Best Practices
📄 **Read:** [references/accessibility-and-best-practices.md](references/autocomplete-accessibility-and-best-practices.md)
- WCAG compliance and accessibility standards
- ARIA attributes
- Keyboard navigation support
- Screen reader compatibility
- Performance optimization tips
- Common issues and troubleshooting

### Quick Start Example

A minimal AutoComplete implementation with local data:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Country" DataSource="@Countries">
    <AutoCompleteFieldSettings Value="CountryName"></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Country
    {
        public string CountryName { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { CountryName = "Austria" },
        new Country { CountryName = "Brazil" },
        new Country { CountryName = "Canada" }
    };
}
```

### Common Patterns

#### Pattern 1: Filtering User Input
Enable real-time filtering as users type:
```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Options"
                AllowFiltering="true"
                FilterType="FilterType.Contains">
</SfAutoComplete>
```

#### Pattern 2: Remote Data with Debounce
Reduce server requests with debounce delay:
```blazor
<SfAutoComplete TValue="string" TItem="Product" 
                AllowFiltering="true"
                DebounceDelay="300">
    <SfDataManager Url="api/products" Adaptor="Syncfusion.Blazor.Adaptors.ODataAdaptor"></SfDataManager>
</SfAutoComplete>
```

#### Pattern 3: Custom Item Display with Templates
Customize list item appearance:
```blazor
<SfAutoComplete TValue="string" TItem="Product" DataSource="@Products">
    <AutoCompleteTemplates TItem="Product">
        <ItemTemplate>
            <div>
                <span>@((context as Product)?.ProductName)</span>
                <span style="float:right">@((context as Product)?.Price)</span>
            </div>
        </ItemTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>
```

#### Pattern 4: Grouped & Sorted Display
Organize data with grouping and sorting:
```blazor
<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees"
                SortOrder="SortOrder.Ascending">
    <AutoCompleteFieldSettings GroupBy="Department" Value="EmployeeName"></AutoCompleteFieldSettings>
</SfAutoComplete>
```

### Key Props

| Prop | Type | Purpose |
|------|------|---------|
| `DataSource` | `IEnumerable<TItem>` | Source data for suggestions |
| `AllowFiltering` | `bool` | Enable/disable filtering |
| `FilterType` | `FilterType` | Filter mode (StartsWith, Contains, EndsWith) |
| `DebounceDelay` | `int` | Delay in ms before filter triggers |
| `MinLength` | `int` | Min characters to trigger filtering |
| `SortOrder` | `SortOrder` | Sort list items (Ascending, Descending) |
| `EnableVirtualization` | `bool` | Virtualize large datasets |
| `AllowCustom` | `bool` | Allow users to enter custom values |
| `Placeholder` | `string` | Input placeholder text |
| `FloatLabelType` | `FloatLabelType` | Floating label behavior |

### Common Use Cases

1. **Search-as-you-type:** Autocomplete on employee names, products, locations
2. **Filtered dropdowns:** Show matching items as users filter
3. **Remote APIs:** Fetch suggestions from backend services
4. **Multi-column display:** Show product details alongside names
5. **Grouped suggestions:** Organize by category or department
6. **Custom values:** Allow users to create new entries
7. **Large datasets:** Virtualize for performance with 1000+ items

---

**Next Steps:** Start with [getting-started.md](references/autocomplete-getting-started.md) for setup, or jump to the reference that matches your task.

---

## ComboBox

A comprehensive skill for implementing the ComboBox component. The ComboBox allows users to select a value from a dropdown list while also providing filtering, custom templates, cascading scenarios, data binding, and extensive customization options.

### When to Use This Skill

Use this skill when you need to:
- Install and set up the ComboBox component
- Implement ComboBox with local or remote data sources
- Configure data binding (primitive types, complex objects, collections)
- Enable and configure filtering and search functionality
- Handle value selection and change events
- Create cascading ComboBox scenarios (dependent dropdowns)
- Customize appearance with templates (items, header, footer)
- Integrate ComboBox with form validation (EditForm, data annotations)
- Configure popup settings (height, width, resize, positioning)
- Apply grouping and sorting to ComboBox data
- Handle events (ValueChange, OnValueSelect, Blur, etc.)
- Implement accessibility and keyboard navigation
- Customize styling and themes
- Troubleshoot common ComboBox issues

### Quick Start Example

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string" 
    Placeholder="Select a country" 
    DataSource="@CountryData"
    @bind-Value="@SelectedValue">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    private string SelectedValue = "USA";
    private List<Country> CountryData = new()
    {
        new Country { Name = "United States", Code = "USA" },
        new Country { Name = "United Kingdom", Code = "UK" },
        new Country { Name = "Canada", Code = "CA" }
    };

    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }
}
```

### Key Props Reference

| Property | Type | Purpose |
|----------|------|---------|
| `TValue` | Generic | Type of the selected value |
| `TItem` | Generic | Type of data items in the list |
| `DataSource` | IEnumerable | List of items to display |
| `@bind-Value` | TValue | Two-way binding for selected value |
| `@bind-Index` | int? | Two-way binding for selected index |
| `Placeholder` | string | Hint text when no value selected |
| `AllowFiltering` | bool | Enable/disable filtering |
| `AllowCustom` | bool | Allow free-text entry |
| `Readonly` | bool | Make component read-only |
| `Disabled` | bool | Disable the component |

### Common Patterns

#### Pattern 1: Basic Data Binding
Bind ComboBox to local list with primitive or complex types. Use `ComboBoxFieldSettings` to map text/value fields.

#### Pattern 2: Filtering & Search
Enable `AllowFiltering` to let users filter data as they type. Control filter behavior with `FilterType` and `DebounceDelay`.

#### Pattern 3: Cascading ComboBox
Use `ValueChange` event in parent ComboBox to populate child ComboBox data dynamically based on parent selection.

#### Pattern 4: Form Integration
Wrap ComboBox in EditForm with data annotations for automatic validation. Use `ValidationMessage` to display errors.

#### Pattern 5: Custom Templates
Use `ItemTemplate`, `HeaderTemplate`, `FooterTemplate` to create custom UI for list items and popup sections.

---

### Documentation Navigation Guide

Read the appropriate reference file based on your task:

#### 📄 Getting Started
**Read:** [references/getting-started.md](references/combobox-getting-started.md)
- Installation and NuGet packages
- Basic ComboBox implementation
- Web App vs Server App setup
- CSS imports and themes
- First working example

#### 📄 Data Binding
**Read:** [references/data-binding.md](references/combobox-data-binding.md)
- Local data binding (arrays, lists, collections)
- Primitive type vs complex object binding
- Index-based value binding
- Remote data with DataManager
- OData and Web API adaptors
- Custom data adaptors
- Dynamic object binding scenarios

#### 📄 Filtering & Search
**Read:** [references/filtering.md](references/combobox-filtering.md)
- Enable filtering with `AllowFiltering`
- Local vs remote data filtering
- Filter types (contains, startsWith, endsWith)
- Custom filtering logic
- Debounce delay for performance
- Case-sensitive filtering options

#### 📄 Selection & Value Binding
**Read:** [references/selection-and-value.md](references/combobox-selection-and-value.md)
- Get and set selected value
- Value vs Index binding
- Preselected values on initialization
- Programmatic value changes
- Selection events (ValueChange, OnValueSelect)
- Autofill functionality

#### 📄 Cascading ComboBox
**Read:** [references/cascading-combobox.md](references/combobox-cascading-combobox.md)
- Create dependent/cascading ComboBox chains
- Populate child ComboBox based on parent selection
- Multi-level cascading (3+ levels)
- Populate other form fields from selection
- Real-world examples

#### 📄 Templates & Customization
**Read:** [references/templates-and-customization.md](references/combobox-templates-and-customization.md)
- Item templates for custom list rendering
- Group templates for grouped data
- Header and footer templates
- Value template customization
- HTML content in templates
- Template debugging tips

#### 📄 Events & Validation
**Read:** [references/events-and-validation.md](references/combobox-events-and-validation.md)
- ComboBox events (Creating, Created, Blur, etc.)
- ValueChange and OnValueSelect events
- Form validation with EditForm
- Data annotations and validation rules
- Custom validation logic
- Preventing operations with event cancellation

#### 📄 Popup & Appearance
**Read:** [references/popup-and-appearance.md](references/combobox-popup-and-appearance.md)
- Popup height and width configuration
- Popup positioning and z-index
- Popup open/close events
- Allow popup resize
- Show popup on initial load
- Placeholder and FloatLabel
- CSS classes and styling

#### 📄 Advanced Features
**Read:** [references/advanced-features.md](references/combobox-advanced-features.md)
- Grouping data by category
- Sorting options and custom sort order
- Virtualization for large datasets
- Disabled items in the list
- RTL (right-to-left) support
- Accessibility (WCAG compliance)
- Keyboard navigation

#### 📄 Troubleshooting
**Read:** [references/troubleshooting.md](references/combobox-troubleshooting.md)
- Data not loading or empty list
- Filtering not working as expected
- Selection/binding issues
- Event handlers not firing
- Performance optimization tips
- Common errors and solutions

---

### Common Use Cases

**Use Case 1: Country/State/City Selection**
- Create 3-level cascading ComboBox
- User selects country → states populate → cities populate
- See: Cascading ComboBox + Events & Validation

**Use Case 2: Search/Filter List with Custom Display**
- Enable filtering with custom templates
- Show complex data (icons, descriptions, colors)
- See: Filtering & Search + Templates & Customization

**Use Case 3: Form with Multiple Dropdowns**
- Integrate ComboBox into EditForm
- Validate selections with data annotations
- Cascade between dropdowns
- See: Events & Validation + Cascading ComboBox

**Use Case 4: Large Dataset Performance**
- Bind to 1000+ items with virtualization
- Enable remote filtering via API
- Configure debounce delay
- See: Advanced Features + Data Binding

### Key Features Summary

✅ **Local & Remote Data Binding** - Support for arrays, lists, observables, DataManager  
✅ **Flexible Filtering** - Built-in filtering with customization options  
✅ **Templates** - Item, group, header, footer templates for custom UI  
✅ **Cascading** - Create dependent dropdown chains  
✅ **Form Integration** - Native EditForm and validation support  
✅ **Events** - Rich event system for user interactions  
✅ **Accessibility** - WCAG compliance, keyboard navigation  
✅ **Customization** - Theming, styling, CSS classes  
✅ **Performance** - Virtualization support for large lists  
✅ **RTL Support** - Right-to-left language support

---

### Related Components

- **DropdownList** - Similar to ComboBox but without free-text entry
- **AutoComplete** - Suggestive text input with dropdown
- **MultiSelect** - Allow multiple selections from dropdown
- **ListBox** - Scrollable list with selection support

---

## DropDown List

A comprehensive skill for implementing the Syncfusion DropDown List component in Blazor applications. This component provides flexible item selection with support for data binding, filtering, templating, cascading, and extensive customization options.

### When to Use This Skill

Use this skill when you need to:
- Create a dropdown list component for item selection in Blazor
- Bind dropdown data from local collections or remote APIs
- Implement filtering and search functionality
- Customize dropdown rendering with templates
- Handle selection events and value binding
- Create cascading dropdown relationships
- Group and sort dropdown items
- Implement form validation with dropdown selection
- Apply styling and theming to dropdowns
- Support accessibility and keyboard navigation
- Enable RTL (Right-to-Left) support for localization
- Manage large datasets with virtualization
- Configure popup behavior and positioning
- Handle disabled items and placeholders

### Component Overview

**Key Capabilities:**
- **Multiple Selection**: Select one or many items using various modes
- **Data Sources**: Bind to collections, APIs, or custom data providers
- **Filtering**: Built-in search with customizable filter options
- **Grouping & Sorting**: Organize items hierarchically with sorting
- **Custom Templates**: Design custom item, group, header, and footer templates
- **Keyboard Navigation**: Full keyboard support and accessibility (WCAG 2.1)
- **Theming**: Bootstrap, Material, Fluent, Tailwind themes with light/dark modes
- **Validation**: Form validation support with custom validators
- **RTL & Localization**: Right-to-left language support and multi-language
- **Virtualization**: Handle large datasets efficiently

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started-dropdown-list.md](references/dropdown-list-getting-started.md)
- Installation and NuGet package setup
- Basic component implementation
- CSS theme imports
- Minimal working example
- Rendering the dropdown

#### Data Binding
📄 **Read:** [references/data-binding.md](references/dropdown-list-data-binding.md)
- Binding local collections (primitives, complex types, observables)
- Remote data binding with Web API and OData
- Data source events (OnActionBegin, OnActionComplete)
- Dynamic and enum data binding
- Value tuple and expando object binding

#### Filtering and Searching
📄 **Read:** [references/filtering-and-searching.md](references/dropdown-list-filtering-and-searching.md)
- Filter types and strategies
- Case-sensitive filtering
- Minimum filter length configuration
- Debounce delay for performance optimization
- Multi-column filtering
- Custom filtering logic

#### Templates and Rendering
📄 **Read:** [references/templates-and-rendering.md](references/dropdown-list-templates-and-rendering.md)
- Item template customization
- Header and footer templates
- Value template for selection display
- Conditional rendering in templates
- Complex template patterns

#### Selection and Value Binding
📄 **Read:** [references/selection-and-value-binding.md](references/dropdown-list-selection-and-value-binding.md)
- Getting and setting selected values
- Value binding with @bind-Value directive
- Value changed events
- Clearing and resetting selection
- Working with complex object selections

#### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/dropdown-list-customization-and-styling.md)
- Opening dropdown on focus
- CSS class application
- Theme application and switching
- Component sizing and appearance
- Styling open and closed states

#### Advanced Features
📄 **Read:** [references/advanced-features.md](references/dropdown-list-advanced-features.md)
- Cascading dropdowns for dependent selections
- Item grouping and organization
- Sorting and ordering options
- Disabled items and states
- Placeholder text and float label
- Popup settings and positioning
- Virtualization for large datasets

#### Form Validation
📄 **Read:** [references/form-validation.md](references/dropdown-list-form-validation.md)
- EditForm integration
- Data annotation validation
- Validation error display
- Custom validation rules
- Form submission patterns

#### Localization and RTL
📄 **Read:** [references/localization-and-rtl.md](references/dropdown-list-localization-and-rtl.md)
- RTL (Right-to-Left) support
- Localization patterns
- Culture-specific formatting
- Multi-language support

#### Accessibility
📄 **Read:** [references/accessibility.md](references/dropdown-list-accessibility.md)
- WCAG 2.1 compliance
- WAI-ARIA attributes and roles
- Keyboard navigation (Arrow keys, Enter, Escape)
- Screen reader compatibility
- Focus management
- High contrast support

### Quick Start

#### Basic Dropdown Implementation

```razor
@page "/dropdown-demo"

<h3>Simple Dropdown List</h3>

<SfDropDownList TValue="int" TItem="Country" DataSource="@Countries" Placeholder="Select a country">
    <DropDownListFieldSettings Text="@nameof(Country.CountryName)" Value="@nameof(Country.CountryId)" />
</SfDropDownList>

@code {
    public List<Country> Countries { get; set; }

    protected override void OnInitialized()
    {
        Countries = new List<Country>
        {
            new Country { CountryId = 1, CountryName = "United States" },
            new Country { CountryId = 2, CountryName = "Canada" },
            new Country { CountryId = 3, CountryName = "Mexico" }
        };
    }

    public class Country
    {
        public int CountryId { get; set; }
        public string CountryName { get; set; }
    }
}
```

#### With Value Binding and Selection Event

```razor
<SfDropDownList TValue="int" TItem="Country" @bind-Value="SelectedCountryId"
                DataSource="@Countries"
                Placeholder="Choose a country">
    <DropDownListFieldSettings Text="@nameof(Country.CountryName)" Value="@nameof(Country.CountryId)" />
    <DropDownListEvents TValue="int" TItem="Country" ValueChange="@OnValueChange"></DropDownListEvents>
</SfDropDownList>

<p>Selected: @SelectedCountryId</p>

@code {
    private int SelectedCountryId;
    
    protected override void OnInitialized()
    {
        Countries = new List<Country>
        {
            new Country { CountryId = 1, CountryName = "United States" },
            new Country { CountryId = 2, CountryName = "Canada" },
            new Country { CountryId = 3, CountryName = "Mexico" }
        };
    }

    public class Country
    {
        public int CountryId { get; set; }
        public string CountryName { get; set; }
    }

    private void OnValueChange(ChangeEventArgs<int, Country> args)
    {
        SelectedCountryId = args.Value;
        // Handle value change
    }
}
```

### Common Patterns

#### Pattern 1: Dropdown with Filtering

Enable filter-as-you-type functionality to let users quickly find items in large lists:

```razor
<SfDropDownList TValue="string" TItem="string"
                DataSource="@Items"
                AllowFiltering="true"
                FilterType="Syncfusion.Blazor.DropDowns.FilterType.Contains"
                Placeholder="Type to filter">
</SfDropDownList>
```

#### Pattern 2: Cascading Dropdowns

Create dependent dropdowns where selection in one dropdown affects the options in another:

```razor
<SfDropDownList TValue="int" TItem="Country" @bind-Value="SelectedCountry"
                DataSource="@Countries"
                Placeholder="Select Country">
    <DropDownListFieldSettings Text="@nameof(Country.Name)" Value="@nameof(Country.Id)" />
    <DropDownListEvents TValue="int" TItem="Country" ValueChange="@OnCountryChange"></DropDownListEvents>
</SfDropDownList>

<SfDropDownList TValue="int" TItem="City"
                DataSource="@FilteredCities"
                Placeholder="Select City">
    <DropDownListFieldSettings Text="@nameof(City.Name)" Value="@nameof(City.Id)" />
</SfDropDownList>

@code {
    private int SelectedCountry;
    private List<City> FilteredCities;

    private void OnCountryChange(ChangeEventArgs<int, Country> args)
    {
        SelectedCountry = args.Value;
        FilteredCities = Cities.Where(c => c.CountryId == SelectedCountry).ToList();
    }
}
```

#### Pattern 3: Remote Data Binding

Connect to APIs for dynamic data loading:

```razor
<SfDropDownList TValue="int" TItem="DataItem"
                DataSource="@RemoteData"
                Placeholder="Select item">
    <DropDownListFieldSettings Text="@nameof(DataItem.CountryName)" Value="@nameof(DataItem.CountryId)" />
    <DropDownListEvents TValue="int" TItem="DataItem" OnActionComplete="@OnActionComplete"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<DataItem> RemoteData;
    
    private async Task OnActionComplete(ActionCompleteEventArgs<DataItem> args)
    {
        var response = await HttpClient.GetAsync("api/items");
        RemoteData = await response.Content.ReadAsAsync<List<DataItem>>();
    }

    public class DataItem
    {
        public int CountryId { get; set; }
        public string CountryName { get; set; }
    }
}
```

#### Pattern 4: Custom Item Template

Use templates to display rich content in dropdown items:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Employees">
    <DropDownListFieldSettings Text="@nameof(Employee.EmployeeName)" Value="@nameof(Employee.Id)" />
    <DropDownListTemplates TValue="Employee">
        <ItemTemplate>
            <span>@context.EmployeeName - @context.Designation</span>
        </ItemTemplate>
    </DropDownListTemplates>
</SfDropDownList>
```

#### Pattern 5: Form Validation

Integrate with EditForm for validation:

```razor
<EditForm Model="@FormModel">
    <DataAnnotationsValidator />
    <ValidationSummary />
    
    <div class="form-group">
        <label>Select Department</label>
        <SfDropDownList TValue="int" TItem="Department" @bind-Value="FormModel.DepartmentId"
                        DataSource="@Departments"
                        Placeholder="Choose department">
            <DropDownListFieldSettings Text="@nameof(Department.Name)" Value="@nameof(Department.Id)" />
        </SfDropDownList>
    </div>
    
    <button type="submit">Submit</button>
</EditForm>

@code {
    private FormData FormModel = new();
    
    public class FormData
    {
        [Required(ErrorMessage = "Department is required")]
        public int DepartmentId { get; set; }
    }
}
```

### Key Props and Events

#### Essential Properties

| Property | Description |
|----------|-------------|
| `DataSource` | `IEnumerable<T>` Collection of items to display |
| `Value` / `@bind-Value` | `TValue` Currently selected value |
| `Placeholder` | `string` Hint text when no selection |
| `AllowFiltering` | `bool` Enable search/filter functionality |
| `FilterType` | `FilterType` Filter strategy (StartsWith, Contains, EndsWith) |
| `Enabled` | `bool` Enable or disable the dropdown |
| `EnableRtl` | `bool` Right-to-Left text direction |
| `Width` | `string` Component width (px, %, etc.) |

> **Field mapping:** Use the `<DropDownListFieldSettings Text="..." Value="..." />` child component tag to map data fields.

#### Essential Events (inside `<DropDownListEvents>`)

| Event | Description |
|-------|-------------|
| `ValueChange` | Triggered when selected value changes |
| `OnActionBegin` | Before remote data fetch begins |
| `OnActionComplete` | After remote data fetch completes |
| `OnActionFailure` | When remote data fetch fails |
| `OnOpen` | When dropdown opens |
| `OnClose` | When dropdown closes |
| `Focus` | When component receives focus |
| `Blur` | When component loses focus |

### Common Use Cases

1. **User Selection in Forms** - Select users from a list for assignment or notification
2. **Category/Type Selection** - Choose from predefined categories or types
3. **Cascading Selections** - Dependent dropdowns (Country → State → City)
4. **Dynamic Data from APIs** - Load options from backend services
5. **Searchable Lists** - Filter through large datasets efficiently
6. **Multi-stage Workflows** - Selection-based form navigation
7. **Data Filtering** - Apply filters based on dropdown selection
8. **Templated Dropdowns** - Display rich content (images, descriptions)
9. **Localized Selections** - Region/language-specific options
10. **Accessibility-Compliant Forms** - WCAG-compliant selection interface

### Related Components

- **ComboBox** - Editable dropdown with text input capability
- **AutoComplete** - Text input with auto-suggestion dropdown
- **ListBox** - Multi-item list with selection options
- **MultiSelect Dropdown** - Select multiple items from a list
- **Mention** - @mention autocomplete (like social media)

### Next Steps

1. Choose your use case from "Common Use Cases" above
2. Navigate to the relevant reference guide in the "Documentation and Navigation Guide" section
3. Copy the pattern example and adapt it to your specific data and requirements
4. Consult the specific reference for advanced configurations and edge cases

For detailed implementation patterns, complete code examples, and troubleshooting guidance, read the appropriate reference file based on your specific needs.

---

## MultiSelect Dropdown

The MultiSelect Dropdown component enables users to select multiple items from a list with support for filtering, grouping, sorting, keyboard navigation, accessibility, and extensive customization options. This skill guides you through installation, implementation, data binding, features, customization, and advanced scenarios.

### When to Use This Skill

Use this skill when you need to:
- Install and configure the MultiSelect Dropdown component in Blazor projects
- Implement multiple item selection in forms and applications
- Set up data binding with collections, APIs, or remote sources
- Configure selection modes (Checkbox, Delimiter, Box)
- Add filtering and grouping capabilities to dropdowns
- Customize appearance, styling, and templates
- Implement keyboard navigation and accessibility features
- Handle selection events and programmatic selection
- Support localization, RTL, and globalization
- Optimize performance with virtualization
- Integrate with forms and validation

### Component Overview

**Key Capabilities:**
- **Multiple Selection**: Select one or many items using various modes
- **Data Sources**: Bind to collections, APIs, or custom data providers
- **Filtering**: Built-in search with customizable filter options
- **Grouping & Sorting**: Organize items hierarchically with sorting
- **Custom Templates**: Design custom item, group, header, and footer templates
- **Keyboard Navigation**: Full keyboard support and accessibility (WCAG 2.1)
- **Theming**: Bootstrap, Material, Fluent, Tailwind themes with light/dark modes
- **Validation**: Form validation support with custom validators
- **RTL & Localization**: Right-to-left language support and multi-language
- **Virtualization**: Handle large datasets efficiently

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/multiselect-getting-started.md)
- Installation and NuGet package setup
- Basic MultiSelect Dropdown implementation
- Namespace imports and service registration
- Theme application
- Minimal working example
- Common setup troubleshooting

#### Data Binding
📄 **Read:** [references/data-binding.md](references/multiselect-data-binding.md)
- Binding to collections (List, ObservableCollection)
- Remote data binding and API integration
- Custom data adapters and sources
- Value binding patterns
- Handling null and empty data
- Performance considerations

#### Features and Selection
📄 **Read:** [references/features-and-selection.md](references/multiselect-features-and-selection.md)
- Selection modes (Checkbox, Delimiter, Box)
- Single vs. multiple item selection
- Select/deselect all functionality
- Programmatic selection and value updates
- Custom values and free-form text input
- Default selected values
- Disabled items and item groups
- Virtualization for large datasets

#### Filtering and Grouping
📄 **Read:** [references/filtering-and-grouping.md](references/multiselect-filtering-and-grouping.md)
- Enable and configure filtering
- Filter placeholder and debounce delay
- Custom filter implementation
- Case-sensitive and multi-field filtering
- Remote filtering from APIs
- Data grouping with group headers
- Sorting within groups
- Filter performance optimization

#### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/multiselect-customization-and-styling.md)
- CSS classes and theme customization
- Placeholder and floating labels
- Icon support (prefix/suffix icons)
- Popup width and height customization
- Chip display modes and styling
- Popup positioning
- RTL (Right-to-Left) support
- Dark mode implementation
- Custom CSS variables and overrides

#### Accessibility and Templates
📄 **Read:** [references/accessibility-and-templates.md](references/multiselect-accessibility-and-templates.md)
- ARIA attributes and screen reader support
- Keyboard navigation shortcuts
- Focus management and visual focus indicators
- WCAG 2.1 compliance
- ItemTemplate for custom item rendering
- GroupTemplate for custom group headers
- HeaderTemplate and FooterTemplate
- Template binding and context
- Accessibility in custom templates

#### Events and API Reference
📄 **Read:** [references/events-and-api.md](references/multiselect-events-and-api.md)
- Complete event reference (Change, Focus, Blur, Open, Close)
- Event handling patterns in Blazor
- Event arguments and return values
- Component API methods (Open, Close, Focus, Refresh)
- Property access and state updates
- Reactive patterns for state management
- Real-world event handling examples

#### Advanced Scenarios
📄 **Read:** [references/advanced-scenarios.md](references/multiselect-advanced-scenarios.md)
- Form integration and validation
- Localization and globalization setup
- Custom value creation and suggestion
- Performance optimization techniques
- Multiple dropdown instances management
- Server-side vs. client-side filtering
- Real-world use cases and patterns
- Edge cases and troubleshooting
- Best practices and gotchas

### Quick Start

#### Minimal Example

**1. Install NuGet Package:**
```bash
dotnet add package Syncfusion.Blazor.DropDowns
```

**2. Add to `_Imports.razor`:**
```csharp
@using Syncfusion.Blazor
@using Syncfusion.Blazor.DropDowns
```

**3. Register Service in `Program.cs`:**
```csharp
builder.Services.AddSyncfusionBlazor();
```

**4. Add Theme in `App.razor`:**
```html
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
<script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
```

**5. Use MultiSelect Dropdown:**
```csharp
@page "/multiselect-demo"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]" 
               TItem="EmployeeData"
               DataSource="@Employees"
               Placeholder="Select employees">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<EmployeeData> Employees { get; set; } = new();

    protected override void OnInitialized()
    {
        Employees = new List<EmployeeData>
        {
            new() { ID = "1", Name = "Alice Johnson" },
            new() { ID = "2", Name = "Bob Smith" },
            new() { ID = "3", Name = "Carol White" }
        };
    }

    public class EmployeeData
    {
        public string ID { get; set; }
        public string Name { get; set; }
    }
}
```

### Common Patterns

#### Pattern 1: Two-Way Binding with Selection Change

```csharp
@page "/multiselect-binding"
@using Syncfusion.Blazor.DropDowns

<div>
    <p>Selected IDs: @string.Join(", ", SelectedValues)</p>
    <SfMultiSelect TValue="string[]" 
                   TItem="ItemData"
                   DataSource="@Items"
                   @bind-Value="SelectedValues"
                   Placeholder="Select items">
        <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    </SfMultiSelect>
</div>

@code {
    private string[] SelectedValues { get; set; } = Array.Empty<string>();
    private List<ItemData> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<ItemData>
        {
            new() { ID = "1", Name = "Item 1" },
            new() { ID = "2", Name = "Item 2" },
            new() { ID = "3", Name = "Item 3" }
        };
    }

    public class ItemData
    {
        public string ID { get; set; }
        public string Name { get; set; }
    }
}
```

#### Pattern 2: Filtering with Remote Data

```csharp
<SfMultiSelect TValue="string[]" 
               TItem="RemoteItem"
               DataSource="@RemoteData"
               AllowFiltering="true"
               Mode="VisualMode.CheckBox"
               Placeholder="Search and select">
    <MultiSelectFieldSettings Text="Text" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectEvents TValue="string[]" TItem="RemoteItem" 
                       Filtering="OnFiltering">
    </MultiSelectEvents>
</SfMultiSelect>

@code {
    private List<RemoteItem> RemoteData { get; set; } = new();

    private async Task OnFiltering(FilteringEventArgs args)
    {
        // Filter items based on search text
        args.PreventDefaultAction = true;
        var filtered = RemoteData
            .Where(x => x.Text.Contains(args.Text, StringComparison.OrdinalIgnoreCase))
            .ToList();
        
        // Update DataSource with filtered results
        // (Implementation depends on your component reference handling)
    }

    public class RemoteItem
    {
        public string ID { get; set; }
        public string Text { get; set; }
    }
}
```

#### Pattern 3: Custom Validation in Form

```csharp
<EditForm Model="FormData" OnValidSubmit="HandleSubmit">
    <DataAnnotationsValidator />
    
    <div class="form-group">
        <label>Select at least 2 items:</label>
        <SfMultiSelect TValue="string[]"
                       TItem="ItemData"
                       DataSource="@Items"
                       @bind-Value="FormData.SelectedItems"
                       Placeholder="Select items">
            <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
        </SfMultiSelect>
        <ValidationMessage For="@(() => FormData.SelectedItems)" />
    </div>
    
    <button type="submit">Submit</button>
</EditForm>

@code {
    private FormModel FormData { get; set; } = new();
    private List<ItemData> Items { get; set; } = new();

    private async Task HandleSubmit()
    {
        // Handle form submission
    }

    public class FormModel
    {
        [Required(ErrorMessage = "Please select items")]
        [MinLength(2, ErrorMessage = "Select at least 2 items")]
        public string[] SelectedItems { get; set; } = Array.Empty<string>();
    }

    public class ItemData
    {
        public string ID { get; set; }
        public string Name { get; set; }
    }
}
```

### Key Props Reference

| Property | Type | Description | When to Use |
|----------|------|-------------|-----------|
| `DataSource` | `IEnumerable<TItem>` | Collection of items to display | Always required |
| `Value` | `TValue` | Currently selected values (array or collection) | Binding selections |
| `Placeholder` | `string` | Placeholder text when empty | UX improvement |
| `AllowFiltering` | `bool` | Enable/disable search filtering | For searchable lists |
| `Mode` | `VisualMode` | Selection display mode (Default, Box, Delimiter, CheckBox) | Customize display style |
| `Enabled` | `bool` | Enable/disable component (default: true) | Conditional states |
| `AllowCustomValue` | `bool` | Allow user-entered custom values | Free-form input |
| `EnableVirtualization` | `bool` | Enable virtualization for large data | Performance optimization |
| `PopupHeight` | `string` | Height of dropdown popup (default: 300px) | Customize appearance |
| `PopupWidth` | `string` | Width of dropdown popup (default: 100%) | Customize appearance |
| `CssClass` | `string` | Custom CSS class | Custom styling |
| `ShowSelectAll` | `bool` | Show select all option in CheckBox mode | Bulk selection |
| `ShowClearButton` | `bool` | Display clear button (default: true) | Allow clearing selection |
| `ShowDropDownIcon` | `bool` | Display dropdown icon (default: true) | Visual indicator |
| `MaximumSelectionLength` | `int` | Max items that can be selected (default: 1000) | Limit selections |
| `HideSelectedItem` | `bool` | Hide selected items in popup | Clean popup display |
| `EnableSelectionOrder` | `bool` | Enable selection order display (default: true) | Show selection sequence |
| `EnableCloseOnSelect` | `bool` | Auto-close popup after selection | Quick selection UX |
| `DelimiterChar` | `string` | Separator for Delimiter mode (default: ",") | Customize separator |
| `FilterBarPlaceholder` | `string` | Placeholder for filter input | Filter UX |
| `FloatLabelType` | `FloatLabelType` | Floating label behavior (Never, Always, Auto) | Modern form styling |
| `EnableRtl` | `bool` | Right-to-left language support | International apps |
| `ReadOnly` | `bool` | Read-only mode (default: false) | Display-only state |
| `TabIndex` | `int` | Tab order index (default: 0) | Keyboard navigation |

### Common Use Cases

**Case 1: Employee Selection in Team Assignment**
- User needs to select multiple employees for a team
- Use checkbox mode for clear selection
- Add filtering for easier search
- Validate minimum selection requirement

**Case 2: Category/Tag Selection for Content**
- User tags content with multiple categories
- Use custom values for new tags
- Show selected items as chips
- Allow deselect with delete key

**Case 3: Department/Location Multi-Filter**
- Filter data by multiple departments and locations
- Remote data source from API
- Grouping by department/location
- Programmatic selection updates

**Case 4: Subscription Preferences**
- User selects multiple notification types
- Grouping by category (Email, SMS, Push)
- All-select/deselect functionality
- RTL support for international apps

---

**Ready to implement MultiSelect Dropdown?** Start with [Getting Started](references/multiselect-getting-started.md) for setup, then navigate to other references based on your specific needs.

---

## Mention

The Mention component provides @mention functionality for tagging users, items, or entities within text content. It displays a suggestion list when users type a trigger character (default: `@`), enabling easy selection and insertion of tagged items.

### When to Use This Skill

Use the Mention component when you need to:
- Add @mention tagging in comments, chat, or social features
- Tag users, products, or entities in text areas
- Implement autocomplete suggestions with a trigger character
- Create collaborative commenting systems
- Build social media-style mention features
- Enable context-aware item selection in text input

### Component Overview

The **Mention component** is a dropdown that enables users to mention items from a configured data source by typing a trigger character (default: `@`). It displays a filtered suggestion list that users can select from, automatically inserting the mention into the target element.

#### Key Capabilities
- **Trigger-based suggestions:** Displays suggestions when users type the mention character
- **Multiple data source types:** Supports local primitives, complex objects, enums, and remote data
- **Advanced filtering:** StartsWith, Contains, EndsWith filter types with minimum character limits
- **Templating:** Customize item display, mention format, empty states, and loading indicators
- **Accessibility:** Full WCAG 2.2 compliance with keyboard navigation and screen reader support
- **Remote data:** OData v4, Web API adaptors with offline mode support

---

### Documentation & Navigation Guide

Choose your topic below to get started:

#### 📄 Getting Started
**Read:** [references/getting-started.md](references/mention-getting-started.md)
- Installation and package setup (NuGet, themes)
- Creating Blazor WASM and Server applications
- Basic Mention component implementation
- Target element configuration (div, textarea, input)
- Initial data binding

#### 📄 Working with Data
**Read:** [references/working-with-data.md](references/mention-working-with-data.md)
- Binding local data (primitives, complex objects, ExpandoObject)
- Enum data binding
- Remote data binding with DataManager
- OData v4 and Web API adaptors
- Offline mode for caching
- Data fetch events (ActionBegin, ActionComplete, ActionFailure)

#### 📄 Filtering & Search
**Read:** [references/filtering-and-search.md](references/mention-filtering-and-search.md)
- MinLength property for minimum search characters
- FilterType options (StartsWith, Contains, EndsWith)
- AllowSpaces for multi-word searching
- SuggestionCount for result limiting

#### 📄 Customization
**Read:** [references/customization.md](references/mention-customization.md)
- ShowMentionChar to display mention character in selected text
- SuffixText for adding space or newline after mention
- Popup dimensions (PopupHeight, PopupWidth)
- Custom mention trigger character
- RequireLeadingSpace for space-prefixed triggers

#### 📄 Templates & Display
**Read:** [references/templates.md](references/mention-templates.md)
- ItemTemplate for custom suggestion list styling
- DisplayTemplate for formatted mention display
- NoRecordsTemplate for empty states
- SpinnerTemplate for loading states
- Template context access and data usage

#### 📄 Accessibility
**Read:** [references/accessibility.md](references/mention-accessibility.md)
- WCAG 2.2 compliance details
- WAI-ARIA attributes (aria-selected, aria-activedescendent)
- Keyboard navigation shortcuts
- Screen reader support
- Mobile and RTL language support


### Quick Start Example

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <textarea id="mentionTarget" placeholder="Type @ to mention someone"></textarea>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

<style>
    #mentionTarget {
        min-height: 100px;
        border: 1px solid #D7D7D7;
        border-radius: 4px;
        padding: 8px;
        font-size: 14px;
        width: 100%;
    }
</style>

@code {
    public class PersonData
    {
        public string Name { get; set; }
        public string Email { get; set; }
    }

    List<PersonData> TeamMembers = new List<PersonData>
    {
        new PersonData { Name = "Alice Johnson", Email = "alice@company.com" },
        new PersonData { Name = "Bob Smith", Email = "bob@company.com" },
        new PersonData { Name = "Carol White", Email = "carol@company.com" }
    };
}
```

---

### Common Patterns

#### Pattern 1: Comment Section with User Mentions
```razor
<SfMention TItem="UserData" DataSource="@AllUsers" MentionChar="@MentionCharAt">
    <TargetComponent>
        <div id="comments" contenteditable="true" placeholder="Type @ to mention..."></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="UserName"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
}
```

#### Pattern 2: Filtered Suggestions with Remote Data
```razor
<SfMention TItem="EmployeeData" MentionChar="@MentionCharAt" MinLength="2" FilterType="FilterType.StartsWith">
    <TargetComponent>
        <input id="employeeInput" type="text" placeholder="Search employees..." />
    </TargetComponent>
    <ChildContent>
        <SfDataManager Url="YOUR_API_ENDPOINT" Adaptor="Adaptors.WebApiAdaptor"></SfDataManager>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
}
```

#### Pattern 3: Custom Display with Templates
```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers" MentionChar="@MentionCharAt">
    <TargetComponent>
        <div id="mentionDiv" contenteditable="true"></div>
    </TargetComponent>
    <ItemTemplate>
        <div class="mention-item">
            <span>@((context as PersonData).Name)</span>
            <small>@((context as PersonData).Email)</small>
        </div>
    </ItemTemplate>
    <DisplayTemplate>
        <span class="mentioned-user">@((context as PersonData).Name)</span>
    </DisplayTemplate>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
}
```

---

### Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `TItem` | Generic | - | Data source item type |
| `DataSource` | IEnumerable<TItem> | - | Local data collection |
| `MentionChar` | char | `'@'` | Trigger character for suggestions |
| `Target` | string | - | CSS selector for target element |
| `MinLength` | int | 0 | Minimum characters to show suggestions |
| `FilterType` | FilterType | Contains | Search filter mode (StartsWith, Contains, EndsWith) |
| `AllowSpaces` | bool | false | Allow spaces in mention search |
| `ShowMentionChar` | bool | false | Display trigger character with mention |
| `SuffixText` | string | - | Text appended after mention (space, newline) |
| `RequireLeadingSpace` | bool | false | Require space before mention character |
| `PopupHeight` | string | 300px | Suggestion list height |
| `PopupWidth` | string | auto | Suggestion list width |
| `SuggestionCount` | int | 25 | Maximum items in suggestion list |

---

### Common Use Cases

**User Tagging in Comments**
- Create collaboration tools where users mention @username in comments
- Combine with DisplayTemplate to show user avatars
- Use remote data binding to fetch team members dynamically

**Task Assignment Notifications**
- Mention team members when assigning tasks
- Customize MentionChar to use # for tasks, @ for users
- Use ActionComplete event to log mentions for notifications

**Code or Entity References**
- Use Mention to reference code snippets (#snippet)
- Mention entities or resources in documentation
- Support enum data binding for predefined entities

**Multi-target Mention**
- Implement mention support in multiple textareas on same page
- Each Mention component can target a different element
- Use Target property with unique CSS selectors

---

### Next Steps

1. **Start here:** Read [Getting Started](references/mentions-getting-started.md) to install and set up
2. **Bind data:** Learn [Working with Data](references/mentions-working-with-data.md) for local/remote sources
3. **Enhance UX:** Explore [Filtering & Search](references/mentions-filtering-and-search.md) and [Templates](references/templates.md)
4. **Ensure accessibility:** Review [Accessibility](references/mentions-accessibility.md) for inclusive design
5. **Fine-tune:** Use [Customization](references/mentions-customization.md) for appearance and behavior adjustments

---

**For additional help:**
- Official Documentation: https://blazor.syncfusion.com/documentation/mention/getting-started
- API Reference: https://help.syncfusion.com/cr/blazor/Syncfusion.Blazor.DropDowns.SfMention-1.html
- Community Support: https://www.syncfusion.com/forums/blazor

---

## ListBox

A comprehensive skill for implementing and working with the **SfListBox** component in Blazor applications. The ListBox displays a scrollable list of items with support for single/multiple selection, checkboxes, filtering, drag-and-drop, icons, and custom templates.

### When to Use This Skill

Use this skill when you need to:

- **Installation & Setup**
  - Install Syncfusion.Blazor.DropDowns NuGet package
  - Register services and configure themes
  - Set up Blazor WebAssembly, Server, or Web App projects

- **Data Binding**
  - Bind array of strings or objects to ListBox
  - Map complex nested objects to list items
  - Load data from remote sources (DataManager, APIs)
  - Update data dynamically

- **Selection & Interaction**
  - Implement single or multiple selection modes
  - Add checkboxes for item selection
  - Enable "Select All" functionality
  - Set maximum selection limits
  - Retrieve selected items and values
  - Handle selection change events

- **Features & Customization**
  - Enable filtering and search capabilities
  - Implement drag-and-drop reordering
  - Create dual-listbox patterns (source/target)
  - Enable/disable specific items
  - Add icons and custom templates
  - Apply sorting and grouping

- **Styling & Appearance**
  - Apply themes (Bootstrap, Material, Fluent, Tailwind)
  - Customize CSS and styling
  - Create responsive layouts
  - Implement dark mode

- **Accessibility**
  - Ensure WCAG 2.1 compliance
  - Configure keyboard navigation
  - Add ARIA labels and roles
  - Support screen readers

### Component Overview

The **SfListBox** component is a flexible dropdown alternative that displays items in a scrollable list format.

**Key Characteristics:**
- **TValue**: Type parameter for selected values (e.g., `string[]`, `int[]`)
- **TItem**: Type parameter for data source items
- **Multiple Selection**: Default behavior; supports single mode
- **Checkbox Support**: Optional checkboxes for item selection
- **Field Mapping**: Maps data object properties to display and value
- **Templates**: Supports custom item templates for rich formatting
- **Data Binding**: Supports local arrays, objects, remote data
- **Events**: Change, select, focus events for interaction handling

### Quick Start Example

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@Items" TItem="string"></SfListBox>

@code {
    public string[] Items = new string[] { "Apple", "Banana", "Orange", "Mango", "Grape" };
}
```

With data binding:

```razor
<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>

@code {
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

### Key Props & Events

**Important Properties:**
- `DataSource` - Array or list of items to display
- `TValue` - Type of selected values (string[], int[], etc.)
- `TItem` - Type of data source items
- `Value` - Currently selected values (two-way bindable)
- `MaximumSelectionLength` - Limit number of selections (default: 500)
- `Enabled` - Enable/disable the component
- `AllowFiltering` - Enable search/filter functionality
- `Allowdragging` - Enable drag-and-drop reordering

**Selection Settings:**
- `Mode` - SelectionMode.Single or SelectionMode.Multiple
- `ShowCheckbox` - Show checkboxes for selection
- `ShowSelectAll` - Show "Select All" checkbox

**Common Events:**
- `ValueChange` - Fires when selected values change
- `Change` - Fires on item selection change
- `Select` - Fires when item is selected

### Common Patterns

#### 1. Single Selection Mode

```razor
<ListBoxSelectionSettings Mode="Syncfusion.Blazor.DropDowns.SelectionMode.Single" />
```

#### 2. Multiple Selection with Checkboxes

```razor
<ListBoxSelectionSettings ShowCheckbox="true" ShowSelectAll="true" />
```

#### 3. Getting Selected Values

```razor
@bind-Value="@SelectedValues"

@code {
    public string[] SelectedValues { get; set; }
}
```

#### 4. Handling Selection Change

```razor
<SfListBox ValueChange="@OnSelectionChanged" ...>
</SfListBox>

@code {
    private void OnSelectionChanged(ChangeEventArgs args)
    {
        var selectedValues = args.Value as string[];
        // Process selected values
    }
}
```

#### 5. Filtering Enabled

```razor
<SfListBox AllowFiltering="true" FilterType="FilterType.Contains" ... >
</SfListBox>
```

### Documentation & Navigation Guide

Choose the reference that matches your current task:

#### Getting Started
📄 **Read:** [references/getting-started.md](references/listboxgetting-started.md)
- Installation and NuGet package setup
- Project configuration (WebAssembly, Server, Web App)
- Basic component markup and first example
- Theme configuration and stylesheets
- Running and testing your first ListBox

#### Data Binding
📄 **Read:** [references/data-binding.md](references/listbox-data-binding.md)
- Binding array of strings
- Binding array of objects with field mapping
- Binding complex nested objects
- Remote data loading with DataManager
- Dynamic data updates
- Best practices for data binding

#### Selection & Modes
📄 **Read:** [references/selection-and-modes.md](references/listbox-selection-and-modes.md)
- Single selection configuration
- Multiple selection (default mode)
- Checkbox selection with ShowCheckbox
- Select All functionality
- Getting selected items and values
- MaximumSelectionLength constraints
- Selection change events
- Common selection patterns

#### Features & Interactions
📄 **Read:** [references/features-and-interactions.md](references/listbox-features-and-interactions.md)
- Filtering and search capabilities
- Drag-and-drop reordering (Allowdragging)
- Item enable/disable functionality
- Icons and icon CSS classes
- Item templates for custom rendering
- Sorting and grouping data
- Dual ListBox pattern (source to target)
- Accessibility attributes

#### Styling & Appearance
📄 **Read:** [references/styling-and-appearance.md](references/listbox-styling-and-appearance.md)
- Theme application (Bootstrap, Material, Fluent, Tailwind)
- CSS class customization
- Custom item templates for styling
- Icon integration and styling
- Dark mode implementation
- Responsive design patterns
- Layout and sizing

#### Accessibility & Events
📄 **Read:** [references/accessibility-and-events.md](references/listbox-accessibility-and-events.md)
- WCAG 2.1 compliance guidelines
- Keyboard navigation support
- ARIA labels and roles
- Event binding (ValueChange, Change, Select)
- Event handling patterns
- Focus management
- Screen reader support
- Common accessibility patterns

### Use Case Examples

**Choose a reference based on your scenario:**

- **"I need to add a ListBox to my Blazor project"** → Getting Started
- **"How do I bind data to ListBox?"** → Data Binding
- **"I want users to select multiple items with checkboxes"** → Selection & Modes
- **"Can I let users search/filter the list?"** → Features & Interactions
- **"How do I customize colors and styling?"** → Styling & Appearance
- **"Does ListBox support keyboard navigation?"** → Accessibility & Events
- **"I need a source/target ListBox pattern"** → Features & Interactions

### Next Steps

1. **New to ListBox?** Start with [Getting Started](references/listbox-getting-started.md)
2. **Have data to bind?** Go to [Data Binding](references/listbox-data-binding.md)
3. **Need multi-selection?** Check [Selection & Modes](references/listbox-selection-and-modes.md)
4. **Want advanced features?** Explore [Features & Interactions](references/listbox-features-and-interactions.md)
5. **Making it look good?** Read [Styling & Appearance](references/listbox-styling-and-appearance.md)
6. **Accessibility needed?** Review [Accessibility & Events](references/listbox-accessibility-and-events.md)
