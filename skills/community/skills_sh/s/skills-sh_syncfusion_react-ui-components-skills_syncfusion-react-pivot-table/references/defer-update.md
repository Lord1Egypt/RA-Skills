# Deferred Update Reference - Syncfusion React Pivot Table

## Overview

The deferred update feature in the Syncfusion React Pivot Table allows you to control when the pivot table recalculates and updates its display. Instead of updating immediately whenever a field is added, removed, or modified, you can configure the pivot table to update only when an "Apply" button is clicked. This is particularly valuable for performance optimization when working with large datasets or complex field configurations.

### Key Benefits
- **Performance Improvement**: Avoid multiple recalculations during field operations
- **User Control**: Users explicitly apply changes when ready
- **Batch Operations**: Perform multiple field changes before triggering an update
- **Reduced Flicker**: Eliminate visual rendering delays from repeated updates
- **Better UX**: Cleaner interface with predictable update behavior

## Use Cases

The deferred update feature is especially useful in these scenarios:

1. **Large Datasets**: Prevent lag when working with thousands of records
2. **Complex Calculations**: Avoid recursive recalculation overhead
3. **Multiple Field Changes**: Allow users to configure multiple fields before applying
4. **Real-Time Data Updates**: Control when fresh data is fetched and calculated

## Implementation

### With Field List (Popup)

Enable deferred update in the Field List component by setting `allowDeferLayoutUpdate` to **true**:

```typescript
import { FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sales' }, { name: 'Amount' }],
    dataSource: pivotData as IDataSet[]
  };

  let pivotObj: PivotViewComponent;

  return (
    <PivotViewComponent
      ref={(d: PivotViewComponent) => pivotObj = d}
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      allowDeferLayoutUpdate={true}
      showFieldList={true}
    >
      <Inject services={[FieldList]} />
    </PivotViewComponent>
  );
}

export default App;
```

### With Stand-alone Field List (Fixed)

When using a fixed field list positioned alongside the pivot table, set `allowDeferLayoutUpdate` on the `PivotFieldListComponent`:

```typescript
import { PivotFieldListComponent, PivotViewComponent, IDataSet, Inject, FieldList } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sales' }, { name: 'Amount' }],
    dataSource: pivotData as IDataSet[]
  };

  let pivotObj: PivotViewComponent;
  let fieldListObj: PivotFieldListComponent;

  return (
    <div style={{ display: 'flex' }}>
      <PivotFieldListComponent
        ref={(d: PivotFieldListComponent) => fieldListObj = d}
        id='PivotFieldList'
        dataSourceSettings={dataSourceSettings}
        renderMode='Fixed'
        allowDeferLayoutUpdate={true}
      >
        <Inject services={[FieldList]} />
      </PivotFieldListComponent>
      <PivotViewComponent
        ref={(d: PivotViewComponent) => pivotObj = d}
        id='PivotView'
        height={350}
        dataSourceSettings={dataSourceSettings}
      >
        <Inject services={[FieldList]} />
      </PivotViewComponent>
    </div>
  );
}

export default App;
```

## Apply Button

When deferred update is enabled, an **Apply** button automatically appears in the Field List UI. Users click this button to apply all pending changes to the pivot table.

### Apply Button Behavior
1. **Inactive State**: Disabled when no changes are pending
2. **Active State**: Enabled when fields are added, removed, or modified
3. **Click Action**: Applies all changes and triggers pivot table recalculation

## Synchronization Between Components

When using a stand-alone field list with deferred updates, you must ensure both components stay in sync using the `updateView()` and `update()` methods:

```typescript
// Synchronize field list changes to pivot table
function onUpdateView(): void {
  if (fieldListObj && pivotObj) {
    fieldListObj.updateView(pivotObj);
  }
}

// Update pivot table with new datasource settings
function onUpdate(): void {
  if (fieldListObj && pivotObj) {
    fieldListObj.update(pivotObj);
  }
}
```

## Events

### enginePopulated

Triggered after the pivot engine completes calculation:

