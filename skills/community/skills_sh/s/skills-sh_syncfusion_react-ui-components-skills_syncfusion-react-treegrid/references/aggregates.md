---
name: aggregates
description: 'Aggregates in React TreeGrid - standard aggregates (Sum, Avg, Min, Max, Count), custom aggregates, footer aggregates, group aggregates.'
---

# Aggregates

## Table of Contents
- [Standard Aggregates](#standard-aggregates)
- [Custom Aggregates](#custom-aggregates)
- [Footer Aggregates](#footer-aggregates)
- [Group Aggregates](#group-aggregates)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Overview

Display aggregate calculations (sum, average, min, max, count) at multiple levels in TreeGrid.

## Standard Aggregates

Built-in aggregate functions:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Aggregate, AggregatesDirective, AggregateDirective, AggregateColumnsDirective, AggregateColumnDirective } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    {
      TaskID: 1,
      TaskName: 'Planning',
      Budget: 10000,
      Children: [
        { TaskID: 2, TaskName: 'Plan timeline', Budget: 2000 },
        { TaskID: 3, TaskName: 'Plan budget', Budget: 3000 }
      ]
    }
  ];

  return (
    <TreeGridComponent dataSource={data} childMapping="Children" treeColumnIndex={1}>
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Budget" headerText="Budget" width={120} type="number" format="N2" />
      </ColumnsDirective>
      <AggregatesDirective>
        <AggregateDirective>
          <AggregateColumnsDirective>
            <AggregateColumnDirective field="Budget" type="Sum" footerTemplate="Total: ${Sum}" />
            <AggregateColumnDirective field="Budget" type="Average" footerTemplate="Avg: ${Average}" />
          </AggregatesDirective>
        </AggregateDirective>
      </AggregatesDirective>
      <Inject services={[Aggregate]} />
    </TreeGridComponent>
  );
}
```

## Custom Aggregates

Implement custom calculation logic:

```tsx
<AggregatesDirective>
  <AggregateDirective>
    <AggregateColumnsDirective>
      <AggregateColumnDirective 
        field="Budget" 
        type="Custom" 
        customAggregate={(data) => {
          return data.reduce((sum, item) => sum + item.Budget, 0) / data.length;
        }}
        footerTemplate="Weighted Avg: ${Custom}"
      />
    </AggregateColumnsDirective>
  </AggregateDirective>
</AggregatesDirective>
```

## Footer Aggregates

Display aggregates in footer rows:

```tsx
<AggregatesDirective>
  <AggregateDirective>
    <AggregateColumnsDirective>
      <AggregateColumnDirective field="Budget" type="Sum" footerTemplate="Total Budget: ${Sum}" />
      <AggregateColumnDirective field="TaskID" type="Count" footerTemplate="Items: ${Count}" />
    </AggregateColumnsDirective>
  </AggregateDirective>
</AggregatesDirective>
```

## Group Aggregates

Show aggregates at each hierarchy level:

```tsx
<AggregatesDirective>
  <AggregateDirective>
    <AggregateColumnsDirective>
      <AggregateColumnDirective 
        field="Budget" 
        type="Sum" 
        footerTemplate="Subtotal: ${Sum}"
        showChildSummary={true}
      />
    </AggregateColumnsDirective>
  </AggregateDirective>
</AggregatesDirective>
```

## Key APIs

| Property | Type | Description |
|---|---|---|
| `type` | string | 'Sum', 'Average', 'Min', 'Max', 'Count', 'Custom' |
| `field` | string | Column to aggregate |
| `footerTemplate` | string | Display format in footer |
| `customAggregate` | function | Custom aggregate logic |
| `showChildSummary` | boolean | Show per-level aggregates |

## Common Patterns

1. **Financial Summary**: Sum totals at each level
2. **Data Statistics**: Count, average, min/max for metrics
3. **Hierarchical Summary**: Aggregate child data with parent totals

