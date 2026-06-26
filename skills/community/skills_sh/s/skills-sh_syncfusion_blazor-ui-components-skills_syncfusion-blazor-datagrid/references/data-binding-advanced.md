# Data Binding Advanced — Syncfusion Blazor DataGrid

> Extended topics for data binding. See [data-binding.md](data-binding.md) for the core reference.

---

## Table of Contents
1. [List Binding — Use Cases](#list-binding--use-cases)
2. [ExpandoObject Complex Data Binding](#expandoobject-complex-data-binding)
3. [DynamicObject Complex Data Binding](#dynamicobject-complex-data-binding)
4. [DataTable — Grouping and Aggregates](#datatable--grouping-and-aggregates)
5. [DataTable — CRUD Operations](#datatable--crud-operations)
6. [OData v3 Binding](#odata-v3-binding)
7. [Authorization and Authentication](#authorization-and-authentication)
8. [Fetch Data via External Button](#fetch-data-via-external-button)
9. [SignalR — OnActionComplete Integration](#signalr--onactioncomplete-integration)

---

## List Binding — Use Cases

**List binding is suitable for:**
- Small and large in-memory datasets
- Preloaded or static data
- Local CRUD operations without a server

Each object in the list becomes a row; its properties map to columns. `ColumnType.DateOnly` and `ColumnType.TimeOnly` are supported for `DateOnly`/`TimeOnly` model properties.

```razor
<SfGrid DataSource="@OrderData" AllowPaging="true">
    <GridPageSettings PageSize="5"></GridPageSettings>
    <GridColumns>
        <GridColumn Field="OrderID"   HeaderText="Order ID"   TextAlign="TextAlign.Right" Width="100"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Format="d" Type="ColumnType.DateOnly" Width="130"></GridColumn>
        <GridColumn Field="OrderTime" HeaderText="Order Time" Type="ColumnType.TimeOnly" Width="130"></GridColumn>
        <GridColumn Field="Freight"   HeaderText="Freight"    Format="C2" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>
@code {
    private List<OrderDetails> OrderData = new();
    protected override void OnInitialized() => OrderData = OrderDetails.GetAllRecords();
}
```

---

## ExpandoObject Complex Data Binding

Nested `ExpandoObject` fields are accessed using dot (`.`) notation. Assign sub-objects to properties and reference them as `Field="ParentProp.ChildProp"`. Full CRUD and data operations are supported.

```razor
@using System.Dynamic
<SfGrid DataSource="@orders" AllowPaging="true" AllowFiltering="true" AllowSorting="true" AllowGrouping="true"
        Toolbar="@(new List<string>{ "Add","Edit","Delete","Update","Cancel" })">
    <GridEditSettings AllowAdding="true" AllowDeleting="true" AllowEditing="true"></GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID"           HeaderText="Order ID"      IsPrimaryKey="true" Width="120"></GridColumn>
        <GridColumn Field="CustomerID.Name"   HeaderText="Customer Name" Width="120"></GridColumn>
        <GridColumn Field="Freight"           HeaderText="Freight"       Format="C2" Width="120"></GridColumn>
        <GridColumn Field="ShipCountry.Country" HeaderText="Ship Country" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
@code {
    private List<ExpandoObject> orders = new();
    protected override void OnInitialized()
    {
        orders = Enumerable.Range(1, 75).Select(Index =>
        {
            dynamic Order = new ExpandoObject();
            dynamic CustomerName = new ExpandoObject();
            dynamic CountryName = new ExpandoObject();
            Order.OrderID = 1000 + Index;
            CustomerName.Name = new[] { "ALFKI", "ANANTR", "BOLID" }[Random.Shared.Next(3)];
            Order.CustomerID = CustomerName;
            Order.Freight = Math.Round(2.5 * Index, 2);
            CountryName.Country = new[] { "USA", "UK" }[Random.Shared.Next(2)];
            Order.ShipCountry = CountryName;
            return (ExpandoObject)Order;
        }).ToList();
    }
}
```

> The DataGrid supports data operations and full CRUD even with complex fields in `ExpandoObject` bindings.

---

## DynamicObject Complex Data Binding

Nested `DynamicObject` fields also use dot (`.`) notation. Override `GetDynamicMemberNames()` on every nested `DynamicObject` so the Grid can discover property names at runtime.

```razor
@using System.Dynamic
<SfGrid DataSource="@orders" AllowPaging="true" AllowFiltering="true" AllowSorting="true"
        Toolbar="@(new List<string>{ "Add","Edit","Delete","Update","Cancel" })">
    <GridEditSettings AllowAdding="true" AllowDeleting="true" AllowEditing="true"></GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID"           HeaderText="Order ID"      IsPrimaryKey="true" Width="120"></GridColumn>
        <GridColumn Field="CustomerID.Name"   HeaderText="Customer Name" Width="150"></GridColumn>
        <GridColumn Field="Freight"           HeaderText="Freight"       Format="C2" Width="120"></GridColumn>
        <GridColumn Field="ShipCountry.Country" HeaderText="Ship Country" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
@code {
    private List<DynamicDictionary> orders = new();
    protected override void OnInitialized()
    {
        orders = Enumerable.Range(1, 15).Select(Index =>
        {
            dynamic Order = new DynamicDictionary();
            dynamic CustomerName = new DynamicDictionary();
            dynamic CountryName = new DynamicDictionary();
            Order.OrderID = 1000 + Index;
            CustomerName.Name = new[] { "ALFKI", "ANANTR", "BOLID" }[Random.Shared.Next(3)];
            Order.CustomerID = CustomerName;
            Order.Freight = Math.Round(2.5 * Index, 2);
            CountryName.Country = new[] { "USA", "UK" }[Random.Shared.Next(2)];
            Order.ShipCountry = CountryName;
            return (DynamicDictionary)Order;
        }).ToList();
    }

    private class DynamicDictionary : DynamicObject
    {
        private readonly Dictionary<string, object> _dict = new();
        public override bool TryGetMember(GetMemberBinder b, out object r) => _dict.TryGetValue(b.Name, out r);
        public override bool TrySetMember(SetMemberBinder b, object v) { _dict[b.Name] = v; return true; }
        public override IEnumerable<string> GetDynamicMemberNames() => _dict.Keys;
    }
}
```

> The DataGrid supports data operations and full CRUD even with complex fields in `DynamicObject` bindings.

---

## DataTable — Grouping and Aggregates

Use `DataUtil.Group<ExpandoObject>` and `DataUtil.PerformAggregation` inside the custom adaptor's `Read` override.

```razor
<SfGrid TValue="ExpandoObject" AllowPaging="true" AllowGrouping="true">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Adaptors.CustomAdaptor"></SfDataManager>
    <GridAggregates>
        <GridAggregate>
            <GridAggregateColumns>
                <GridAggregateColumn Field="Freight" Type="AggregateType.Sum" Format="C2">
                    <FooterTemplate>
                        @{ var agg = (context as AggregateTemplateContext); }
                        <div>Sum: @agg.Sum</div>
                    </FooterTemplate>
                </GridAggregateColumn>
            </GridAggregateColumns>
        </GridAggregate>
    </GridAggregates>
    <GridColumns>
        <GridColumn Field="OrderID"    HeaderText="Order ID"    Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer"    Width="120"></GridColumn>
        <GridColumn Field="Freight"    HeaderText="Freight"     Format="C2" Width="100" AllowGrouping="false"></GridColumn>
    </GridColumns>
</SfGrid>
@code {
    private static DataTable? ordersTable;
    private static IQueryable? dataSource;

    protected override void OnInitialized() => ordersTable = GetData();

    private class CustomAdaptor : DataAdaptor
    {
        public override object Read(DataManagerRequest request, string? key = null)
        {
            dataSource = ToQueryableCollection(ordersTable!);
            int count = dataSource.Cast<ExpandoObject>().Count();

            if (request.Skip != 0) dataSource = QueryableOperation.PerformSkip<object>((IQueryable<object>)dataSource, request.Skip);
            if (request.Take != 0) dataSource = QueryableOperation.PerformTake<object>((IQueryable<object>)dataSource, request.Take);

            IDictionary<string, object> aggregates = new Dictionary<string, object>();
            if (request.Aggregates != null)
                aggregates = DataUtil.PerformAggregation(dataSource, request.Aggregates);

            if (request.Group != null)
            {
                IEnumerable result = (IEnumerable)dataSource;
                foreach (var group in request.Group)
                    result = DataUtil.Group<ExpandoObject>(result, group, request.Aggregates, 0, request.GroupByFormatter);
                return request.RequiresCounts
                    ? new DataResult { Result = result, Count = count, Aggregates = aggregates }
                    : (object)dataSource;
            }

            return request.RequiresCounts
                ? new DataResult { Result = dataSource, Count = count, Aggregates = aggregates }
                : (object)dataSource;
        }
    }
}
```

---

## DataTable — CRUD Operations

Override `Insert`, `Update`, `Remove`, and `BatchUpdate` (for batch editing) on `DataAdaptor` to mutate the `DataTable` in memory.

```csharp
public override object Insert(DataManager request, object value, string key)
{
    var newRow = ordersTable!.NewRow();
    foreach (var item in (ExpandoObject)value)
        newRow[item.Key] = item.Value ?? DBNull.Value;
    ordersTable.Rows.InsertAt(newRow, 0);
    return value;
}

public override object Remove(DataManager request, object value, string keyField, string key)
{
    var row = ordersTable!.Rows.Cast<DataRow>()
        .FirstOrDefault(r => r[keyField].Equals(value));
    if (row != null) ordersTable.Rows.Remove(row);
    return value;
}

public override object Update(DataManager request, object value, string keyField, string key)
{
    var data = (IDictionary<string, object>)value;
    var row = ordersTable!.Rows.Cast<DataRow>()
        .FirstOrDefault(r => r[keyField].Equals(data[keyField]));
    if (row != null)
        foreach (DataColumn col in ordersTable.Columns)
            row[col.ColumnName] = data[col.ColumnName] ?? col.DefaultValue;
    return value;
}

// BatchUpdate handles batch editing (Add/Edit/Delete in one transaction)
public override object BatchUpdate(DataManager request, object changed, object added,
    object deleted, string keyField, string key, int? dropIndex)
{
    // process changed / added / deleted collections against ordersTable
    return ordersTable!;
}
```

> Use `BatchUpdate`/`BatchUpdateAsync` when the Grid's edit mode is set to **Batch**.

---

## OData v3 Binding

Use `ODataAdaptor` for OData v3 services and `ODataV4Adaptor` for v4 services.

```razor
<SfGrid TValue="Order" AllowPaging="true">
    <SfDataManager Url="https://services.odata.org/Northwind/Northwind.svc/Orders"
                   Adaptor="Adaptors.ODataAdaptor">
    </SfDataManager>
    <GridColumns>
        <GridColumn Field="OrderID"     HeaderText="Order ID"    Width="120" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="CustomerID"  HeaderText="Customer"    Width="150"></GridColumn>
        <GridColumn Field="Freight"     HeaderText="Freight"     Format="C2" Width="120"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

| Adaptor | Protocol |
|---|---|
| `ODataAdaptor` | OData v3 |
| `ODataV4Adaptor` | OData v4 |

---

## Authorization and Authentication

Three ways to pass auth tokens to `SfDataManager`:

**Option 1 — `Headers` property** (simplest):
```razor
<SfDataManager Url="/api/orders" Adaptor="Adaptors.WebApiAdaptor"
               Headers="@(new Dictionary<string,string>{ {"Authorization","Bearer <token>"} })">
</SfDataManager>
```

**Option 2 — Inject `HttpClient` and set `DefaultRequestHeaders`**:
```csharp
@inject HttpClient _httpClient
protected override async Task OnInitializedAsync()
{
    _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {tokenValue}");
}
```

**Option 3 — Pre-configured `HttpClient` in `Program.cs`** (register *before* `AddSyncfusionBlazor()`):
```csharp
builder.Services.AddHttpClient("MyClient", client => {
    client.BaseAddress = new Uri("https://api.example.com/");
    client.DefaultRequestHeaders.Add("Authorization", "Bearer <token>");
});
```
Then pass via `HttpClientInstance` property:
```razor
<SfDataManager HttpClientInstance="@myClient" Url="/api/orders" Adaptor="Adaptors.WebApiAdaptor">
</SfDataManager>
```

> **Typed clients** are not supported with `SfDataManager`. Use a custom adaptor for similar functionality.

---

## Fetch Data via External Button

Fetch data on demand and assign to `DataSource` — defers loading until a specific user event.

```razor
<SfButton OnClick="ExecuteQuery" CssClass="e-primary">Execute Query</SfButton>
<p>@StatusMessage</p>

<SfGrid TValue="OrdersDetails" DataSource="@Orders" AllowPaging="true">
    <GridColumns>
        <GridColumn Field="OrderID"     HeaderText="Order ID"    Width="120" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="CustomerID"  HeaderText="Customer ID" Width="160"></GridColumn>
        <GridColumn Field="Freight"     HeaderText="Freight"     Format="C2" Width="150"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    @inject HttpClient Http
    private string StatusMessage = "";
    private List<OrdersDetails> Orders = new();

    private async Task ExecuteQuery()
    {
        StatusMessage = "Fetching data...";
        var response = await Http.GetFromJsonAsync<GridResponse<OrdersDetails>>("https://localhost:xxxx/api/Grid");
        if (response != null)
        {
            Orders = response.Items;
            StatusMessage = $"Loaded {response.Count} records.";
        }
    }

    public class GridResponse<T> { public List<T> Items { get; set; } public int Count { get; set; } }
}
```

---

## SignalR — OnActionComplete Integration

Use `OnActionComplete` (`ActionEventArgs<T>`) to broadcast changes to other clients after Save or Delete, so their Grids refresh in real time.

```razor
<SfGrid @ref="grid" DataSource="@orderData" Toolbar="@(new List<string>{"Add","Edit","Delete","Update","Cancel"})">
    <GridEvents OnActionComplete="ActionComplete" TValue="OrderDetails"></GridEvents>
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"></GridEditSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
@code {
    private async Task ActionComplete(ActionEventArgs<OrderDetails> args)
    {
        if (args.RequestType == Syncfusion.Blazor.Grids.Action.Save)
        {
            await OrderService.UpdateAsync(args.Data);
            if (IsConnected) await hubConnection!.SendAsync("SendMessage");
        }
        if (args.RequestType == Syncfusion.Blazor.Grids.Action.Delete)
        {
            orderData = OrderService.DeleteAsync(args.Data);
            if (IsConnected) await hubConnection!.SendAsync("SendMessage");
        }
    }
}
```

> `grid.Refresh()` is called on the *receiving* client (via `hubConnection.On("ReceiveMessage", ...)`) — not on the sender.
