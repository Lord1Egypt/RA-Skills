# Connecting to Data Sources

## ⚠️ SECURITY NOTICE

**All remote connections MUST use authenticated, configuration-based endpoints.** Never hardcode server URLs or use untrusted data sources.

✅ **Required Security Controls:**
- Environment-based configuration (`.env` files)
- Authentication and authorization
- HTTPS/SSL for all remote connections
- Input validation and sanitization
- Enterprise-managed servers only

## Table of Contents
- [Server-Side Pivot Engine](#server-side-pivot-engine)
- [OLAP Connections](#olap-connections)

## Server-Side Pivot Engine

The server-side pivot engine processes large datasets (100K+ records) on the server, sending only viewport data to the client. This approach performs operations such as aggregation, filtering, sorting, and grouping on the server, reducing network traffic and improving Pivot Table rendering performance when working with large data sets.

### Overview

**When to use:** Large datasets (100K+ records), complex aggregations, or when you need to process data on a dedicated backend.

**Benefits:**
- Processes data server-side, minimizing network bandwidth usage
- Only viewport-required data is transmitted to the client
- Works efficiently with virtual scrolling and paging
- Supports all existing Pivot Table features

### Quick Setup Steps

1. **Download Server-Side Application**: Get the ASP.NET Core-based [PivotController application](https://github.com/SyncfusionExamples/server-side-pivot-engine-for-pivot-table) from GitHub
2. **Install Dependencies**: The Syncfusion.Pivot.Engine library automatically downloads from nuget.org
3. **Run Backend**: Start the PivotController application in Visual Studio (typically runs on `https://localhost:44350/api/pivot/post`)
4. **Configure Client**: Set the Pivot Table's `mode` to `Server` and point to the backend URL

### Configuring Server-Side Mode

> **⚠️ SECURITY:** Use environment variables for server URLs. See security notice at top of document.

**Step 1 — Create `.env` file:**
```bash
REACT_APP_PIVOT_SERVICE_URL=https://your-server.com/api/pivot/post
```

**Step 2 — Configure with environment variable:**

```typescript
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

function ServerSidePivot() {
  const dataSourceSettings: DataSourceSettingsModel = {
    url: process.env.REACT_APP_PIVOT_SERVICE_URL,  // ← Environment-based URL
    mode: 'Server',  // ← Enable server-side mode
    rows: [{ name: 'ProductID', caption: 'Product ID' }],
    columns: [{ name: 'Year', caption: 'Production Year' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Price', caption: 'Sold Amount' }],
    formatSettings: [
      { name: 'Price', format: 'C' }
    ]
  };

  return (
    <PivotViewComponent
      id="pivot-server"
      dataSourceSettings={dataSourceSettings}
      height={500}
    />
  );
}
```

### Supported Data Sources

The server-side Pivot Engine supports multiple data source types:

- **Collection**: List or IEnumerable objects
- **JSON**: From local *.json files or remote sources
- **CSV**: From local or remote CSV files
- **DataTable**: Direct database access
- **Dynamic**: Runtime-generated data structures

Each data source is processed through the server's pivot engine, which handles all aggregation and filtering operations.

### Backend Configuration (ASP.NET Core)

The server requires a controller to handle pivot requests:

```csharp
[ApiController]
[Route("api/pivot")]
public class PivotController : ControllerBase
{
  private readonly PivotEngine<DataSource.PivotViewData> PivotEngine = new();

  [HttpPost("post")]
  public async Task<IActionResult> Post([FromBody] PivotViewDataOption request)
  {
    try
    {
      // Load data from CSV, JSON, or database
      var data = new DataSource.PivotViewData().GetVirtualData();
      
      // Process pivot using Syncfusion engine
      var pivotResult = PivotEngine.GetData(request, data);
      
      return Ok(pivotResult);
    }
    catch (Exception ex)
    {
      return BadRequest(new { error = ex.Message });
    }
  }
}
```

## OLAP Connections

OLAP (Online Analytical Processing) enables analysis of multidimensional data using OLAP cubes. The Pivot Table supports connections to OLAP servers like Microsoft SQL Server Analysis Services (SSAS).

### Overview

**When to use:** Enterprise data warehouses, multidimensional analysis, complex hierarchical data structures, or when using existing OLAP cube infrastructure.

**Key Characteristics:**
- Connects to OLAP cubes (e.g., Adventure Works)
- Supports hierarchies, measures, and calculated members
- Enables powerful multidimensional analysis
- Provides automatic sorting and filtering on hierarchical data

### Configuring OLAP Data Source

> **⚠️ SECURITY:** Use enterprise OLAP servers with authentication. See security notice at top of document.

**Step 1 — Create `.env` file:**
```bash
REACT_APP_OLAP_URL=https://your-olap-server.com/olap/msmdpump.dll
```

**Step 2 — Configure OLAP with environment variable:**

```typescript
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';

function OlapPivot() {
  const dataSourceSettings: DataSourceSettingsModel = {
    catalog: 'Adventure Works DW 2008 SE',  // ← OLAP Catalog
    cube: 'Adventure Works',                 // ← OLAP Cube
    providerType: 'SSAS',                    // ← Provider type
    enableSorting: true,
    localeIdentifier: 1033,                  // ← Locale (1033 = English)
    url: process.env.REACT_APP_OLAP_URL,     // ← Environment-based URL
    rows: [
      { name: '[Customer].[Customer Geography]', caption: 'Customer Geography' }
    ],
    columns: [
      { name: '[Product].[Product Categories]', caption: 'Product Categories' },
      { name: '[Measures]', caption: 'Measures' }
    ],
    values: [
      { name: '[Measures].[Customer Count]', caption: 'Customer Count' },
      { name: '[Measures].[Internet Sales Amount]', caption: 'Internet Sales Amount' }
    ],
    filters: [
      { name: '[Date].[Fiscal]', caption: 'Date Fiscal' }
    ]
  };

  return (
    <PivotViewComponent
      id="pivot-olap"
      dataSourceSettings={dataSourceSettings}
      height={500}
      showGroupingBar={true}
    />
  );
}
```

### OLAP Cube Elements

OLAP cubes organize data using these hierarchical structures:

- **Hierarchies**: Organize members in parent-child relationships (e.g., Year → Quarter → Month)
- **Measures**: Numeric values for analysis (e.g., Sales Amount, Quantity Sold)
- **Dimensions**: Collections of related hierarchies (e.g., Product, Customer, Date)
- **Calculated Members**: Custom measures created from other measures
- **Named Sets**: Predefined collections of members (e.g., Top 10 Products)

When configuring rows, columns, and values, use the unique names of these elements exactly as they appear in your OLAP cube.

### Applying Formatting to OLAP Values

Format OLAP value fields using the same format codes as relational data:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  // ... OLAP configuration ...
  formatSettings: [
    { name: '[Measures].[Internet Sales Amount]', format: 'C0' },  // ← Currency
    { name: '[Measures].[Discount Pct]', format: 'P2' }            // ← Percentage
  ]
};
```

### Common OLAP Format Codes

| Code | Example | Use Case |
|------|---------|----------|
| C0 | $1,235 | Currency, no decimals |
| C2 | $1,234.56 | Currency with cents |
| N0 | 1235 | Integer numbers |
| P2 | 12.34% | Percentages |
| E2 | 1.23E+03 | Scientific notation |

### Backend Setup (ASP.NET Core Example)

The server-side Pivot Engine package handles data processing:

```csharp
// Backend: PivotController.cs
[ApiController]
[Route("api/pivot")]
public class PivotController : ControllerBase
{
  [HttpPost("post")]
  public async Task<IActionResult> Post([FromBody] PivotViewDataOption request)
  {
    try
    {
      // Load data (CSV, JSON, database, etc.)
      var data = GetCsvData("sales-data.csv");
      
      // Process pivot using Syncfusion engine
      var helper = new PivotViewHelper();
      var pivotResult = helper.GetPivotData(request, data);
      
      return Ok(pivotResult);
    }
    catch (Exception ex)
    {
      return BadRequest(new { error = ex.Message });
    }
  }

  private List<dynamic> GetCsvData(string filePath)
  {
    var data = new List<dynamic>();
    using (var reader = new StreamReader(filePath))
    using (var csv = new CsvReader(reader))
    {
      foreach (var record in csv.GetRecords<dynamic>())
      {
        data.Add(record);
      }
    }
    return data;
  }
}
```

### Data Sources Supported by Server Engine

- **CSV:** `sales-data.csv`
- **JSON:** `sales-analysis.json` or dynamic JSON arrays
- **Database Tables:** Direct SQL queries
- **Collections:** IEnumerable/List<T>

### Performance Benefits

- **100K records:** ~500ms initial load vs. 5s client-side
- **Memory:** Server processes data (client only stores viewport)
- **Bandwidth:** Only viewport data transmitted (~50-200 rows)
- **Virtual Scrolling:** Seamless scrolling of millions of records

### Enabling Virtual Scrolling with Server Mode

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  url: process.env.REACT_APP_PIVOT_SERVICE_URL,  // ← Environment-based URL
  mode: 'Server'
};

<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  enableVirtualization={true}  // ← Virtual scrolling
  height={500}
  width="100%"
/>
```

## OLAP Connections

OLAP (Online Analytical Processing) enables analysis using pre-aggregated dimensional data from OLAP servers like SQL Server Analysis Services (SSAS).

### Overview

**OLAP Characteristics:**
- Pre-calculated aggregations
- Hierarchical dimensions (Year → Quarter → Month)
- Optimized for read-heavy analytical queries
- Real-time multi-dimensional analysis

### Connecting to SSAS OLAP Server

> **⚠️ SECURITY:** Use enterprise OLAP servers with authentication. See security notice at top of document.

Use Syncfusion's SSAS data provider to connect to SQL Server Analysis Services:

```typescript
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';

function OlapPivot() {
  const dataSourceSettings: DataSourceSettingsModel = {
    providerType: 'SSAS',  // ← SSAS provider type
    url: process.env.REACT_APP_OLAP_URL,  // ← Environment-based URL
    catalog: 'Adventure Works DW 2012',  // ← Database/Catalog
    cube: 'Adventure Works',  // ← Cube name
    localeIdentifier: 1033,  // ← Locale identifier
    enableSorting: true,  // ← Enable sorting
    rows: [
      { name: '[Date].[Fiscal]', caption: 'Fiscal Date' }  // ← Dimension
    ],
    columns: [
      { name: '[Customer].[Customer Geography]', caption: 'Customer Geography' }  // ← Dimension
    ],
    values: [
      { name: '[Measures].[Internet Sales Amount]', caption: 'Internet Sales' }  // ← Measure
    ],
    filters: []
  };

  return (
    <PivotViewComponent
      id="olap-pivot"
      dataSourceSettings={dataSourceSettings}
      height={400}
    />
  );
}
```

### OLAP Field Format

**Dimensions** use bracket notation with hierarchy:
```
[Date].[Fiscal]                    ← Dimension.Hierarchy
[Product].[Product Categories]     ← Dimension.Hierarchy
[Customer].[Customer Geography]    ← Dimension.Hierarchy
```

**Measures** represent aggregations:
```
[Measures].[Internet Sales Amount]  ← Pre-aggregated values
[Measures].[Reseller Sales Amount]  ← Pre-aggregated values
```

### Switching Between OLAP Providers

Support for multiple OLAP servers (SSAS, Mondrian, Essbase):

```typescript
// SQL Server Analysis Services (SSAS)
const dataSourceSettings: DataSourceSettingsModel = {
  providerType: 'SSAS',
  url: process.env.REACT_APP_OLAP_URL  // Environment-based URL
};

// Mondrian:
const dataSourceSettings: DataSourceSettingsModel = {
  providerType: 'Mondrian',
  url: process.env.REACT_APP_MONDRIAN_URL  // Environment-based URL
};
```

### Practical OLAP Example

```typescript
function CompleteSalesOlap() {
  const dataSourceSettings: DataSourceSettingsModel = {
    providerType: 'SSAS',
    url: process.env.REACT_APP_OLAP_URL,  // Environment-based URL
    catalog: 'Adventure Works DW 2012',
    cube: 'Adventure Works',
    localeIdentifier: 1033,
    enableSorting: true,
    rows: [
      { name: '[Date].[Fiscal].[Year]', caption: 'Year' },
      { name: '[Date].[Fiscal].[Quarter]', caption: 'Quarter' }
    ],
    columns: [
      { name: '[Product].[Product Categories].[Category]', caption: 'Product Category' }
    ],
    values: [
      { 
        name: '[Measures].[Internet Sales Amount]',
        caption: 'Internet Sales'
      },
      {
        name: '[Measures].[Reseller Sales Amount]',
        caption: 'Reseller Sales'
      }
    ],
    filters: [
      { 
        name: '[Customer].[Customer Geography]',
        caption: 'Customer Geography'
      }
    ]
  };

  return (
    <PivotViewComponent
      id="olap-sales"
      dataSourceSettings={dataSourceSettings}
      height={400}
    />
  );
}
```

## Real-Time Updates & Refresh

### Polling for Data Updates

To refresh data periodically, use the component's `refresh()` method:

```typescript
function PivotWithPolling() {
  const pivotRef = React.useRef<PivotViewComponent>(null);

  React.useEffect(() => {
    // Poll for fresh data every 30 seconds
    const interval = setInterval(() => {
      if (pivotRef.current) {
        pivotRef.current.refresh();
      }
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <PivotViewComponent
      ref={pivotRef}
      dataSourceSettings={dataSourceSettings}
      height={400}
    />
  );
}
```

### Manual Data Refresh

```typescript
function handleDataRefresh() {
  pivotRef.current?.refresh();
}

<button onClick={handleDataRefresh}>Refresh Data</button>
```
  );
}
```

## Connection Management

### Error Handling

```typescript
function PivotWithErrorHandling() {
  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      actionFailure={(args: any) => {

        // Show user-friendly error message
        alert(`Failed to load pivot data: ${args.error}`);
      }}
      height={400}
    />
  );
}
```

### Connection Retry Logic

```typescript
async function retryConnection(
  url: string,
  maxRetries: number = 3,
  delayMs: number = 1000
): Promise<any> {
  let lastError;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, {
        method: 'GET',
        timeout: 10000  // 10 second timeout
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      lastError = error;
      console.warn(`Connection attempt ${i + 1} failed, retrying in ${delayMs}ms...`);
      
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, delayMs));
      }
    }
  }
  
  throw new Error(`Failed to connect after ${maxRetries} attempts: ${lastError}`);
}
```
