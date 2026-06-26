# Connecting to Databases

## ⚠️ CRITICAL SECURITY NOTICE

**All database connections MUST be handled through secure backend APIs.** Never expose database connection strings or credentials to the client-side React application.

✅ **Required Security Controls:**
- Backend API with authentication/authorization
- Secure connection strings (server-side only)
- SQL injection prevention (parameterized queries)
- Input validation and sanitization
- Rate limiting and CORS configuration
- HTTPS/TLS encryption
- API key or JWT authentication

❌ **NEVER:**
- Connect directly to databases from React
- Expose connection strings in client code
- Accept user-provided database endpoints
- Skip authentication on API endpoints
- Use HTTP for sensitive data
- Trust client-side data without validation

## Table of Contents
- [Overview](#overview)
- [Security Best Practices](#security-best-practices)
- [Database Support](#database-support)
- [Architecture Pattern](#architecture-pattern)
- [Web API Setup](#web-api-setup)
- [React Configuration](#react-configuration)
- [Database Connection Examples](#database-connection-examples)

---

## Overview

Connect PivotView to enterprise databases (SQL Server, MySQL, PostgreSQL, MongoDB, etc.) using a **secure Web API intermediary**. This pattern ensures database credentials remain server-side and provides proper authentication, validation, and authorization layers.

---

## Security Best Practices

### 1. **Backend API Security**

✅ **DO**: Implement authentication and authorization
```csharp
[Authorize(Roles = "DataAnalyst")]
[ApiController]
[Route("api/[controller]")]
public class PivotController : ControllerBase
{
    [HttpGet]
    public IActionResult GetData()
    {
        // Verify user permissions
        if (!User.HasClaim("Permission", "ViewSalesData"))
            return Forbid();
        
        return Ok(FetchDatabaseData());
    }
}
```

### 2. **Connection String Security**

✅ **DO**: Store in secure configuration (server-side)
```csharp
// appsettings.json (never commit to source control)
{
  "ConnectionStrings": {
    "SalesDB": "Server=prod-db;Database=Sales;User Id=apiuser;Password=***;"
  }
}

// Usage in controller
private readonly IConfiguration _config;
string connectionString = _config.GetConnectionString("SalesDB");
```

❌ **DON'T**: Hardcode or expose connection strings
```csharp
// NEVER DO THIS - Security Risk!
string conStr = "Server=prod;User=admin;Password=secret123;";
```

### 3. **SQL Injection Prevention**

✅ **DO**: Use parameterized queries
```csharp
private DataTable FetchData(string customerId)
{
    string query = "SELECT * FROM Orders WHERE CustomerId = @customerId";
    var command = new SqlCommand(query, connection);
    command.Parameters.AddWithValue("@customerId", customerId);
    // Execute command
}
```

❌ **DON'T**: Use string concatenation
```csharp
// VULNERABLE TO SQL INJECTION
string query = $"SELECT * FROM Orders WHERE CustomerId = '{customerId}'";
```

### 4. **React Authentication**

✅ **DO**: Secure API calls with authentication
```typescript
const fetchData = async () => {
    const token = localStorage.getItem('authToken');
    const response = await fetch(process.env.REACT_APP_API_ENDPOINT, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    
    if (!response.ok) {
        throw new Error('Unauthorized');
    }
    
    return await response.json();
};
```

### 5. **Input Validation**

```csharp
private bool ValidateInput(string input)
{
    // Whitelist validation
    if (string.IsNullOrWhiteSpace(input) || input.Length > 100)
        return false;
    
    // Check for SQL injection patterns
    if (input.Contains("--") || input.Contains(";") || input.Contains("'"))
        return false;
    
    return true;
}
```

### 6. **Error Handling**

```csharp
try
{
    return Ok(FetchDatabaseData());
}
catch (Exception ex)
{
    _logger.LogError(ex, "Database error");
    // Don't expose internal details to client
    return StatusCode(500, "An error occurred");
}
```

## Database Support

The PivotView integrates with these databases via ASP.NET Core Web API:

| Database | Library | Nuget Package |
|----------|---------|---|
| **Microsoft SQL Server** | SqlClient | `System.Data.SqlClient` |
| **MySQL** | MySql.Data | `MySql.Data` |
| **PostgreSQL** | Npgsql | `Npgsql.EntityFrameworkCore.PostgreSQL` |
| **MongoDB** | MongoDB.Driver | `MongoDB.Driver`, `MongoDB.Bson` |
| **Oracle** | OracleClient | `Oracle.ManagedDataAccess.Core` |
| **Elasticsearch** | NEST | `Nest` |
| **Snowflake** | Snowflake.Data | `Snowflake.Data` |

## Architecture Pattern

### Step 1: ASP.NET Core Web API Service
Create a PivotController that:
1. Connects to the database using appropriate NuGet library
2. Executes SQL query to fetch data
3. Serializes result to JSON using Newtonsoft.Json
4. Returns JSON to React frontend

### Step 2: React Pivot Table Configuration
Configure the `url` property in `dataSourceSettings` to point to the Web API endpoint.

## Web API Setup

### Generic Controller Pattern

```csharp
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System.Data;
using YourDatabaseLibrary;

namespace MyWebService.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class PivotController : ControllerBase
    {
        private readonly IConfiguration _configuration;
        private readonly ILogger<PivotController> _logger;
        
        public PivotController(IConfiguration configuration, ILogger<PivotController> logger)
        {
            _configuration = configuration;
            _logger = logger;
        }

        [Authorize] // 🔒 SECURITY: Require authentication
        [HttpGet(Name = "GetDatabaseResult")]
        public IActionResult Get()
        {
            try
            {
                // 🔒 SECURITY: Verify user has permission
                if (!User.HasClaim("Permission", "ViewPivotData"))
                    return Forbid();
                
                var data = FetchDatabaseData();
                return Ok(JsonConvert.SerializeObject(data));
            }
            catch (Exception ex)
            {
                // 🔒 SECURITY: Log error, don't expose details
                _logger.LogError(ex, "Error fetching database data");
                return StatusCode(500, "An error occurred");
            }
        }

        private DataTable FetchDatabaseData()
        {
            // 🔒 SECURITY: Get connection string from secure configuration
            string connectionString = _configuration.GetConnectionString("YourDatabase");
            
            if (string.IsNullOrEmpty(connectionString))
                throw new InvalidOperationException("Connection string not configured");

            // 1. Create database-specific connection
            var connection = new YourDatabaseConnection(connectionString);
            connection.Open();

            // 🔒 SECURITY: Use parameterized queries to prevent SQL injection
            string query = "SELECT * FROM TableName WHERE IsActive = @isActive";
            var command = new YourDatabaseCommand(query, connection);
            command.Parameters.AddWithValue("@isActive", true);
            
            var dataAdapter = new YourDatabaseDataAdapter(command);

            // 3. Populate DataTable
            DataTable dataTable = new DataTable();
            dataAdapter.Fill(dataTable);
            connection.Close();

            return dataTable;
        }
    }
}
```

### Required NuGet Packages
- `Newtonsoft.Json` - JSON serialization
- Database-specific library (above table)
- `Microsoft.AspNetCore.Mvc` - ASP.NET Core framework

## React Configuration

### Approach 1: Direct URL Binding

Directly bind the Web API endpoint to the `url` property within `dataSourceSettings`. The API returns JSON data that is automatically mapped to the pivot table fields.

```typescript
import { PivotViewComponent, FieldList, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

function App() {
  // 🔒 SECURITY: Use environment variables, not hardcoded URLs
  const apiEndpoint = process.env.REACT_APP_PIVOT_API_ENDPOINT;

  const dataSourceSettings: DataSourceSettingsModel = {
    url: apiEndpoint,  // Direct URL to Web API endpoint
    expandAll: false,
    enableSorting: true,
    columns: [{ name: 'Product' }],
    rows: [
      { name: 'Country' },
      { name: 'State' }
    ],
    values: [
      { name: 'Quantity' },
      { name: 'Amount', caption: 'Sold Amount' }
    ],
    filters: [],
    formatSettings: [
      { name: 'Amount', format: 'C0' }
    ]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      showFieldList={true}
    >
      <Inject services={[FieldList]} />
    </PivotViewComponent>
  );
}

export default App;
```

### Approach 2: Using DataManager

Use `DataManager` with `WebApiAdaptor` to fetch data from the Web API and configure report structure separately.

```typescript
import { PivotViewComponent, FieldList, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

function App() {
  // 🔒 SECURITY: Use environment variables, not hardcoded URLs
  const apiEndpoint = process.env.REACT_APP_PIVOT_API_ENDPOINT;
  const authToken = localStorage.getItem('authToken');

  // Create DataManager for secure data fetching
  const dataSource = new DataManager({
    url: apiEndpoint,
    adaptor: new WebApiAdaptor(),
    headers: [
      { 'Authorization': `Bearer ${authToken}` },
      { 'Content-Type': 'application/json' }
    ]
  });

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: dataSource,
    expandAll: false,
    enableSorting: true,
    columns: [{ name: 'Product' }],
    rows: [
      { name: 'Country' },
      { name: 'State' }
    ],
    values: [
      { name: 'Quantity' },
      { name: 'Amount', caption: 'Sold Amount' }
    ],
    filters: [],
    formatSettings: [
      { name: 'Amount', format: 'C0' }
    ]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      showFieldList={true}
    >
      <Inject services={[FieldList]} />
    </PivotViewComponent>
  );
}

export default App;
```

### Comparison

| Feature | Approach 1 (Direct URL) | Approach 2 (DataManager) |
|---------|------------------------|--------------------------|
| **Setup** | Simple, minimal configuration | More control with headers and adaptor |
| **Authentication** | Limited | Full support with custom headers |
| **Error Handling** | Basic | Advanced with adaptor events |
| **Best For** | Simple API endpoints | Complex scenarios with auth, error handling |

## Database Connection Examples

### Microsoft SQL Server

```csharp
private static DataTable FetchSQLResult()
{
    string connStr = @"Server=localhost;Database=MyDb;User Id=sa;Password=YourPassword;";
    SqlConnection connection = new SqlConnection(connStr);
    connection.Open();
    SqlCommand cmd = new SqlCommand("SELECT * FROM Orders", connection);
    SqlDataAdapter adapter = new SqlDataAdapter(cmd);
    DataTable dt = new DataTable();
    adapter.Fill(dt);
    connection.Close();
    return dt;
}
```

**Port**: Default 1433

### MySQL

```csharp
private static DataTable FetchMySQLResult()
{
    string connStr = "Server=localhost;Database=mydb;Uid=myuser;Pwd=password;";
    MySqlConnection connection = new MySqlConnection(connStr);
    connection.Open();
    MySqlCommand cmd = new MySqlCommand("SELECT * FROM orders", connection);
    MySqlDataAdapter adapter = new MySqlDataAdapter(cmd);
    DataTable dt = new DataTable();
    adapter.Fill(dt);
    connection.Close();
    return dt;
}
```

**Port**: Default 3306

### PostgreSQL

```csharp
private static DataTable FetchPostgreSQLResult()
{
    string connStr = "Server=localhost;Database=mydb;User Id=myuser;Password=password;";
    NpgsqlConnection connection = new NpgsqlConnection(connStr);
    connection.Open();
    NpgsqlCommand cmd = new NpgsqlCommand("SELECT * FROM tablename", connection);
    NpgsqlDataAdapter adapter = new NpgsqlDataAdapter(cmd);
    DataTable dt = new DataTable();
    adapter.Fill(dt);
    connection.Close();
    return dt;
}
```

**Port**: Default 5432

### MongoDB

```csharp
private static List<BsonDocument> FetchMongoDbResult()
{
    string connStr = "mongodb://localhost:27017";
    MongoClient client = new MongoClient(connStr);
    IMongoDatabase db = client.GetDatabase("sample_training");
    var collection = db.GetCollection<BsonDocument>("ProductDetails");
    return collection.Find(new BsonDocument()).ToList();
}
```

**Port**: Default 27017

### Oracle

```csharp
private static DataTable FetchOracleResult()
{
    string connStr = "Data Source=localhost;User Id=myuser;Password=password;";
    OracleConnection connection = new OracleConnection(connStr);
    connection.Open();
    OracleCommand cmd = new OracleCommand("SELECT * FROM EMPLOYEES", connection);
    OracleDataAdapter adapter = new OracleDataAdapter(cmd);
    DataTable dt = new DataTable();
    adapter.Fill(dt);
    connection.Close();
    return dt;
}
```

**Port**: Default 1521

### Elasticsearch

```csharp
private static object FetchElasticsearchData()
{
    var uri = new Uri("http://localhost:9200");
    var settings = new ConnectionSettings(uri);
    var client = new ElasticClient(settings);
    var response = client.Search<object>(s => s
        .Index("product")
        .Size(1000)
    );
    return response.Documents;
}
```

**Port**: Default 9200

### Snowflake

```csharp
private static DataTable FetchSnowflakeResult()
{
    using (var connection = new SnowflakeDbConnection())
    {
        connection.ConnectionString = 
            "account=myaccount;user=myuser;password=password;db=mydb;schema=public;";
        connection.Open();
        var adapter = new SnowflakeDbDataAdapter("SELECT * FROM MY_TABLE", connection);
        DataTable dt = new DataTable();
        adapter.Fill(dt);
        return dt;
    }
}
```

## Connection String Anatomy

**Format**: `Server=host;Port=port;Database=dbname;User Id=user;Password=pwd;`

**Common Parameters**:
- `Server`/`Host`: Database server address
- `Port`: Port number (varies by database)
- `Database`: Database name
- `User Id`/`Uid`: Username
- `Password`/`Pwd`: Password

## Testing the Connection

1. Run Web API application
2. Access endpoint in browser: `https://localhost:PORT/Pivot`
3. Verify JSON data displays correctly
4. Update React `url` to match running port

## Error Handling

Add error handling to PivotController:

```csharp
[HttpGet]
public object Get()
{
    try
    {
        return JsonConvert.SerializeObject(FetchDatabaseData());
    }
    catch (Exception ex)
    {
        return new { error = ex.Message };
    }
}
```

## CORS Configuration

Enable CORS in Startup.cs for React frontend:

```csharp
services.AddCors(options =>
{
    options.AddPolicy("AllowReact",
        builder => builder.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader()
    );
});

app.UseCors("AllowReact");
```
