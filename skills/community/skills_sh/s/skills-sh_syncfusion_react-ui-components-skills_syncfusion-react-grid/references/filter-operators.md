# Filter Operators and Conditions

## Table of Contents
- [Filter Operators](#filter-operators)
- [Initial Filters](#initial-filters)
- [Wildcard and LIKE Filters](#wildcard-and-like-filters)
- [Case Sensitivity](#case-sensitivity)
- [Diacritics Filter](#diacritics-filter)

---

## Filter Operators

Grid supports 21+ operators for different data types. Set via `operator` property in `filterSettings.columns` or `filterByColumn()` method.

### Complete Operators Table

| Operator | Type | Example | Data Types |
|----------|------|---------|-----------|
| `startsWith` | String | Field starts with "A" | String |
| `endsWith` | String | Field ends with ".com" | String |
| `contains` | String | Field contains "test" | String |
| `doesnotstartwith` | String | NOT starts with | String |
| `doesnotendwith` | String | NOT ends with | String |
| `doesnotcontain` | String | NOT contains | String |
| `equal` | All | Exactly equals value | String, Number, Boolean, Date |
| `notEqual` | All | Does NOT equal value | String, Number, Boolean, Date |
| `greaterThan` | Number/Date | Value > specified | Number, Date |
| `greaterThanOrEqual` | Number/Date | Value ≥ specified | Number, Date |
| `lessThan` | Number/Date | Value < specified | Number, Date |
| `lessThanOrEqual` | Number/Date | Value ≤ specified | Number, Date |
| `isnull` | All | Value IS null | String, Number, Date |
| `isnotnull` | All | Value IS NOT null | String, Number, Date |
| `isempty` | String | Value IS empty string | String |
| `isnotempty` | String | Value IS NOT empty | String |
| `between` | Number/Date | Within range start-end | Number, Date |
| `in` | All | Matches any in list | String, Number, Date |
| `notin` | All | NOT in list | String, Number, Date |

**Default Operators by Type:**
- String columns: `startswith`
- Numeric columns: `equal`
- Boolean columns: `equal`
- Date columns: `equal`

### Using Filter Operators

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Filter } from '@syncfusion/ej2-react-grids';

// Method 1: Via filterByColumn (programmatic)
const applyFilter = () => {
  grid.filterByColumn('Freight', 'greaterThan', 100);
  grid.filterByColumn('CustomerID', 'startswith', 'VIN');
  grid.filterByColumn('OrderDate', 'between', [new Date(2023, 0, 1), new Date(2023, 11, 31)]);
};

// Method 2: Via filterSettings (initial)
const filterSettings = {
  columns: [
    { field: 'Freight', operator: 'greaterThan', value: 100 },
    { field: 'CustomerID', operator: 'startswith', value: 'VIN', matchCase: false }
  ]
};

<GridComponent dataSource={data} filterSettings={filterSettings} allowFiltering={true}>
  {/* columns */}
</GridComponent>
```

---

## Initial Filters

Apply filters automatically when Grid loads using `filterSettings.columns` array.

### Single Column with Multiple Values (OR logic)

```tsx
const filterSettings = {
  type: 'Excel',
  columns: [
    {
      field: 'CustomerID',
      matchCase: false,
      operator: 'startswith',
      predicate: 'or',
      value: 'VINET'
    },
    {
      field: 'CustomerID',
      matchCase: false,
      operator: 'startswith',
      predicate: 'or',
      value: 'HANAR'
    }
  ]
};

<GridComponent dataSource={data} filterSettings={filterSettings} allowFiltering={true} />
```

Shows only records where CustomerID starts with "VINET" OR "HANAR".

### Multiple Columns (AND logic)

```tsx
const filterSettings = {
  columns: [
    {
      field: 'ShipCity',
      matchCase: false,
      operator: 'startswith',
      predicate: 'and',
      value: 'reims'
    },
    {
      field: 'ShipName',
      matchCase: false,
      operator: 'startswith',
      predicate: 'and',
      value: 'Vins et alcools'
    }
  ]
};

<GridComponent dataSource={data} filterSettings={filterSettings} allowFiltering={true} />
```

Shows only records where ShipCity starts with "reims" AND ShipName starts with "Vins et alcools".

---

## Wildcard and LIKE Filters

### Wildcard Filter (asterisk *)

Pattern matching on string columns using `*` symbol.

| Pattern | Matches |
|---------|---------|
| `a*b` | Starts with "a", ends with "b" |
| `a*` | Starts with "a" |
| `*b` | Ends with "b" |
| `*a*` | Contains "a" anywhere |
| `ab*` | Starts with "ab", followed by anything |

### LIKE Filter (percent %)

Similar to SQL LIKE operator, works in Filter Menu and Filter Bar with `showFilterBarOperator: true`.

| Pattern | Matches |
|---------|---------|
| `%ab%` | Contains "ab" |
| `ab%` | Ends with "ab" |
| `%ab` | Starts with "ab" |

```tsx
const filterSettings = {
  showFilterBarOperator: true,  // Enable operator dropdown in filter bar
  columns: [
    { field: 'CustomerID', operator: 'like', value: '%VIN%' }
  ]
};

<GridComponent dataSource={data} filterSettings={filterSettings} allowFiltering={true} />
```

---

## Case Sensitivity

Control whether filtering considers letter case via `enableCaseSensitivity` property in `filterSettings`.

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  let grid;
  const [caseSensitive, setCaseSensitive] = useState(false);

  const handleToggle = (args) => {
    grid.filterSettings.enableCaseSensitivity = args.checked;
  };

  return (
    <div>
      <label>Enable Case Sensitivity: </label>
      <SwitchComponent change={handleToggle}></SwitchComponent>
      
      <GridComponent 
        ref={(g) => grid = g}
        dataSource={data} 
        allowFiltering={true}
        filterSettings={{ enableCaseSensitivity: caseSensitive }}
      >
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='100' textAlign='Right' />
          <ColumnDirective field='CustomerID' headerText='Customer ID' width='100' />
          <ColumnDirective field='ShipCountry' headerText='Ship Country' width='100' />
        </ColumnsDirective>
        <Inject services={[Filter]} />
      </GridComponent>
    </div>
  );
}
```

---

## Diacritics Filter

Handle accented characters (é, ñ, ü, ç) in filtering. Enable via `ignoreAccent: true` to treat accented and non-accented versions as equivalent.

```tsx
const filterSettings = {
  ignoreAccent: true  // "José" matches "Jose"
};

<GridComponent 
  dataSource={data} 
  allowFiltering={true}
  filterSettings={filterSettings}
>
  <ColumnsDirective>
    <ColumnDirective field='EmployeeID' headerText='Employee ID' width='140' textAlign='Right' />
    <ColumnDirective field='Name' headerText='Name' width='140' />
    <ColumnDirective field='ShipName' headerText='Ship Name' width='170' textAlign='Right' />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</GridComponent>
```

**Use Cases:**
- International names (José, François, Müller)
- Search should match with/without accents
- User enters "Jose" but data has "José"
