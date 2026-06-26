# Drill-Down Reference - Syncfusion React Pivot Table

## Overview

Drill-down is a core feature of the Syncfusion React Pivot Table that allows users to explore hierarchical data by expanding row and column members to see their child members. This feature is essential for hierarchical analysis, enabling users to navigate from summary data to detailed breakdowns. When a user drills down, the pivot table expands to reveal the next level of hierarchy without losing the current view.

### Key Concepts
- **Expand/Collapse Hierarchy**: Click icons to expand parent members and view child members
- **Drill Position**: Drilling in one location doesn't affect the same member elsewhere
- **Hierarchical Navigation**: Move from high-level summaries to detailed data
- **Field-Level Control**: Configure expansion settings per field
- **Real-Time Updates**: Changes reflect immediately in the pivot table

## Basic Drill-Down Implementation

### Enable Drill-Down

Drill-down is enabled by default in the Syncfusion React Pivot Table. Users can expand/collapse members by clicking the expand/collapse icons in row and column headers.

```typescript
import { PivotViewComponent, Inject, IDataSet } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sales' }, { name: 'Amount' }],
    dataSource: pivotData as IDataSet[],
    // Drill-down enabled by default
  };

  let pivotObj: PivotViewComponent;

  return (
    <PivotViewComponent
      ref={(d: PivotViewComponent) => pivotObj = d}
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

## Expand All Members

### Global Expand All

Expand all hierarchical members across all fields using the `expandAll` property:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year' }, { name: 'Quarter' }],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  values: [{ name: 'Sales' }],
  dataSource: pivotData as IDataSet[],
  expandAll: true  // Expand all hierarchy levels on load
};

<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  height={350}
/>
```

**Result:** All row and column members will be expanded, showing the deepest level of detail immediately.

### Field-Specific Expand All

Control expansion for individual fields:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  columns: [
    { name: 'Year', expandAll: true },   // Expand Year hierarchy
    { name: 'Quarter', expandAll: false } // Keep Quarter collapsed
  ],
  rows: [
    { name: 'Country', expandAll: true },   // Expand Country hierarchy
    { name: 'Products', expandAll: false }  // Keep Products collapsed
  ],
  values: [{ name: 'Sales' }],
  dataSource: pivotData as IDataSet[]
};
```

## Selective Member Expansion

### Using drilledMembers

The `drilledMembers` property allows you to specify exactly which members should be expanded on load:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year' }, { name: 'Quarter' }],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  values: [{ name: 'Sales' }],
  dataSource: pivotData as IDataSet[],
  drilledMembers: [
    {
      name: 'Country',
      items: ['USA', 'Canada']  // Expand only USA and Canada
    },
    {
      name: 'Year',
      items: ['FY 2020', 'FY 2021']  // Expand only these years
    }
  ]
};

<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  height={350}
/>
```

**Result:** Only specified members are expanded; others remain collapsed.

### Hierarchical Member Paths

For multi-level hierarchies, use the `delimiter` property to specify parent-child paths:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  rows: [
    { name: 'Region' },
    { name: 'Country' },
    { name: 'City' }
  ],
  drilledMembers: [
    {
      name: 'Region',
      items: [
        'North~USA',        // North>USA
        'North~USA~NewYork' // North>USA>NewYork
      ],
      delimiter: '~'  // Define the hierarchy separator
    }
  ]
};
```

## Programmatic Drill Control

### Expand Member Programmatically

Expand specific members at runtime:

```typescript
const expandMember = (fieldName: string, members: string[]): void => {
  if (pivotObj && pivotObj.dataSourceSettings) {
    pivotObj.dataSourceSettings.drilledMembers = [
      {
        name: fieldName,
        items: members
      }
    ];
    pivotObj.refresh();
  }
};

// Example: Expand USA and Canada in Country field
expandMember('Country', ['USA', 'Canada']);
```

### Collapse Member Programmatically

Remove members from drilledMembers to collapse them:

```typescript
const collapseMember = (fieldName: string, memberToRemove: string): void => {
  if (pivotObj && pivotObj.dataSourceSettings?.drilledMembers) {
    const drilledMembers = pivotObj.dataSourceSettings.drilledMembers;
    
    const updatedMembers = drilledMembers.map(member => {
      if (member.name === fieldName) {
        return {
          ...member,
          items: member.items.filter((item: string) => item !== memberToRemove)
        };
      }
      return member;
    });
    
    pivotObj.dataSourceSettings.drilledMembers = updatedMembers;
    pivotObj.refresh();
  }
};

// Example: Collapse USA in Country field
collapseMember('Country', 'USA');
```

### Expand/Collapse Toggle

```typescript
const toggleMember = (fieldName: string, member: string): void => {
  if (pivotObj && pivotObj.dataSourceSettings?.drilledMembers) {
    const drilledMembers = pivotObj.dataSourceSettings.drilledMembers;
    const fieldDrilled = drilledMembers.find(d => d.name === fieldName);
    
    if (fieldDrilled?.items?.includes(member)) {
      // Member is expanded, collapse it
      collapseMember(fieldName, member);
    } else {
      // Member is collapsed, expand it
      expandMember(fieldName, [...(fieldDrilled?.items || []), member]);
    }
  }
};
```

## Drill-Down Events

### drill Event

Triggered when a member is expanded or collapsed:

```typescript
const onDrill = (args: PivotDrillEventArgs): void => {
  console.log('Drill action:', args.action);           // 'Up' or 'Down'
  console.log('Drilled field:', args.fieldName);       // Field being drilled
  console.log('Drilled member:', args.memberName);     // Member being drilled
  console.log('Member position:', args.memberPosition);// Position in array
};

