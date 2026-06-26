# Column Spanning — Syncfusion Blazor DataGrid

## Table of Contents
1. [AutoSpan Modes](#autospan-modes)
2. [Enable Column Spanning](#enable-column-spanning)
3. [Disable Spanning for Specific Column](#disable-spanning-for-specific-column)
4. [Row vs Column Spanning](#row-vs-column-spanning)

---

## AutoSpan Modes

The DataGrid provides automatic cell merging options through the `AutoSpan` property:

| Mode | Description |
|------|-------------|
| `AutoSpanMode.None` | Disables cell spanning (default) |
| `AutoSpanMode.Row` | Enables horizontal merging across columns within same row |
| `AutoSpanMode.Column` | Enables vertical merging of adjacent cells with identical values |
| `AutoSpanMode.HorizontalAndVertical` | Enables both horizontal and vertical merging |

---

## Enable Column Spanning

Enable vertical cell merging for identical values in the same column:

```razor
<SfGrid DataSource="@EmployeeTimeSheet" 
        GridLines="GridLine.Both"
        AutoSpan="AutoSpanMode.Column" 
        AllowSelection="false" 
        EnableHover="false">
    <GridColumns>
        <GridColumn Field="EmployeeID" HeaderText="Employee ID" Width="150" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="EmployeeName" HeaderText="Employee Name" Width="180"></GridColumn>
        <GridColumn Field="Time_9_00" HeaderText="9:00 AM" Width="150" TextAlign="TextAlign.Center"></GridColumn>
        <GridColumn Field="Time_9_30" HeaderText="9:30 AM" Width="150" TextAlign="TextAlign.Center"></GridColumn>
        <GridColumn Field="Time_10_00" HeaderText="10:00 AM" Width="150" TextAlign="TextAlign.Center"></GridColumn>
    </GridColumns>
</SfGrid>
```

How it works:
- Grid automatically merges stacked cells with identical values
- Reduces visual redundancy
- Provides cleaner, more structured layout
- Requires no additional code

Use cases:
- Timesheet data with repeated activities
- Task tracking across time periods
- Status columns with repeated values

---

## Disable Spanning for Specific Column

Override grid-level spanning for individual columns:

```razor
<SfGrid DataSource="@EmployeeTimeSheet"
        AutoSpan="AutoSpanMode.Column"
        GridLines="GridLine.Both">
    <GridColumns>
        <GridColumn Field="EmployeeID" HeaderText="Employee ID" Width="150"></GridColumn>
        <GridColumn Field="EmployeeName" HeaderText="Employee Name" Width="180"></GridColumn>
        <GridColumn Field="Time_9_00" HeaderText="9:00 AM" Width="150"></GridColumn>
        <GridColumn Field="Time_9_30" HeaderText="9:30 AM" Width="150" AutoSpan="AutoSpanMode.None"></GridColumn>
        <GridColumn Field="Time_10_00" HeaderText="10:00 AM" Width="150"></GridColumn>
        <GridColumn Field="Time_10_30" HeaderText="10:30 AM" Width="150" AutoSpan="AutoSpanMode.None"></GridColumn>
    </GridColumns>
</SfGrid>
```

Column-level property:
- Set `AutoSpan="AutoSpanMode.None"` on GridColumn
- Overrides grid-level AutoSpan setting
- Provides precise control over which columns merge

Benefits:
- Exclude specific columns from spanning
- Maintain standard display for certain data
- Mix spanning and non-spanning columns

---

## Row vs Column Spanning

Different spanning modes provide different merging behaviors:

### Column Spanning (Vertical)

Merges cells vertically when identical values appear in consecutive rows:

```razor
<SfGrid DataSource="@Orders" AutoSpan="AutoSpanMode.Column">
    <!-- Identical values in same column are merged vertically -->
</SfGrid>
```

Result:
```
├─ Employee 1 ──┐   Same Employee ID
│               │   merged vertically
├─ Employee 1 ──┤   
│               │
├─ Employee 2 ──┤
```

### Row Spanning (Horizontal)

Merges cells horizontally across columns in the same row:

```razor
<SfGrid DataSource="@Orders" AutoSpan="AutoSpanMode.Row">
    <!-- Identical values in same row are merged horizontally -->
</SfGrid>
```

### Horizontal and Vertical

Combines both vertical and horizontal merging:

```razor
<SfGrid DataSource="@Orders" AutoSpan="AutoSpanMode.HorizontalAndVertical">
    <!-- Executes row merging first, then column merging -->
</SfGrid>
```

Choose based on data structure:
- **Column**: For repeated values down rows (timesheets, activities)
- **Row**: For repeated values across columns
- **HorizontalAndVertical**: For complex data with both types of repetition

