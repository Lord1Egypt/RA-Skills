# Field List Reference - Syncfusion React Pivot Table

## Overview

The Field List is a powerful UI component that allows users to organize and analyze data in the Pivot Table. It provides an Excel-like interface for managing fields across different axes (columns, rows, values, and filters), and offers features like sorting, filtering, and drag-drop functionality.

### Field List Modes

The Field List can be displayed in two ways:

1. **In-built Field List (Popup)**: A dialog-based field list that appears on demand
2. **Stand-alone Field List (Fixed)**: A permanently visible field list positioned alongside the Pivot Table

---

## In-built Field List (Popup)

### Configuration

Enable the built-in field list by setting the `showFieldList` property to `true`. A field list icon appears in the top-left corner of the Pivot Table (or top-right when the grouping bar is enabled).

**Required Module**: Inject the `FieldList` module into the Pivot Table.

### Basic Implementation

```ts
import { FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    allowLabelFilter: true,
    allowValueFilter: true,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }
  let pivotObj: PivotViewComponent;

  return (
    <PivotViewComponent 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      showFieldList={true}>
      <Inject services={[FieldList]} />
    </PivotViewComponent>
  );
}

export default App;
```

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `showFieldList` | boolean | Enables/disables the field list icon |
| `allowLabelFilter` | boolean | Enables label filtering in field list |
| `allowValueFilter` | boolean | Enables value filtering in field list |

---

## Stand-alone Field List (Fixed)

### Configuration

The stand-alone field list remains visible at a fixed position on the page. Use the `renderMode` property set to `"Fixed"` in the `PivotFieldListComponent`.

### Synchronization Methods

- **`updateView()`**: Synchronizes data source changes from field list to Pivot Table
- **`update()`**: Synchronizes data source changes from Pivot Table to field list

### Complete Implementation

```ts
import { CalculatedField, PivotFieldListComponent, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

const SAMPLE_CSS = `
.e-pivotview {
    width: 58%;
    height: 100%;
    float: left;
}
.e-pivotfieldlist {
    width: 42%;
    height: 100%;
    float: right;
}
.e-pivotfieldlist .e-static {
    width: 100% !important;
}`;

function App() {
  React.useEffect(() => {
    renderComplete();
  }, []);

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }
  let pivotObj: PivotViewComponent;
  let fieldlistObj: PivotFieldListComponent;

  return (
    <div className="control-section">
      <style>{SAMPLE_CSS}</style>
      <PivotViewComponent 
        id='PivotViewFieldList' 
        ref={(d: PivotViewComponent) => pivotObj = d} 
        enginePopulated={afterPivotPopulate.bind(this)} 
        width={'99%'} 
        height={'530'} 
        gridSettings={{columnWidth: 140}}>
      </PivotViewComponent>
      <PivotFieldListComponent 
        id='PivotFieldList' 
        ref={(d: PivotFieldListComponent) => fieldlistObj = d} 
        enginePopulated={afterPopulate.bind(this)} 
        dataSourceSettings={dataSourceSettings} 
        renderMode={"Fixed"} 
        allowCalculatedField={true}>
        <Inject services={[CalculatedField]} />
      </PivotFieldListComponent>
    </div>
  );

  function afterPopulate(): void {
    pivotObj = document.getElementById('PivotViewFieldList').ej2_instances[0];
    fieldlistObj = document.getElementById('PivotFieldList').ej2_instances[0];
    fieldlistObj.updateView(pivotObj);
  }
  
  function afterPivotPopulate(): void {
    pivotObj = document.getElementById('PivotViewFieldList').ej2_instances[0];
    fieldlistObj = document.getElementById('PivotFieldList').ej2_instances[0];
    fieldlistObj.update(pivotObj);
  }
  
  function renderComplete(): void {
    fieldlistObj.updateView(pivotObj);
  }
}

export default App;
```

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `renderMode` | string | Set to `"Fixed"` for stand-alone mode |
| `updateView()` | method | Syncs field list changes to Pivot Table |
| `update()` | method | Syncs Pivot Table changes to field list |

---

## Dynamic Field List Invocation

### External Button Trigger

Open the field list dialog using an external button by setting `renderMode` to `"Popup"` and using the dialog renderer API.

### Implementation