<PivotViewComponent
  onDrill={onDrill}
  dataSourceSettings={dataSourceSettings}
/>
```

### actionBegin and actionComplete

Track drill-down actions:

```typescript
const onActionBegin = (args: PivotActionBeginEventArgs): void => {
  if (args.actionName === 'Drill down' || args.actionName === 'Drill up') {
    console.log('Drill action starting:', args.actionName);
    // Perform pre-drill operations
  }
};

const onActionComplete = (args: PivotActionCompleteEventArgs): void => {
  if (args.actionName === 'Drill down' || args.actionName === 'Drill up') {
    console.log('Drill action completed:', args.actionName);
    // Perform post-drill operations
  }
};

<PivotViewComponent
  actionBegin={onActionBegin}
  actionComplete={onActionComplete}
  dataSourceSettings={dataSourceSettings}
/>
```

## Drill Position

Drill position determines how drilling affects other instances of the same member:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  columns: [
    { name: 'Year' },
    { name: 'Quarter' }
  ],
  rows: [
    { name: 'Country' },
    { name: 'Sales Rep' }  // Different rep per country
  ],
  values: [{ name: 'Amount' }],
  dataSource: pivotData as IDataSet[],
  // Drill position is separate for each Country
  // Expanding "USA" doesn't auto-expand "Canada"
};
```

## Performance Considerations

### Large Hierarchies

For datasets with deep hierarchies (5+ levels), consider:

1. **Lazy Loading**: Don't expand all levels by default
```typescript
expandAll: false  // Start collapsed for performance
```

2. **Selective Expansion**: Expand only necessary members
```typescript
drilledMembers: [
  {
    name: 'region',
    items: ['important-region'] // Only critical members
  }
]
```

3. **Deferred Update**: Use with deferred layout updates
```typescript
allowDeferLayoutUpdate: true
```

## Best Practices

1. **Default State**: Start with reasonable defaults - not fully collapsed or expanded
2. **User Guidance**: Provide visual indicators for expandable members
3. **Performance**: For large datasets, limit default expanded members
4. **Consistency**: Use consistent drill patterns across your application
5. **Event Handling**: Track drill events for analytics and logging

## Complete Example

```typescript
import { PivotViewComponent, Inject, IDataSet } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { hierarchicalData } from './datasource';

function DrillDownExample() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [
      { name: 'Year', expandAll: false },
      { name: 'Quarter', expandAll: false }
    ],
    rows: [
      { name: 'Country', expandAll: false },
      { name: 'Region', expandAll: false },
      { name: 'City', expandAll: false }
    ],
    values: [{ name: 'Sales', caption: 'Total Sales' }],
    dataSource: hierarchicalData as IDataSet[],
    drilledMembers: [
      {
        name: 'Country',
        items: ['USA', 'Canada'],
        delimiter: '~'
      }
    ],
    formatSettings: [{ name: 'Sales', format: 'C2' }]
  };

  let pivotObj: PivotViewComponent;

  const handleDrill = (args: PivotDrillEventArgs): void => {
    console.log(`${args.action}:`, args.memberName, 'in', args.fieldName);
  };

  const expandAll = (): void => {
    if (pivotObj && pivotObj.dataSourceSettings) {
      pivotObj.dataSourceSettings.expandAll = true;
      pivotObj.refresh();
    }
  };

  const collapseAll = (): void => {
    if (pivotObj && pivotObj.dataSourceSettings) {
      pivotObj.dataSourceSettings.expandAll = false;
      pivotObj.dataSourceSettings.drilledMembers = [];
      pivotObj.refresh();
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={expandAll} style={{ marginRight: '10px' }}>
          Expand All
        </button>
        <button onClick={collapseAll}>
          Collapse All
        </button>
      </div>
      <PivotViewComponent
        ref={(d: PivotViewComponent) => pivotObj = d}
        id='PivotView'
        dataSourceSettings={dataSourceSettings}
        height={500}
        onDrill={handleDrill}
      />
    </div>
  );
}

export default DrillDownExample;
```

## Related Features

- **Drill-Through**: View raw data behind aggregated cells
- **State Persistence**: Save drill state across sessions
- **Field List**: Filter and configure field drilling from UI
- **Grouping Bar**: Quick drilling via grouping bar interface

## Troubleshooting

**Drill icons not appearing?**
- Ensure data has hierarchical structure (multiple row/column fields)
- Check that fields are properly configured in dataSourceSettings
- Verify data has nested values to drill into

**Drill not working?**
- Check drilledMembers member names match data exactly
- Verify delimiter matches hierarchy structure
- Check browser console for data structure errors

**Performance issues when drilling?**
- Reduce number of drilledMembers on initial load
- Enable virtual scrolling for large datasets
- Consider data pagination

**Drilledmembers not applying?**
- Call refresh() after modifying drilledMembers
- Ensure field names match exactly
- Verify member names are correct case
