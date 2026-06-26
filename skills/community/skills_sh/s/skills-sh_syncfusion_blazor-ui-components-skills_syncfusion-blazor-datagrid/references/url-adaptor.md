# UrlAdaptor — Syncfusion Blazor DataGrid

## Table of Contents
1. [Overview](#overview)
2. [When to Use UrlAdaptor](#when-to-use-urladaptor)
3. [Creating the API Service](#creating-the-api-service)
4. [Connecting DataGrid to API](#connecting-datagrid-to-api)
5. [Handling Grid Operations](#handling-grid-operations)
   - [Searching](#searching)
   - [Filtering](#filtering)
   - [Sorting](#sorting)
   - [Paging](#paging)
6. [CRUD Operations](#crud-operations)
   - [Separate URL Mapping](#separate-url-mapping)
   - [Single CrudUrl Method](#single-crudurl-method)
   - [Batch Operations](#batch-operations)
7. [CRUDModel Helper Class](#crudmodel-helper-class)

---

## Overview

`UrlAdaptor` is the **base adaptor** for communicating with custom APIs. Unlike `WebApiAdaptor` (which uses QueryString params), `UrlAdaptor` sends a `POST` request with a `DataManagerRequest` body containing all operation details. The server responds with `{ result: [...], count: N }` format.

**Adaptor enum:** `Adaptors.UrlAdaptor`  
**Request method:** `POST` with `DataManagerRequest` JSON body  
**Response format:** `{ result: [...], count: N }` (lowercase keys)  
**NuGet (Server):** `Syncfusion.Blazor.Data` (for `DataManagerRequest` and `DataOperations`)

---

## When to Use UrlAdaptor

Use `UrlAdaptor` when:
- You have a **custom API** with unique business logic that can't use OData conventions
- You want the grid to send all operation details in a single `POST` body
- Your response uses `{ result, count }` format (lowercase)
- You need separate `InsertUrl`, `UpdateUrl`, `RemoveUrl` or a unified `CrudUrl`
- You want to use `Syncfusion.Blazor.Data` `DataOperations` helper methods

Use `WebApiAdaptor` instead when your controller returns `{ Items, Count }` format.

---

## Creating the API Service

### 1. Install NuGet Package (Server project)

```powershell
Install-Package Syncfusion.Blazor.Data
```

### 2. Create a Model Class

```csharp
namespace URLAdaptor.Models
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

### 3. Create API Controller

```csharp
using Microsoft.AspNetCore.Mvc;
using Syncfusion.Blazor.Data;
using Syncfusion.Blazor;
using URLAdaptor.Models;

[ApiController]
public class GridController : ControllerBase
{
    [HttpGet]
    public List<OrdersDetails> GetOrderData()
    {
        return OrdersDetails.GetAllRecords().ToList();
    }

    // Basic POST — returns all data (no server-side operations yet)
    [HttpPost]
    [Route("api/[controller]")]
    public object Post()
    {
        IQueryable<OrdersDetails> DataSource = GetOrderData().AsQueryable();
        int totalRecordsCount = DataSource.Count();
        return new { result = DataSource, count = totalRecordsCount };
    }
}
```

### 4. Register Controllers (`Program.cs`)

```csharp
builder.Services.AddControllers();
// ...
app.MapControllers();
```

---

## Connecting DataGrid to API

```razor
@using Syncfusion.Blazor.Grids
@using Syncfusion.Blazor.Data

<!-- Use a configuration-backed base URL to avoid embedding literal URLs. Set `ALLOWED_API_URL` in secure config. -->
@inject Microsoft.Extensions.Configuration.IConfiguration Configuration

@code {
    private string DataApiUrl => Configuration["ALLOWED_API_URL"] ?? "https://api.example.com/api/grid"; // operator-configured only
    private string InsertUrl => Configuration["ALLOWED_API_INSERT_URL"] ?? DataApiUrl + "/Insert";
    private string UpdateUrl => Configuration["ALLOWED_API_UPDATE_URL"] ?? DataApiUrl + "/Update";
    private string RemoveUrl => Configuration["ALLOWED_API_REMOVE_URL"] ?? DataApiUrl + "/Remove";
    private string CrudUrl => Configuration["ALLOWED_API_CRUD_URL"] ?? DataApiUrl + "/CrudUpdate";
    private string BatchUrl => Configuration["ALLOWED_API_BATCH_URL"] ?? DataApiUrl + "/BatchUpdate";
}

<SfGrid TValue="OrdersDetails" Height="348">
    <SfDataManager Url="@DataApiUrl"
                   Adaptor="Adaptors.UrlAdaptor">
    </SfDataManager>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="100"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="100"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

---

## Handling Grid Operations

The `DataManagerRequest` body contains all operation details. Use `DataOperations` helper methods for each operation. **Always get the total count before applying paging.**

### Searching

```csharp
[HttpPost]
[Route("api/[controller]")]
public object Post([FromBody] DataManagerRequest DataManagerRequest)
{
    IQueryable<OrdersDetails> DataSource = GetOrderData().AsQueryable();

    if (DataManagerRequest.Search != null && DataManagerRequest.Search.Count > 0)
    {
        DataSource = DataOperations.PerformSearching(DataSource, DataManagerRequest.Search);
    }

    int totalRecordsCount = DataSource.Count();
    return new { result = DataSource, count = totalRecordsCount };
}
```

```razor
<SfGrid TValue="OrdersDetails" Toolbar="@(new List<string>() { "Search" })" Height="348">
    <SfDataManager Url="@DataApiUrl" Adaptor="Adaptors.UrlAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Filtering

```csharp
if (DataManagerRequest.Where != null && DataManagerRequest.Where.Count > 0)
{
    foreach (var condition in DataManagerRequest.Where)
    {
        foreach (var predicate in condition.predicates)
        {
            DataSource = DataOperations.PerformFiltering(
                DataSource, DataManagerRequest.Where, predicate.Operator);
        }
    }
}
```

```razor
<SfGrid TValue="OrdersDetails" AllowFiltering="true" Height="348">
    <SfDataManager Url="@DataApiUrl" Adaptor="Adaptors.UrlAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Sorting

```csharp
if (DataManagerRequest.Sorted != null && DataManagerRequest.Sorted.Count > 0)
{
    DataSource = DataOperations.PerformSorting(DataSource, DataManagerRequest.Sorted);
}
```

```razor
<SfGrid TValue="OrdersDetails" AllowSorting="true" Height="348">
    <SfDataManager Url="@DataApiUrl" Adaptor="Adaptors.UrlAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Paging

```csharp
// Get count BEFORE applying paging
int totalRecordsCount = DataSource.Count();

if (DataManagerRequest.Skip != 0)
{
    DataSource = DataOperations.PerformSkip(DataSource, DataManagerRequest.Skip);
}
if (DataManagerRequest.Take != 0)
{
    DataSource = DataOperations.PerformTake(DataSource, DataManagerRequest.Take);
}

return new { result = DataSource, count = totalRecordsCount };
```

```razor
<SfGrid TValue="OrdersDetails" AllowPaging="true" Height="348">
    <SfDataManager Url="@DataApiUrl" Adaptor="Adaptors.UrlAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Combined Operations Example

```csharp
[HttpPost]
[Route("api/[controller]")]
public object Post([FromBody] DataManagerRequest dm)
{
    IQueryable<OrdersDetails> DataSource = GetOrderData().AsQueryable();

    if (dm.Search != null && dm.Search.Count > 0)
        DataSource = DataOperations.PerformSearching(DataSource, dm.Search);

    if (dm.Where != null && dm.Where.Count > 0)
        foreach (var c in dm.Where)
            foreach (var p in c.predicates)
                DataSource = DataOperations.PerformFiltering(DataSource, dm.Where, p.Operator);

    if (dm.Sorted != null && dm.Sorted.Count > 0)
        DataSource = DataOperations.PerformSorting(DataSource, dm.Sorted);

    int totalRecordsCount = DataSource.Count();

    if (dm.Skip != 0) DataSource = DataOperations.PerformSkip(DataSource, dm.Skip);
    if (dm.Take != 0) DataSource = DataOperations.PerformTake(DataSource, dm.Take);

    return new { result = DataSource, count = totalRecordsCount };
}
```

---

## CRUD Operations

### CRUDModel Helper Class

Define this helper class to deserialize incoming CRUD request bodies:

```csharp
public class CRUDModel<T> where T : class
{
    public string? action { get; set; }
    public string? keyColumn { get; set; }
    public object? key { get; set; }
    public T? value { get; set; }
    public List<T>? added { get; set; }
    public List<T>? changed { get; set; }
    public List<T>? deleted { get; set; }
    public IDictionary<string, object>? @params { get; set; }
}
```

### Separate URL Mapping

Use `InsertUrl`, `UpdateUrl`, `RemoveUrl` on `SfDataManager` for individual CRUD actions:

```razor
<SfGrid TValue="OrdersDetails"
        Toolbar="@(new List<string>() { "Add", "Edit", "Delete", "Update", "Cancel" })"
        Height="348">
    <SfDataManager Url="@DataApiUrl"
                   InsertUrl="@InsertUrl"
                   UpdateUrl="@UpdateUrl"
                   RemoveUrl="@RemoveUrl"
                   Adaptor="Adaptors.UrlAdaptor">
    </SfDataManager>
    <GridEditSettings AllowEditing="true" AllowDeleting="true" AllowAdding="true"
                      Mode="EditMode.Normal">
    </GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID" IsPrimaryKey="true" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="100"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="100"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

```csharp
[HttpPost]
[Route("api/[controller]/Insert")]
public void Insert([FromBody] CRUDModel<OrdersDetails> newRecord)
{
    if (newRecord.value != null)
        OrdersDetails.GetAllRecords().Insert(0, newRecord.value);
}

[HttpPost]
[Route("api/[controller]/Update")]
public void Update([FromBody] CRUDModel<OrdersDetails> updatedRecord)
{
    var updated = updatedRecord.value;
    if (updated != null)
    {
        var data = OrdersDetails.GetAllRecords().FirstOrDefault(o => o.OrderID == updated.OrderID);
        if (data != null)
        {
            data.CustomerID = updated.CustomerID;
            data.ShipCity = updated.ShipCity;
            data.ShipCountry = updated.ShipCountry;
        }
    }
}

[HttpPost]
[Route("api/[controller]/Remove")]
public void Remove([FromBody] CRUDModel<OrdersDetails> deletedRecord)
{
    int orderId = int.Parse(deletedRecord.key.ToString());
    var data = OrdersDetails.GetAllRecords().FirstOrDefault(o => o.OrderID == orderId);
    if (data != null)
        OrdersDetails.GetAllRecords().Remove(data);
}
```

### Single CrudUrl Method

Use `CrudUrl` to handle all CRUD operations in one endpoint:

```razor
<SfDataManager Url="https://localhost:xxxx/api/grid"
               CrudUrl="https://localhost:xxxx/api/grid/CrudUpdate"
               Adaptor="Adaptors.UrlAdaptor">
</SfDataManager>
```

```csharp
[HttpPost]
[Route("api/[controller]/CrudUpdate")]
public void CrudUpdate([FromBody] CRUDModel<OrdersDetails> request)
{
    if (request.action == "update")
    {
        var existing = OrdersDetails.GetAllRecords()
            .FirstOrDefault(o => o.OrderID == request.value.OrderID);
        if (existing != null)
        {
            existing.CustomerID = request.value.CustomerID;
            existing.ShipCity = request.value.ShipCity;
            existing.ShipCountry = request.value.ShipCountry;
        }
    }
    else if (request.action == "insert")
    {
        OrdersDetails.GetAllRecords().Insert(0, request.value);
    }
    else if (request.action == "remove")
    {
        int id = int.Parse(request.key.ToString());
        var record = OrdersDetails.GetAllRecords().FirstOrDefault(o => o.OrderID == id);
        if (record != null)
            OrdersDetails.GetAllRecords().Remove(record);
    }
}
```

### Batch Operations

Use `BatchUrl` with `EditMode.Batch` for batch editing:

```razor
<SfGrid TValue="OrdersDetails"
        Toolbar="@(new List<string>() { "Add", "Delete", "Update", "Cancel" })"
        Height="348">
    <SfDataManager Url="https://localhost:xxxx/api/grid"
                   BatchUrl="https://localhost:xxxx/api/grid/BatchUpdate"
                   Adaptor="Adaptors.UrlAdaptor">
    </SfDataManager>
    <GridEditSettings AllowEditing="true" AllowDeleting="true" AllowAdding="true"
                      Mode="EditMode.Batch">
    </GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID" IsPrimaryKey="true" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" Width="100"></GridColumn>
        <GridColumn Field="ShipCity" Width="100"></GridColumn>
        <GridColumn Field="ShipCountry" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

```csharp
[HttpPost]
[Route("api/[controller]/BatchUpdate")]
public IActionResult BatchUpdate([FromBody] CRUDModel<OrdersDetails> batchModel)
{
    if (batchModel.added != null)
        foreach (var record in batchModel.added)
            OrdersDetails.GetAllRecords().Insert(0, record);

    if (batchModel.changed != null)
        foreach (var changed in batchModel.changed)
        {
            var existing = OrdersDetails.GetAllRecords()
                .FirstOrDefault(o => o.OrderID == changed.OrderID);
            if (existing != null)
            {
                existing.CustomerID = changed.CustomerID;
                existing.ShipCity = changed.ShipCity;
                existing.ShipCountry = changed.ShipCountry;
            }
        }

    if (batchModel.deleted != null)
        foreach (var deleted in batchModel.deleted)
        {
            var record = OrdersDetails.GetAllRecords()
                .FirstOrDefault(o => o.OrderID == deleted.OrderID);
            if (record != null)
                OrdersDetails.GetAllRecords().Remove(record);
        }

    return new JsonResult(batchModel);
}
```

> Use `EditMode.Batch` in `GridEditSettings` when using `BatchUrl`. All changes are submitted in a single POST.
