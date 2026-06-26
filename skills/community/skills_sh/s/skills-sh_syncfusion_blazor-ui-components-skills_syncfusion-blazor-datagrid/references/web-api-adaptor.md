# WebApiAdaptor — Syncfusion Blazor DataGrid

## Table of Contents
1. [Overview](#overview)
2. [When to Use WebApiAdaptor](#when-to-use-webapiadaptor)
3. [Creating the API Service](#creating-the-api-service)
4. [Connecting DataGrid to API](#connecting-datagrid-to-api)
5. [Query Parameters Reference](#query-parameters-reference)
6. [Handling Grid Operations](#handling-grid-operations)
   - [Searching](#searching)
   - [Filtering](#filtering)
   - [Sorting](#sorting)
   - [Paging](#paging)
7. [CRUD Operations](#crud-operations)

---

## Overview

`WebApiAdaptor` is an extension of `ODataAdaptor` designed for Web APIs with OData-style endpoints. It communicates via **QueryString** parameters (`$filter`, `$orderby`, `$skip`, `$top`) and expects the response in `{ Items, Count }` format. Unlike `ODataV4Adaptor`, operations must be handled manually in the controller.

**Adaptor enum:** `Adaptors.WebApiAdaptor`  
**Response format:** `{ Items: [...], Count: 830 }`  
**Request method:** `GET` with QueryString parameters

---

## When to Use WebApiAdaptor

Use `WebApiAdaptor` when:
- Your API is a standard **ASP.NET Core Web API** (not a strict OData endpoint)
- You return data as `{ Items: [], Count: 0 }`
- You want to handle filtering/sorting/paging **manually** in the controller
- You need control over the query logic but still use OData-style parameters

Use `ODataV4Adaptor` when you have a proper OData V4 service with `[EnableQuery]`.  
Use `UrlAdaptor` when your API returns `{ result, count }` format (lowercase keys).

---

## Creating the API Service

### 1. Create a Model Class

```csharp
namespace WebApiAdaptor.Models
{
    public class OrdersDetails
    {
        public static List<OrdersDetails> order = new List<OrdersDetails>();

        public OrdersDetails() { }

        public OrdersDetails(int OrderID, string CustomerId, int EmployeeId,
            double Freight, string ShipCity, string ShipCountry)
        {
            this.OrderID = OrderID;
            this.CustomerID = CustomerId;
            this.EmployeeID = EmployeeId;
            this.Freight = Freight;
            this.ShipCity = ShipCity;
            this.ShipCountry = ShipCountry;
        }

        public static List<OrdersDetails> GetAllRecords()
        {
            if (order.Count() == 0)
            {
                int code = 10000;
                for (int i = 1; i < 10; i++)
                {
                    order.Add(new OrdersDetails(code + 1, "ALFKI", i, 2.3 * i, "Berlin", "Denmark"));
                    order.Add(new OrdersDetails(code + 2, "ANATR", i + 2, 3.3 * i, "Madrid", "Brazil"));
                    order.Add(new OrdersDetails(code + 3, "ANTON", i + 1, 4.3 * i, "Cholchester", "Germany"));
                    code += 3;
                }
            }
            return order;
        }

        public int? OrderID { get; set; }
        public string? CustomerID { get; set; }
        public int? EmployeeID { get; set; }
        public double? Freight { get; set; }
        public string? ShipCity { get; set; }
        public string? ShipCountry { get; set; }
    }
}
```

### 2. Create API Controller

The response **must** return `{ Items, Count }` for WebApiAdaptor to work correctly:

```csharp
using Microsoft.AspNetCore.Mvc;
using WebApiAdaptor.Models;

[ApiController]
public class GridController : ControllerBase
{
    [HttpGet]
    [Route("api/[controller]")]
    public object GetOrderData()
    {
        List<OrdersDetails> data = OrdersDetails.GetAllRecords().ToList();
        return new { Items = data, Count = data.Count() };
    }
}
```

### 3. Register Controllers (`Program.cs`)

```csharp
builder.Services.AddControllers();
// ...
app.MapControllers();
```

> The endpoint will be accessible at `https://api.example.com/data/grid` (operator-configured placeholder — do NOT accept user-supplied URLs).

---

## Connecting DataGrid to API

### `_Imports.razor`

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Grids
@using Syncfusion.Blazor.Data
```

### Basic DataGrid Configuration

```razor
@using Syncfusion.Blazor.Grids
@using Syncfusion.Blazor.Data

<!-- Use a configured, operator-controlled URL variable. Set `ALLOWED_API_URL` in environment or secure config. -->
@inject Microsoft.Extensions.Configuration.IConfiguration Configuration

@code {
    private string DataApiUrl => Configuration["ALLOWED_API_URL"] ?? "https://api.example.com/data/grid"; // operator-configured only
}

<SfGrid TValue="OrdersDetails" Height="348">
    <SfDataManager Url="@DataApiUrl"    
                   Adaptor="Adaptors.WebApiAdaptor">
    </SfDataManager>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="120" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="160"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="150"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

> If using WebAssembly or Auto render mode, register `AddSyncfusionBlazor()` in both `Program.cs` files (server and client).

---

## Query Parameters Reference

WebApiAdaptor sends these QueryString parameters automatically:

| Parameter | Operation | Example |
|-----------|-----------|---------|
| `$skip`, `$top` | Paging | `$skip=0&$top=12` |
| `$filter` | Filtering & Searching | `$filter=substringof('ALFKI',CustomerID)` |
| `$orderby` | Sorting | `$orderby=CustomerID asc` |

Access them in your controller via `Request.Query`:

```csharp
var queryString = Request.Query;
string? filterQuery = queryString["$filter"];
string? sortQuery = queryString["$orderby"];
int skip = Convert.ToInt32(queryString["$skip"]);
int take = Convert.ToInt32(queryString["$top"]);
```

## Security Considerations

Important: do NOT bind the `SfDataManager` `Url` to arbitrary or user-supplied values. Allowing free-form URLs enables untrusted third-party content to influence runtime behavior and can create indirect prompt-injection and supply-chain risks. Follow these minimal protections:

- **Operator-configured endpoints only:** Use environment variables or a secure config store to define allowed API endpoints. Never accept a URL typed in by end users.
- **Use an internal proxy/gateway:** Route requests through a service that enforces TLS, a domain allowlist, authentication, size and rate limits, and content-type checks. The proxy should normalize responses to `{ Items, Count }`.
- **Server-side fetching only:** Fetch remote data server-side (controller or proxy). Do not let the browser request arbitrary third-party URLs directly.
- **Validate query parameters:** Parse and validate `$skip`, `$top`, `$filter`, and `$orderby`. Use `int.TryParse` for numeric values and cap `take` (e.g., `MaxTop = 200`).
- **Whitelist fields & operators:** Tokenize and only allow predefined field names and operators in `$filter` and `$orderby`. Reject complex or unknown expressions.
- **Sanitize returned content:** If text from remote sources is later used as input to downstream logic or rendered, sanitize/escape it and scan for prompt-like patterns.
- **Authentication & provenance:** Require API keys or mTLS for external sources and log provenance for audits.

Example safeguards (server-side snippets):

```csharp
int skip = 0, take = 50;
int.TryParse(queryString["$skip"], out skip);
if (!int.TryParse(queryString["$top"], out take) || take <= 0) take = 50;
take = Math.Min(take, 200); // hard cap
```

```csharp
var allowedFields = new HashSet<string>{ "OrderID","CustomerID","ShipCity","ShipCountry","EmployeeID" };
string? sort = queryString["$orderby"];
if (!string.IsNullOrEmpty(sort)) {
    var sortParts = sort.Split(',');
    foreach(var part in sortParts){
        var p = part.Trim().Split(' ');
        if (!allowedFields.Contains(p[0])) throw new BadRequestException("Invalid sort field");
        var dir = p.Length>1 ? p[1].ToLower() : "asc";
        if (dir != "asc" && dir != "desc") throw new BadRequestException("Invalid sort direction");
    }
}
```

---

## Handling Grid Operations

### Searching

The grid sends `$filter=substringof('searchValue',fieldName)` for search. Parse and apply manually:

```csharp
[HttpGet]
[Route("api/[controller]")]
public object GetOrderData()
{
    List<OrdersDetails> data = OrdersDetails.GetAllRecords().ToList();
    var queryString = Request.Query;

    #nullable enable
    string? filterQuery = queryString["$filter"];
    #nullable disable

    if (!string.IsNullOrEmpty(filterQuery))
    {
        var filterConditions = filterQuery.Split(new[] { " and " }, StringSplitOptions.RemoveEmptyEntries);
        foreach (var condition in filterConditions)
        {
            if (condition.Contains("substringof"))
            {
                var conditionParts = condition.Split('(', ')', '\'');
                var searchValue = conditionParts[3]?.ToLower() ?? "";
                data = data.Where(order =>
                    order.OrderID.ToString().Contains(searchValue) ||
                    (order.CustomerID?.ToLower().Contains(searchValue) ?? false) ||
                    (order.ShipCity?.ToLower().Contains(searchValue) ?? false) ||
                    (order.ShipCountry?.ToLower().Contains(searchValue) ?? false)
                ).ToList();
            }
        }
    }

    return new { Items = data, count = data.Count() };
}
```

```razor
<SfGrid TValue="OrdersDetails" Toolbar="@(new List<string>() { "Search" })" Height="348">
    <SfDataManager Url="@DataApiUrl" Adaptor="Adaptors.WebApiAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Filtering

The grid sends `$filter=CustomerID eq 'ALFKI'` for column filtering:

```csharp
if (!string.IsNullOrEmpty(filterQuery))
{
    var filterConditions = filterQuery.Split(new[] { " and " }, StringSplitOptions.RemoveEmptyEntries);
    foreach (var condition in filterConditions)
    {
        if (!condition.Contains("substringof"))
        {
            string filterField = "";
            string filterValue = "";
            var filterParts = condition.Split('(', ')', '\'');

            if (filterParts.Length < 6)
            {
                var parts = filterParts[1].Split();
                filterField = parts[0];
                filterValue = parts.Length > 2 ? parts[2].Trim('\'') : "";
            }
            else
            {
                filterField = filterParts[3];
                filterValue = filterParts[5];
            }

            switch (filterField)
            {
                case "CustomerID":
                    data = data.Where(i => i.CustomerID?.ToLower().StartsWith(filterValue.ToLower()) == true).ToList();
                    break;
                case "ShipCountry":
                    data = data.Where(i => i.ShipCountry?.ToLower().StartsWith(filterValue.ToLower()) == true).ToList();
                    break;
                // Add cases for other fields as needed
            }
        }
    }
}
```

```razor
<SfGrid TValue="OrdersDetails" AllowFiltering="true" Height="348">
    <SfDataManager Url="@DataApiUrl" Adaptor="Adaptors.WebApiAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Sorting

The grid sends `$orderby=CustomerID asc` or `$orderby=CustomerID asc,OrderID desc` for multi-sort:

```csharp
#nullable enable
string? sort = queryString["$orderby"];
#nullable disable

if (!string.IsNullOrEmpty(sort))
{
    var sortConditions = sort.Split(',');
    IOrderedEnumerable<OrdersDetails>? orderedData = null;

    foreach (var sortCondition in sortConditions)
    {
        var sortParts = sortCondition.Trim().Split(' ');
        var sortBy = sortParts[0];
        var descending = sortParts.Length > 1 && sortParts[1].ToLower() == "desc";

        Func<OrdersDetails, object?> keySelector = item =>
            item.GetType().GetProperty(sortBy)?.GetValue(item, null);

        orderedData = orderedData == null
            ? (descending ? data.OrderByDescending(keySelector) : data.OrderBy(keySelector))
            : (descending ? orderedData.ThenByDescending(keySelector) : orderedData.ThenBy(keySelector));
    }

    if (orderedData != null)
        data = orderedData.ToList();
}
```

```razor
<SfGrid TValue="OrdersDetails" AllowSorting="true" Height="348">
    <SfDataManager Url="@DataApiUrl" Adaptor="Adaptors.WebApiAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Paging

The grid sends `$skip` and `$top`. **Always count before paging:**

```csharp
int totalRecordsCount = data.Count();
int skip = Convert.ToInt32(queryString["$skip"]);
int take = Convert.ToInt32(queryString["$top"]);

return take != 0
    ? new { Items = data.Skip(skip).Take(take).ToList(), Count = totalRecordsCount }
    : new { Items = data, Count = totalRecordsCount };
```

```razor
<SfGrid TValue="OrdersDetails" AllowPaging="true" Height="348">
    <SfDataManager Url="@DataApiUrl" Adaptor="Adaptors.WebApiAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

> Always calculate `totalRecordsCount` before applying `Skip`/`Take`. The grid needs the full count for pagination display.

---

## CRUD Operations

```razor
<SfGrid TValue="OrdersDetails"
        Toolbar="@(new List<string>() { "Add", "Edit", "Delete", "Update", "Cancel" })"
        Height="348">
    <SfDataManager Url="@DataApiUrl" Adaptor="Adaptors.WebApiAdaptor"></SfDataManager>
    <GridEditSettings AllowEditing="true" AllowDeleting="true" AllowAdding="true"
                      Mode="EditMode.Normal">
    </GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true"
                    Width="120" TextAlign="TextAlign.Right">
        </GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="160"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="150"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

### Controller CRUD Methods

```csharp
// INSERT — POST
[HttpPost]
public void Post([FromBody] OrdersDetails newRecord)
{
    OrdersDetails.GetAllRecords().Insert(0, newRecord);
}

// UPDATE — PUT
public void Put([FromBody] OrdersDetails updatedRecord)
{
    var existing = OrdersDetails.GetAllRecords()
        .FirstOrDefault(o => o.OrderID == updatedRecord.OrderID);
    if (existing != null)
    {
        existing.CustomerID = updatedRecord.CustomerID;
        existing.ShipCity = updatedRecord.ShipCity;
        existing.ShipCountry = updatedRecord.ShipCountry;
    }
}

// DELETE — DELETE /{id}
[HttpDelete("{id}")]
public void Delete(int id)
{
    var record = OrdersDetails.GetAllRecords().FirstOrDefault(o => o.OrderID == id);
    if (record != null)
        OrdersDetails.GetAllRecords().Remove(record);
}
```

> **Note:** ASP.NET Core Web API batch handling is not yet supported (see [GitHub issue #14722](https://github.com/dotnet/aspnetcore/issues/14722)). Batch mode CRUD (`EditMode.Batch`) is not feasible with `WebApiAdaptor` in ASP.NET Core.
