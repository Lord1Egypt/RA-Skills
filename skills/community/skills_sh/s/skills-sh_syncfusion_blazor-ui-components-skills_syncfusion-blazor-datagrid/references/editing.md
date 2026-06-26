# Editing — Syncfusion Blazor DataGrid

## Table of Contents

- [Enable Editing](#enable-editing)
- [GridEditSettings Properties](#gridedsettings-properties)
- [EditMode Enum](#editmode-enum)
- [Column EditType](#column-edittype)
- [EditorSettings (Customize Editors)](#editorsettings-customize-editors)
- [Custom EditTemplate per Column](#custom-edittemplate-per-column)
- [Normal (Inline) Edit Mode](#normal-inline-edit-mode)
- [Dialog Edit Mode](#dialog-edit-mode)
- [Batch Edit Mode](#batch-edit-mode)
- [Command Column](#command-column)
- [Validation](#validation)
- [Programmatic Editing Methods](#programmatic-editing-methods)
- [Editing Events](#editing-events)

📄 **Advanced patterns** (cancel conditions, default values, new row position, single-click, delete multiple, inline template, limitations):
→ [editing-patterns.md](editing-patterns.md)

📄 **Validation deep-dive** (data annotations, custom attributes, complex types, custom validator component):
→ [editing-validation.md](editing-validation.md)

---

## Enable Editing

```razor
<SfGrid DataSource="@Orders" Toolbar="@(new List<string>{ "Add","Edit","Delete","Update","Cancel" })">
    <GridEditSettings AllowEditing="true" AllowAdding="true" AllowDeleting="true"
                      Mode="EditMode.Normal" AllowEditOnDblClick="true"
                      ShowDeleteConfirmDialog="true">
    </GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID" IsPrimaryKey="true" HeaderText="Order ID" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer" Width="150"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" EditType="EditType.NumericEdit" Width="120"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Date" EditType="EditType.DatePickerEdit" Width="130"></GridColumn>
    </GridColumns>
</SfGrid>
```

> **`IsPrimaryKey` is required** — without it, all edits target the first row.

## GridEditSettings Properties

| Property | Type | Description |
|---|---|---|
| `AllowEditing` | bool | Enable row editing |
| `AllowAdding` | bool | Enable adding new rows |
| `AllowDeleting` | bool | Enable row deletion |
| `Mode` | `EditMode` | Editing mode (`Normal`, `Dialog`, `Batch`) |
| `AllowEditOnDblClick` | bool | Enable edit on double-click (default `true`) |
| `ShowDeleteConfirmDialog` | bool | Show confirm dialog before delete |
| `NewRowPosition` | `NewRowPosition` | Position of new row: `Top` (default) or `Bottom` |
| `ShowAddNewRow` | bool | Always display a blank add-new-row form (Normal mode only) |
| `Validator` | `Type` | Custom validator component type for the edit form |

> `ShowAddNewRow` is supported in **Normal** mode only. See [editing-patterns.md](editing-patterns.md) for limitations.

**Column-level editing properties:**

| Property | Description |
|---|---|
| `GridColumn.AllowEditing` | Set to `false` to make a specific column read-only during edit |
| `GridColumn.AllowAdding` | Set to `false` to prevent value entry for a column on new-row add |
| `GridColumn.IsIdentity` | Set to `true` for auto-increment/identity columns — column becomes read-only in both edit and add modes |

## EditMode Enum

| Mode | Description |
|---|---|
| `Normal` | Inline editing within the row (default) |
| `Dialog` | Opens a popup dialog for editing |
| `Batch` | Double-click any cell; save all changes at once |

## Column EditType

Set `EditType` per column to control the editor widget:

| EditType | Widget |
|---|---|
| `DefaultEdit` | `SfTextBox` |
| `NumericEdit` | `SfNumericTextBox` |
| `DropDownEdit` | `SfDropDownList` |
| `BooleanEdit` | `SfCheckBox` |
| `DatePickerEdit` | `SfDatePicker` |
| `DateTimePickerEdit` | `SfDateTimePicker` |
| `TimePickerEdit` | `SfTimePicker` |

## EditorSettings (Customize Editors)

Pass typed params via `EditorSettings` on `GridColumn`:

```razor
@code {
    public StringEditCellParams StringParams = new StringEditCellParams
    {
        Params = new TextBoxModel { ShowClearButton = true, Multiline = true }
    };

    public NumericEditCellParams NumericParams = new NumericEditCellParams
    {
        Params = new NumericTextBoxModel<object> { Decimals = 2, ShowSpinButton = false, Format = "N2" }
    };

    public DropDownEditCellParams DropDownParams = new DropDownEditCellParams
    {
        Params = new DropDownListModel<object, object> { AllowFiltering = true, ShowClearButton = true }
    };

    public BooleanEditCellParams BooleanParams = new BooleanEditCellParams
    {
        Params = new CheckBoxModel { Label = "Active", LabelPosition = LabelPosition.After }
    };

    public DateEditCellParams DateParams = new DateEditCellParams
    {
        Params = new DatePickerModel { Format = "MM/dd/yyyy", ShowClearButton = true }
    };
}
```

```razor
<GridColumn Field="Freight" EditType="EditType.NumericEdit"
            EditorSettings="@NumericParams" Width="120"></GridColumn>
```

## Custom EditTemplate per Column

Use `EditTemplate` for fully custom per-column editors:

```razor
<GridColumn Field="ShipCity" HeaderText="Ship City" Width="150">
    <EditTemplate>
        @{ var order = context as Order; }
        <SfDropDownList @bind-Value="order.ShipCity" DataSource="@Cities">
            <DropDownListFieldSettings Text="Name" Value="Name"></DropDownListFieldSettings>
        </SfDropDownList>
    </EditTemplate>
</GridColumn>
```

**Nested object** — use `__` (double underscore) instead of `.` in `Field`:

```razor
<GridColumn Field="Address__City" HeaderText="City">
    <EditTemplate>
        <SfTextBox @bind-Value="(context as Order).Address.City"></SfTextBox>
    </EditTemplate>
</GridColumn>
```

**Enum column:**

```razor
<GridColumn Field="Status" HeaderText="Status">
    <EditTemplate>
        @{ var item = context as Order; }
        <SfDropDownList TValue="OrderStatus" TItem="string"
                        DataSource="@(Enum.GetNames(typeof(OrderStatus)).ToList())"
                        @bind-Value="item.Status">
        </SfDropDownList>
    </EditTemplate>
</GridColumn>
```

**Foreign key column:**

```razor
<GridForeignColumn Field="EmployeeID" HeaderText="Employee"
                   ForeignKeyValue="FirstName" ForeignDataSource="@Employees">
    <EditTemplate>
        @{ var order = context as Order; }
        <SfComboBox TValue="int" TItem="Employee" DataSource="@Employees"
                    @bind-Value="order.EmployeeID">
            <ComboBoxFieldSettings Text="FirstName" Value="EmployeeID"></ComboBoxFieldSettings>
        </SfComboBox>
    </EditTemplate>
</GridForeignColumn>
```

> All custom editors must use **`@bind-Value`** for two-way data binding.

## Normal (Inline) Edit Mode

```razor
<GridEditSettings AllowEditing="true" AllowAdding="true" AllowDeleting="true"
                  Mode="EditMode.Normal">
</GridEditSettings>
```

Auto-update a dependent column using `EditTemplate` + `ValueChange`:

```razor
<GridColumn Field="UnitPrice" HeaderText="Unit Price">
    <EditTemplate>
        @{ var item = context as Order; }
        <SfNumericTextBox @ref="PriceBox" @bind-Value="item.UnitPrice"
                          ValueChange="@OnPriceChange">
        </SfNumericTextBox>
    </EditTemplate>
</GridColumn>

@code {
    SfNumericTextBox<double?> PriceBox;

    async Task OnPriceChange(ChangeEventArgs<double?> args)
    {
        // recalculate dependent field, then force re-render
        await Grid.PreventRender(false);
    }
}
```

## Dialog Edit Mode

```razor
<GridEditSettings AllowEditing="true" Mode="EditMode.Dialog"
                  Dialog="@(new DialogSettings { Height = "400px", Width = "600px" })">
    <HeaderTemplate>
        @{ var order = context as Order; }
        <span>@(order?.OrderID == 0 ? "New Record" : $"Edit Order {order.OrderID}")</span>
    </HeaderTemplate>
    <FooterTemplate>
        <SfButton OnClick="@SaveClick" IsPrimary="true">Save</SfButton>
        <SfButton OnClick="@CancelClick">Cancel</SfButton>
    </FooterTemplate>
</GridEditSettings>

@code {
    SfGrid<Order> Grid;
    async Task SaveClick()   => await Grid.EndEditAsync();
    async Task CancelClick() => await Grid.CloseEditAsync();
}
```

> Dialog max height is ~658px on a 1920×1080 screen.

## Full-Row / Dialog Template Editing (GridEditSettings.Template)

Use `GridEditSettings.Template` to replace the **entire row or dialog form** with a custom layout. This differs from per-column `EditTemplate` — it controls the whole edit UI at once.

**Inline (Normal) template** — renders a custom row in-place:

```razor
<SfGrid DataSource="@Orders" Toolbar="@(new string[] { "Add","Edit","Delete","Update","Cancel" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"
                      Mode="EditMode.Normal">
        <Template>
            @{
                var order = context as Order;
                <table>
                    <tr>
                        <td>
                            <SfNumericTextBox @bind-Value="order.OrderID"
                                              Enabled="@(order.OrderID == 0)"
                                              TValue="int">
                            </SfNumericTextBox>
                        </td>
                        <td>
                            <SfTextBox @bind-Value="order.CustomerID"></SfTextBox>
                        </td>
                        <td>
                            <SfDatePicker @bind-Value="order.OrderDate"></SfDatePicker>
                        </td>
                    </tr>
                </table>
            }
        </Template>
    </GridEditSettings>
</SfGrid>
```

**Dialog template** — same approach with `Mode="EditMode.Dialog"`:

```razor
<GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true"
                  Mode="EditMode.Dialog" Dialog="@(new DialogSettings { Width = "450px" })">
    <Template>
        @{
            var order = context as Order;
            <div class="form-row">
                <div class="form-group col-md-6">
                    <SfNumericTextBox @bind-Value="order.OrderID"
                                      Enabled="@(order.OrderID == 0)"
                                      FloatLabelType="FloatLabelType.Always"
                                      Placeholder="Order ID" TValue="int">
                    </SfNumericTextBox>
                </div>
                <div class="form-group col-md-6">
                    <SfTextBox @bind-Value="order.CustomerID"
                               FloatLabelType="FloatLabelType.Always"
                               Placeholder="Customer Name">
                    </SfTextBox>
                </div>
            </div>
        }
    </Template>
</GridEditSettings>
```

> - Always use **`@bind-Value`** on every editor inside the template.
> - Disable the primary key editor with `Enabled="@(order.OrderID == 0)"` to prevent editing on existing rows.
> - For validation inside templates, wrap with `<EditForm>` or use `<DataAnnotationsValidator>`.

## Batch Edit Mode

Double-click any cell to edit; all changes are committed together:

```razor
<SfGrid @ref="Grid" DataSource="@Orders"
        Toolbar="@(new List<string>{ "Add","Delete","Update","Cancel" })">
    <GridEditSettings AllowEditing="true" AllowAdding="true" AllowDeleting="true"
                      Mode="EditMode.Batch">
    </GridEditSettings>
</SfGrid>
```

Auto-update another column from `CellSaved`:

```razor
<GridEvents TValue="Order" CellSaved="OnCellSaved"></GridEvents>

@code {
    async Task OnCellSaved(CellSaveArgs<Order> args)
    {
        if (args.ColumnName == "UnitPrice" || args.ColumnName == "Quantity")
        {
            var rowIndex = await Grid.GetRowIndexByPrimaryKeyAsync(args.Data.OrderID);
            await Grid.UpdateCellAsync(rowIndex, "Total",
                                       args.Data.UnitPrice * args.Data.Quantity);
        }
    }
}
```

Save all pending batch changes programmatically by passing a `BatchChanges<TValue>` object that contains the added, changed, and deleted records:

```razor
@code {
    async Task SaveBatchChanges()
    {
        var batchChanges = new BatchChanges<Order>
        {
            AddedRecords = new List<Order> { /* newly added rows */ },
            ChangedRecords = new List<Order> { /* modified rows */ },
            DeletedRecords = new List<Order> { /* deleted rows */ }
        };
        await Grid.ApplyBatchChangesAsync(batchChanges);
    }
}
```

## Command Column

Add inline CRUD buttons directly inside a column:

```razor
<GridColumn HeaderText="Actions" Width="160">
    <GridCommandColumns>
        <GridCommandColumn Type="CommandButtonType.Edit"
            ButtonOption="@(new CommandButtonOptions { IconCss="e-icons e-edit", CssClass="e-flat" })">
        </GridCommandColumn>
        <GridCommandColumn Type="CommandButtonType.Delete"
            ButtonOption="@(new CommandButtonOptions { IconCss="e-icons e-delete", CssClass="e-flat" })">
        </GridCommandColumn>
        <GridCommandColumn Type="CommandButtonType.Save"
            ButtonOption="@(new CommandButtonOptions { IconCss="e-icons e-save", CssClass="e-flat" })">
        </GridCommandColumn>
        <GridCommandColumn Type="CommandButtonType.Cancel"
            ButtonOption="@(new CommandButtonOptions { IconCss="e-icons e-cancel", CssClass="e-flat" })">
        </GridCommandColumn>
    </GridCommandColumns>
</GridColumn>
```

**Custom command button:**

```razor
<GridCommandColumn ButtonOption="@(new CommandButtonOptions { Content = "Details", CssClass = "e-flat" })">
</GridCommandColumn>

<GridEvents TValue="Order" CommandClicked="OnCommandClick"></GridEvents>

@code {
    void OnCommandClick(CommandClickEventArgs<Order> args)
    {
        if (args.CommandColumn.ButtonOption.Content == "Details")
        {
            // handle custom action using args.RowData
        }
    }
}
```

> **Command column does not support Add** — buttons render only after a record exists.

## Validation

Quick reference — for full detail see [editing-validation.md](editing-validation.md).

**Per-column rules:**

```razor
<GridColumn Field="CustomerID"
            ValidationRules="@(new ValidationRules { Required = true, MinLength = 3, MaxLength = 8 })">
</GridColumn>

<GridColumn Field="Freight" EditType="EditType.NumericEdit"
            ValidationRules="@(new ValidationRules { Required = true, Min = 1, Max = 1000 })">
</GridColumn>
```

**Data annotations on model:**

```csharp
public class Order
{
    [Key]                              // primary key
    public int OrderID { get; set; }

    [Required]
    [StringLength(8, MinimumLength = 3)]
    public string CustomerID { get; set; }

    [Range(1, 1000)]
    public double Freight { get; set; }
}
```

> See [editing-validation.md](editing-validation.md) for custom attributes, complex type validation, and custom validator components.

## Programmatic Editing Methods

```razor
@code {
    SfGrid<Order> Grid;

    // Add empty row, or pass data + insert index
    await Grid.AddRecordAsync();
    await Grid.AddRecordAsync(newRecord, index);

    // Edit the currently selected row
    await Grid.StartEditAsync();

    // Save current edit
    await Grid.EndEditAsync();

    // Cancel current edit
    await Grid.CloseEditAsync();

    // Delete selected row(s); or target by field + object
    await Grid.DeleteRecordAsync();
    await Grid.DeleteRecordAsync("OrderID", selectedOrder);

    // Update an entire row by index (persists to datasource)
    await Grid.UpdateRowAsync(rowIndex, updatedOrder);

    // Update a single cell by primary key — UI only, NOT datasource
    await Grid.SetCellValueAsync(primaryKeyValue, "FieldName", newValue);

    // Batch mode: save all pending changes — requires a BatchChanges<TValue> argument
    var batchChanges = new BatchChanges<Order>
    {
        AddedRecords   = new List<Order> { /* newly added rows */ },
        ChangedRecords = new List<Order> { /* modified rows */ },
        DeletedRecords = new List<Order> { /* deleted rows */ }
    };
    await Grid.ApplyBatchChangesAsync(batchChanges);

    // Batch mode: queue a cell change before ApplyBatchChangesAsync
    var idx = await Grid.GetRowIndexByPrimaryKeyAsync(primaryKeyValue);
    await Grid.UpdateCellAsync(idx, "FieldName", newValue);
}
```

> **`SetCellValueAsync`** updates the rendered cell only — use `UpdateRowAsync` to persist to the datasource.  
> **`UpdateCellAsync`** is Batch mode only — queues the change until `ApplyBatchChangesAsync` is called.  
> **`ApplyBatchChangesAsync`** requires a `BatchChanges<TValue>` argument containing `AddedRecords`, `ChangedRecords`, and `DeletedRecords` lists.

## Server-side CRUD Persistence

When the Grid is bound to a **remote data source**, CRUD operations must be persisted to the server via `SfDataManager`. The adaptor handles translating Grid actions into server requests automatically.

| Adaptor | Use Case |
|---|---|
| `UrlAdaptor` | Custom REST API with `InsertUrl`, `UpdateUrl`, `RemoveUrl`, or `CrudUrl`/`BatchUrl` |
| `ODataV4Adaptor` | OData V4 services — uses `POST`/`PATCH`/`DELETE` automatically |
| `WebApiAdaptor` | ASP.NET Core Web API — maps to `GET`/`POST`/`PUT`/`DELETE` |
| `GraphQLAdaptor` | GraphQL servers — flexible query/mutation approach |

```razor
<SfGrid DataSource="@DataManager" Toolbar="@(new List<string>{ "Add","Edit","Delete","Update","Cancel" })">
    <SfDataManager Url="/api/orders" InsertUrl="/api/orders/insert"
                   UpdateUrl="/api/orders/update" RemoveUrl="/api/orders/remove"
                   Adaptor="Adaptors.UrlAdaptor">
    </SfDataManager>
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true">
    </GridEditSettings>
</SfGrid>
```

> For full server-side adaptor setup (including CRUD endpoints and request/response formats), see [url-adaptor.md](url-adaptor.md), [odatav4-adaptor.md](odatav4-adaptor.md), and [web-api-adaptor.md](web-api-adaptor.md).

## Editing Events

### Event Sequence (Normal / Dialog)

| Operation | Sequence |
|---|---|
| Add | `RowCreating` → `RowCreated` |
| Edit | `OnRowEditStart` → `OnBeginEdit` → `RowEditing` → `RowEdited` |
| Save | `RowUpdating` → `RowUpdated` |
| Delete | `RowDeleting` → `RowDeleted` |
| Cancel | `EditCanceling` → `EditCanceled` |

### Full Reference

| Event | Args | Cancelable | Description |
|---|---|---|---|
| `RowCreating` | `RowCreatingEventArgs<T>` | ✅ | Before new row added; set `args.Data` for defaults |
| `RowCreated` | `RowCreatedEventArgs<T>` | ❌ | After new row added |
| `OnRowEditStart` | `OnRowEditStartEventArgs<T>` | ❌ | Before row enters edit mode (data cloning setup) |
| `OnBeginEdit` | `BeginEditArgs<T>` | ❌ | Before edit UI renders; set `args.RowData` for custom clone |
| `RowEditing` | `RowEditingEventArgs<T>` | ✅ | Before edit performed; `args.Cancel = true` to block |
| `RowEdited` | `RowEditedEventArgs<T>` | ❌ | After row has entered edit mode |
| `RowUpdating` | `RowUpdatingEventArgs<T>` | ✅ | Before save; `args.Cancel = true` to block |
| `RowUpdated` | `RowUpdatedEventArgs<T>` | ❌ | After row saved to datasource |
| `RowDeleting` | `RowDeletingEventArgs<T>` | ✅ | Before delete; `args.Cancel = true` to block |
| `RowDeleted` | `RowDeletedEventArgs<T>` | ❌ | After row deleted |
| `EditCanceling` | `EditCancelingEventArgs<T>` | ✅ | Before cancel; `args.Cancel = true` to keep edit open |
| `EditCanceled` | `EditCanceledEventArgs<T>` | ❌ | After edit canceled |
| `OnCellEdit` | `CellEditArgs<T>` | ✅ | **Batch only** — cell enters edit mode |
| `CellSaved` | `CellSaveArgs<T>` | ❌ | **Batch only** — batch cell value saved |

**Cancel delete with custom confirmation dialog:**

```razor
<GridEvents TValue="Order" RowDeleting="OnRowDeleting"></GridEvents>

@code {
    bool ShowConfirm = false;
    Order PendingDelete;

    async Task OnRowDeleting(RowDeletingEventArgs<Order> args)
    {
        args.Cancel = true;
        PendingDelete = args.Data;
        ShowConfirm = true;
    }

    async Task ConfirmDelete()
    {
        ShowConfirm = false;
        await Grid.DeleteRecordAsync("OrderID", PendingDelete);
    }
}
```
