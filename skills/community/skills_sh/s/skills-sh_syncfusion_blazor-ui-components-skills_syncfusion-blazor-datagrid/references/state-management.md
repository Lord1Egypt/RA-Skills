# State Management — Syncfusion Blazor DataGrid

## Table of Contents
- [Enable State Persistence](#enable-state-persistence)
- [What is Persisted](#what-is-persisted)
- [Restore initial Blazor DataGrid state](#restore-initial-blazor-datagrid-state)
  - [Using ResetPersistDataAsync](#using-resetpersistdataasync)
  - [Clearing Local Storage](#clearing-local-storage)
- [Get and Set State Manually](#get-and-set-state-manually)
- [Restore to specific state version](#restore-to-specific-state-version)
- [Restore to previous state](#restore-to-previous-state)
- [Maintaining custom query in a persistent state](#maintaining-custom-query-in-a-persistent-state)
- [Get or set local storage value](#get-or-set-local-storage-value)
- [Server-Side State Persistence](#server-side-state-persistence)
  - [Save and Load via API](#save-and-load-via-api)
  - [Minimal API Example (Server)](#minimal-api-example-server)
  - [Combining with `EnablePersistence`](#combining-with-enablepersistence)
- [SignalR Buffer Increase](#signalr-buffer-increase)

## Enable State Persistence

Persists grid settings (paging, sorting, filtering, grouping, column visibility) in browser `localStorage`:

```razor
<SfGrid ID="Grid" DataSource="@Orders" EnablePersistence="true"
        AllowPaging="true" AllowSorting="true"
        AllowFiltering="true" AllowGrouping="true">
    <GridColumns>...</GridColumns>
</SfGrid>
```

> **`ID` is required** — state is stored with a key that combines the **component name** and its assigned **ID** (e.g., component name `Grid` + ID `OrderDetails` = key `gridOrderDetails`). Without it, persistence is unreliable.

## What is Persisted

| Feature | Persisted | Not Persisted |
|---|---|---|
| **PageSettings** | CurrentPage, PageCount, PageSize, EnableQueryString, EnableExternalMessage | Template |
| **GroupSettings** | AllowReordering, DisablePageWiseAggregates, ShowDropArea, ShowGroupedColumn, ShowToggleButton, ShowUngroupButton, EnableLazyLoading | CaptionTemplate, ExpandAllGroups, PersistGroupState |
| **Columns** | AllowAdding, AllowEditing, AllowFiltering, AllowGrouping, AllowReordering, AllowResizing, AllowSearching, AllowSorting, AutoFit, DisableHtmlEncode, DisplayAsCheckBox, EditType, EnableGroupByFormat, Field, HeaderText, HeaderTextAlign, HideAtMedia, Index, OriginalIndex, IsFrozen, IsIdentity, IsPrimaryKey, FixedColumn, MaxWidth, MinWidth, ShowColumnMenu, ShowInColumnChooser, TextAlign, Freeze, Type, Uid, Visible, Width | EditorSettings, FilterEditorSettings, EditTemplate, FilterTemplate, HeaderTemplate, SortComparer, Template, AutoSpan, FilterItemTemplate |
| **FilterSettings** | All properties | None |
| **SearchSettings** | All properties | None |
| **SortSettings** | All properties | None |

> Data source must be reloaded on page refresh — only configuration is persisted.

> When a row is initially selected using the `SelectedRowIndex` property, only that configured value is persisted. Changes made through UI interactions are not retained after a reload.

## Restore initial Blazor DataGrid state

The grid provides two ways to restore it to its original configuration:

1. **Using `ResetPersistDataAsync` Method** — Clears the persisted state from local storage and restores the grid to its original property values.
2. **Clearing Local Storage** — Removes the stored state directly from the browser's local storage and reloads the grid with its initial configuration.

### Using ResetPersistDataAsync

Clears stored state and restores the grid to its original configuration:

```razor
<SfButton OnClick="ResetGrid">Restore Defaults</SfButton>

@code {
    SfGrid<Order> Grid;

    async Task ResetGrid()
    {
        await Grid.ResetPersistDataAsync();
    }
}
```

### Clearing Local Storage

Clear the local storage entry directly to remove all stored configuration and reload the grid with initial settings:

```razor
@inject IJSRuntime JS

<SfButton OnClick="RestoreGridState">Restore Grid State</SfButton>
<SfGrid ID="OrderDetails" @ref="Grid" DataSource="@Orders"
        EnablePersistence="true" AllowPaging="true" AllowFiltering="true">
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    async Task RestoreGridState()
    {
        await Grid.ResetPersistDataAsync();
        await JS.InvokeVoidAsync("localStorage.setItem", "gridOrderDetails", "");
        await JS.InvokeVoidAsync("location.reload");
    }
}
```

> The localStorage key follows the pattern `{componentName}{ID}` (e.g., `gridOrderDetails` for a grid with ID `OrderDetails`).

## Get and Set State Manually

Save and restore state programmatically (e.g., per user profile, versioned layouts):

```razor
@code {
    SfGrid<Order> Grid;
    string SavedState;

    // Save current state
    async Task SaveState()
    {
        SavedState = await Grid.GetPersistDataAsync();
        // Store SavedState in DB or localStorage via IJSRuntime
    }

    // Restore saved state
    async Task RestoreState()
    {
        if (!string.IsNullOrEmpty(SavedState))
            await Grid.SetPersistDataAsync(SavedState);
    }
}
```

## Restore to specific state version

Switch between saved layouts for the same grid using the `PersistenceKey` property. Set `PersistenceKey` dynamically based on the selected version (e.g., `gridOrderDetails_v1`). This ensures each version maintains a distinct state in `localStorage`:

```razor
@inject IJSRuntime JS

@if (!string.IsNullOrEmpty(CurrentVersion))
{
    <SfGrid ID="OrderDetails" @ref="Grid" DataSource="@Orders"
            EnablePersistence="true"
            PersistenceKey="@($"gridOrderDetails_{CurrentVersion}")"
            AllowPaging="true" AllowFiltering="true"
            AllowSorting="true" AllowGrouping="true">
        <GridColumns>...</GridColumns>
    </SfGrid>
}

@code {
    SfGrid<Order> Grid;
    string CurrentVersion = "v.0";
    string Message;

    async Task ChangeVersion(string version)
    {
        // Save current state to localStorage before switching
        if (Grid != null)
        {
            var currentData = await Grid.GetPersistDataAsync();
            await JS.InvokeVoidAsync("localStorage.setItem",
                $"gridOrderDetails_{CurrentVersion}", currentData);
        }

        // Switch to new version
        CurrentVersion = version;

        // Load persisted state for the selected version, if available
        var saved = await JS.InvokeAsync<string>("localStorage.getItem",
            $"gridOrderDetails_{version}");

        if (!string.IsNullOrEmpty(saved))
        {
            await Grid.SetPersistDataAsync(saved);
            Message = $"Grid state restored to {version}";
        }
        else
        {
            Message = $"No saved state found for {version}. New state will be stored.";
        }

        StateHasChanged();
    }
}
```

> `PersistenceKey` overrides the default localStorage key, enabling distinct state storage per version.

## Restore to previous state

Save and restore the grid's current state using local storage. This feature preserves configurations such as **column order**, **sorting**, **filtering**, **grouping**, and **paging**, allowing a return to a previously saved state.

**How It Works**

* The `GetPersistDataAsync()` method retrieves the current state of the Grid as a string. This string can be stored in local storage or transmitted to a server.
* The `SetPersistDataAsync()` method applies a previously saved state to the Grid.
* If no saved state exists, the Grid remains in the current configuration.

```razor
@inject IJSRuntime JS

<SfButton CssClass="e-success" OnClick="SaveGridState">Save</SfButton>
<SfButton CssClass="e-danger" OnClick="RestoreGridState">Restore</SfButton>

<div style="text-align: center; color: red">
    <span>@Message</span>
</div>

<SfGrid @ref="Grid" DataSource="@Orders" Height="300" 
        AllowPaging="true" AllowSorting="true" AllowFiltering="true" 
        AllowGrouping="true" EnablePersistence="true" 
        Toolbar="@(new List<string> { "Edit", "Update", "Cancel" })">
    <GridFilterSettings Type="FilterType.Menu"></GridFilterSettings>
    <GridEditSettings AllowEditing="true"></GridEditSettings>
    <GridEvents OnActionBegin="OnActionBegin" TValue="OrderDetails"></GridEvents>
    <GridColumns>
        <GridColumn Field=@nameof(OrderDetails.OrderID) HeaderText="Order ID" 
                    TextAlign="TextAlign.Right" Width="140" IsPrimaryKey="true" 
                    ValidationRules="@(new ValidationRules{ Required=true, Number=true})" />
        <GridColumn Field=@nameof(OrderDetails.CustomerID) HeaderText="Customer ID" 
                    Width="140" ValidationRules="@(new ValidationRules{ Required=true})"/>
        <GridColumn Field=@nameof(OrderDetails.Freight) HeaderText="Freight" 
                    Width="140" Format="C2" TextAlign="TextAlign.Right" 
                    ValidationRules="@(new ValidationRules{ Required=true })"/>
        <GridColumn Field=@nameof(OrderDetails.OrderDate) HeaderText="Order Date" 
                    Width="150" AllowGrouping="false" Format="M/d/y hh:mm a" 
                    Type="ColumnType.DateTime" EditType="EditType.DateTimePickerEdit" 
                    TextAlign="TextAlign.Right" />
        <GridColumn Field=@nameof(OrderDetails.ShipCountry) HeaderText="Ship Country" 
                    Width="150" EditType="EditType.DropDownEdit"/>
    </GridColumns>
</SfGrid>

@code {
    SfGrid<OrderDetails> Grid;
    string Message = string.Empty;
    public List<OrderDetails> Orders { get; set; }

    protected override void OnInitialized()
    {
        Orders = OrderDetails.GetAllRecords();
    }

    async Task SaveGridState()
    {
        var state = await Grid.GetPersistDataAsync();
        await JS.InvokeVoidAsync("localStorage.setItem", "gridOrders", state);
        Message = "Grid state saved.";
    }

    async Task RestoreGridState()
    {
        var state = await JS.InvokeAsync<string>("localStorage.getItem", "gridOrders");
        if (!string.IsNullOrEmpty(state))
        {
            await Grid.SetPersistDataAsync(state);
            Message = "Previous Grid state restored.";
        }
        else
        {
            Message = "No saved state found.";
        }
    }

    void OnActionBegin(ActionEventArgs<OrderDetails> args)
    {
        Message = string.Empty;
    }
}
```

## Maintaining custom query in a persistent state

When `EnablePersistence` is enabled, the grid persists its configuration. Custom query parameters can be re-applied after persistence during data binding by using the `DataBound` event. Re-applying parameters in `DataBound` ensures the query remains consistent across reloads and navigation when persistence is enabled.

```razor
@using Syncfusion.Blazor.Data

<SfGrid ID="OrderDetails" @ref="Grid" DataSource="@Orders" 
        Query="@QueryData" AllowFiltering="true" AllowPaging="true" 
        EnablePersistence="true" Height="230">
    <GridEvents DataBound="OnDataBound" TValue="OrderDetails"></GridEvents>
    <GridColumns>
        <GridColumn Field="@nameof(OrderDetails.OrderID)" HeaderText="Order ID" 
                    TextAlign="TextAlign.Right" Width="120" />
        <GridColumn Field="@nameof(OrderDetails.CustomerID)" HeaderText="Customer ID" 
                    Width="150" />
        <GridColumn Field="@nameof(OrderDetails.ShipCity)" HeaderText="Ship City" 
                    Width="150" />
        <GridColumn Field="@nameof(OrderDetails.ShipName)" HeaderText="Ship Name" 
                    Width="150" />
    </GridColumns>
</SfGrid>

@code {
    SfGrid<OrderDetails> Grid;
    public List<OrderDetails> Orders { get; set; } = new();
    Query QueryData = new Query().Where("CustomerID", "equal", "VINET");

    protected override void OnInitialized()
    {
        Orders = OrderDetails.GetAllRecords();
    }

    void OnDataBound()
    {
        Grid?.Query?.AddParams("dataSource", "orders");
    }
}
```

## Get or set local storage value

When `EnablePersistence` is enabled, the grid saves its configuration in `window.localStorage`. This includes settings such as **paging**, **filtering**, **sorting**, and **column visibility**. The stored state can be retrieved or updated using JavaScript interop.

To retrieve the grid model from local storage:

```csharp
string localStorageKey = "gridOrders"; // Key format: component name + component ID
string modelJson = await JS.InvokeAsync<string>("localStorage.getItem", localStorageKey);

// Deserialize the JSON string into an object
var modelObject = JsonSerializer.Deserialize<object>(modelJson);
```

Update the grid state in local storage:

```csharp
await JS.InvokeVoidAsync("localStorage.setItem", localStorageKey, modelJson);
```

## Server-Side State Persistence

For Blazor Server apps (or any scenario where `localStorage` is unavailable or insufficient), persist the grid state on the server — in a database, session store, or user profile.

### Save and Load via API

Use `GetPersistDataAsync()` to capture state as a JSON string and send it to your server. Restore it on load with `SetPersistDataAsync()`:

```razor
@inject HttpClient Http

@code {
    SfGrid<Order> Grid;
    string UserId = "user-123";

    // Called on Save button click
    async Task SaveStateToServer()
    {
        var state = await Grid.GetPersistDataAsync();
        await Http.PostAsJsonAsync($"/api/grid-state/{UserId}", state);
    }

    // Called after grid renders (e.g., OnAfterRenderAsync)
    async Task LoadStateFromServer()
    {
        var state = await Http.GetStringAsync($"/api/grid-state/{UserId}");
        if (!string.IsNullOrEmpty(state))
            await Grid.SetPersistDataAsync(state);
    }
}
```

### Minimal API Example (Server)

```csharp
// Program.cs — server
app.MapGet("/api/grid-state/{userId}", async (string userId, IStateStore store) =>
    await store.GetAsync(userId));

app.MapPost("/api/grid-state/{userId}", async (string userId, string state, IStateStore store) =>
    await store.SaveAsync(userId, state));
```

> The state string returned by `GetPersistDataAsync()` is plain JSON — store it in any string-capable field (e.g., `NVARCHAR(MAX)`, Redis string, etc.).

### Combining with `EnablePersistence`

You can disable built-in `localStorage` persistence (`EnablePersistence="false"`) and manage state entirely server-side, giving full control over when and how state is saved:

```razor
<SfGrid @ref="Grid" DataSource="@Orders">
    <!-- No EnablePersistence — we manage state manually -->
    <GridColumns>...</GridColumns>
</SfGrid>
```

Call `SaveStateToServer()` on meaningful user actions (e.g., toolbar button, page unload) and `LoadStateFromServer()` in `OnAfterRenderAsync` on first render.

## SignalR Buffer Increase

When persistence is enabled with many columns, SignalR may hit buffer limits. Increase in `Program.cs`:

```csharp
builder.Services.AddSignalR(hubOptions =>
{
    hubOptions.MaximumReceiveMessageSize = 10 * 1024 * 1024; // 10MB
});

