# CustomAdaptor — Syncfusion Blazor DataGrid

## Table of Contents
1. [Overview](#overview)
2. [When to Use CustomAdaptor](#when-to-use-customadaptor)
3. [DataAdaptor Abstract Class](#dataadaptor-abstract-class)
4. [Basic Data Binding](#basic-data-binding)
5. [Injecting Services](#injecting-services)
6. [Custom Adaptor as a Component](#custom-adaptor-as-a-component)
7. [Handling Grid Operations](#handling-grid-operations)
   - [Searching](#searching)
   - [Filtering](#filtering)
   - [Sorting](#sorting)
   - [Paging](#paging)
   - [Grouping](#grouping)
   - [Aggregates](#aggregates)
8. [CRUD Operations](#crud-operations)
9. [Passing Additional Parameters](#passing-additional-parameters)

---

## Overview

`CustomAdaptor` provides **complete manual control** over data operations. You extend the `DataAdaptor` abstract class and override its methods to handle read, insert, update, delete, and batch operations yourself. There is no automatic query translation — every operation is implemented with your own logic.

**Adaptor enum:** `Adaptors.CustomAdaptor`  
**Usage:** `AdaptorInstance="@typeof(CustomAdaptor)"`  
**NuGet:** `Syncfusion.Blazor.Data` (for `DataAdaptor`, `DataOperations`, `DataManagerRequest`)

## Security Considerations

When building a `CustomAdaptor` you have full control — with that power comes responsibility. Follow these rules to avoid introducing remote-content or configuration injection risks:

- **Do not use user-supplied endpoints:** If your `CustomAdaptor` forwards requests to remote services, use operator-configured endpoints (environment variables or secure config) rather than URLs provided by end users.
- **Validate `dm.Params`:** If you accept custom parameters via `Query.AddParams`, validate keys and values against an allowlist and reject unexpected entries. Do not treat `dm.Params` as executable configuration.
- **Whitelist fields and operations:** When applying filters, sorting, or grouping, restrict to known model fields and supported operators. Reject or sanitize unknown expressions.
- **Sanitize external content:** If the adaptor ingests textual data from third-party sources, sanitize or escape content before using it in logic or rendering.
- **Prefer server-side proxies:** When integrating third-party APIs, call them from a server-side proxy that enforces TLS, authentication, rate limits, and content-type checks. Normalize responses before the adaptor consumes them.
- **Log and audit sources:** Record provenance, the configured endpoint, and request metadata for any external data source.

Implement small defensive checks inside `Read` (e.g., strict parsing of `dm.Where`, `dm.Sorted`, numeric validation for `dm.Skip`/`dm.Take`) rather than trusting incoming requests.

---

## When to Use CustomAdaptor

Use `CustomAdaptor` when:
- You need full control over every data operation (custom caching, transformation, multi-source merging)
- Your data comes from a non-HTTP source (in-memory service, SignalR, gRPC, local DB)
- You want to inject Blazor services (e.g., Entity Framework `DbContext`) directly into the adaptor
- You need to handle aggregates, grouping, or complex business logic during read operations
- None of the other adaptors (`ODataV4`, `WebApi`, `Url`) fit your architecture

---

## DataAdaptor Abstract Class

The `DataAdaptor` abstract class exposes synchronous and asynchronous method pairs you can override:

```csharp
public abstract class DataAdaptor
{
    // Read operations
    public virtual object Read(DataManagerRequest dataManagerRequest, string key = null)
    public virtual Task<object> ReadAsync(DataManagerRequest dataManagerRequest, string key = null)

    // Insert operations
    public virtual object Insert(DataManager dataManager, object data, string key)
    public virtual Task<object> InsertAsync(DataManager dataManager, object data, string key)

    // Remove operations
    public virtual object Remove(DataManager dataManager, object data, string keyField, string key)
    public virtual Task<object> RemoveAsync(DataManager dataManager, object data, string keyField, string key)

    // Update operations
    public virtual object Update(DataManager dataManager, object data, string keyField, string key)
    public virtual Task<object> UpdateAsync(DataManager dataManager, object data, string keyField, string key)

    // Batch CRUD operations
    public virtual object BatchUpdate(DataManager dataManager, object changedRecords,
        object addedRecords, object deletedRecords, string keyField, string key, int? dropIndex)
    public virtual Task<object> BatchUpdateAsync(DataManager dataManager, object changedRecords,
        object addedRecords, object deletedRecords, string keyField, string key, int? dropIndex)
}
```

**`DataManagerRequest` key properties:**

| Property | Type | Description |
|----------|------|-------------|
| `Search` | `List<SearchFilter>` | Search criteria |
| `Where` | `List<WhereFilter>` | Filter conditions |
| `Sorted` | `List<Sort>` | Sort columns and directions |
| `Skip` | `int` | Records to skip (paging) |
| `Take` | `int` | Records to take (paging) |
| `Group` | `List<string>` | Group-by fields |
| `Aggregates` | `List<Aggregate>` | Aggregate definitions |
| `RequiresCounts` | `bool` | Whether total count is needed |
| `Params` | `IDictionary` | Custom parameters |

---

## Basic Data Binding

Override `Read` to return data. When `dm.RequiresCounts` is `true`, return a `DataResult`:

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Data
@using Syncfusion.Blazor.Grids

<SfGrid TValue="Order" AllowSorting="true" AllowFiltering="true" AllowPaging="true">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)"
                   Adaptor="Adaptors.CustomAdaptor">
    </SfDataManager>
    <GridPageSettings PageSize="8"></GridPageSettings>
    <GridColumns>
        <GridColumn Field="@nameof(Order.OrderID)" HeaderText="Order ID"
                    IsPrimaryKey="true" TextAlign="TextAlign.Right" Width="140">
        </GridColumn>
        <GridColumn Field="@nameof(Order.CustomerID)" HeaderText="Customer Name" Width="150"></GridColumn>
        <GridColumn Field="@nameof(Order.Freight)" HeaderText="Freight" Format="C2" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    public static List<Order> Orders { get; set; }

    protected override void OnInitialized()
    {
        Orders = Enumerable.Range(1, 75).Select(x => new Order
        {
            OrderID = 1000 + x,
            CustomerID = (new string[] { "ALFKI", "ANANTR", "ANTON", "BLONP", "BOLID" })[new Random().Next(5)],
            Freight = 2.1 * x,
        }).ToList();
    }

    public class Order
    {
        public int OrderID { get; set; }
        public string CustomerID { get; set; }
        public double Freight { get; set; }
    }

    public class CustomAdaptor : DataAdaptor
    {
        public override object Read(DataManagerRequest dm, string key = null)
        {
            IEnumerable<Order> DataSource = Orders;

            if (dm.Search != null && dm.Search.Count > 0)
                DataSource = DataOperations.PerformSearching(DataSource, dm.Search);
            if (dm.Sorted != null && dm.Sorted.Count > 0)
                DataSource = DataOperations.PerformSorting(DataSource, dm.Sorted);
            if (dm.Where != null && dm.Where.Count > 0)
                DataSource = DataOperations.PerformFiltering(DataSource, dm.Where, dm.Where[0].Operator);

            int count = DataSource.Cast<Order>().Count();

            if (dm.Skip != 0) DataSource = DataOperations.PerformSkip(DataSource, dm.Skip);
            if (dm.Take != 0) DataSource = DataOperations.PerformTake(DataSource, dm.Take);

            return dm.RequiresCounts
                ? new DataResult() { Result = DataSource, Count = count }
                : (object)DataSource;
        }
    }
}
```

> If `dm.RequiresCounts` is `false`, return the collection directly — not `DataResult`. The grid uses `RequiresCounts` when paging or aggregates are enabled.

---

## Injecting Services

Register services in `Program.cs` and inject them via the constructor:

```csharp
// Program.cs
builder.Services.AddSingleton<OrderDataAccessLayer>();
builder.Services.AddScoped<CustomAdaptor>();
```

```razor
@code {
    public class CustomAdaptor : DataAdaptor
    {
        public OrderDataAccessLayer context { get; set; }

        public CustomAdaptor(OrderDataAccessLayer _context)
        {
            context = _context;
        }

        public override object Read(DataManagerRequest dm, string key = null)
        {
            IEnumerable<Order> DataSource = context.GetAllOrders();

            if (dm.Search != null && dm.Search.Count > 0)
                DataSource = DataOperations.PerformSearching(DataSource, dm.Search);
            if (dm.Sorted != null && dm.Sorted.Count > 0)
                DataSource = DataOperations.PerformSorting(DataSource, dm.Sorted);
            if (dm.Where != null && dm.Where.Count > 0)
                DataSource = DataOperations.PerformFiltering(DataSource, dm.Where, dm.Where[0].Operator);

            int count = DataSource.Cast<Order>().Count();

            if (dm.Skip != 0) DataSource = DataOperations.PerformSkip(DataSource, dm.Skip);
            if (dm.Take != 0) DataSource = DataOperations.PerformTake(DataSource, dm.Take);

            return dm.RequiresCounts
                ? new DataResult() { Result = DataSource, Count = count }
                : (object)DataSource;
        }
    }
}
```

---

## Custom Adaptor as a Component

When you need Blazor lifecycle and scoped services, extend `OwningComponentBase<T>` instead of just `DataAdaptor`. Create a separate `.razor` component:

```csharp
// Register in Program.cs
builder.Services.AddScoped<Order>();
```

```razor
{{!-- In parent grid --}}
<SfGrid TValue="Order" AllowSorting="true" AllowFiltering="true" AllowPaging="true">
    <SfDataManager Adaptor="Adaptors.CustomAdaptor">
        <CustomAdaptorComponent></CustomAdaptorComponent>
    </SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

```csharp
// CustomAdaptorComponent.razor — extends DataAdaptor<T> for a single service
@inherits DataAdaptor<Order>

<CascadingValue Value="@this">
    @ChildContent
</CascadingValue>

@code {
    [Parameter]
    [JsonIgnore]
    public RenderFragment ChildContent { get; set; }

    public override object Read(DataManagerRequest dm, string key = null)
    {
        IEnumerable<Order> DataSource = (IEnumerable<Order>)Service.GetAllRecords();

        if (dm.Search != null && dm.Search.Count > 0)
            DataSource = DataOperations.PerformSearching(DataSource, dm.Search);
        if (dm.Sorted != null && dm.Sorted.Count > 0)
            DataSource = DataOperations.PerformSorting(DataSource, dm.Sorted);
        if (dm.Where != null && dm.Where.Count > 0)
            DataSource = DataOperations.PerformFiltering(DataSource, dm.Where, dm.Where[0].Operator);

        int count = DataSource.Cast<Order>().Count();

        if (dm.Skip != 0) DataSource = DataOperations.PerformSkip(DataSource, dm.Skip);
        if (dm.Take != 0) DataSource = DataOperations.PerformTake(DataSource, dm.Take);

        return dm.RequiresCounts
            ? new DataResult() { Result = DataSource, Count = count }
            : (object)DataSource;
    }
}
```

> Use `DataAdaptor` (non-generic) with `OwningComponentBase` to request multiple services via `ScopedServices.GetService(typeof(T))`.

---

## Handling Grid Operations

### Searching

```csharp
if (dm.Search != null && dm.Search.Count > 0)
    DataSource = DataOperations.PerformSearching(DataSource, dm.Search);
```

```razor
<SfGrid TValue="Order" Toolbar="@(new List<string>() { "Search" })">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Adaptors.CustomAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Filtering

```csharp
if (dm.Where != null && dm.Where.Count > 0)
    DataSource = DataOperations.PerformFiltering(DataSource, dm.Where, dm.Where[0].Operator);
```

```razor
<SfGrid TValue="Order" AllowFiltering="true">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Adaptors.CustomAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Sorting

```csharp
if (dm.Sorted != null && dm.Sorted.Count > 0)
    DataSource = DataOperations.PerformSorting(DataSource, dm.Sorted);
```

```razor
<SfGrid TValue="Order" AllowSorting="true">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Adaptors.CustomAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Paging

```csharp
// Count BEFORE applying skip/take
int count = DataSource.Cast<Order>().Count();
if (dm.Skip != 0) DataSource = DataOperations.PerformSkip(DataSource, dm.Skip);
if (dm.Take != 0) DataSource = DataOperations.PerformTake(DataSource, dm.Take);
```

```razor
<SfGrid TValue="Order" AllowPaging="true">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Adaptors.CustomAdaptor"></SfDataManager>
    <GridPageSettings PageSize="8"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Grouping

Use `DataUtil.Group<T>` to apply grouping:

```csharp
DataResult DataObject = new DataResult();

if (dm.Group != null)
{
    IEnumerable ResultData = DataSource.ToList();
    foreach (var group in dm.Group)
        ResultData = DataUtil.Group<Order>(ResultData, group, dm.Aggregates, 0, dm.GroupByFormatter);

    DataObject.Result = ResultData;
    DataObject.Count = count;
    return dm.RequiresCounts ? DataObject : (object)ResultData;
}
```

```razor
<SfGrid TValue="Order" AllowGrouping="true">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Adaptors.CustomAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Aggregates

Use `DataUtil.PerformAggregation` inside a `DataResult`:

```csharp
DataResult DataObject = new DataResult();

if (dm.Aggregates != null)
{
    DataObject.Result = DataSource;
    DataObject.Count = count;
    DataObject.Aggregates = DataUtil.PerformAggregation(DataSource, dm.Aggregates);
    return dm.RequiresCounts ? DataObject : (object)DataSource;
}
```

---

## CRUD Operations

Override `Insert`, `Remove`, `Update`, and `BatchUpdate` for full CRUD support:

```csharp
public class CustomAdaptor : DataAdaptor
{
    // Read (same as above)
    public override object Read(DataManagerRequest dm, string key = null) { ... }

    // Insert
    public override object Insert(DataManager dm, object value, string key)
    {
        Orders.Insert(0, value as Order);
        return value;
    }

    // Remove
    public override object Remove(DataManager dm, object value, string keyField, string key)
    {
        Orders.Remove(Orders.FirstOrDefault(o => o.OrderID == int.Parse(value.ToString())));
        return value;
    }

    // Update
    public override object Update(DataManager dm, object value, string keyField, string key)
    {
        var data = Orders.FirstOrDefault(o => o.OrderID == (value as Order).OrderID);
        if (data != null)
        {
            data.CustomerID = (value as Order).CustomerID;
            data.Freight = (value as Order).Freight;
        }
        return value;
    }

    // Batch Update (for EditMode.Batch)
    public override object BatchUpdate(DataManager dm, object Changed, object Added,
        object Deleted, string KeyField, string Key, int? dropIndex)
    {
        if (Changed != null)
            foreach (var record in (IEnumerable<Order>)Changed)
            {
                var val = Orders.FirstOrDefault(o => o.OrderID == record.OrderID);
                if (val != null) { val.CustomerID = record.CustomerID; val.Freight = record.Freight; }
            }

        if (Added != null)
            foreach (var record in (IEnumerable<Order>)Added)
                Orders.Add(record);

        if (Deleted != null)
            foreach (var record in (IEnumerable<Order>)Deleted)
                Orders.Remove(Orders.FirstOrDefault(o => o.OrderID == record.OrderID));

        return Orders;
    }
}
```

```razor
<SfGrid TValue="Order" AllowSorting="true" AllowPaging="true"
        Toolbar="@(new List<string>() { "Add", "Delete", "Update", "Cancel" })">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Adaptors.CustomAdaptor"></SfDataManager>
    <GridEditSettings AllowEditing="true" AllowDeleting="true" AllowAdding="true"
                      Mode="EditMode.Normal">
    </GridEditSettings>
    <GridColumns>
        <GridColumn Field="@nameof(Order.OrderID)" IsPrimaryKey="true" Width="140"></GridColumn>
        <GridColumn Field="@nameof(Order.CustomerID)" Width="150"></GridColumn>
        <GridColumn Field="@nameof(Order.Freight)" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

---

## Passing Additional Parameters

Use `Query.AddParams` on the grid and read them from `dm.Params` in the adaptor:

```razor
<SfGrid TValue="Order" Query="@Query">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Adaptors.CustomAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    public Query Query = new Query().AddParams("Code", 10);
}
```

```csharp
public override object Read(DataManagerRequest dm, string key = null)
{
    // Access custom parameters
    if (dm.Params != null && dm.Params.Count > 0)
    {
        var customCode = dm.Params["Code"]; // e.g., 10
        // Use customCode for filtering, authorization, or business logic
    }

    IEnumerable<Order> DataSource = Orders;
    // ... rest of read logic
}
```

> Use `AddParams` to pass user roles, tenant IDs, auth tokens, or any context-specific data to the adaptor without modifying the grid's column/filter state.
