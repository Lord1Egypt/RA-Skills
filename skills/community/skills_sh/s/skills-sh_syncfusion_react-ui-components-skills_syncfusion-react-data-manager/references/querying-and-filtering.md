# Querying & Filtering in React DataManager

## Table of Contents
- [Query Class Fundamentals](#query-class-fundamentals)
- [Specifying Resource with from()](#specifying-resource-with-from)
- [Filtering with where()](#filtering-with-where)
- [Predicate Logic](#predicate-logic)
- [Sorting](#sorting)
- [Pagination with take() and skip()](#pagination-with-take-and-skip)
- [Field Projection with select()](#field-projection-with-select)
- [Related Data with expand()](#related-data-with-expand)
- [Grouping Data](#grouping-data)
- [Chaining Queries](#chaining-queries)
- [Complex Filter Scenarios](#complex-filter-scenarios)

---

## Query Class Fundamentals

The `Query` class builds structured database-like queries for both local and remote data sources. Chain methods to compose complex data operations:

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, Query, JsonAdaptor } from '@syncfusion/ej2-data';

export default function QueryExample() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    const data = [
      { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38, OrderDate: new Date(1996, 6, 4) },
      { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61, OrderDate: new Date(1996, 6, 5) },
      { OrderID: 10250, CustomerID: 'HANAR', Freight: 65.83, OrderDate: new Date(1996, 6, 8) },
    ];

    // Create query: Filter → Sort → Paginate
    const query = new Query()
      .where('Freight', 'greaterthan', 30)
      .sortBy('OrderDate')
      .take(5);

    const dm = new DataManager(data);
    dm.executeLocal(query).then((e) => {
      setResults(e.result);
    });
  }, []);

  return <pre>{JSON.stringify(results, null, 2)}</pre>;
}
```

**Key points:**
- Query methods return the Query instance, enabling chaining
- Use `executeLocal()` for local data or `executeQuery()` for remote
- Results come in `e.result` from the Promise

---

## Specifying Resource with from()

Identify which data source or table to query using `from()`:

```tsx
// For OData services with multiple entities
const query = new Query()
  .from('Orders') // Entity name in OData service
  .take(10);

// For remote APIs, from() is optional - url defines the resource
const dm = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

// From is primarily used with OData
const odataQuery = new Query()
  .from('Products')
  .where('Price', 'lessthan', 100);
```

---

## Filtering with where()

Create filter conditions to retrieve matching records:

```tsx
// Simple condition
new Query().where('CustomerID', 'equal', 'VINET')

// Comparison operators
new Query()
  .where('Freight', 'greaterthan', 100)      // >
  .where('Freight', 'lessthan', 500)         // <
  .where('Freight', 'greaterthanorequal', 50) // >=
  .where('Freight', 'lessthanorequal', 200)  // <=
  .where('OrderID', 'notequal', 10248)       // !=

// String operations
new Query()
  .where('CustomerID', 'startswith', 'V')   // Starts with
  .where('CustomerID', 'endswith', 'T')     // Ends with
  .where('CustomerID', 'contains', 'VI')    // Contains
```

### Multiple Filters (AND Logic)

Chain `where()` calls for AND conditions:

```tsx
const query = new Query()
  .where('OrderDate', 'greaterthan', new Date(1996, 5, 1))
  .where('Freight', 'lessthan', 100)
  .where('CustomerID', 'equal', 'VINET');

// Returns records WHERE OrderDate > June 1, 1996 AND Freight < 100 AND CustomerID = 'VINET'
```

---

## Predicate Logic

Use `Predicate` class for complex OR/AND combinations:

```tsx
import { Predicate } from '@syncfusion/ej2-data';

// OR condition
const predicate = new Predicate('CustomerID', 'equal', 'VINET')
  .or('CustomerID', 'equal', 'TOMSP');

const query = new Query().where(predicate);
// Returns: CustomerID = 'VINET' OR CustomerID = 'TOMSP'

// Complex: (A OR B) AND C
const predicate2 = new Predicate('CustomerID', 'equal', 'VINET')
  .or('CustomerID', 'equal', 'TOMSP')
  .and('Freight', 'greaterthan', 50);

const query2 = new Query().where(predicate2);
// Returns: (CustomerID = 'VINET' OR CustomerID = 'TOMSP') AND Freight > 50
```

---

## Sorting

Arrange records in ascending or descending order:

```tsx
// Ascending (default)
new Query().sortBy('OrderDate')

// Descending
new Query().sortByDesc('Freight')

// Multiple sorts
new Query()
  .sortBy('CustomerID')        // First by Customer
  .sortByDesc('OrderDate');    // Then by Date descending

// Dynamic sort
new Query().sortBy('Freight', true) // true = descending
```

---

## Pagination with take() and skip()

Limit results and implement paging:

```tsx
// Get first 10 records
new Query().take(10)

// Skip first 20, get next 10 (page 3, page size 10)
new Query().skip(20).take(10)

// Page calculation
const pageSize = 10;
const pageNumber = 2; // 0-based
const skip = pageNumber * pageSize; // 10
new Query().skip(skip).take(pageSize)

// For grid - Grid.pageSettings manages this, but DataManager handles raw API
const query = new Query()
  .skip((currentPage - 1) * pageSize)
  .take(pageSize);
```

---

## Field Projection with select()

Retrieve only specific fields, reducing payload size:

```tsx
// Select specific columns
new Query().select(['OrderID', 'CustomerID', 'Freight'])

// From remote API - sends to server
const query = new Query()
  .select(['OrderID', 'CustomerID', 'Freight'])
  .take(100);

const dm = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

dm.executeQuery(query).then((e) => {
  // e.result only has OrderID, CustomerID, Freight
  console.log(e.result[0]); // { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 }
});

// Local data - still filters properties
const localDm = new DataManager(dataArray);
localDm.executeLocal(query).then((e) => {
  console.log(e.result[0]); // Only selected fields returned
});
```

---

## Related Data with expand()

Eagerly load related objects instead of separate queries:

```tsx
// Without expand - Customer data requires separate fetch
const query1 = new Query().take(10);
// Returns: { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 }

// With expand - Related data included
const query2 = new Query()
  .expand('Customer') // Fetch Customer details from related table
  .take(10);

const dm = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor()
});

dm.executeQuery(query2).then((e) => {
  // Returns:
  // {
  //   OrderID: 10248,
  //   CustomerID: 'VINET',
  //   Freight: 32.38,
  //   Customer: { CustomerID: 'VINET', CompanyName: 'Vins et alcools Chevalier', ... }
  // }
  console.log(e.result[0].Customer.CompanyName);
});

// Multiple related entities
const query3 = new Query()
  .expand('Customer')
  .expand('Employee')
  .take(10);
```

---

## Grouping Data

Organize records by field values:

```tsx
// Group by CustomerID
const query = new Query()
  .group('CustomerID')
  .take(10);

const dm = new DataManager(orders);
dm.executeLocal(query).then((e) => {
  // Returns grouped structure:
  // [
  //   { key: 'VINET', items: [{...}, {...}], count: 2 },
  //   { key: 'TOMSP', items: [{...}], count: 1 }
  // ]
  console.log(e.result);
});

// Group by multiple fields
const query2 = new Query()
  .group('CustomerID')
  .group('OrderDate');

// Group with aggregation
import { Aggregates } from '@syncfusion/ej2-data';
const query3 = new Query()
  .group('CustomerID')
  .aggregate('sum', 'Freight');
```

---

## Chaining Queries

Combine multiple operations in a single query:

```tsx
const complexQuery = new Query()
  // Filter
  .where('OrderDate', 'greaterthanorequal', new Date(1996, 0, 1))
  .where('Freight', 'lessthan', 500)
  
  // Select fields
  .select(['OrderID', 'CustomerID', 'Freight', 'OrderDate'])
  
  // Sort
  .sortByDesc('Freight')
  
  // Paginate
  .skip(0)
  .take(20);

const dm = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

dm.executeQuery(complexQuery).then((e) => {
  console.log(`Found ${e.count} total records, showing ${e.result.length}`);
  console.log(e.result);
});
```

**Query Execution Order:**
1. Filter (where)
2. Select fields (select)
3. Sort (sortBy)
4. Group (group)
5. Paginate (skip/take)
6. Expand (expand)

---

## Complex Filter Scenarios

### Scenario 1: Date Range Filter

```tsx
const startDate = new Date(1996, 6, 1);  // July 1, 1996
const endDate = new Date(1996, 6, 31);   // July 31, 1996

const query = new Query()
  .where('OrderDate', 'greaterthanorequal', startDate)
  .where('OrderDate', 'lessthanorequal', endDate)
  .sortByDesc('OrderDate')
  .take(50);
```

### Scenario 2: OR with Multiple Categories

```tsx
import { Predicate } from '@syncfusion/ej2-data';

const statusFilter = new Predicate('Status', 'equal', 'Shipped')
  .or('Status', 'equal', 'Processing')
  .or('Status', 'equal', 'Pending');

const query = new Query()
  .where(statusFilter)
  .take(100);
```

### Scenario 3: Combine AND & OR

```tsx
import { Predicate } from '@syncfusion/ej2-data';

// (CustomerID = 'VINET' OR CustomerID = 'TOMSP') AND Freight >= 50
const predicate = new Predicate('CustomerID', 'equal', 'VINET')
  .or('CustomerID', 'equal', 'TOMSP')
  .and('Freight', 'greaterthanorequal', 50);

const query = new Query()
  .where(predicate)
  .sortBy('OrderDate');
```

### Scenario 4: Search with Contains

```tsx
const searchTerm = 'Synchron';

const query = new Query()
  .where('CompanyName', 'contains', searchTerm)
  .orWhere('ContactName', 'contains', searchTerm)
  .take(20);

// This searches either CompanyName or ContactName containing the term
```

---

## Performance Tips

- **Use select()** on remote queries to reduce payload
- **Use take()** to limit results instead of fetching all
- **Use expand()** instead of separate queries for related data
- **Filter on server** with where() for large datasets
- **Cache results** with DataManager.enableCache
