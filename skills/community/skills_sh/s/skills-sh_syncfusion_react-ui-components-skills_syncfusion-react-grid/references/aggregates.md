# Aggregates in React Grid

## Table of Contents
- [Overview](#overview)
- [Setup and Configuration](#setup-and-configuration)
- [Aggregate Types](#aggregate-types)
- [Footer Aggregates](#footer-aggregates)
- [Group Aggregates](#group-aggregates)
- [Caption Aggregates](#caption-aggregates)
- [Custom Aggregates](#custom-aggregates)
- [Reactive Updates](#reactive-updates)

## Overview

Aggregates provide summary calculations (Sum, Average, Count, Min, Max) that can be displayed in footer rows, group footers, or group captions. This is useful for displaying total quantities, average values, and other summary statistics.

## Setup and Configuration

### Enable Aggregate Module

```tsx
import { Inject, Aggregate } from '@syncfusion/ej2-react-grids';

<GridComponent>
  <Inject services={[Aggregate]} />
</GridComponent>
```

### Using Directives

```tsx
import {
  GridComponent,
  ColumnsDirective,
  ColumnDirective,
  AggregatesDirective,
  AggregateDirective,
  AggregateColumnsDirective,
  AggregateColumnDirective,
  Inject,
  Aggregate
} from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data}>
  <ColumnsDirective>
    <ColumnDirective field='Freight' headerText='Freight' format='C2' />
  </ColumnsDirective>
  <AggregatesDirective>
    <AggregateDirective>
      <AggregateColumnsDirective>
        <AggregateColumnDirective field='Freight' type='Sum' />
      </AggregateColumnsDirective>
    </AggregateDirective>
  </AggregatesDirective>
  <Inject services={[Aggregate]} />
</GridComponent>
```

## Aggregate Types

### Supported Aggregate Functions

| Type | Description | Example |
|------|-------------|---------|
| `Sum` | Total of all values | `type='Sum'` |
| `Average` | Mean value | `type='Average'` |
| `Count` | Number of records | `type='Count'` |
| `Min` | Minimum value | `type='Min'` |
| `Max` | Maximum value | `type='Max'` |
| `TrueCount` | Count of true values | `type='TrueCount'` |
| `FalseCount` | Count of false values | `type='FalseCount'` |

## Footer Aggregates

Display summary values in grid footer:

```tsx
const footerSum = (props) => {
  return <span>Total: {props.Sum}</span>;
};

<AggregatesDirective>
  <AggregateDirective>
    <AggregateColumnsDirective>
      <AggregateColumnDirective
        field='Freight'
        type='Sum'
        format='C2'
        footerTemplate={footerSum}
      />
      <AggregateColumnDirective
        field='Freight'
        type='Average'
        format='C2'
        footerTemplate={(props) => <span>Average: ${props.Average}</span>}
      />
    </AggregateColumnsDirective>
  </AggregateDirective>
</AggregatesDirective>
```

### Multiple Aggregates in Footer

```tsx
<AggregatesDirective>
  <AggregateDirective>
    <AggregateColumnsDirective>
      <AggregateColumnDirective field='Freight' type='Sum' footerTemplate={`Sum: \${Sum}`} />
      <AggregateColumnDirective field='Freight' type='Average' footerTemplate={`Avg: \${Average}`} />
      <AggregateColumnDirective field='Freight' type='Max' footerTemplate={`Max: \${Max}`} />
      <AggregateColumnDirective field='OrderID' type='Count' footerTemplate={`Count: \${Count}`} />
    </AggregateColumnsDirective>
  </AggregateDirective>
</AggregatesDirective>
```

## Group Aggregates

Display summary values for each group:

```tsx
<AggregatesDirective>
  <AggregateDirective>
    <AggregateColumnsDirective>
      <AggregateColumnDirective
        field='Freight'
        type='Sum'
        format='C2'
        groupFooterTemplate={`Group Total: \${Sum}`}
      />
    </AggregateColumnsDirective>
  </AggregateDirective>
</AggregatesDirective>
```

> Template prop determines where the aggregate appears in the group:
> - `groupFooterTemplate` → rendered in the **footer row** of each group (below group rows)
> - `groupCaptionTemplate` → rendered in the **caption row** of each group (at the top of the group)
> - `footerTemplate` → rendered in the **overall grid footer** (not per group — do not use this for group summaries)

### Group Footer with Formatting

```tsx
const groupFooterSum = (props) => {
  return (
    <div>
      <strong>Group Sum: ${props.Sum}</strong>
    </div>
  );
};

<AggregateColumnDirective
  field='Freight'
  type='Sum'
  format='C2'
  groupFooterTemplate={groupFooterSum}
/>
```

## Caption Aggregates

Display summaries in group caption row:

```tsx
<AggregatesDirective>
  <AggregateDirective>
    <AggregateColumnsDirective>
      <AggregateColumnDirective
        field='Freight'
        type='Sum'
        format='C2'
        groupCaptionTemplate={`Total Freight: \${Sum}`}
      />
    </AggregateColumnsDirective>
  </AggregateDirective>
</AggregatesDirective>
```

### Custom Group Caption Format

```tsx
const groupCaption = (props) => {
  return (
    <div>
      <strong>{props.ShipCountry}</strong> - {props.Sum} items
    </div>
  );
};

<AggregateColumnDirective
  field='OrderID'
  type='Count'
  groupCaptionTemplate={groupCaption}
/>
```

## Custom Aggregates

Create custom aggregate calculations:

```tsx
const customAggregate = (args) => {
  const total = args.reduce((acc, item) => acc + item.Freight, 0);
  return (total / args.length) * 1.1; // 10% markup
};

<AggregateColumnDirective
  field='Freight'
  customAggregate={customAggregate}
  footerTemplate={`Custom: \${customAggregate}`}
/>
```

### Complex Custom Aggregate

```tsx
const calculateMedian = (field, records) => {
  const values = records.map(r => r[field]).sort((a, b) => a - b);
  const mid = Math.floor(values.length / 2);
  return values.length % 2 !== 0
    ? values[mid]
    : (values[mid - 1] + values[mid]) / 2;
};
```

## Reactive Updates

### Update Aggregates on Data Change

```tsx
import React, { useState } from 'react';

function App() {
  const [gridData, setGridData] = useState(initialData);

  const addRow = () => {
    setGridData([
      ...gridData,
      { OrderID: 10251, Freight: 100, ShipCountry: 'France' }
    ]);
    // Aggregates automatically recalculate
  };

  return (
    <div>
      <button onClick={addRow}>Add Row</button>
      <GridComponent dataSource={gridData}>
        <AggregatesDirective>
          {/* aggregate definitions */}
        </AggregatesDirective>
      </GridComponent>
    </div>
  );
}
```

### Using Aggregate Configuration Object

```tsx
const aggregates = [
  {
    columns: [
      {
        field: 'Freight',
        type: 'Sum',
        format: 'C2',
        footerTemplate: 'Sum: ${Sum}'
      },
      {
        field: 'Freight',
        type: 'Average',
        format: 'C2',
        footerTemplate: 'Avg: ${Average}'
      }
    ]
  }
];

<GridComponent dataSource={data} aggregates={aggregates}>
  {/* columns and other configs */}
</GridComponent>
```