```typescript
function enginePopulated(): void {
  console.log('Pivot table engine refresh completed');
}

<PivotViewComponent
  allowDeferLayoutUpdate={true}
  onEnginePopulated={enginePopulated}
  showFieldList={true}
>
  <Inject services={[FieldList]} />
</PivotViewComponent>
```

### isRequiredUpdate

Allows you to conditionally prevent the update:

```typescript
function isRequiredUpdate(args: PivotEngineEventArgs): void {
  if (args.dataSourceSettings.values.length === 0) {
    args.update = false; // Prevent update if no values field
  }
}

<PivotViewComponent
  allowDeferLayoutUpdate={true}
  onIsRequiredUpdate={isRequiredUpdate}
  showFieldList={true}
>
  <Inject services={[FieldList]} />
</PivotViewComponent>
```

## Best Practices

1. **Large Datasets**: Always enable deferred update for datasets with >10,000 rows
2. **Complex Hierarchies**: Use deferred update when drilling down through many levels
3. **User Guidance**: Inform users that changes don't apply immediately
4. **Validation**: Validate field configurations before allowing the Apply action
5. **Server-Side Data**: Use deferred update when fetching data from backend APIs

## Programmatic Apply

You can programmatically trigger the apply action from your code:

```typescript
function applyChanges(): void {
  if (fieldListObj) {
    fieldListObj.applyChanges(); // Apply pending changes
  }
}

// In your UI
<button onClick={applyChanges}>Apply Changes</button>
```

## Performance Comparison

| Scenario | Without Deferred Update | With Deferred Update |
|----------|------------------------|----------------------|
| Add 5 fields | 5 updates (5-25ms each) | 1 update (5-25ms total) |
| Remove 3 fields | 3 updates (5-25ms each) | 1 update (5-25ms total) |
| Large dataset (100k rows) | Immediate lag | Smooth interaction |
| Multiple changes | Visible flickering | Single smooth transition |

## Configuration Reference

```typescript
interface DeferUpdateSettings {
  // Enable/disable deferred layout update
  allowDeferLayoutUpdate: boolean;
  
  // AutoCalculate after field changes (when false, requires Apply click)
  autoCalculate?: boolean;
  
  // Time delay before auto-applying (in milliseconds)
  autoApplyDelay?: number;
  
  // Show/hide the Apply button
  showApplyButton?: boolean;
}
```

## Complete Example

```typescript
import { PivotViewComponent, FieldList, Inject, IDataSet } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function PivotWithDeferredUpdate() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [
      { name: 'Year', caption: 'Production Year' },
      { name: 'Quarter' }
    ],
    rows: [
      { name: 'Country' },
      { name: 'Products' }
    ],
    values: [
      { name: 'Sold', caption: 'Units Sold' },
      { name: 'Amount', caption: 'Sold Amount' }
    ],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    formatSettings: [{ name: 'Amount', format: 'C0' }]
  };

  let pivotObj: PivotViewComponent;

  const handleEnginePopulated = () => {
    console.log('Pivot table updated with deferred changes');
  };

  return (
    <PivotViewComponent
      ref={(d: PivotViewComponent) => pivotObj = d}
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      allowDeferLayoutUpdate={true}
      showFieldList={true}
      onEnginePopulated={handleEnginePopulated}
    >
      <Inject services={[FieldList]} />
    </PivotViewComponent>
  );
}

export default PivotWithDeferredUpdate;
```

## Related Features

- **Field List**: Required to display field configuration interface
- **Grouping Bar**: Can also work with grouping bar, though typically used with field list
- **Virtual Scrolling**: Combine with virtual scrolling for optimal large dataset performance
- **Performance Best Practices**: Part of overall performance optimization strategy

## Troubleshooting

**Apply button not appearing?**
- Ensure `allowDeferLayoutUpdate` is set to `true`
- Verify `showFieldList` is enabled
- Check that FieldList module is injected

**Changes not applying?**
- Ensure you're clicking the Apply button
- Check for JavaScript errors in console
- Verify field configuration is valid

**Lag still occurring?**
- Enable Virtual Scrolling additionally
- Check data compression settings
- Consider server-side aggregation for massive datasets
