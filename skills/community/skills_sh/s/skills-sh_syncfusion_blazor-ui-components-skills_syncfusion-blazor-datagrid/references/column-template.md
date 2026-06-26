# Column Template — Syncfusion Blazor DataGrid

## Table of Contents
1. [Render HTML Elements](#render-html-elements)
2. [Render Image in Column](#render-image-in-column)
3. [Render Hyperlink in Column](#render-hyperlink-in-column)
4. [Render Components in Column](#render-components-in-column)
5. [Render DropDownList](#render-dropdownlist)
6. [Render Chip](#render-chip)
7. [Render ProgressBar](#render-progressbar)

---

## Render HTML Elements

The `Template` property allows rendering custom HTML elements or Blazor components instead of the default field value:

```razor
<GridColumn HeaderText="Custom Content" Width="200">
    <Template>
        @{
            var data = (context as OrderData);
            <div class="custom-cell">
                <strong>@data.OrderID</strong>
            </div>
        }
    </Template>
</GridColumn>
```

> Template columns are primarily intended for rendering custom content and do not provide built-in support for sorting, filtering, or editing. Define the `Field` property for a Template column to enable CRUD and data operations.

---

## Render Image in Column

Display images in a DataGrid column using the Template property:

```razor
<GridColumn HeaderText="Employee Image" TextAlign="TextAlign.Center" Width="120">
    <Template>
        @{
            var employee = (context as OrderData);
            <div class="image">
                <img src="@($"scripts/Images/Employees/{employee.EmployeeID}.png")" 
                     alt="@employee.EmployeeID" style="height: 55px; width: 55px; border-radius: 50px;" />
            </div>
        }
    </Template>
</GridColumn>
```

Use cases:
- Employee/product photos
- Status icons
- Custom visual indicators

---

## Render Hyperlink in Column

Display hyperlinks in columns using the Template property:

```razor
<GridColumn Field="FirstName" HeaderText="First Name" Width="150">
    <Template>
        @{
            var data = (context as EmployeeDetails);
            <div>
                <a href="https://www.google.com/search?q=@data.FirstName" target="_blank">
                    @data.FirstName
                </a>
            </div>
        }
    </Template>
</GridColumn>
```

Benefits:
- Link to external resources
- Navigate to related pages
- Create interactive content

---

## Render Components in Column

Embed Syncfusion or custom components inside columns using the Template property:

```razor
<GridColumn HeaderText="Status" Width="150">
    <Template>
        @{
            var data = (context as OrderData);
            <SfDropDownList TValue="string" Placeholder="Select Status" 
                          TItem="StatusOption" DataSource="@StatusOptions">
                <DropDownListFieldSettings Value="Value"></DropDownListFieldSettings>
            </SfDropDownList>
        }
    </Template>
</GridColumn>
```

Supported components:
- DropDownList
- Sparkline (LineChart, ColumnChart)
- Chip
- ProgressBar
- Custom Blazor components

---

## Render DropDownList

Include a DropDownList component in a column:

```razor
<GridColumn Field="OrderStatus" HeaderText="Order Status" Width="150">
    <Template>
        @{
            var data = (context as OrderDetails);
            <SfDropDownList TValue="string" @bind-Value="@data.OrderStatus" 
                          TItem="StatusOption" DataSource="@EmployeeDetails">
                <DropDownListFieldSettings Value="Status"></DropDownListFieldSettings>
            </SfDropDownList>
        }
    </Template>
</GridColumn>
```

Features:
- Inline selection of predefined values
- Two-way binding support
- Custom data source

---

## Render Chip

Display data as visually distinct chip/tag elements:

```razor
<GridColumn Field="FirstName" HeaderText="First Name" Width="150">
    <Template>
        @{
            var data = (context as EmployeeDetails);
            <SfChip ID="chip">
                <ChipItems>
                    <ChipItem Text="@data.FirstName"></ChipItem>
                </ChipItems>
            </SfChip>
        }
    </Template>
</GridColumn>
```

Use cases:
- Tagging and labeling
- Visual categorization
- Status display

---

## Render ProgressBar

Display progress visualization in columns:

```razor
<GridColumn Field="Freight" HeaderText="Freight" Width="150">
    <Template>
        @{
            var data = (context as OrderDetails);
            <SfProgressBar Type="ProgressType.Linear" Value="data.Freight" 
                         CornerRadius="CornerType.Square" Height="60" 
                         TrackThickness="24" ProgressThickness="20">
            </SfProgressBar>
        }
    </Template>
</GridColumn>
```

Benefits:
- Visual progress tracking
- Data range visualization
- Professional appearance