```ts
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { CalculatedField, PivotFieldListComponent, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  React.useEffect(() => {
    renderComplete();
  }, []);

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }
  let pivotObj: PivotViewComponent;
  let fieldlistObj: PivotFieldListComponent;
  
  return (
    <div>
      <div className="control-section">
        <ButtonComponent cssClass='e-primary' onClick={btnClick.bind(this)}>
          Field List
        </ButtonComponent>
        <PivotViewComponent 
          id='PivotView' 
          ref={(d: PivotViewComponent) => pivotObj = d} 
          enginePopulated={afterPivotPopulate.bind(this)} 
          height={350} 
          gridSettings={{columnWidth: 140}}>
        </PivotViewComponent>
        <PivotFieldListComponent 
          id='PivotFieldList' 
          ref={(d: PivotFieldListComponent) => fieldlistObj = d} 
          enginePopulated={afterPopulate.bind(this)} 
          dataSourceSettings={dataSourceSettings} 
          target='#PivotFieldList' 
          renderMode={"Popup"} 
          allowCalculatedField={true}>
          <Inject services={[CalculatedField]} />
        </PivotFieldListComponent>
      </div>
    </div>
  );

  function btnClick(): void {
    fieldlistObj.dialogRenderer.fieldListDialog.show();
  }

  function afterPopulate(): void {
    if (fieldlistObj && pivotObj) {
      fieldlistObj.updateView(pivotObj);
    }
  }
  
  function afterPivotPopulate(): void {
    if (fieldlistObj && pivotObj) {
      fieldlistObj.update(pivotObj);
    }
  }
  
  function renderComplete(): void {
    fieldlistObj.updateView(pivotObj);
  }
}

export default App;
```

### Target Property

Use the `target` property to specify where the dialog appears:
- Default: `null` (positions relative to `document.body`)
- Custom: Specify any DOM element selector

---

## Field List UI Interactions

### 1. Drag-and-Drop

Users can drag fields from the field list and drop them into any axis area (rows, columns, values, or filters) to reorganize the Pivot Table structure dynamically.

### 2. Field Operations

#### Add/Remove Fields
- Check/uncheck field checkboxes to include/exclude them from the report

#### Re-arrange Fields
- Drag fields between different axis areas
- Reorder fields within the same axis

### 3. Filtering

Click the filter icon next to any field to open the filter dialog and include/exclude specific members.

### 4. Sorting

Click the sort icon next to any field to arrange members in ascending or descending order.

### 5. Aggregation Type Selection

For value fields, click the dropdown icon to select aggregation types:
- Sum
- Average
- Count
- Min
- Max
- Product
- Distinct Count
- etc.

---

## Field Search Feature

### Enable Field Search

Allow users to search for fields by name in the field list.

#### For Stand-alone Field List

```ts
<PivotFieldListComponent 
  id='PivotFieldList' 
  dataSourceSettings={dataSourceSettings} 
  renderMode={"Fixed"} 
  enableFieldSearching={true}>
</PivotFieldListComponent>
```

#### For Built-in Popup Field List

```ts
<PivotViewComponent 
  id='PivotView' 
  dataSourceSettings={dataSourceSettings} 
  showFieldList={true} 
  enableFieldSearching={true}>
  <Inject services={[FieldList]} />
</PivotViewComponent>
```

### Key Property

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enableFieldSearching` | boolean | false | Enables search box in field list |

---

## Field Sorting Options

### Sort Order Options

Fields in the field list can be sorted in three ways:
- **None** (Default): As they appear in the data source
- **Ascending**: A to Z
- **Descending**: Z to A

### Set Default Sort Order

```ts
import { FieldList, IDataSet, Inject, PivotViewComponent, PivotActionBeginEventArgs } from '@syncfusion/ej2-react-pivotview';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    columns: [{ name: 'Year', caption: 'Production Year' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }],
    rows: [{ name: 'Country' }],
    formatSettings: [{ name: 'Amount', format: 'C0' }]
  }

  return (
    <PivotViewComponent 
      id='PivotView' 
      height={350} 
      load={onLoad.bind(this)} 
      dataSourceSettings={dataSourceSettings} 
      showFieldList={true}>
      <Inject services={[FieldList]} />
    </PivotViewComponent>
  );

  function onLoad(args: PivotActionBeginEventArgs): void {
    args.defaultFieldListOrder = 'Descending';
  }
}
```

---

## Field Grouping

### Group Fields by Folder

Organize fields under custom folder names for better categorization.

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year', caption: 'Production Year' }],
  dataSource: pivotData as IDataSet[],
  values: [{ name: 'Sold', caption: 'Units Sold' }],
  rows: [{ name: 'Country' }],
  fieldMapping: [
    { name: 'Quarter', groupName: 'Product category' },
    { name: 'Products', groupName: 'Product category' },
    { name: 'Amount', groupName: 'Product category', caption: 'Sold Amount' }
  ]
}
```

