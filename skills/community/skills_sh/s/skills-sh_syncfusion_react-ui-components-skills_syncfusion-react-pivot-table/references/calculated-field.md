# Calculated Field Reference

## Overview

The calculated field feature enables users to create custom value fields using mathematical formulas and existing fields from their data source. Users can perform complex calculations with basic arithmetic operators and seamlessly integrate these custom fields into their pivot table for enhanced data visualization and reporting.

## Enabling Calculated Field

To enable the calculated field functionality, set the [`allowCalculatedField`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#allowcalculatedfield) property to **true**. Once enabled, a "CALCULATED FIELD" button appears in the Field List UI. Clicking this button opens the calculated field dialog, where users can create and manage custom fields using an intuitive interface.

### Module Injection

To use the calculated field feature, you must inject the `CalculatedField` module into the pivot table:

```typescript
import { CalculatedField } from '@syncfusion/ej2-react-pivotview';

<Inject services={[CalculatedField]} />
```

## Creating Calculated Fields

Users can create calculated fields in two convenient ways:

### 1. Interactive Method: Using the Built-in Dialog

The built-in dialog is accessible from the Field List UI. Click the "CALCULATED FIELD" button to open the calculated field dialog, where users can create and manage custom fields using an intuitive interface.

### 2. Code-Based Method: Using calculatedFieldSettings Property

You can define calculated fields programmatically using the [`calculatedFieldSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/dataSourceSettings/#calculatedfieldsettings) property. This approach is ideal for pre-configuring specific calculations.

## Properties

### name
[`name`](https://ej2.syncfusion.com/react/documentation/api/pivotview/calculatedFieldSettingsModel/#name): Specifies a unique name for the calculated field.

### formula
[`formula`](https://ej2.syncfusion.com/react/documentation/api/pivotview/calculatedFieldSettingsModel/#formula): Defines the mathematical expression using existing field names and arithmetic operators.

### formatSettings
[`formatSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/formatSettings/): Configures the number format for displaying calculated results.

## Formula Syntax

Formulas use field names and arithmetic operators. Field names must be enclosed in double quotes when referenced in formulas:

```typescript
formula: '"Sum(Amount)"+"Sum(Sold)"'
```

### Supported Operators and Functions

#### Basic Arithmetic Operators

* `+` – addition operator
  ```typescript
  Syntax: X + Y
  ```

* `-` – subtraction operator
  ```typescript
  Syntax: X - Y
  ```

* `*` – multiplication operator
  ```typescript
  Syntax: X * Y
  ```

* `/` – division operator
  ```typescript
  Syntax: X / Y
  ```

* `^` – power operator
  ```typescript
  Syntax: X^2
  ```

#### Comparison Operators

* `<` - less than operator
  ```typescript
  Syntax: X < Y
  ```

* `<=` – less than or equal operator
  ```typescript
  Syntax: X <= Y
  ```

* `>` – greater than operator
  ```typescript
  Syntax: X > Y
  ```

* `>=` – greater than or equal operator
  ```typescript
  Syntax: X >= Y
  ```

* `==` – equal operator
  ```typescript
  Syntax: X == Y
  ```

* `!=` – not equal operator
  ```typescript
  Syntax: X != Y
  ```

#### Logical Operators

* `|` – OR operator
  ```typescript
  Syntax: X | Y
  ```

* `&` – AND operator
  ```typescript
  Syntax: X & Y
  ```

* `?` – conditional operator
  ```typescript
  Syntax: condition ? then : else
  ```

#### Built-in Functions

* `isNaN` – function that checks if the value is not a number
  ```typescript
  Syntax: isNaN(value)
  ```

* `!isNaN` – function that checks if the value is a number
  ```typescript
  Syntax: !isNaN(value)
  ```

* `abs` – function that returns the absolute value of a number
  ```typescript
  Syntax: abs(number)
  ```

* `min` – function that returns the minimum value
  ```typescript
  Syntax: min(number1, number2)
  ```

* `max` – function that returns the maximum value
  ```typescript
  Syntax: max(number1, number2)
  ```

> **Note**: You can also use JavaScript [Math](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math) object properties and methods directly in formulas.

## Adding Calculated Fields to Values Array

> **Important**: The calculated field feature applies only to value fields. By default, calculated fields created programmatically are added to the field list and calculated field dialog UI. To display a calculated field in the pivot table UI, it must be added to the [`values`](https://ej2.syncfusion.com/react/documentation/api/pivotview/dataSourceSettings/#values) property.

```typescript
values: [
  { name: 'Sold', caption: 'Units Sold' },
  { name: 'Amount', caption: 'Sold Amount' },
  { name: 'Total', caption: 'Total Units', type: 'CalculatedField' }
]
```

## Calculated Field Dialog UI

### Opening the Dialog Programmatically

You can display the calculated field dialog by calling the [`createCalculatedFieldDialog`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#createcalculatedfielddialog) method when an external button is clicked:

```typescript
function btnClick(): void {
  pivotObj.calculatedFieldModule.createCalculatedFieldDialog();
}
```

### Dialog Operations

The calculated field dialog provides several operations:

1. **Create New Calculated Field**: Enter a field name, build a formula, and set format options
2. **Edit Existing Field**: Click the edit icon next to a calculated field to modify it
3. **Rename Field**: Change the name of an existing calculated field
4. **Delete Field**: Remove a calculated field from the configuration
5. **Reuse Formulas**: Drag and drop existing calculated fields into the formula section

## Editing and Deleting Calculated Fields

### Editing through Field List and Grouping Bar

You can easily modify existing calculated fields using the built-in edit option available in both the field list and grouping bar:

1. Locate the calculated field button in either the field list or the grouping bar
2. Click the **Edit** icon next to the calculated field name
3. The calculated field dialog opens, displaying the current settings
4. Make changes to the field name, formula, or format as needed
5. Click **OK** to apply the changes

### Renaming an Existing Calculated Field

To rename a calculated field:

1. Locate the calculated field button in either the field list or the grouping bar
2. Click the **Edit** icon next to the calculated field name
3. The calculated field dialog opens, displaying the current field name in the text box at the top
4. Replace the existing name with your preferred name
5. Click **OK** to save the new name

### Editing Formula

To edit an existing calculated field formula:

1. Open the calculated field dialog
2. Select the calculated field you want to edit from the list
3. Click the **Edit** icon next to the selected field
4. The existing formula appears in a multiline text box at the bottom of the dialog
5. Update the formula according to your requirements
6. Click **OK** to save your changes

The pivot table will automatically refresh to reflect the updated calculations.

### Reusing an Existing Formula

To reuse an existing formula in a new calculated field:

1. Open the calculated field dialog to create a new field
2. Locate the existing calculated field whose formula you want to reuse
3. Drag the existing calculated field from the tree view
4. Drop it into the **Formula** section
5. The formula from the existing field is automatically added to your new calculated field
6. Modify the formula further if needed, or use it as is
7. Click **OK** to create the new calculated field

## Complete Code Examples

### Example 1: Basic Calculated Field with Field List

```typescript
import { CalculatedField, FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }, { name: 'Total', format: 'C2' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }, 
      { name: 'Total', caption: 'Total Units', type: 'CalculatedField' }
    ],
    calculatedFieldSettings: [{ name: 'Total', formula: '"Sum(Amount)"+"Sum(Sold)"' }]
  }
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent  
      ref={ (d: PivotViewComponent) => pivotObj = d } 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      allowCalculatedField={true} 
      showFieldList={true}>
      <Inject services={[CalculatedField, FieldList]}/> 
    </PivotViewComponent>
  );
};

export default App;
```

### Example 2: Opening Calculated Field Dialog with Button

```typescript
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { CalculatedField, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }, { name: 'Total', format: 'C2' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }, 
      { name: 'Total', caption: 'Total Units', type: 'CalculatedField' }
    ],
    calculatedFieldSettings: [{ name: 'Total', formula: '"Sum(Amount)"+"Sum(Sold)"' }]
  }
  let pivotObj: PivotViewComponent;
  
  return (
    <div>
      <div className="col-md-9"> 
        <PivotViewComponent  
          ref={ (d: PivotViewComponent) => pivotObj = d } 
          id='PivotView' 
          height={350} 
          dataSourceSettings={dataSourceSettings} 
          allowCalculatedField={true}>
          <Inject services={[CalculatedField]}/> 
        </PivotViewComponent>
      </div>
      <div className='col-lg-3 property-section'>
        <ButtonComponent cssClass='e-primary' onClick={btnClick.bind(this)}>
          Calculated Field
        </ButtonComponent>
      </div>
    </div>
  );

  function btnClick(): void {
    pivotObj.calculatedFieldModule.createCalculatedFieldDialog();
  }
};

export default App;
```

### Example 3: Complex Formula with Math Functions

```typescript
import { CalculatedField, FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }, 
      { name: 'Total', caption: 'Total Units', type: 'CalculatedField' }
    ],
    calculatedFieldSettings: [
      { 
        name: 'Total', 
        formula: 'Math.round("Sum(Amount)") > abs("Sum(Sold)") ? min("Sum(Amount)", "Sum(Sold)") : Math.sqrt("Sum(Sold)")'
      }
    ]
  }
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent  
      ref={ (d: PivotViewComponent) => pivotObj = d } 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      allowCalculatedField={true} 
      showFieldList={true}>
      <Inject services={[CalculatedField, FieldList]}/> 
    </PivotViewComponent>
  );
};

export default App;
```

## Format Settings for Calculated Fields

### Formatting Through Code

To format calculated field values in your code, use the [`formatSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/formatSettings/) property:

```typescript
formatSettings: [
  { name: 'Amount', format: 'C0' }, 
  { name: 'Total', format: 'C2' }
]
```

For more information about supported number formats, refer to the [number formatting documentation](https://ej2.syncfusion.com/react/documentation/pivotview/number-formatting).

### Formatting Through User Interface

To apply formatting to calculated field values via the user interface, use the built-in "Format" dropdown available in the calculated field dialog. This dropdown provides the following predefined format options:

* **Standard** - Displays numbers in their basic numeric form
* **Currency** - Displays numbers as currency values
* **Percent** - Displays numbers as percentage values
* **Custom** - Allows you to specify a custom format pattern
* **None** - Applies no formatting to the values

> **Note**: By default, **None** is selected in the dropdown.

### Applying Custom Formatting

For specific formatting requirements, select the **Custom** option from the "Format" dropdown. This allows you to enter custom format patterns that meet your exact display needs.

## Best Practices for Formula Creation

1. **Use Descriptive Names**: Choose clear, meaningful names for calculated fields that indicate their purpose

2. **Enclose Field Names**: Always enclose field names in double quotes within formulas (e.g., `"Sum(Amount)"`)

3. **Test Formulas**: Verify your formulas with sample data before deploying to production

4. **Apply Formatting**: Always apply appropriate format settings to ensure calculated values display correctly

5. **Use Math Functions**: Leverage JavaScript Math object methods for complex calculations

6. **Handle Edge Cases**: Consider using conditional operators and validation functions (isNaN, abs) to handle edge cases

7. **Document Complex Formulas**: Add comments or documentation for complex formulas to aid maintenance

8. **Optimize Performance**: Keep formulas simple and efficient for better performance with large datasets

9. **Reuse Formulas**: Use the drag-and-drop feature to reuse existing formulas and maintain consistency

10. **Validate Before Saving**: Use the `calculatedFieldCreate` event to validate formulas before they are applied

## Events

### calculatedFieldCreate Event

The [`calculatedFieldCreate`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#calculatedfieldcreate) event enables you to validate and manage calculated field details before they are applied to the pivot table. This event is triggered when the "OK" button is clicked to close the calculated field dialog.

**Event Parameters:**

* [`calculatedField`](https://ej2.syncfusion.com/react/documentation/api/pivotview/calculatedFieldCreateEventArgs/#calculatedfield): Contains the calculated field information (new or existing) that was entered in the dialog
* [`calculatedFieldSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/dataSourceSettings/#calculatedfieldsettings): Provides access to the current calculated field settings
* [`cancel`](https://ej2.syncfusion.com/react/documentation/api/pivotview/calculatedFieldCreateEventArgs/#cancel): Boolean property to prevent the dialog changes from being applied
* [`dataSourceSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/calculatedFieldCreateEventArgs/#datasourcesettings): Contains the current data source configuration
* [`fieldName`](https://ej2.syncfusion.com/react/documentation/api/pivotview/calculatedFieldCreateEventArgs/#fieldname): Specifies the name of the field being created or updated

**Example:**

```typescript
import { CalculatedField, FieldList, IDataSet, Inject, PivotViewComponent, CalculatedFieldCreateEventArgs } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }, 
      { name: 'Total', caption: 'Total Units', type: 'CalculatedField' }
    ],
    calculatedFieldSettings: [
      { 
        name: 'Total', 
        formula: 'Math.round("Sum(Amount)") > abs("Sum(Sold)") ? min("Sum(Amount)", "Sum(Sold)") : Math.sqrt("Sum(Sold)")'
      }
    ]
  }
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent  
      ref={ (d: PivotViewComponent) => pivotObj = d } 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      allowCalculatedField={true} 
      showFieldList={true} 
      calculatedFieldCreate={calculatedFieldCreate.bind(this)}>
      <Inject services={[CalculatedField, FieldList]}/> 
    </PivotViewComponent>
  );

  function calculatedFieldCreate(args: CalculatedFieldCreateEventArgs) {
    if(args.calculatedField.formatString === '') {
      args.cancel = true;
    }
  }
};

export default App;
```

### actionBegin Event

The [`actionBegin`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#actionbegin) event allows you to control and monitor calculated field operations before they are executed. This event is triggered when users interact with calculated field functionality.

**Event Parameters:**

* [`dataSourceSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/pivotActionBeginEventArgs/#datasourcesettings): Current data source configuration
* [`actionName`](https://ej2.syncfusion.com/react/documentation/api/pivotview/pivotActionBeginEventArgs/#actionname): Identifies the specific action being performed
* [`fieldInfo`](https://ej2.syncfusion.com/react/documentation/api/pivotview/pivotActionBeginEventArgs/#fieldinfo): Information about the selected field (when applicable)
* [`cancel`](https://ej2.syncfusion.com/react/documentation/api/pivotview/pivotActionBeginEventArgs/#cancel): Boolean to prevent the action from proceeding

**Action Names:**

| User Action | Action Name |
|-------------|-------------|
| Calculated field button click | Open calculated field dialog |
| Edit icon click for calculated field | Edit calculated field |
| Context menu in calculated field dialog tree view | Calculated field context menu |

**Example:**

```typescript
function actionBegin(args: PivotActionBeginEventArgs): void {
  if (args.actionName == 'Open calculated field dialog') {
    args.cancel = true;
  }
}
```

### actionComplete Event

The [`actionComplete`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#actioncomplete) event enables you to track when calculated field operations are successfully completed.

**Event Parameters:**

* [`dataSourceSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/pivotActionCompleteEventArgs/#datasourcesettings): Updated data source configuration after the operation
* [`actionName`](https://ej2.syncfusion.com/react/documentation/api/pivotview/pivotActionCompleteEventArgs/#actionname): Identifies the completed action
* [`fieldInfo`](https://ej2.syncfusion.com/react/documentation/api/pivotview/pivotActionCompleteEventArgs/#fieldinfo): Information about the selected field (when applicable)
* [`actionInfo`](https://ej2.syncfusion.com/react/documentation/api/pivotview/pivotActionCompleteEventArgs/#actioninfo): Detailed information about the completed action

**Action Names:**

| User Action | Action Name |
|-------------|-------------|
| Creating calculated field | Calculated field applied |
| Editing calculated field | Calculated field edited |

**Example:**

```typescript
function actionComplete(args: PivotActionCompleteEventArgs): void {
  if (args.actionName == 'Calculated field applied') {
    // Triggers when the calculated field is applied
  }
}
```

### actionFailure Event

The [`actionFailure`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#actionfailure) event is triggered when a UI action fails to produce the expected result.

**Event Parameters:**

* [`actionName`](https://ej2.syncfusion.com/react/documentation/api/pivotview/pivotActionFailureEventArgs/#actionname): Name of the failed action
* [`errorInfo`](https://ej2.syncfusion.com/react/documentation/api/pivotview/pivotActionFailureEventArgs/#errorinfo): Error information about the failed action

**Action Names:**

| Action | Action Name |
|--------|-------------|
| Calculated field button | Open calculated field dialog |
| Edit icon in calculated field | Edit calculated field |
| Context menu in tree view | Calculated field context menu |

**Example:**

```typescript
function actionFailure(args: PivotActionFailureEventArgs): void {
  if (args.actionName == 'Open calculated field dialog') {
    // Handle the failure
  }
}
```

## Sample Data Source

```typescript
export let pivotData: object[] = [
  { 'In_Stock': 34, 'Sold': 51, 'Amount': 383, 'Country': 'France', 'Product_Categories': 'Accessories', 'Products': 'Bottles and Cages', 'Order_Source': 'Retail Outlets', 'Year': 'FY 2015', 'Quarter': 'Q1' },
  { 'In_Stock': 4, 'Sold': 423, 'Amount': 3595.5, 'Country': 'France', 'Product_Categories': 'Accessories', 'Products': 'Cleaners', 'Order_Source': 'Sales Person', 'Year': 'FY 2016', 'Quarter': 'Q1' },
  { 'In_Stock': 11, 'Sold': 19, 'Amount': 85.5, 'Country': 'France', 'Product_Categories': 'Bikes', 'Products': 'Touring Bikes', 'Order_Source': 'Retail Outlets', 'Year': 'FY 2017', 'Quarter': 'Q4' },
  { 'In_Stock': 10, 'Sold': 64, 'Amount': 320, 'Country': 'France', 'Product_Categories': 'Bikes', 'Products': 'Mountain Bikes', 'Order_Source': 'Sales Person', 'Year': 'FY 2018', 'Quarter': 'Q4' },
  { 'In_Stock': 2, 'Sold': 141, 'Amount': 1692, 'Country': 'France', 'Product_Categories': 'Clothing', 'Products': 'Jerseys', 'Order_Source': 'Sales Person', 'Year': 'FY 2015', 'Quarter': 'Q1' },
  // Additional data rows...
];
```
