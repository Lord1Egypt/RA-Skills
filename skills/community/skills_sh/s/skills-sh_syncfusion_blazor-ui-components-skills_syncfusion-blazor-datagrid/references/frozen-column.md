# Frozen Column — Syncfusion Blazor DataGrid

## Table of Contents
1. [Freeze by Column Count](#freeze-by-column-count)
2. [Freeze Specific Columns](#freeze-specific-columns)
3. [Freeze Direction](#freeze-direction)
4. [Customize Frozen Line Color](#customize-frozen-line-color)
5. [Freeze Line Moving](#freeze-line-moving)
6. [Frozen Columns with Detail Template](#frozen-columns-with-detail-template)

---

## Freeze by Column Count

Keep the first N columns visible while scrolling horizontally using the `FrozenColumns` property:

```razor
<SfGrid DataSource="@Orders" FrozenColumns="2" FrozenRows="2">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="100"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Format="d" Width="160"></GridColumn>
        <GridColumn Field="ShipName" HeaderText="Ship Name" Width="130"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="120"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

Properties:
- **FrozenColumns**: Number of columns to freeze from the left (0 = no freeze)
- **FrozenRows**: Number of rows to freeze from the top
- First N columns remain visible during horizontal scrolling

Benefits:
- Keep important columns always visible
- Improved navigation in wide grids
- Works with sorting and filtering

---

## Freeze Specific Columns

Freeze individual columns regardless of their position using column-level configuration:

```razor
<SfGrid DataSource="@Orders" Height="315">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" 
                  IsFrozen="true" Freeze="FreezeDirection.Left" 
                  Width="100"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Width="160"></GridColumn>
        <GridColumn Field="ShipAddress" HeaderText="Ship Address" 
                  IsFrozen="true" Freeze="FreezeDirection.Fixed" 
                  Width="150"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" 
                  IsFrozen="true" Freeze="FreezeDirection.Right" 
                  Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Column-level freezing:
- Set `IsFrozen="true"` to freeze a column
- Specify `Freeze` direction (Left, Right, Fixed)
- Mix frozen and non-frozen columns
- Override grid-level `FrozenColumns`

---

## Freeze Direction

Control where frozen columns appear using the `Freeze` property:

| Direction | Behavior |
|-----------|----------|
| **Left** | Freeze column to the left side; scrolls with left panel |
| **Right** | Freeze column to the right side; scrolls with right panel |
| **Fixed** | Keep column fixed in place; doesn't move with scroll |

```razor
<!-- Freeze to left (default) -->
<GridColumn Field="OrderID" IsFrozen="true" Freeze="FreezeDirection.Left" Width="100"></GridColumn>

<!-- Freeze to right -->
<GridColumn Field="Notes" IsFrozen="true" Freeze="FreezeDirection.Right" Width="150"></GridColumn>

<!-- Fixed in place -->
<GridColumn Field="Status" IsFrozen="true" Freeze="FreezeDirection.Fixed" Width="100"></GridColumn>
```

Practical uses:
- **Left**: Keep ID and name columns visible
- **Right**: Keep action buttons or status columns visible
- **Fixed**: Keep critical columns in view during any scroll

---

## Customize Frozen Line Color

Change the border color of frozen column separators using CSS:

```razor
<SfGrid DataSource="@Orders" Height="315">
    <GridColumns>
        <GridColumn Field="OrderID" IsFrozen="true" Freeze="FreezeDirection.Left" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" Width="150"></GridColumn>
        <GridColumn Field="ShipCountry" IsFrozen="true" Freeze="FreezeDirection.Right" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

<style>
    /* Left frozen columns border */
    .e-grid .e-leftfreeze.e-freezeleftborder {
        border-right-color: rgb(198, 30, 204) !important;
    }
    
    /* Right frozen columns border */
    .e-grid .e-rightfreeze.e-freezerightborder {
        border-left-color: rgb(19, 228, 243) !important;
    }
    
    /* Fixed frozen columns borders */
    .e-grid .e-fixedfreeze.e-freezeleftborder {
        border-left-color: rgb(9, 209, 9) !important;
    }
    
    .e-grid .e-fixedfreeze.e-freezerightborder {
        border-right-color: rgb(10, 224, 10) !important;
    }
</style>
```

Customization options:
- Change separator colors
- Match application theme
- Improve visual hierarchy

---

## Freeze Line Moving

Enable users to dynamically freeze/unfreeze columns by dragging the freeze separator:

```razor
<SfGrid DataSource="@Orders" 
        Height="315" 
        AllowFreezeLineMoving="true"
        FrozenColumns="2">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="100"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Width="160"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="150"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Features:
- Set `AllowFreezeLineMoving="true"` to enable dragging
- Users drag freeze separator to change frozen column count
- Visual feedback during drag
- Flexible column layout management

---

## Frozen Columns with Detail Template

Combine frozen columns with row detail templates for expanded information:

```razor
<SfGrid DataSource="@Employees">
    <GridTemplates>
        <DetailTemplate>
            @{
                var employee = (context as EmployeeDetails);
                <table class="detail-table" width="100%">
                    <tbody>
                        <tr>
                            <td><strong>Email:</strong> @employee.Email</td>
                            <td><strong>Phone:</strong> @employee.Phone</td>
                        </tr>
                        <tr>
                            <td><strong>Hire Date:</strong> @employee.HireDate.ToShortDateString()</td>
                            <td><strong>Reports To:</strong> @employee.ReportsTo</td>
                        </tr>
                    </tbody>
                </table>
            }
        </DetailTemplate>
    </GridTemplates>
    <GridColumns>
        <GridColumn Field="FirstName" HeaderText="First Name" 
                  IsFrozen="true" Width="110"></GridColumn>
        <GridColumn Field="LastName" HeaderText="Last Name" Width="110"></GridColumn>
        <GridColumn Field="Title" Width="200"></GridColumn>
        <GridColumn Field="Address" Width="250"></GridColumn>
        <GridColumn Field="City" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

<style>
    .detail-table td {
        font-size: 13px;
        padding: 4px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>
```

Use case:
- Frozen identification column (Name)
- Scrollable data columns
- Expandable row for additional details
- Improves data exploration

> **Note:** If no columns are frozen, the freeze separator appears at the left and right edges. Drag it to freeze columns dynamically.

