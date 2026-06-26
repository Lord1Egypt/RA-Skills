# Query Conversion

Learn how to convert Query Builder rules to SQL, Mongo queries, and parameterized queries for backend execution.

## Table of Contents
- [Overview](#overview)
- [SQL Generation](#sql-generation)
- [Mongo Query Conversion](#mongo-query-conversion)
- [Parameterized Queries](#parameterized-queries)
- [Predicate Conversion](#predicate-conversion)
- [Importing from SQL](#importing-from-sql)
- [Localization](#localization)

## Overview

The Query Builder provides multiple methods to convert rules into backend-compatible query formats:

| Method | Output | Use Case |
|--------|--------|----------|
| `getSqlFromRules()` | SQL WHERE clause | SQL databases |
| `getMongoQuery()` | Mongo query object | MongoDB |
| `getParameterizedSql()` | SQL with placeholders | SQL injection prevention |
| `getParameterizedNamedSql()` | SQL with named parameters | Named parameter binding |
| `getPredicate()` | DataManager predicate | Local filtering |

## SQL Generation

### Basic SQL Query

Convert rules to SQL WHERE clause:

```tsx
let qryBldrObj: QueryBuilderComponent;

function generateSQL(): void {
  const sqlQuery = qryBldrObj.getSqlFromRules();
  console.log('SQL Query:', sqlQuery);
}

// Example output:
// (EmployeeID = 1001) AND (Title LIKE '%Manager%')
```

### Complete SQL Example

```tsx
import { QueryBuilderComponent, RuleModel } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';

function App() {
  let qryBldrObj: QueryBuilderComponent;

  const rule: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'EmployeeID',
        label: 'Employee ID',
        operator: 'equal',
        type: 'number',
        value: 1001
      },
      {
        field: 'Title',
        label: 'Title',
        operator: 'contains',
        type: 'string',
        value: 'Manager'
      }
    ]
  };

  function generateSQL(): void {
    const sqlQuery = qryBldrObj.getSqlFromRules();
    console.log('Generated SQL:', sqlQuery);
    // Output: (EmployeeID = 1001) AND (Title LIKE '%Manager%')
    
    // Send to backend
    fetch('/api/query', {
      method: 'POST',
      body: JSON.stringify({ query: sqlQuery })
    });
  }

  return (
    <div>
      <QueryBuilderComponent
        columns={columns}
        rule={rule}
        ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      />
      <button onClick={generateSQL}>Execute Query</button>
    </div>
  );
}

export default App;
```

### SQL Operators Mapping

| Operator | SQL Output |
|----------|-----------|
| `equal` | `= value` |
| `notequal` | `!= value` |
| `contains` | `LIKE '%value%'` |
| `startswith` | `LIKE 'value%'` |
| `endswith` | `LIKE '%value'` |
| `greaterthan` | `> value` |
| `lessthan` | `< value` |
| `greaterthanorequal` | `>= value` |
| `lessthanorequal` | `<= value` |
| `between` | `BETWEEN value1 AND value2` |
| `in` | `IN (value1, value2)` |

### Escaping Special Characters

Exclude escape characters from SQL:

```tsx
function generateSQL(): void {
  const sqlQuery = qryBldrObj.getSqlFromRules(undefined, true);
  console.log('SQL without escape:', sqlQuery);
  // Special characters like ' and " are not escaped
}
```

## Mongo Query Conversion

### Generate Mongo Query

Convert rules to MongoDB query format:

```tsx
let qryBldrObj: QueryBuilderComponent;

function generateMongoQuery(): void {
  const mongoQuery = qryBldrObj.getMongoQuery();
  console.log('Mongo Query:', mongoQuery);
}

// Example output:
// { $and: [ { EmployeeID: 1001 }, { Title: { $regex: 'Manager' } } ] }
```

### Complete Mongo Example

```tsx
function App() {
  let qryBldrObj: QueryBuilderComponent;

  const rule: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'Country',
        label: 'Country',
        operator: 'equal',
        type: 'string',
        value: 'USA'
      },
      {
        field: 'Salary',
        label: 'Salary',
        operator: 'greaterthan',
        type: 'number',
        value: 50000
      }
    ]
  };

  function getMongoFilter(): void {
    const mongoQuery = qryBldrObj.getMongoQuery();
    console.log('Mongo Query:', mongoQuery);
    // Output: { $and: [ { Country: 'USA' }, { Salary: { $gt: 50000 } } ] }
    
    // Send to backend MongoDB API
    fetch('/api/mongo-query', {
      method: 'POST',
      body: JSON.stringify(mongoQuery)
    });
  }

  return (
    <div>
      <QueryBuilderComponent
        columns={columns}
        rule={rule}
        ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      />
      <button onClick={getMongoFilter}>Get Mongo Query</button>
    </div>
  );
}

export default App;
```

### Mongo Operators Mapping

| Operator | Mongo Output |
|----------|------------|
| `equal` | `field: value` |
| `notequal` | `{ $ne: value }` |
| `contains` | `{ $regex: value }` |
| `greaterthan` | `{ $gt: value }` |
| `lessthan` | `{ $lt: value }` |
| `between` | `{ $gte: value1, $lte: value2 }` |
| `in` | `{ $in: [values] }` |
| `notin` | `{ $nin: [values] }` |

## Parameterized Queries

### Parameter SQL (Positional)

Generate SQL with placeholders to prevent SQL injection:

```tsx
function getParameterizedQuery(): void {
  const paramSql = qryBldrObj.getParameterizedSql();
  console.log('Query:', paramSql.query);
  console.log('Parameters:', paramSql.params);
}

// Example output:
// query: "(EmployeeID = ?) AND (Title LIKE ?)"
// params: [1001, '%Manager%']
```

### Complete Parameterized Example

```tsx
function App() {
  let qryBldrObj: QueryBuilderComponent;

  function getSecureQuery(): void {
    const { query, params } = qryBldrObj.getParameterizedSql();
    
    // Send to backend for parameterized query execution
    fetch('/api/execute-query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, params })
    })
    .then(res => res.json())
    .then(data => console.log('Results:', data));
  }

  return (
    <div>
      <QueryBuilderComponent
        columns={columns}
        ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      />
      <button onClick={getSecureQuery}>Execute Secure Query</button>
    </div>
  );
}
```

### Named Parameter SQL

Generate SQL with named parameters:

```tsx
function getNamedParameterQuery(): void {
  const paramSql = qryBldrObj.getParameterizedNamedSql();
  console.log('Query:', paramSql.query);
  console.log('Parameters:', paramSql.params);
}

// Example output:
// query: "(EmployeeID = @EmployeeID_1) AND (Title LIKE @Title_1)"
// params: { '@EmployeeID_1': 1001, '@Title_1': '%Manager%' }
```

### Backend Execution (C# Example)

```csharp
[HttpPost]
public IActionResult ExecuteQuery([FromBody] QueryRequest request)
{
    using (var connection = new SqlConnection(connectionString))
    {
        var command = new SqlCommand(request.Query, connection);
        
        // Add named parameters
        foreach (var param in request.Params)
        {
            command.Parameters.AddWithValue(param.Key, param.Value);
        }
        
        connection.Open();
        var reader = command.ExecuteReader();
        // Process results
    }
}
```

## Predicate Conversion

### Getting DataManager Predicate

Convert rules to a predicate for DataManager filtering:

```tsx
import { Query } from '@syncfusion/ej2-data';

let qryBldrObj: QueryBuilderComponent;

function filterWithPredicate(): void {
  const predicate = qryBldrObj.getPredicate(qryBldrObj.rule);
  const query = new Query().where(predicate);
  
  // Apply to DataManager
  const dataManager = new DataManager(employeeData);
  const filteredData = dataManager.executeQuery(query);
}
```

### Filtering Local Data

```tsx
function App() {
  let qryBldrObj: QueryBuilderComponent;
  const dataManager = new DataManager(employeeData);

  const rule: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'Country',
        label: 'Country',
        operator: 'equal',
        type: 'string',
        value: 'USA'
      }
    ]
  };

  function applyFilter(): void {
    const predicate = qryBldrObj.getPredicate(rule);
    const filteredData = dataManager.executeQuery(new Query().where(predicate));
    console.log('Filtered:', filteredData);
  }

  return (
    <div>
      <QueryBuilderComponent
        dataSource={employeeData}
        columns={columns}
        rule={rule}
        ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      />
      <button onClick={applyFilter}>Filter Data</button>
    </div>
  );
}
```

## Importing from SQL

### Parse SQL to Rules

Convert SQL WHERE clause to Query Builder rules:

```tsx
function importFromSQL(): void {
  const sqlString = "EmployeeID = 1001 AND Title LIKE '%Manager%'";
  qryBldrObj.setRulesFromSql(sqlString);
}
```

### Complete Import Example

```tsx
function App() {
  let qryBldrObj: QueryBuilderComponent;

  const savedSqlQuery = "(Country = 'USA') AND (Salary > 50000)";

  function loadSavedQuery(): void {
    qryBldrObj.setRulesFromSql(savedSqlQuery);
  }

  return (
    <div>
      <button onClick={loadSavedQuery}>Load Saved Query</button>
      <QueryBuilderComponent
        columns={columns}
        ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      />
    </div>
  );
}
```

### Get Rules from SQL

```tsx
function parseSQL(): void {
  const sqlString = "EmployeeID = 1001 AND Country = 'USA'";
  const rules = qryBldrObj.getRulesFromSql(sqlString);
  console.log('Parsed Rules:', rules);
}
```

## Localization

### SQL Localization

Generate localized SQL queries:

```tsx
function getLocalizedSQL(): void {
  const sqlQuery = qryBldrObj.getSqlFromRules(undefined, false, true);
  // true = enable SQL localization
}
```

### Mongo Localization

```tsx
function getLocalizedMongo(): void {
  const mongoQuery = qryBldrObj.getMongoQuery(undefined, true);
  // true = enable Mongo localization
}
```

### Parameterized SQL Localization

```tsx
function getLocalizedParameterizedSQL(): void {
  const { query, params } = qryBldrObj.getParameterizedSql(undefined, true);
  // true = enable localization
}
```

## Complete Workflow Example

```tsx
import { ColumnsModel, QueryBuilderComponent, RuleModel } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';

function App() {
  let qryBldrObj: QueryBuilderComponent;

  const columns: ColumnsModel[] = [
    { field: 'EmployeeID', label: 'Employee ID', type: 'number' },
    { field: 'Country', label: 'Country', type: 'string' },
    { field: 'Salary', label: 'Salary', type: 'number' }
  ];

  function exportToSQL(): void {
    const sql = qryBldrObj.getSqlFromRules();
    console.log('SQL:', sql);
  }

  function exportToMongo(): void {
    const mongo = qryBldrObj.getMongoQuery();
    console.log('Mongo:', mongo);
  }

  function exportParameterized(): void {
    const { query, params } = qryBldrObj.getParameterizedSql();
    console.log('Query:', query);
    console.log('Params:', params);
  }

  function importFromSQL(): void {
    const sql = "(Country = 'USA') AND (Salary > 50000)";
    qryBldrObj.setRulesFromSql(sql);
  }

  return (
    <div>
      <QueryBuilderComponent
        width="100%"
        columns={columns}
        ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      />
      <div>
        <button onClick={exportToSQL}>Export as SQL</button>
        <button onClick={exportToMongo}>Export as Mongo</button>
        <button onClick={exportParameterized}>Export Parameterized</button>
        <button onClick={importFromSQL}>Import from SQL</button>
      </div>
    </div>
  );
}

export default App;
```

This example demonstrates:
- Multiple export formats
- Parameterized query generation
- SQL import capability
- Complete workflow integration
