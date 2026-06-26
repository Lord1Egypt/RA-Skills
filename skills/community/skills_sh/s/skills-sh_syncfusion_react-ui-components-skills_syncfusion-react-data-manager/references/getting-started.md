# Getting Started with React DataManager

## Installation

Start by installing the Syncfusion DataManager package using npm:

```bash
npm install @syncfusion/ej2-data --save
```

## Dependencies

The DataManager requires the following peer dependencies:

```javascript
|-- @syncfusion/ej2-data
    |-- @syncfusion/ej2-base
    |-- es6-promise (if window.Promise not available)
```

> **Important:** Ensure `window.Promise` is available in your browser environment. For older browsers, you may need to include a Promise polyfill.

## Basic Project Setup

Set up a React application using **create-react-app** (recommended):

```bash
npx create-react-app my-datamanager-app
cd my-datamanager-app
npm install @syncfusion/ej2-data --save
npm start
```

For TypeScript support:

```bash
npx create-react-app my-datamanager-app --template typescript
cd my-datamanager-app
npm install @syncfusion/ej2-data --save
npm start
```

## Importing DataManager

Import the necessary classes from `@syncfusion/ej2-data`:

```tsx
import React from 'react';
import { DataManager, Query, JsonAdaptor } from '@syncfusion/ej2-data';

export default function App() {
  return <div>Ready to use DataManager</div>;
}
```

## First DataManager Instance

Create a DataManager instance with local data:

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, Query, JsonAdaptor } from '@syncfusion/ej2-data';

export default function FirstQuery() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Sample data array
    const dataArray = [
      { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
      { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 },
      { OrderID: 10250, CustomerID: 'HANAR', Freight: 65.83 },
    ];

    // Initialize DataManager with local data
    const dataManager = new DataManager(dataArray);

    // Execute query
    dataManager.executeLocal(new Query().take(2)).then((e) => {
      setData(e.result); // Bind results to state
    });
  }, []);

  return (
    <div>
      <h2>Orders</h2>
      <ul>
        {data.map((item) => (
          <li key={item.OrderID}>{item.CustomerID}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Common Setup Errors & Fixes

**Error: "DataManager is not defined"**
- Solution: Ensure `@syncfusion/ej2-data` is installed: `npm install @syncfusion/ej2-data --save`
- Check import statement: `import { DataManager } from '@syncfusion/ej2-data';`

**Error: "Adaptor is not a function"**
- Solution: Ensure adaptor is instantiated: `new WebApiAdaptor()` (not just `WebApiAdaptor`)

**Error: "Promise is not defined"**
- Solution: Add Promise polyfill for older browsers, or ensure `window.Promise` exists

**Error: CORS errors on remote requests**
- Solution: Set `crossDomain: true` in DataManager configuration

**Error: "executeQuery is not a function"**
- Solution: Use `executeQuery()` for remote, `executeLocal()` for local data
