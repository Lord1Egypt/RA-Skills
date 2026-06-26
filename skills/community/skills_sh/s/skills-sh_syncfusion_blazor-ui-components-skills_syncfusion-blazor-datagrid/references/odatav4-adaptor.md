# ODataV4Adaptor — Syncfusion Blazor DataGrid

## Table of Contents
1. [Overview](#overview)
2. [When to Use ODataV4Adaptor](#when-to-use-odatav4adaptor)
3. [Configuring an OData V4 Service](#configuring-an-odata-v4-service)
4. [Connecting DataGrid to OData V4 Service](#connecting-datagrid-to-odata-v4-service)
5. [Handling Grid Operations](#handling-grid-operations)
   - [Searching](#searching)
   - [Filtering](#filtering)
   - [Sorting](#sorting)
   - [Paging](#paging)
6. [CRUD Operations](#crud-operations)

---

## Overview

`ODataV4Adaptor` integrates the Syncfusion Blazor DataGrid with OData V4 services. It automatically translates grid operations (search, filter, sort, page) into OData V4 query options (`$filter`, `$orderby`, `$skip`, `$top`) and sends them to the server. The server uses `[EnableQuery]` to handle these automatically.

**NuGet (Server):** `Microsoft.AspNetCore.OData`  
**Adaptor enum:** `Adaptors.ODataV4Adaptor`  
**Response format:** OData `value` array + `@odata.count`

---

## When to Use ODataV4Adaptor

Use `ODataV4Adaptor` when:
- Your backend exposes a proper **OData V4** endpoint (e.g., `/odata/Orders`)
- You want **automatic** server-side filtering, sorting, paging via OData query options
- You use `[EnableQuery]` in your ASP.NET Core controller

Use `WebApiAdaptor` instead when your API returns `{ Items, Count }` format but is not a strict OData service.  
Use `UrlAdaptor` when you need full manual control over query handling.

---

## Configuring an OData V4 Service

### 1. Install NuGet Package (Server project)

```powershell
Install-Package Microsoft.AspNetCore.OData
```

### 2. Create a Model Class

```csharp
using System.ComponentModel.DataAnnotations;

public class OrdersDetails
{
    public static List<OrdersDetails> order = new List<OrdersDetails>();

    public OrdersDetails() { }

    public OrdersDetails(int OrderID, string CustomerId, int EmployeeId, string ShipCountry)
    {
        this.OrderID = OrderID;
        this.CustomerID = CustomerId;
        this.EmployeeID = EmployeeId;
        this.ShipCountry = ShipCountry;
    }

    public static List<OrdersDetails> GetAllRecords()
    {
        if (order.Count() == 0)
        {
            int code = 10000;
            for (int i = 1; i < 10; i++)
            {
                order.Add(new OrdersDetails(code + 1, "ALFKI", i + 0, "Denmark"));
                order.Add(new OrdersDetails(code + 2, "ANATR", i + 2, "Brazil"));
                order.Add(new OrdersDetails(code + 3, "ANTON", i + 1, "Germany"));
                code += 3;
            }
        }
        return order;
    }

    [Key]
    public int OrderID { get; set; }
    public string? CustomerID { get; set; }
    public int? EmployeeID { get; set; }
    public string? ShipCountry { get; set; }
}
```

> The `[Key]` attribute on `OrderID` is required for OData entity sets.

### 3. Build Entity Data Model and Register OData Services (`Program.cs`)

```csharp
using Microsoft.AspNetCore.OData;

var modelBuilder = new ODataConventionModelBuilder();
modelBuilder.EntitySet<OrdersDetails>("Grid");

var recordCount = OrdersDetails.GetAllRecords().Count;

// Registers controllers AND attaches OData middleware in one call.
// Do NOT call builder.Services.AddControllers() again separately —
// chaining .AddOData() here already covers standard controller registration.
builder.Services.AddControllers().AddOData(
    options => options
        .Count()
        .Filter()
        .OrderBy()
        .SetMaxTop(recordCount)
        .AddRouteComponents("odata", modelBuilder.GetEdmModel())
);

// Map controller routes (required for both OData and standard API routes).
app.MapControllers();
```

> ⚠️ **Do NOT call `builder.Services.AddControllers()` twice.** Calling `.AddOData()` on the return value of `AddControllers()` is sufficient — it registers both standard controller routing and OData middleware in a single chain. A duplicate `AddControllers()` call can cause OData route conflicts or silent override of the OData configuration.

### 4. Create API Controller

```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;

[ApiController]
[Route("[controller]")]
public class GridController : ControllerBase
{
    [HttpGet]
    [EnableQuery]
    public IActionResult Get()
    {
        var data = OrdersDetails.GetAllRecords().AsQueryable();
        return Ok(data);
    }
}
```

> `[EnableQuery]` automatically applies `$filter`, `$orderby`, `$skip`, `$top` from the request URL. The endpoint will be `/odata/grid`.

---

## Connecting DataGrid to OData V4 Service

### `_Imports.razor`

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Grids
@using Syncfusion.Blazor.Data
```

### `Program.cs` (Client/Blazor project)

```csharp
using Syncfusion.Blazor;
builder.Services.AddSyncfusionBlazor();
```

### `App.razor` (theme + script)

```html
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
<script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
```

### Basic DataGrid Configuration

```razor
@using Syncfusion.Blazor.Grids
@using Syncfusion.Blazor.Data

<SfGrid TValue="OrdersDetails" Height="348">
    <SfDataManager Url="https://localhost:xxxx/odata/grid"
                   Adaptor="Adaptors.ODataV4Adaptor">
    </SfDataManager>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="100"></GridColumn>
        <GridColumn Field="EmployeeID" HeaderText="Employee ID" TextAlign="TextAlign.Right" Width="100"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

> Replace `https://localhost:xxxx/odata/grid` with your actual OData V4 endpoint URL.

---

## Handling Grid Operations

ODataV4Adaptor sends operations as OData query options automatically. You only need to enable them in `Program.cs`.

### Searching

OData V4 does not support global search natively. Use `EnableODataSearchFallback` to enable it:

```csharp
// Program.cs — enable Filter for search fallback
builder.Services.AddControllers().AddOData(
    options => options.Count().Filter()
        .AddRouteComponents("odata", modelBuilder.GetEdmModel())
);
```

```razor
<SfGrid TValue="OrdersDetails" Toolbar="@(new List<string>() { "Search" })" Height="348">
    <SfDataManager @ref="DataManager" Url="https://localhost:xxxx/odata/grid"
                   Adaptor="Adaptors.ODataV4Adaptor">
    </SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    public SfDataManager? DataManager { get; set; }

    protected override void OnAfterRender(bool firstRender)
    {
        if (DataManager?.DataAdaptor is ODataV4Adaptor odataAdaptor)
        {
            RemoteOptions options = odataAdaptor.Options;
            options.EnableODataSearchFallback = true;
            odataAdaptor.Options = options;
        }
    }
}
```

> ⚠️ **`EnableODataSearchFallback` must be set inside `OnAfterRender`**, not `OnInitialized` or `OnInitializedAsync`. The `DataAdaptor` property on `SfDataManager` is only populated **after** the component completes its first render cycle — accessing it earlier results in a `null` reference. Always guard with `if (firstRender)` or a null-check as shown above.

### Filtering

Enable `.Filter()` in OData options, then set `AllowFiltering="true"`:

```razor
<SfGrid TValue="OrdersDetails" AllowFiltering="true" Height="348">
    <SfDataManager Url="https://localhost:xxxx/odata/grid"
                   Adaptor="Adaptors.ODataV4Adaptor">
    </SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

> The grid sends `$filter=CustomerID eq 'ALFKI'` automatically via the `[EnableQuery]` controller.

### Sorting

Enable `.OrderBy()` in OData options, then set `AllowSorting="true"`:

```razor
<SfGrid TValue="OrdersDetails" AllowSorting="true" Height="348">
    <SfDataManager Url="https://localhost:xxxx/odata/grid"
                   Adaptor="Adaptors.ODataV4Adaptor">
    </SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

> Sends `$orderby=CustomerID asc` or `$orderby=CustomerID asc,OrderID desc` for multi-sort.

### Paging

Enable `.SetMaxTop(count)` and `.Count()` in OData options, then set `AllowPaging="true"`:

```razor
<SfGrid TValue="OrdersDetails" AllowPaging="true" Height="348">
    <SfDataManager Url="https://localhost:xxxx/odata/grid"
                   Adaptor="Adaptors.ODataV4Adaptor">
    </SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

> Sends `$skip=0&$top=12&$count=true` for the first page with 12 records.

---

## CRUD Operations

Enable editing toolbar and `GridEditSettings`. The controller needs `POST`, `PATCH`, and `DELETE` methods.

```razor
<SfGrid TValue="OrdersDetails"
        Toolbar="@(new List<string>() { "Add", "Edit", "Delete", "Update", "Cancel" })"
        Height="348">
    <SfDataManager Url="https://localhost:xxxx/odata/grid"
                   Adaptor="Adaptors.ODataV4Adaptor">
    </SfDataManager>
    <GridEditSettings AllowEditing="true" AllowDeleting="true" AllowAdding="true"
                      Mode="EditMode.Normal">
    </GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true"
                    Width="100" TextAlign="TextAlign.Right">
        </GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="100"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

> `IsPrimaryKey="true"` is required on at least one column for CRUD to work.

### Controller CRUD Methods

```csharp
// INSERT — POST /odata/grid
[HttpPost]
[EnableQuery]
public IActionResult Post([FromBody] OrdersDetails addRecord)
{
    if (addRecord == null) return BadRequest("Null order");
    OrdersDetails.GetAllRecords().Insert(0, addRecord);
    return new JsonResult(addRecord);
}

// UPDATE — PATCH /odata/grid(key)
[HttpPatch("{key}")]
public IActionResult Patch(int key, [FromBody] OrdersDetails updateRecord)
{
    if (updateRecord == null) return BadRequest("No records");
    var existing = OrdersDetails.GetAllRecords().FirstOrDefault(o => o.OrderID == key);
    if (existing != null)
    {
        existing.CustomerID = updateRecord.CustomerID ?? existing.CustomerID;
        existing.EmployeeID = updateRecord.EmployeeID ?? existing.EmployeeID;
        existing.ShipCountry = updateRecord.ShipCountry ?? existing.ShipCountry;
    }
    return new JsonResult(updateRecord);
}

// DELETE — DELETE /odata/grid(key)
[HttpDelete("{key}")]
public IActionResult Delete(int key)
{
    var record = OrdersDetails.GetAllRecords().FirstOrDefault(o => o.OrderID == key);
    if (record != null)
        OrdersDetails.GetAllRecords().Remove(record);
    return new JsonResult(record);
}
```

> ODataV4Adaptor uses `PATCH` (not `PUT`) for updates. Ensure your controller matches this HTTP method.