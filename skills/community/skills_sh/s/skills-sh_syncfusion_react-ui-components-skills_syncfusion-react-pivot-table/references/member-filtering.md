# Member Filtering Reference - Syncfusion React Pivot Table

## Overview

Member filtering enables users to selectively include or exclude specific members (values) from rows, columns, and filter fields in the pivot table. Unlike label filtering which filters based on field headers/text patterns, member filtering works directly with the actual data member values. This feature is essential for focusing analysis on specific subsets of data.

### Key Features
- **Individual Member Selection**: Choose specific values to include or exclude
- **UI-Based Filtering**: Built-in member filter dialog in Field List
- **Programmatic Control**: Filter members via code using `drilledMembers`
- **Multi-Select Support**: Select multiple members at once
- **Hierarchical Support**: Filter members within grouped/hierarchical data
- **Performance**: Efficient handling of large member lists

### Basic Setup

To enable member filtering, set `allowMemberFilter` to **true** and inject the required modules:

```typescript
import { PivotViewComponent, FieldList, MemberFilter, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales' }],
    filters: [{ name: 'Year' }],
    allowMemberFilter: true
  };

  return (
    <PivotViewComponent
      id="PivotView"
      dataSourceSettings={dataSourceSettings}
      showFieldList={true}
      height={350}
    >
      <Inject services={[FieldList, MemberFilter]} />
    </PivotViewComponent>
  );
}

export default App;
```

### Enabling Member Filtering Programmatically using filterSettings.

Include or exclude specific field members from the pivot table.

```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-filter',
  template: `<ejs-pivotview [dataSourceSettings]="dataSourceSettings"></ejs-pivotview>`
})
export class AppComponent {
  dataSourceSettings: IDataOptions = {
    dataSource: data,
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Year' }],
    values: [{ name: 'Sales', type: 'Sum' }],
    filterSettings: [{
      name: 'Country',
      type: 'Include',
      items: ['USA', 'Canada']
    }]
  };
}
```

## Member Filter Dialog

### Accessing the Filter Dialog

Member filter options appear in the Field List UI. Click the filter icon next to any field to open the member filter dialog:

```typescript
// Member filter dialog automatically shows when you click filter icon in Field List
// Features available in the dialog:
// - Search box to find specific members
// - Select All / Deselect All buttons
// - Checkbox list of all members
// - Apply and Cancel buttons
```

### Filter Dialog Configuration

```typescript

<PivotViewComponent
  maxNodeLimitInMemberEditor={500}
  showFieldList={true}
  dataSourceSettings={{
    ...dataSourceSettings,
    allowMemberFilter: true
  }}
/>
```

## Performance Considerations

1. **Large Member Lists**: For fields with 10,000+ members, enable search in filter dialog
2. **Field List Limits**: Use `maxNodeLimitInMemberEditor` to optimize UI performance
3. **Hierarchical Data**: Filter at appropriate hierarchy levels for better performance
4. **Lazy Loading**: Load member lists on-demand when needed

```typescript
// Performance optimization for large datasets
const fieldListSettings = {
  maxNodeLimitInMemberEditor: 1000,  // Limit displayed members
  allowSearching: true               // Enable search for finding members
};

<PivotViewComponent
  fieldListSettings={fieldListSettings}
  dataSourceSettings={{
    ...dataSourceSettings,
    allowMemberFilter: true
  }}
/>
```

## Best Practices

✅ **Do:**
- Use member filtering for focused analysis on specific data subsets
- Combine with other filters (label, value) for comprehensive filtering
- Provide UI controls for easy member selection
- Cache filter selections for quick re-application
- Use hierarchical filtering for multi-level data

❌ **Don't:**
- Filter out all members (results in empty pivot)
- Apply excessive member filters on large datasets without optimization
- Forget to update pivot when member selections change
- Use member filter for what should be label filtering

## Common Issues

**No filter icon visible?**
- Verify `allowMemberFilter` is `true`
- Check that `FieldList` or `GroupingBar` is injected
- Ensure `showFieldList={true}` or `showGroupingBar={true}`

**Member filter not applying?**
- Verify `drilledMembers` is correctly configured with matching member values
- Check console for JavaScript errors
- Ensure data source contains the specified members

**Performance slow with many members?**
- Use `maxNodeLimitInMemberEditor` to limit displayed members
- Enable search functionality for navigation
- Consider server-side filtering for very large datasets

## Related Features

- **Label Filtering**: Filter by field headers/text patterns
- **Value Filtering**: Filter by aggregated measure values
- **Field List**: UI for managing fields and filters
- **Grouping Bar**: Alternative UI for field management with filters
