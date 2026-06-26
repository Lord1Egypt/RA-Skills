# Data Binding — Syncfusion Blazor DataGrid

## Table of Contents
1. [Local Data](#local-data)
2. [Remote Data](#remote-data)
3. [Custom DataAdaptor](#custom-dataadaptor)
4. [Special Data Types](#special-data-types)

---

## Local Data

Local data is bound by assigning an `IEnumerable` collection (e.g., `List<T>`, `ObservableCollection<T>`, `ExpandoObject`, `DynamicObject`, or `DataTable`) directly to the `DataSource` property.

> When using `DataSource` as `IEnumerable<T>`, `TValue` is inferred. When using `SfDataManager`, `TValue` must be explicitly specified.

### IEnumerable / List

```razor
<SfGrid DataSource="@orderData" AllowPaging="true">
    <GridPageSettings PageSize="5"></GridPageSettings>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true" Width="120" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="150"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="120" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Format="d" Type="ColumnType.DateOnly" Width="130"></GridColumn>
    </GridColumns>
</SfGrid>
@code {
    private List<Order> orderData = new();
    protected override void OnInitialized() => orderData = Order.GetAllRecords();
}
```

> `ColumnType.DateOnly` and `ColumnType.TimeOnly` are supported for `DateOnly`/`TimeOnly` model properties.

### ObservableCollection (Reactive Updates)

The Grid automatically reflects add/remove/update changes via `INotifyCollectionChanged`. For property-level updates, implement `INotifyPropertyChanged` on the model.

```razor
@using System.Collections.ObjectModel
@using System.ComponentModel

<SfGrid DataSource="@Orders">...</SfGrid>
@code {
    public ObservableCollection<Order> Orders = new();
    // Grid auto-refreshes on Add/Remove. For property changes, model must implement INotifyPropertyChanged.
}
```

**AddRange optimization** — extend `ObservableCollection<T>` to batch-add items with a single UI refresh:

```csharp
public class SmartObservableCollection<T> : ObservableCollection<T>
{
    private bool _preventNotification;
    protected override void OnCollectionChanged(NotifyCollectionChangedEventArgs e)
    {
        if (!_preventNotification) base.OnCollectionChanged(e);
    }
    public void AddRange(IEnumerable<T> list)
    {
        _preventNotification = true;
        foreach (var item in list) Add(item);
        _preventNotification = false;
        OnCollectionChanged(new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Reset));
    }
}
```

> When updating the collection from external triggers (e.g., timers), call `StateHasChanged()` to refresh the UI.

### DataTable

DataTable binding requires `TValue="ExpandoObject"` with a `CustomAdaptor`. Bind via `SfDataManager`, **not** directly to `DataSource`. Convert the `DataTable` to `IQueryable<ExpandoObject>` and use `DynamicObjectOperation` / `QueryableOperation` helpers for filtering, sorting, and paging.

```razor
<SfGrid TValue="ExpandoObject" AllowPaging="true" AllowSorting="true" AllowFiltering="true">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Adaptors.CustomAdaptor"></SfDataManager>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="120"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Format="d" Type="ColumnType.Date" Width="130"></GridColumn>
    </GridColumns>
</SfGrid>
@code {
    private static DataTable? ordersTable;

    protected override void OnInitialized() => ordersTable = GetData();

    private static IQueryable ToQueryableCollection(DataTable table)
    {
        var list = new List<ExpandoObject>();
        foreach (DataRow row in table.Rows)
        {
            var expando = (IDictionary<string, object?>)new ExpandoObject();
            foreach (DataColumn col in table.Columns)
                expando[col.ColumnName] = row[col] == DBNull.Value ? null : row[col];
            list.Add((ExpandoObject)expando);
        }
        return list.AsQueryable();
    }

    private class CustomAdaptor : DataAdaptor
    {
        public override object Read(DataManagerRequest dm, string? key = null)
        {
            var dataSource = ToQueryableCollection(ordersTable!);
            if (dm.Search?.Count > 0)
                dataSource = DynamicObjectOperation.PerformSearching(dataSource, dm.Search);
            if (dm.Where?.Count > 0)
                dataSource = DynamicObjectOperation.PerformFiltering(dataSource, dm.Where, dm.Where[0].Operator);
            if (dm.Sorted?.Count > 0)
                dataSource = DynamicObjectOperation.PerformSorting(dataSource, dm.Sorted);
            int count = dataSource.Cast<ExpandoObject>().Count();
            if (dm.Skip != 0) dataSource = QueryableOperation.PerformSkip<object>((IQueryable<object>)dataSource, dm.Skip);
            if (dm.Take != 0) dataSource = QueryableOperation.PerformTake<object>((IQueryable<object>)dataSource, dm.Take);
            return dm.RequiresCounts ? new DataResult { Result = dataSource, Count = count } : (object)dataSource;
        }
    }
}
```

> DataTable also supports grouping (`DataUtil.Group<ExpandoObject>`), aggregates (`DataUtil.PerformAggregation`), and full CRUD via `Insert`/`Update`/`Remove`/`BatchUpdate` overrides on `DataAdaptor`. Use `BatchUpdate`/`BatchUpdateAsync` when edit mode is **Batch**. 📄 [Grouping & Aggregates](data-binding-advanced.md#datatable--grouping-and-aggregates) · [CRUD Operations](data-binding-advanced.md#datatable--crud-operations)

> **List binding use cases:** small/large datasets, preloaded/static data, local CRUD. `ColumnType.DateOnly` and `ColumnType.TimeOnly` are supported for `DateOnly`/`TimeOnly` model properties. 📄 [Full list binding details](data-binding-advanced.md#list-binding--use-cases)

### ExpandoObject (Dynamic Columns)

`ExpandoObject` supports paging, sorting, filtering, and editing. Use `List<ExpandoObject>` bound to `DataSource`. Nested fields use dot (`.`) notation (e.g., `Field="CustomerID.Name"`).

> **Complex/nested fields:** Assign sub-objects to `ExpandoObject` properties and reference them via dot notation (`Field="CustomerID.Name"`). Full CRUD and data operations are supported. 📄 [ExpandoObject complex binding](data-binding-advanced.md#expandoobject-complex-data-binding)

```razor
@using System.Dynamic
<SfGrid DataSource="@orders" AllowPaging="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="150"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
@code {
    private List<ExpandoObject> orders = new();
    protected override void OnInitialized()
    {
        orders = Enumerable.Range(1, 15).Select(i => {
            dynamic o = new ExpandoObject();
            o.OrderID = 1000 + i;
            o.CustomerID = new[] { "ALFKI", "ANANTR", "BOLID" }[Random.Shared.Next(3)];
            o.Freight = Math.Round(2.5 * i, 2);
            return (ExpandoObject)o;
        }).ToList();
    }
}
```

### DynamicObject

Inherit from `DynamicObject`, override `TryGetMember`, `TrySetMember`, and **`GetDynamicMemberNames`** (required for Grid to detect properties for sorting/filtering/editing).

```csharp
// @using System.Dynamic required at top of .razor file
public class DynamicDictionary : DynamicObject
{
    private readonly Dictionary<string, object> _dict = new();
    public override bool TryGetMember(GetMemberBinder binder, out object result)
        => _dict.TryGetValue(binder.Name, out result);
    public override bool TrySetMember(SetMemberBinder binder, object value)
    {
        _dict[binder.Name] = value;
        return true;
    }
    // Required: allows the Grid to discover property names at runtime
    public override IEnumerable<string> GetDynamicMemberNames() => _dict.Keys;
}
```

> Nested fields with dot notation (e.g., `Field="CustomerID.Name"`) are supported for both `ExpandoObject` and `DynamicObject`. Override `GetDynamicMemberNames()` on every nested `DynamicObject` as well. 📄 [DynamicObject complex binding](data-binding-advanced.md#dynamicobject-complex-data-binding)

### Spinner Visibility During Data Loading

Use `ShowSpinnerAsync()` and `HideSpinnerAsync()` to control the built-in spinner:

```razor
<SfGrid @ref="grid" TValue="Order" DataSource="@orders">...</SfGrid>
@code {
    SfGrid<Order> grid;
    async Task LoadData()
    {
        await grid.ShowSpinnerAsync();
        orders = await FetchDataAsync();
        await grid.HideSpinnerAsync();
    }
}
```

### Change DataSource Dynamically

Reassign the `DataSource` property at runtime; the Grid re-renders automatically:

```razor
<SfGrid DataSource="@orders" AllowPaging="true">...</SfGrid>
@code {
    private List<Order> orders = Order.GetAllRecords();
    private void ChangeDataSource() => orders = Order.GetNewRecords();
}
```

---

## Remote Data

Remote data binding is configured via `SfDataManager` with a `Url` and `Adaptor`. Available adaptors: `ODataAdaptor`, `ODataV4Adaptor`, `WebApiAdaptor`, `UrlAdaptor`, `CustomAdaptor`.

> If no adaptor is specified, `ODataAdaptor` is used by default. `TValue` must be explicitly provided on the Grid when using `SfDataManager`.

### SfDataManager with OData v4

```razor
@using Syncfusion.Blazor.Data

<SfGrid TValue="Order" AllowPaging="true">
    <SfDataManager Url="https://services.odata.org/V4/Northwind/Northwind.svc/Orders"
                   Adaptor="Adaptors.ODataV4Adaptor">
    </SfDataManager>
    <GridColumns>
        <GridColumn Field="OrderID"    HeaderText="Order ID"    Width="120" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="150"></GridColumn>
        <GridColumn Field="Freight"    HeaderText="Freight"     Format="C2" Width="120"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

### Enable SfDataManager After Initial Render

Defer remote loading by rendering the Grid without data and adding `SfDataManager` conditionally:

```razor
<SfButton OnClick="@(() => IsEnabled = true)">Enable Data Manager</SfButton>
<SfGrid TValue="Order" AllowPaging="true">
    <GridPageSettings PageSize="10"></GridPageSettings>
    @if (IsEnabled)
    {
        <SfDataManager Url="https://blazor.syncfusion.com/services/production/api/Orders/"
                       Adaptor="Adaptors.WebApiAdaptor">
        </SfDataManager>
    }
    <GridColumns>...</GridColumns>
</SfGrid>
@code { private bool IsEnabled = false; }
```

### Custom Headers (Authentication)

Use the `Headers` property on `SfDataManager` to pass auth tokens or API keys:

```razor
<SfGrid TValue="Order" AllowPaging="true">
    <SfDataManager Url="/api/orders" Adaptor="Adaptors.WebApiAdaptor"
                   Headers="@HeaderData">
    </SfDataManager>
    ...
</SfGrid>
@code {
    private IDictionary<string, string> HeaderData = new Dictionary<string, string>
    {
        { "Authorization", "Bearer your-token" }
    };
}
```

Three ways to authenticate:
- **`Headers` property** — pass a `Dictionary<string,string>` directly on `SfDataManager` (shown above)
- **`DefaultRequestHeaders`** — inject `HttpClient` and set headers in `OnInitializedAsync`
- **`HttpClientInstance` property** — pass a specific pre-configured `HttpClient` instance when multiple named clients are needed

> Typed clients are not supported with `SfDataManager`. Use a custom adaptor for similar functionality. 📄 [Full Auth/Authentication details](data-binding-advanced.md#authorization-and-authentication)

### Query Class (Filtering/Sorting Remote Data)

```razor
<SfGrid TValue="Order" Query="@GridQuery">
    <SfDataManager Url="https://services.odata.org/V4/Northwind/Northwind.svc/Orders"
                   Adaptor="Adaptors.ODataV4Adaptor">
    </SfDataManager>
    ...
</SfGrid>
@code {
    private Query GridQuery = new Query().Where("CustomerID", "equal", "VINET");
}
```

Update `GridQuery` at runtime to dynamically refresh data.

### OData v3 Binding

Use `ODataAdaptor` for OData v3 services (`ODataV4Adaptor` is for v4). 📄 [OData v3 example](data-binding-advanced.md#odata-v3-binding)

```razor
<SfDataManager Url="https://services.odata.org/Northwind/Northwind.svc/Orders"
               Adaptor="Adaptors.ODataAdaptor">
</SfDataManager>
```

### Fetch Data via External Button

Fetch data on demand by calling an API from an external button and assigning the result to `DataSource` — defers loading until a user event. 📄 [Full example](data-binding-advanced.md#fetch-data-via-external-button)

### Offline Mode

Set `Offline="true"` on `SfDataManager` to load all data once and process subsequent grid actions (paging, sorting, filtering) on the client — no further network requests:

```razor
<SfGrid TValue="Order">
    <SfDataManager Url="/api/orders" Adaptor="Adaptors.WebApiAdaptor" Offline="true">
    </SfDataManager>
    ...
</SfGrid>
```

---

## Custom DataAdaptor

> 📄 Full reference: [references/custom-adaptor.md](references/custom-adaptor.md)

Extend `DataAdaptor` and override `Read` (and optionally `Insert`, `Update`, `Remove`, `BatchUpdate`) to fully control data operations. Use the **static** `DataOperations` helpers for searching, filtering, sorting, and paging.

```razor
<SfGrid TValue="Order" AllowPaging="true" AllowSorting="true" AllowFiltering="true">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Adaptors.CustomAdaptor">
    </SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    public static List<Order> Orders { get; set; }

    public class CustomAdaptor : DataAdaptor
    {
        public override object Read(DataManagerRequest dm, string key = null)
        {
            IEnumerable<Order> data = Orders;

            if (dm.Search?.Count > 0)
                data = DataOperations.PerformSearching(data, dm.Search);
            if (dm.Where?.Count > 0)
                data = DataOperations.PerformFiltering(data, dm.Where, dm.Where[0].Operator);
            if (dm.Sorted?.Count > 0)
                data = DataOperations.PerformSorting(data, dm.Sorted);

            int count = data.Count();

            if (dm.Skip != 0) data = DataOperations.PerformSkip(data, dm.Skip);
            if (dm.Take != 0) data = DataOperations.PerformTake(data, dm.Take);

            return dm.RequiresCounts
                ? new DataResult { Result = data, Count = count }
                : (object)data;
        }
    }
}
```

> - Use **static** `DataOperations.PerformSearching/Filtering/Sorting/PerformSkip/PerformTake` — not `new DataOperations().Method(...)`.
> - For `DataTable`-backed adaptors use `DynamicObjectOperation` + `QueryableOperation` instead (see [DataTable](#datatable) section above).
> - Inject services via constructor (register adaptor in DI) or use as a Blazor component with `OwningComponentBase`.
> - For grouping: `DataUtil.Group<T>(...)`. For aggregates: `DataUtil.PerformAggregation(...)`.
> - Pass custom parameters via `Query.AddParams("Key", value)` and read from `dm.Params`.

---

## Special Data Types

### SignalR (Real-time)

```razor
@using Microsoft.AspNetCore.SignalR.Client
@inject NavigationManager NavigationManager
@implements IAsyncDisposable

<SfGrid @ref="grid" DataSource="@orders">...</SfGrid>
@code {
    SfGrid<Order> grid;
    HubConnection hubConnection;
    List<Order> orders = new();

    protected override async Task OnInitializedAsync()
    {
        orders = await LoadOrdersAsync();
        hubConnection = new HubConnectionBuilder()
            .WithUrl(NavigationManager.ToAbsoluteUri("/chathub"))
            .Build();
        hubConnection.On("ReceiveMessage", async () => await grid.Refresh());
        await hubConnection.StartAsync();
    }

    public async ValueTask DisposeAsync()
    {
        if (hubConnection != null) await hubConnection.DisposeAsync();
    }
}
```

> Call `grid.Refresh()` (not `StateHasChanged()`) to force the Grid to re-render after receiving hub messages. Register `Microsoft.AspNetCore.SignalR.Client` NuGet package.

> **Broadcasting changes:** Use `OnActionComplete` (`ActionEventArgs<T>`) to detect Save/Delete actions and call `hubConnection.SendAsync("SendMessage")` so other connected clients refresh in real time. 📄 [SignalR OnActionComplete example](data-binding-advanced.md#signalr--onactioncomplete-integration)

### Binding Data from Excel

Import Excel data using `SfFileUploader` + `Syncfusion.XlsIO` NuGet, parse to a `DataTable`, convert to `List<ExpandoObject>`, and bind to `DataSource`:

```razor
@using Syncfusion.XlsIO
@using Syncfusion.Blazor.Inputs

<SfUploader><UploaderEvents ValueChange="OnChange"></UploaderEvents></SfUploader>
@if (customerList?.Count > 0)
{
    <SfGrid DataSource="@customerList" AllowPaging="true"></SfGrid>
}
@code {
    private List<ExpandoObject> customerList = new();
    private async Task OnChange(UploadChangeEventArgs args)
    {
        // Use ExcelEngine to open workbook, export to DataTable via worksheet.ExportDataTable(...)
        // Convert DataTable rows to ExpandoObject list and assign to customerList
    }
}
```

> 📄 Foreign Key columns (`GridForeignColumn`, `ForeignKeyValue`, `ForeignDataSource`, custom edit/filter templates) are covered in [references/columns.md](references/columns.md).