### Key Property

| Property | Type | Description |
|----------|------|-------------|
| `groupName` | string | Groups field under specified folder name |
| `fieldMapping` | array | Array of field mapping configurations |

**Note**: Fields can only be grouped under a single level.

---

## Exclude Specific Fields

Hide fields from the field list using the `excludeFields` property.

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  dataSource: pivotData as IDataSet[],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
  excludeFields: ["Products", "Amount"]
}
```

---

## Set Field Captions

Set captions for fields not bound to the report using the `enginePopulated` event.

```ts
function afterPopulate(): void {
  Object.keys(pivotObj.engineModule.fieldList).forEach((key, index) => {
    if (key === 'Quarter') {
      pivotObj.engineModule.fieldList[key].caption = 'Production Quarter Year';
    }
    else if (key === 'Year') {
      pivotObj.engineModule.fieldList[key].caption = 'Production Year';
    }
  });  
}
```

---

## Values Button

Enable the Values button to reposition the values field among other fields in column or row axis.

```ts
<PivotFieldListComponent 
  id='PivotFieldList' 
  dataSourceSettings={dataSourceSettings} 
  renderMode={"Fixed"}
  showValuesButton={true}>
</PivotFieldListComponent>
```

**Note**: 
- Only available for relational data sources
- Displayed only when multiple fields are in the Values axis

---

## Field List in Toolbar

Display the field list icon in the toolbar instead of the Pivot Table corner.

```ts
import { FieldList, Toolbar, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { ToolbarItems } from '@syncfusion/ej2-pivotview/src/common/base/enum';

function App() {
  let toolbarOptions: ToolbarItems[] = ['FieldList'];

  return (
    <PivotViewComponent 
      id='PivotView' 
      dataSourceSettings={dataSourceSettings} 
      width={'100%'} 
      height={350} 
      showFieldList={true} 
      showToolbar={true} 
      toolbar={toolbarOptions}>
      <Inject services={[FieldList, Toolbar]} />
    </PivotViewComponent>
  );
}
```

---

## Show Field List Over Specific Target

Configure the field list dialog to appear over a specific element.

```ts
function trend(): void {
  pivotObj.pivotFieldListModule.dialogRenderer.fieldListDialog.target = document.body;
}
```

---

## Events

### 1. enginePopulated

Triggered after the data engine is populated. Use to synchronize field list and Pivot Table.

```ts
function afterPopulate(): void {
  if (fieldlistObj && pivotObj) {
    fieldlistObj.updateView(pivotObj);
  }
}

function afterPivotPopulate(): void {
  if (fieldlistObj && pivotObj) {
    fieldlistObj.update(pivotObj);
  }
}
```

**Parameters**:
- `dataSourceSettings`: Current data source configuration
- `pivotFieldList`: Field list instance
- `pivotValues`: Current pivot values

### 2. fieldListRefreshed

Triggered when field list UI is refreshed after any change.

```ts
function fieldListRefreshed(args: FieldListRefreshedEventArgs): void {
  // Handle field list refresh
}
```

**Parameters**:
- `dataSourceSettings`: Updated data source settings
- `pivotValues`: Updated pivot values

### 3. onFieldDropped

Triggered when a field is dropped into an axis.

```ts
function fieldDropped(args: FieldDroppedEventArgs): void {
  args.droppedField.caption = args.droppedField.name + " --> " + args.droppedAxis;
}
```

**Parameters**:
- `dataSourceSettings`: Current data source settings
- `droppedAxis`: Axis where field was dropped
- `droppedField`: Field item details
- `droppedPosition`: Position in the axis
- `fieldName`: Name of dropped field

### 4. actionBegin

Triggered when UI actions (sorting, filtering, aggregation) begin.

```ts
function actionBegin(args: PivotActionBeginEventArgs): void {
  if (args.actionName == 'Open field list') {
    args.cancel = true; // Prevent action
  }
}
```

**Parameters**:
- `dataSourceSettings`: Current data source settings
- `actionName`: Name of the action
- `fieldInfo`: Selected field information
- `cancel`: Boolean to prevent action

**Action Names**:
| UI Action | Action Name |
|-----------|-------------|
| Sort icon | Sort field |
| Filter icon | Filter field |
| Aggregation | Aggregate field |
| Edit calculated field | Edit calculated field |
| Calculated field button | Open calculated field dialog |
| Field list icon | Open field list |
| Field list tree sort | Sort field tree |

### 5. actionComplete

Triggered when UI actions are completed.

```ts
function actionComplete(args: PivotActionCompleteEventArgs): void {
  if (args.actionName == 'Field list closed') {
    // Handle completion
  }
}
```

**Parameters**:
- `dataSourceSettings`: Updated data source settings
- `actionName`: Name of completed action
- `fieldInfo`: Field information
- `actionInfo`: Action-specific information

**Action Names**:
| UI Action | Action Name |
|-----------|-------------|
| Sort icon | Field sorted |
| Filter icon | Field filtered |
| Aggregation | Field aggregated |
| Edit calculated field | Calculated field edited |
| Calculated field button | Calculated field applied |
| Field list icon | Field list closed |
| Field list tree sort | Field tree sorted |

### 6. actionFailure

Triggered when a UI action fails.

```ts
function actionFailure(args: PivotActionFailureEventArgs): void {
  if (args.actionName == 'Open field list') {
    // Handle failure
  }
}
```

**Parameters**:
- `actionName`: Name of failed action
- `errorInfo`: Error details

---

## Best Practices

### 1. Synchronization
Always implement proper synchronization between field list and Pivot Table:
- Use `updateView()` in field list's `enginePopulated` event
- Use `update()` in Pivot Table's `enginePopulated` event

### 2. Performance
- Use `excludeFields` to hide unnecessary fields
- Enable field search for large datasets
- Group related fields using `fieldMapping`

### 3. User Experience
- Enable `enableFieldSearching` for better field discovery
- Use descriptive field captions
- Group fields logically using `groupName`
- Set appropriate default sort order

### 4. Layout
- For fixed field list, use appropriate CSS for layout
- Position popup field list over suitable target elements
- Consider using toolbar integration for cleaner UI

### 5. Event Handling
- Use `actionBegin` to validate operations before execution
- Use `actionComplete` for post-operation tasks
- Use `actionFailure` for error handling

---

## Common Patterns

### Pattern 1: Basic Popup Field List

```ts
<PivotViewComponent 
  dataSourceSettings={dataSourceSettings} 
  showFieldList={true}>
  <Inject services={[FieldList]} />
</PivotViewComponent>
```

### Pattern 2: Fixed Field List with Synchronization

```ts
// Field List Component
<PivotFieldListComponent 
  enginePopulated={afterPopulate} 
  dataSourceSettings={dataSourceSettings} 
  renderMode="Fixed">
</PivotFieldListComponent>

// Pivot Table Component
<PivotViewComponent 
  enginePopulated={afterPivotPopulate}>
</PivotViewComponent>

// Synchronization Functions
function afterPopulate() {
  fieldlistObj.updateView(pivotObj);
}

function afterPivotPopulate() {
  fieldlistObj.update(pivotObj);
}
```

### Pattern 3: External Button Trigger

```ts
<ButtonComponent onClick={btnClick}>Field List</ButtonComponent>
<PivotFieldListComponent 
  renderMode="Popup" 
  target='#PivotFieldList'>
</PivotFieldListComponent>

function btnClick() {
  fieldlistObj.dialogRenderer.fieldListDialog.show();
}
```

### Pattern 4: Field Search Enabled

```ts
<PivotViewComponent 
  showFieldList={true} 
  enableFieldSearching={true}>
  <Inject services={[FieldList]} />
</PivotViewComponent>
```

### Pattern 5: Grouped Fields

```ts
let dataSourceSettings = {
  dataSource: pivotData as IDataSet[],
  fieldMapping: [
    { name: 'Quarter', groupName: 'Time Period' },
    { name: 'Year', groupName: 'Time Period' },
    { name: 'Products', groupName: 'Sales' },
    { name: 'Amount', groupName: 'Sales' }
  ]
}
```

---

## Summary

The Field List provides comprehensive functionality for managing Pivot Table data:

1. **Modes**: Popup or Fixed display options
2. **Interactions**: Drag-drop, filtering, sorting, aggregation
3. **Customization**: Field search, grouping, exclusion, custom captions
4. **Synchronization**: Seamless updates between field list and Pivot Table
5. **Events**: Complete lifecycle management with actionBegin, actionComplete, actionFailure
6. **Best Practices**: Performance optimization and user experience enhancement

Use the appropriate mode and features based on your application requirements to provide users with an intuitive data analysis interface.
