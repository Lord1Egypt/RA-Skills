# API Reference

Complete reference for all Query Builder properties, methods, and events.

## Table of Contents
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Interfaces and Types](#interfaces-and-types)

## Properties

### Configuration Properties

#### addRuleToNewGroups
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Specifies whether to enable/disable adding new rules when adding new groups.

```tsx
<QueryBuilderComponent addRuleToNewGroups={false} />
```

#### allowDragAndDrop
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enables/disables drag-and-drop support to move rules and groups.

```tsx
<QueryBuilderComponent allowDragAndDrop={true} />
```

#### allowValidation
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enables or disables field validation.

```tsx
<QueryBuilderComponent allowValidation={true} />
```

#### autoSelectField
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Automatically selects the first value for the field dropdown.

```tsx
<QueryBuilderComponent autoSelectField={true} />
```

#### autoSelectOperator
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Automatically selects the first operator for the selected field.

```tsx
<QueryBuilderComponent autoSelectOperator={true} />
```

### Data Properties

#### columns
- **Type:** `ColumnsModel[]`
- **Default:** `{}`
- **Description:** Specifies columns to create filters.

```tsx
const columns: ColumnsModel[] = [
  { field: 'EmployeeID', label: 'Employee ID', type: 'number' },
  { field: 'FirstName', label: 'First Name', type: 'string' }
];

<QueryBuilderComponent columns={columns} />
```

#### dataSource
- **Type:** `Object[] | Object | DataManager`
- **Default:** `[]`
- **Description:** Binds the column names from data source. Can be an array or DataManager instance.

```tsx
<QueryBuilderComponent dataSource={employeeData} />
// or
<QueryBuilderComponent dataSource={new DataManager({url: 'api/data'})} />
```

#### rule
- **Type:** `RuleModel`
- **Default:** `{}`
- **Description:** Defines initial rules in the Query Builder.

```tsx
const initialRule: RuleModel = {
  condition: 'and',
  rules: [{
    field: 'EmployeeID',
    operator: 'equal',
    type: 'number',
    value: 1001
  }]
};

<QueryBuilderComponent rule={initialRule} />
```

### Display Properties

#### displayMode
- **Type:** `'Horizontal' | 'Vertical'`
- **Default:** `'Horizontal'`
- **Description:** Specifies layout orientation.

```tsx
<QueryBuilderComponent displayMode="Vertical" />
```

#### height
- **Type:** `string`
- **Default:** `'auto'`
- **Description:** Specifies the height of the Query Builder.

```tsx
<QueryBuilderComponent height="400px" />
```

#### width
- **Type:** `string`
- **Default:** `'auto'`
- **Description:** Specifies the width of the Query Builder.

```tsx
<QueryBuilderComponent width="100%" />
```

#### cssClass
- **Type:** `string`
- **Default:** `''`
- **Description:** Defines CSS classes for styling.

```tsx
<QueryBuilderComponent cssClass="custom-qb dark-theme" />
```

#### headerTemplate
- **Type:** `string | Function`
- **Default:** `null`
- **Description:** Specifies template for the header area.

```tsx
function customHeader(props: any) {
  return <div>Custom Header</div>;
}

<QueryBuilderComponent headerTemplate={customHeader} />
```

### Behavior Properties

#### enableNotCondition
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enables/disables the NOT group condition.

```tsx
<QueryBuilderComponent enableNotCondition={true} />
```

#### enablePersistence
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enables state persistence to localStorage.

```tsx
<QueryBuilderComponent enablePersistence={true} />
```

#### enableRtl
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enables right-to-left rendering.

```tsx
<QueryBuilderComponent enableRtl={true} locale="ar-AE" />
```

#### enableSeparateConnector
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Displays separate AND/OR connectors between rules.

```tsx
<QueryBuilderComponent enableSeparateConnector={true} />
```

#### readonly
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Makes the component read-only.

```tsx
<QueryBuilderComponent readonly={true} />
```

### Advanced Properties

#### fieldMode
- **Type:** `'Default' | 'DropDownTree'`
- **Default:** `'Default'`
- **Description:** Sets field display as DropDownList or DropDownTree.

```tsx
<QueryBuilderComponent fieldMode="DropDownTree" />
```

#### fieldModel
- **Type:** `DropDownListModel | DropDownTreeModel`
- **Default:** `null`
- **Description:** Specifies properties for the field dropdown.

```tsx
<QueryBuilderComponent fieldModel={{ popupHeight: '300px' }} />
```

#### operatorModel
- **Type:** `DropDownListModel`
- **Default:** `null`
- **Description:** Specifies properties for the operator dropdown.

```tsx
<QueryBuilderComponent operatorModel={{ popupHeight: '200px' }} />
```

#### valueModel
- **Type:** `ValueModel`
- **Default:** `null`
- **Description:** Specifies properties for the value input.

```tsx
<QueryBuilderComponent valueModel={{ placeholder: 'Enter value' }} />
```

### Configuration Constants

#### immediateModeDelay
- **Type:** `number`
- **Default:** `0`
- **Description:** Delay (ms) before triggering rule change event.

```tsx
<QueryBuilderComponent immediateModeDelay={500} />
```

#### locale
- **Type:** `string`
- **Default:** `''`
- **Description:** Overrides global culture and localization.

```tsx
<QueryBuilderComponent locale="fr-FR" />
```

#### matchCase
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Case-sensitive filtering.

```tsx
<QueryBuilderComponent matchCase={true} />
```

#### maxGroupCount
- **Type:** `number`
- **Default:** `5`
- **Description:** Maximum group nesting depth.

```tsx
<QueryBuilderComponent maxGroupCount={3} />
```

#### separator
- **Type:** `string`
- **Default:** `''`
- **Description:** Separator string for column display.

```tsx
<QueryBuilderComponent separator=" - " />
```

#### showButtons
- **Type:** `ShowButtonsModel`
- **Default:** `{ ruleDelete: true, groupInsert: true, groupDelete: true }`
- **Description:** Controls button visibility.

```tsx
<QueryBuilderComponent showButtons={{
  ruleDelete: true,
  groupInsert: true,
  groupDelete: false
}} />
```

#### sortDirection
- **Type:** `'Default' | 'Ascending' | 'Descending'`
- **Default:** `'Default'`
- **Description:** Sort direction of field names.

```tsx
<QueryBuilderComponent sortDirection="Ascending" />
```

#### summaryView
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Shows/hides the filtered query summary.

```tsx
<QueryBuilderComponent summaryView={true} />
```

---

## Methods

### Rule Management

#### addRules
Adds single or multiple rules.

```tsx
addRules(
  rules: RuleModel[],
  groupID: string
): void
```

**Example:**
```tsx
qryBldrObj.addRules([{
  field: 'Country',
  label: 'Country',
  operator: 'equal',
  type: 'string',
  value: 'USA'
}], 'group0');
```

#### addGroups
Adds single or multiple groups.

```tsx
addGroups(
  groups: RuleModel[],
  groupID: string
): void
```

**Example:**
```tsx
qryBldrObj.addGroups([{
  condition: 'or',
  rules: [{
    field: 'Title',
    label: 'Title',
    operator: 'equal',
    type: 'string',
    value: 'Manager'
  }]
}], 'group0');
```

#### deleteRules
Deletes rule(s) by ID.

```tsx
deleteRules(ruleIdColl: string[]): void
```

**Example:**
```tsx
qryBldrObj.deleteRules(['rule_1', 'rule_2']);
```

#### deleteGroups
Deletes group(s) by ID.

```tsx
deleteGroups(groupIdColl: string[]): void
```

**Example:**
```tsx
qryBldrObj.deleteGroups(['group_1']);
```

#### getRules
Gets current rule collection.

```tsx
getRules(): RuleModel
```

**Example:**
```tsx
const rules = qryBldrObj.getRules();
console.log(rules);
```

#### getRule
Gets a single rule by element or ID.

```tsx
getRule(elem: string | HTMLElement): RuleModel
```

**Example:**
```tsx
const rule = qryBldrObj.getRule('rule_1');
```

#### getGroup
Gets a group by element or ID.

```tsx
getGroup(target: string | HTMLElement): RuleModel
```

**Example:**
```tsx
const group = qryBldrObj.getGroup('group_1');
```

#### setRules
Sets rule collection.

```tsx
setRules(rule: RuleModel): void
```

**Example:**
```tsx
qryBldrObj.setRules({
  condition: 'and',
  rules: [{...}]
});
```

#### reset
Clears all rules.

```tsx
reset(): void
```

**Example:**
```tsx
qryBldrObj.reset();
```

### Clone Operations

#### cloneRule
Clones a rule to a group.

```tsx
cloneRule(
  ruleID: string,
  groupID: string,
  index?: number
): void
```

**Example:**
```tsx
qryBldrObj.cloneRule('rule_1', 'group_0', 0);
```

#### cloneGroup
Clones a group to parent group.

```tsx
cloneGroup(
  groupID: string,
  parentGroupID: string,
  index?: number
): void
```

**Example:**
```tsx
qryBldrObj.cloneGroup('group_1', 'group_0', 0);
```

### Lock Operations

#### lockRule
Locks a rule for read-only access.

```tsx
lockRule(ruleID: string): void
```

**Example:**
```tsx
qryBldrObj.lockRule('rule_1');
```

#### lockGroup
Locks a group for read-only access.

```tsx
lockGroup(groupID: string): void
```

**Example:**
```tsx
qryBldrObj.lockGroup('group_1');
```

### Query Conversion

#### getSqlFromRules
Converts rules to SQL WHERE clause.

```tsx
getSqlFromRules(
  rule?: RuleModel,
  allowEscape?: boolean,
  sqlLocale?: boolean
): string
```

**Example:**
```tsx
const sql = qryBldrObj.getSqlFromRules();
// Output: "(EmployeeID = 1001) AND (Title LIKE '%Manager%')"
```

#### getMongoQuery
Converts rules to Mongo query.

```tsx
getMongoQuery(
  rule?: RuleModel,
  mongoLocale?: boolean
): string
```

**Example:**
```tsx
const mongoQuery = qryBldrObj.getMongoQuery();
// Output: { $and: [ { EmployeeID: 1001 }, { Title: { $regex: 'Manager' } } ] }
```

#### getParameterizedSql
Gets parameterized SQL with placeholders.

```tsx
getParameterizedSql(
  rule?: RuleModel,
  sqlLocale?: boolean
): ParameterizedSql
```

**Returns:**
```tsx
{
  query: string;
  params: any[];
}
```

**Example:**
```tsx
const { query, params } = qryBldrObj.getParameterizedSql();
// query: "(EmployeeID = ?) AND (Title LIKE ?)"
// params: [1001, '%Manager%']
```

#### getParameterizedNamedSql
Gets named parameter SQL.

```tsx
getParameterizedNamedSql(
  rule?: RuleModel,
  sqlLocale?: boolean
): ParameterizedNamedSql
```

**Returns:**
```tsx
{
  query: string;
  params: { [key: string]: any };
}
```

**Example:**
```tsx
const { query, params } = qryBldrObj.getParameterizedNamedSql();
// query: "(EmployeeID = @EmployeeID_1) AND (Title LIKE @Title_1)"
// params: { '@EmployeeID_1': 1001, '@Title_1': '%Manager%' }
```

#### getPredicate
Gets DataManager predicate for filtering.

```tsx
getPredicate(rule: RuleModel): Predicate
```

**Example:**
```tsx
const predicate = qryBldrObj.getPredicate(rule);
const query = new Query().where(predicate);
const results = dataManager.executeQuery(query);
```

### Import/Export

#### setRulesFromSql
Imports rules from SQL query.

```tsx
setRulesFromSql(
  sqlString: string,
  sqlLocale?: boolean
): void
```

**Example:**
```tsx
qryBldrObj.setRulesFromSql(
  "(Country = 'USA') AND (Salary > 50000)"
);
```

#### getRulesFromSql
Gets rules from SQL query.

```tsx
getRulesFromSql(
  sqlString: string,
  sqlLocale?: boolean
): RuleModel
```

**Example:**
```tsx
const rules = qryBldrObj.getRulesFromSql(
  "(Country = 'USA')"
);
```

#### setMongoQuery
Sets rules from Mongo query.

```tsx
setMongoQuery(
  mongoQuery: string,
  mongoLocale?: boolean
): void
```

**Example:**
```tsx
qryBldrObj.setMongoQuery(
  "{ Country: 'USA', Salary: { $gt: 50000 } }"
);
```

#### setParameterizedSql
Sets rules from parameterized SQL.

```tsx
setParameterizedSql(
  sqlQuery: ParameterizedSql
): void
```

#### setParameterizedNamedSql
Sets rules from named parameter SQL.

```tsx
setParameterizedNamedSql(
  sqlQuery: ParameterizedNamedSql
): void
```

### Validation & Data

#### validateFields
Validates all rule conditions.

```tsx
validateFields(): boolean
```

**Example:**
```tsx
const isValid = qryBldrObj.validateFields();
if (isValid) {
  // Process valid rules
}
```

#### getValidRules
Gets valid rule collection (non-empty).

```tsx
getValidRules(currentRule?: RuleModel): RuleModel
```

**Example:**
```tsx
const validRules = qryBldrObj.getValidRules();
```

#### getValues
Gets values for a field.

```tsx
getValues(field: string): object[]
```

**Example:**
```tsx
const countryValues = qryBldrObj.getValues('Country');
```

#### getOperators
Gets operators for field(s).

```tsx
getOperators(): { [key: string]: Object }[]
```

**Example:**
```tsx
const operators = qryBldrObj.getOperators();
```

### Utilities

#### getDataManagerQuery
Gets DataManager query.

```tsx
getDataManagerQuery(rule: RuleModel): Query
```

#### getFilteredRecords
Gets filtered records as promise.

```tsx
getFilteredRecords(): Promise<object> | object
```

#### notifyChange
Notifies component of value changes.

```tsx
notifyChange(
  value: string | number | boolean | Date,
  element: Element,
  type?: string
): void
```

#### destroy
Removes component from DOM.

```tsx
destroy(): void
```

---

## Events

### actionBegin
Triggers when field, operator, or value changes.

```tsx
<QueryBuilderComponent
  actionBegin={(args: ActionEventArgs) => {
    console.log('Action:', args.requestType);
  }}
/>
```

### beforeChange
Triggers before condition, field, operator, value changes.

```tsx
<QueryBuilderComponent
  beforeChange={(args: ChangeEventArgs) => {
    if (args.cancel === true) {
      // Prevent change
      args.cancel = true;
    }
  }}
/>
```

### change
Triggers when condition, field, value, operator changes.

```tsx
<QueryBuilderComponent
  change={(args: ChangeEventArgs) => {
    console.log('Changed rules:', args.rule);
  }}
/>
```

### ruleChange
Triggers when rules change with detailed info.

```tsx
<QueryBuilderComponent
  ruleChange={(args: RuleChangeEventArgs) => {
    console.log('Previous:', args.previousRule);
    console.log('New:', args.rule);
  }}
/>
```

### created
Triggers when component is created.

```tsx
<QueryBuilderComponent
  created={() => {
    console.log('Query Builder created');
  }}
/>
```

### destroyed
Triggers when component is destroyed.

```tsx
<QueryBuilderComponent
  destroyed={() => {
    console.log('Query Builder destroyed');
  }}
/>
```

### dataBound
Triggers when data is bound.

```tsx
<QueryBuilderComponent
  dataBound={() => {
    console.log('Data bound');
  }}
/>
```

### drag
Triggers during rule/group dragging.

```tsx
<QueryBuilderComponent
  drag={(args: DragEventArgs) => {
    console.log('Dragging:', args.rule);
  }}
/>
```

### dragStart
Triggers when drag starts.

```tsx
<QueryBuilderComponent
  dragStart={(args: DragEventArgs) => {
    console.log('Drag started');
  }}
/>
```

### drop
Triggers when rule/group is dropped.

```tsx
<QueryBuilderComponent
  drop={(args: DropEventArgs) => {
    console.log('Dropped at:', args.targetID);
  }}
/>
```

---

## Interfaces and Types

### RuleModel
```tsx
interface RuleModel {
  condition?: string;           // 'and' or 'or'
  rules?: RuleModel[];          // Child rules
  field?: string;               // Column field
  label?: string;               // Display label
  operator?: string;            // Operator type
  type?: string;                // Data type
  value?: any;                  // Filter value
  not?: boolean;                // NOT condition
}
```

### ColumnsModel
```tsx
interface ColumnsModel {
  field: string;                // Data field name
  label?: string;               // Display label
  type?: string;                // Data type
  operators?: any[];            // Available operators
  values?: any[];               // Predefined values
  format?: string;              // Format string
  step?: number;                // Step for numbers
  validation?: any;             // Validation rules
}
```

### ShowButtonsModel
```tsx
interface ShowButtonsModel {
  ruleDelete?: boolean;         // Show rule delete
  groupInsert?: boolean;        // Show add group
  groupDelete?: boolean;        // Show group delete
}
```

### ParameterizedSql
```tsx
interface ParameterizedSql {
  query: string;                // SQL with placeholders
  params: any[];                // Parameter values
}
```

### ParameterizedNamedSql
```tsx
interface ParameterizedNamedSql {
  query: string;                // SQL with named params
  params: { [key: string]: any };  // Named parameters
}
```
