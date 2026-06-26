# Data Binding in PivotView

## ⚠️ SECURITY NOTICE

**CRITICAL**: This documentation contains examples for connecting to remote data sources. **Always use trusted, authenticated data sources only.** Never bind to untrusted URLs, user-provided endpoints, or public APIs without proper validation and security controls. See the [Security Best Practices](#security-best-practices) section below.

## Table of Contents
- [Security Best Practices](#security-best-practices)
- [JSON Data Binding](#json-data-binding)
- [CSV Data Binding](#csv-data-binding)
- [Remote Data Binding](#remote-data-binding)
- [Field Mapping](#field-mapping)

---

## Security Best Practices

### Critical Security Guidelines

When implementing data binding for pivot tables, follow these essential security practices:

#### 1. **Use Trusted Data Sources Only**

✅ **RECOMMENDED**: Local in-memory data
```typescript
// Safe: Local data array
const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: localDataArray as IDataSet[],
    rows: [{ name: 'Country' }],
    values: [{ name: 'Amount', type: 'Sum' }]
};
```

❌ **AVOID**: Untrusted remote endpoints
```typescript
// UNSAFE: Never use arbitrary or user-provided URLs
url: userProvidedUrl  // Security risk!
```

#### 2. **Implement Authentication for Remote Sources**

If you must use remote data, always use authenticated endpoints:

```typescript
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

// Use authenticated endpoints with proper headers
const dataSource = new DataManager({
    url: process.env.REACT_APP_API_ENDPOINT,  // Use environment variables
    adaptor: new WebApiAdaptor(),
    headers: [
        { 'Authorization': `Bearer ${getAuthToken()}` },
        { 'X-API-Key': process.env.REACT_APP_API_KEY }
    ]
});
```

#### 3. **Validate and Sanitize Data**

Always validate data received from external sources:

```typescript
const fetchData = async () => {
    const response = await fetch(trustedEndpoint, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    
    // Validate data structure
    if (!isValidDataStructure(data)) {
        console.error('Invalid data structure received');
        return;
    }
    
    // Sanitize data before binding
    const sanitizedData = sanitizeData(data);
    setDataSourceSettings({ dataSource: sanitizedData });
};
```

#### 4. **Use Environment Variables**

Store API endpoints in environment files, never hardcode:

```bash
# .env
REACT_APP_API_ENDPOINT=https://your-trusted-api.com/data
REACT_APP_API_KEY=your-api-key
```

```typescript
// Use in component
const apiEndpoint = process.env.REACT_APP_API_ENDPOINT;
```

### Security Risks to Avoid

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Indirect Prompt Injection** | Malicious data manipulating AI behavior | Validate and sanitize all external data |
| **Data Exfiltration** | Unauthorized access to sensitive data | Use authentication and authorization |
| **SSRF Attacks** | Server-side request forgery via URLs | Whitelist allowed endpoints |
| **XSS via Data** | Malicious scripts in data fields | Sanitize and escape all data |
| **Credential Exposure** | API keys or tokens in code | Use environment variables |

---

## JSON Data Binding

The Pivot Table supports JSON data binding. JSON is the default data type, so you can bind JSON data without explicitly setting the `type` property in `dataSourceSettings`.

### Binding JSON Data Locally

You can bind local JSON data by assigning a local variable to the `dataSource` property in `dataSourceSettings`:

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

### JSON Data with DataManager

Using DataManager with JsonAdaptor is optional for local JSON but provides flexibility and consistency:

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { DataManager, JsonAdaptor } from '@syncfusion/ej2-data';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSource: DataManager = new DataManager({
    json: pivotData,
    adaptor: new JsonAdaptor()
  });

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: dataSource,
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

### Loading JSON from File

Load JSON data from a local *.json file using the Uploader component:

```typescript
import { Uploader } from '@syncfusion/ej2-inputs';
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';

function App() {
  const [dataSourceSettings, setDataSourceSettings] = React.useState({
    dataSource: [] as IDataSet[],
    columns: [{ name: 'Year' }],
    rows: [{ name: 'Country' }],
    values: [{ name: 'Amount' }]
  } as DataSourceSettingsModel);

  const handleFileChange = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const result = JSON.parse(e.target?.result as string);
          setDataSourceSettings(prev => ({
            ...prev,
            dataSource: result as IDataSet[]
          }));
        } catch (error) {
          console.error('Invalid JSON file');
        }
      };
      reader.readAsText(input.files[0]);
    }
  };

  return (
    <div>
      <input type="file" accept=".json" id="fileupload" onChange={handleFileChange} />
      <PivotViewComponent
        id='PivotView'
        height={350}
        dataSourceSettings={dataSourceSettings}
      />
    </div>
  );
}

export default App;
```

### JSON Data Structure Guidelines

Ensure your JSON data follows the proper structure for optimal Pivot Table functionality:

* **Flat object array**: Each element represents one record (no nested objects)
* **Field naming**: Field names must exactly match those used in `rows`, `columns`, `values`, and `filters` configuration
* **Type consistency**: 
  * Numeric fields should be numbers, not strings
  * Dates should be ISO format strings (YYYY-MM-DD)
  * Field values should not have leading/trailing whitespace
* **Required fields**: Include all fields referenced in the pivot configuration

```typescript
// ✅ Correct JSON format
const correctData = [
  { 
    Country: 'USA',            // string field for grouping
    Year: 2020,                // number for sorting
    Sales: 5000,               // number for aggregation
    Date: '2020-01-15'         // ISO date string
  }
];

// ❌ Avoid: nested objects and string numbers
const incorrectData = [
  {
    Location: { Country: 'USA' },  // ← Nested objects won't work
    Year: '2020',                   // ← String number causes issues
    Sales: '5000'                   // ← String number breaks aggregation
  }
];
```

### Binding JSON from Remote URL

To bind remote JSON data, set the endpoint URL in the `url` property of `dataSourceSettings`:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  url: 'https://cdn.syncfusion.com/data/sales-analysis.json',
  expandAll: false,
  rows: [
    { name: 'EnerType', caption: 'Energy Type' }
  ],
  columns: [
    { name: 'EneSource', caption: 'Energy Source' }
  ],
  values: [
    { name: 'PowUnits', caption: 'Units (GWh)' },
    { name: 'ProCost', caption: 'Cost (MM)' }
  ]
};
```

## CSV Data Binding

CSV (Comma-Separated Values) format is compact and reduces bandwidth usage. To use CSV, set the `type` property to `CSV` in `dataSourceSettings`.

> CSV format uses approximately half the size of JSON, reducing bandwidth when transferring data.

### Binding Local CSV Data

Convert CSV data into a string array and assign it to the `dataSource` property:

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { isNullOrUndefined } from '@syncfusion/ej2-base';
import * as React from 'react';
import { csvdata } from './datasource';

function App() {
  const getCSVData = () => {
    const dataSource = [];
    const jsonObject = csvdata.split(/\r?\n|\r/);
    for (let i = 0; i < jsonObject.length; i++) {
      if (!isNullOrUndefined(jsonObject[i]) && jsonObject[i] !== '') {
        dataSource.push(jsonObject[i].split(','));
      }
    }
    return dataSource;
  };

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: getCSVData(),
    type: 'CSV',
    expandAll: false,
    columns: [{ name: 'Item Type' }, { name: 'Sales Channel' }],
    filters: [],
    formatSettings: [{ name: 'Total Cost', format: 'C0' }, { name: 'Total Revenue', format: 'C0' }],
    rows: [{ name: 'Region' }, { name: 'Country' }],
    values: [{ name: 'Total Cost' }, { name: 'Total Revenue' }]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

### Loading CSV from File

Load CSV data from a local *.csv file:

```typescript
import { Uploader } from '@syncfusion/ej2-inputs';
import { PivotViewComponent, FieldList, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';

function App() {
  const pivotRef = React.useRef<PivotViewComponent>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);

  const ondataBound = () => {
    if (inputRef.current) {
      const uploader = new Uploader({});
      const input = document.querySelector('input[type="file"]') as HTMLInputElement;
      input?.addEventListener('change', loadCSV);
    }
  };

  const loadCSV = () => {
    const reader = new FileReader();
    const input = inputRef.current;
    
    reader.onload = function () {
      const result: string[][] = [];
      const readerResult: string[] = (reader.result as string).split(/\r?\n|\r/);
      
      result.push(readerResult[0].split(',').map(e => e.replace(/ /g, '').replace(/^\"(.+)\"$/, "$1")));
      
      for (let i = 1; i < readerResult.length; i++) {
        if (readerResult[i] !== '') {
          result.push(readerResult[i].split(','));
        }
      }

      if (pivotRef.current) {
        pivotRef.current.dataSourceSettings = {
          dataSource: result,
          type: 'CSV'
        };
      }
    };
    
    if (input?.files?.[0]) {
      reader.readAsText(input.files[0]);
      input.value = '';
    }
  };

  return (
    <div>
      <input type="file" ref={inputRef} id="fileupload" />
      <PivotViewComponent
        ref={pivotRef}
        id='PivotView'
        height={350}
        showFieldList={true}
        dataBound={ondataBound}
      >
        <Inject services={[FieldList]} />
      </PivotViewComponent>
    </div>
  );
}

export default App;
```

### Remote CSV Data Binding

To bind remote CSV data, set the endpoint URL in the `url` property with `type: 'CSV'`:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  url: 'https://bi.syncfusion.com/productservice/api/sales',
  type: 'CSV',
  expandAll: false,
  enableSorting: true,
  formatSettings: [{ name: 'Total Cost', format: 'C0' }, { name: 'Total Revenue', format: 'C0' }],
  rows: [
    { name: 'Region' },
    { name: 'Country' }
  ],
  columns: [
    { name: 'Item Type' },
    { name: 'Sales Channel' }
  ],
  values: [
    { name: 'Total Cost' },
    { name: 'Total Revenue' }
  ]
};
```

## Remote Data Binding

⚠️ **SECURITY CRITICAL**: Remote data binding should only be used with trusted, authenticated services under your control. All examples below assume you are connecting to **your own authenticated backend services**.

Remote data binding allows you to connect the Pivot Table to data sources hosted on remote servers through web services, databases, and other external sources.

### OData Service Binding

⚠️ **Use only with trusted OData services that you control and authenticate.**

OData (Open Data Protocol) provides a standard way to create and consume data APIs. Use DataManager with ODataAdaptor for OData v3:

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { DataManager, ODataAdaptor } from '@syncfusion/ej2-data';
import * as React from 'react';

function App() {
  // ⚠️ SECURITY: Only connect to your own authenticated OData services
  // Use environment variables for endpoints
  const dataSource: DataManager = new DataManager({
    url: process.env.REACT_APP_ODATA_ENDPOINT,  // Use environment config
    adaptor: new ODataAdaptor(),
    headers: [
      { 'Authorization': `Bearer ${getAuthToken()}` }
    ],
    crossDomain: true
  });

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: dataSource,
    expandAll: true,
    filters: [],
    columns: [{ name: 'OrderDate' }, { name: 'ShipCity' }],
    rows: [{ name: 'OrderID' }, { name: 'CustomerID' }],
    values: [{ name: 'Freight' }]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

function getAuthToken(): string {
  return localStorage.getItem('authToken') || '';
}

export default App;
```

### OData V4 Service Binding

OData V4 provides enhanced query capabilities and improved performance. Use ODataV4Adaptor:

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';
import * as React from 'react';

function App() {
  const dataSource: DataManager = new DataManager({
    url: 'https://services.odata.org/V4/Northwind/Northwind.svc/Orders/?$top=7',
    adaptor: new ODataV4Adaptor(),
    crossDomain: true
  });

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: dataSource,
    expandAll: true,
    filters: [],
    columns: [{ name: 'OrderDate' }, { name: 'ShipCity' }],
    rows: [{ name: 'OrderID' }, { name: 'CustomerID' }],
    values: [{ name: 'Freight' }]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

### Web API Binding

Connect the Pivot Table to RESTful web services using WebApiAdaptor:

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';
import * as React from 'react';

function App() {
  const dataSource: DataManager = new DataManager({
    url: 'https://bi.syncfusion.com/northwindservice/api/orders',
    adaptor: new WebApiAdaptor(),
    crossDomain: true
  });

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: dataSource,
    expandAll: true,
    filters: [],
    columns: [{ name: 'ProductName', caption: 'Product Name' }],
    rows: [{ name: 'ShipCountry', caption: 'Ship Country' }, { name: 'ShipCity', caption: 'Ship City' }],
    formatSettings: [{ name: 'UnitPrice', format: 'C0' }],
    values: [{ name: 'Quantity' }, { name: 'UnitPrice', caption: 'Unit Price' }]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

### Querying Data with DataManager

Customize DataManager behavior using the `defaultQuery` property to apply filtering, sorting, and paging:

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import * as React from 'react';

function App() {
  const dataSource: DataManager = new DataManager({
    url: 'https://services.odata.org/V4/Northwind/Northwind.svc/Orders',
    adaptor: new ODataV4Adaptor(),
    crossDomain: true
  });

  // Apply query to limit results to 10 records
  dataSource.defaultQuery = new Query().take(10);

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: dataSource,
    expandAll: false,
    columns: [{ name: 'CustomerID', caption: 'Customer ID' }],
    rows: [{ name: 'ShipCountry', caption: 'Ship Country' }, { name: 'ShipCity', caption: 'Ship City' }],
    values: [{ name: 'Freight' }]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

### Choosing Between Data Binding Approaches

| Aspect | Local JSON | CSV | Remote (OData/API) |
|--------|-----------|-----|-------------------|
| **Dataset Size** | < 100K records | < 100K records | 100K+ records |
| **Performance** | Fast client-side | Fast client-side | Server-processed |
| **Bandwidth** | All data downloaded | All data downloaded | Only required data |
| **Use Case** | Small reports, demos | Spreadsheet imports | Enterprise dashboards |
| **Real-time** | Manual refresh | Manual refresh | Can be live |

> **Recommendation**: For large datasets (> 50K records), use remote binding with server-side processing.

## Field Mapping

Field mapping allows you to customize how fields appear and behave in the Pivot Table using the `fieldMapping` property without changing the original data source.

### Field Mapping Configuration

Available options for field mapping:

* **name**: The actual field name in the data source
* **caption**: Display name in the Pivot Table UI

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    rows: [
      { 
        name: 'Country',
        caption: 'Customer Country'  // ← Display name in UI
      }
    ],
    columns: [
      { 
        name: 'Year',
        caption: 'Fiscal Year'
      }
    ],
    values: [
      { 
        name: 'Amount',
        caption: 'Total Sales Amount'
      }
    ]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

### Best Practices for Data Binding

1. **For local data**: Use direct assignment or DataManager with JsonAdaptor
2. **For large datasets**: Use remote binding with server-side processing
3. **For CSV imports**: Convert to proper JSON structure before binding
4. **For real-time data**: Configure OData/Web API with automatic refresh intervals
5. **Field naming**: Keep field names consistent across data source and configuration
6. **Data types**: Ensure proper data types in source for accurate aggregations

## Remote Data Binding

### Binding JSON from Remote URL

To bind remote JSON data, set the endpoint URL in the `url` property of `dataSourceSettings`. The URL can point to:
- Direct downloadable JSON files (*.json)
- Web service endpoints (API/REST endpoints)

```typescript
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';

function PivotWithRemoteData() {
  const dataSourceSettings: DataSourceSettingsModel = {
    url: 'https://cdn.syncfusion.com/data/sales-analysis.json',
    expandAll: false,
    rows: [
      { name: 'EnerType', caption: 'Energy Type' }
    ],
    columns: [
      { name: 'EneSource', caption: 'Energy Source' }
    ],
    values: [
      { name: 'PowUnits', caption: 'Units (GWh)' },
      { name: 'ProCost', caption: 'Cost (MM)' }
    ]
  };

  return (
    <PivotViewComponent
      id="pivot"
      dataSourceSettings={dataSourceSettings}
      height={400}
    />
  );
}

export default PivotWithRemoteData;
```

### Using DataManager for Remote Sources

DataManager simplifies remote data binding with built-in HTTP adaptor:

```typescript
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import * as React from 'react';

function PivotWithDataManagerURL() {
  const dataManager = new DataManager({
    url: 'https://api.example.com/pivot-data',
    adaptor: new UrlAdaptor()
  });

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: dataManager,
    rows: [{ name: 'Category' }],
    columns: [{ name: 'Year' }],
    values: [{ name: 'Revenue', type: 'Sum' }]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      height={400}
    />
  );
}

export default PivotWithDataManagerURL;
```

### Choosing Between Local and Remote Data

| Aspect | Local JSON | Remote Data |
|--------|-----------|-------------|
| **Dataset Size** | < 100K records recommended | 100K+ records |
| **Performance** | Fast client-side processing | Server processes data |
| **Bandwidth** | Must download all data | Only required data sent |
| **Use Case** | Small reports, demos | Enterprise, large dashboards |
| **Data Updates** | Manual refresh needed | Real-time capable |

**Recommendation**: For large datasets (> 50K records), use remote binding or server-side pivot engine

### Using DataManager with HTTP Endpoint

For large datasets or server-side processing, use DataManager with WebApiAdaptor:

```typescript
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

function PivotWithRemoteData() {
  const dataManager = new DataManager({
    url: 'https://api.example.com/api/sales-data',  // ← Your API endpoint
    adaptor: new WebApiAdaptor(),
    headers: [
      { 'Authorization': 'Bearer token' }  // ← Optional: API authentication
    ],
    crossDomain: true
  });

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: dataManager,
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales', type: 'Sum' }]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      height={400}
    />
  );
}
```

### API Response Format

Your backend API must return data in the expected JSON array format:

```json
{
  "result": [
    { "Country": "USA", "Product": "Laptop", "Sales": 5000, "Quantity": 10 },
    { "Country": "USA", "Product": "Desktop", "Sales": 3000, "Quantity": 8 },
    { "Country": "Canada", "Product": "Laptop", "Sales": 2500, "Quantity": 6 }
  ],
  "count": 100
}
```

**Backend Implementation (Node.js/Express example):**

```typescript
// Backend: routes/sales.ts
app.get('/api/sales-data', async (req, res) => {
  try {
    const data = await fetchSalesData();  // Fetch from database
    res.json({
      result: data,
      count: data.length
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### Handling Async Data Loading

```typescript
function PivotWithAsyncRemoteData() {
  const [loading, setLoading] = React.useState(true);
  const [dataManager, setDataManager] = React.useState(null);

  React.useEffect(() => {
    const dm = new DataManager({
      url: 'https://api.example.com/api/sales-data',
      adaptor: new WebApiAdaptor()
    });
    setDataManager(dm);
    setLoading(false);
  }, []);

  if (loading) return <p>Loading pivot data...</p>;

  return (
    <PivotViewComponent
      dataSourceSettings={{
        dataSource: dataManager,
        rows: [{ name: 'Country' }],
        columns: [{ name: 'Product' }],
        values: [{ name: 'Sales' }]
      }}
      height={400}
    />
  );
}
```

## CSV Data Handling

### Loading CSV as JSON Array

Convert CSV data to a JSON array format first, then bind like local JSON:

```typescript
// CSV: "Country,Product,Sales,Quantity\nUSA,Laptop,5000,10\n..."

function PivotWithCSVData() {
  const csvData = [
    { Country: 'USA', Product: 'Laptop', Sales: 5000, Quantity: 10 },
    { Country: 'USA', Product: 'Desktop', Sales: 3000, Quantity: 8 },
    { Country: 'Canada', Product: 'Laptop', Sales: 2500, Quantity: 6 }
    // Parse CSV file into this format
  ];

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: csvData,  // ← Direct JSON array binding (no type property needed)
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales', type: 'Sum' }]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      height={400}
    />
  );
}
```

### CSV File Upload and Parsing

```typescript
import Papa from 'papaparse';  // npm install papaparse

function PivotWithCSVUpload() {
  const [csvData, setCsvData] = React.useState([]);

  const handleCsvUpload = (event) => {
    const file = event.target.files[0];
    
    Papa.parse(file, {
      header: true,           // Use first row as headers
      dynamicTyping: true,    // Convert numbers
      skipEmptyLines: true,
      complete: (results) => {
        setCsvData(results.data);
      },
      error: (error) => {
        console.error('CSV parsing error:', error);
      }
    });
  };

  return (
    <>
      <input 
        type="file" 
        accept=".csv" 
        onChange={handleCsvUpload} 
      />
      {csvData.length > 0 && (
        <PivotViewComponent
          dataSourceSettings={{
            dataSource: csvData,
            rows: [{ name: 'Country' }],
            columns: [{ name: 'Product' }],
            values: [{ name: 'Sales' }]
          }}
          height={400}
        />
      )}
    </>
  );
}
```

## Data Refresh Mechanisms

### Manual Refresh

```typescript
let pivotRef: PivotViewComponent;

function handleDataRefresh() {
  pivotRef.refresh();  // Refresh with current data
}

<button onClick={handleDataRefresh}>Refresh Data</button>
```

## Common Scenarios

### Binding Large Datasets

For large datasets (>10K records), use virtual scrolling:

```typescript
<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  enableVirtualization={true}
  height={500}
/>
```