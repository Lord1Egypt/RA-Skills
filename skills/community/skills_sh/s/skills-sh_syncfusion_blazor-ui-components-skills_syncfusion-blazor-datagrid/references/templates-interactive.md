# Templates — Edit, Toolbar, Caption & Pager — Syncfusion Blazor DataGrid

> *See also: [templates-structural.md](./templates-structural.md) for Column, Row & Detail templates.*

## Table of Contents
- [Toolbar Template](#toolbar-template)
- [Edit Templates](#edit-templates)
  - [Column EditTemplate](#column-edittemplate)
  - [GridEditSettings Template (Inline/Dialog)](#gridedsettings-template-inlinedialog)
  - [Disable Inputs on Add vs Edit (OnBeginEdit / RowCreating)](#disable-inputs-on-add-vs-edit-onbeginedit--rowcreating)
  - [Complex Data Binding — Triple Underscore Rule](#complex-data-binding--triple-underscore-rule)
  - [Set Focus to Specific Editor on Dialog Open](#set-focus-to-specific-editor-on-dialog-open)
  - [RowUpdating — Transform Value Before Save](#rowupdating--transform-value-before-save)
  - [FooterTemplate (Dialog mode)](#footertemplate-dialog-mode)
- [Caption Template](#caption-template)
  - [Render Custom Blazor Component in Caption](#render-custom-blazor-component-in-caption)
  - [Caption Locale / Text Customization](#caption-locale--text-customization)
- [Pager Template](#pager-template)

## Toolbar Template

Replace the entire toolbar with a custom Blazor component:

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true" @ref="Grid">
    <GridTemplates>
        <ToolbarTemplate>
            <SfToolbar>
                <ToolbarEvents Clicked="ToolbarClickHandler"></ToolbarEvents>
                <ToolbarItems>
                    <ToolbarItem Type="ItemType.Button" Id="ExpandAll" Text="Expand All"
                                 PrefixIcon="e-icons e-chevron-down"></ToolbarItem>
                    <ToolbarItem Type="ItemType.Button" Id="CollapseAll" Text="Collapse All"
                                 PrefixIcon="e-icons e-chevron-up"></ToolbarItem>
                </ToolbarItems>
            </SfToolbar>
        </ToolbarTemplate>
    </GridTemplates>
    <GridGroupSettings Columns="@(new string[]{ "CustomerID" })"></GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    async Task ToolbarClickHandler(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        if (args.Item.Id == "ExpandAll")
            await Grid.ExpandAllGroupAsync();
        if (args.Item.Id == "CollapseAll")
            await Grid.CollapseAllGroupAsync();
    }
}
```

## Edit Templates

### Column EditTemplate

Custom editor widget for a column:

```razor
<GridColumn Field="ShipCity" HeaderText="Ship City" Width="150">
    <EditTemplate>
        @{
            var order = context as Order;
        }
        <SfDropDownList @bind-Value="order.ShipCity" DataSource="@Cities">
            <DropDownListFieldSettings Text="Name" Value="Name"></DropDownListFieldSettings>
        </SfDropDownList>
    </EditTemplate>
</GridColumn>
```

> **`@bind-Value` (two-way binding) is mandatory** for all custom editors inside `<EditTemplate>`. Without it, the edited value will not be written back to the Grid's data source when saving.

### GridEditSettings Template (Inline/Dialog)

Replace the entire edit form:

```razor
<GridEditSettings AllowEditing="true" AllowAdding="true" Mode="EditMode.Normal">
    <Template>
        @{
            var order = context as Order;
        }
        <table>
            <tr>
                <td><label>Order ID</label></td>
                <td>
                    <SfNumericTextBox @bind-Value="order.OrderID" Enabled="false"></SfNumericTextBox>
                </td>
            </tr>
            <tr>
                <td><label>Customer</label></td>
                <td>
                    <SfTextBox @bind-Value="order.CustomerID"></SfTextBox>
                </td>
            </tr>
        </table>
    </Template>
</GridEditSettings>
```

### Disable Inputs on Add vs Edit (OnBeginEdit / RowCreating)

Control which fields are editable depending on whether the user is adding a new record or editing an existing one:

```csharp
<GridEvents TValue="Order" OnBeginEdit="BeginEditHandler" RowCreating="RowCreatingHandler"></GridEvents>

@code {
    // Fires when an existing row enters edit mode
    void BeginEditHandler(BeginEditArgs<Order> args)
    {
        // Disable OrderID field when editing (primary key should not change)
        args.ColumnName == "OrderID"; // use Enabled="false" in EditTemplate instead
    }

    // Fires when a new row is being added
    void RowCreatingHandler(RowCreatingEventArgs<Order> args)
    {
        args.Data.OrderID = 0; // pre-set default values for new records
    }
}
```

> To visually disable a field, use `Enabled="@(context as Order)?.OrderID != 0"` inside the `<EditTemplate>` to conditionally disable inputs based on whether a record has a key value.

### Complex Data Binding — Triple Underscore Rule

When binding to nested object properties (e.g., `Employee.Address.City`) inside `<GridColumn>`, replace each `.` with `___` (three underscores) in the `Field` attribute:

```razor
<GridColumn Field="Address___City" HeaderText="City" Width="130"></GridColumn>
```

- Syncfusion uses `___` as the path separator for deeply nested properties.
- The model must be structured with nested objects (not flat), e.g., `Employee.Address.City`.
- Editing and filtering also respect the `___` separator — no extra configuration needed.

> Do **not** use a single underscore or dot notation in `Field` for nested paths — only `___` (triple) is recognized.

### Set Focus to Specific Editor on Dialog Open

To move focus to a particular input when the dialog edit form opens, call `Focus()` on the input component reference inside the `OnActionBegin` event when `RequestType == RequestTypeAction.BeginEdit`:

```razor
<GridEvents TValue="Order" OnActionBegin="ActionBeginHandler"></GridEvents>
<GridColumn Field="CustomerID" HeaderText="Customer" Width="150">
    <EditTemplate>
        <SfTextBox @ref="customerInput" @bind-Value="@((context as Order).CustomerID)"></SfTextBox>
    </EditTemplate>
</GridColumn>

@code {
    SfTextBox customerInput;

    async Task ActionBeginHandler(ActionEventArgs<Order> args)
    {
        if (args.RequestType == Action.BeginEdit)
            await customerInput.FocusAsync();
    }
}
```

### RowUpdating — Transform Value Before Save

Use the `RowUpdating` event to intercept and transform data before it is committed to the data source:

```razor
<GridEvents TValue="Order" RowUpdating="RowUpdatingHandler"></GridEvents>

@code {
    void RowUpdatingHandler(RowUpdatingEventArgs<Order> args)
    {
        // Normalize casing before save
        if (!string.IsNullOrEmpty(args.Data.CustomerID))
            args.Data.CustomerID = args.Data.CustomerID.ToUpperInvariant();

        // Derived field: compute ShipName from CustomerID
        args.Data.ShipName = $"Ship-{args.Data.CustomerID}";
    }
}
```

> `args.Data` is the modified record about to be saved. Mutate it directly — changes are reflected in the Grid's data source after the edit completes. To cancel the save, set `args.Cancel = true`.

### FooterTemplate (Dialog mode)

When embedding a custom UI (e.g., a `Tab` component) inside a dialog edit template, the default dialog footer buttons (Save/Cancel) can conflict with custom submit logic. Use an empty `<FooterTemplate>` to suppress them and provide your own action buttons inside the template:

```razor
<GridEditSettings AllowEditing="true" AllowAdding="true" Mode="EditMode.Dialog">
    <Template>
        @{
            var order = context as Order;
        }
        <div>
            <!-- custom form content -->
            <SfTextBox @bind-Value="order.CustomerID"></SfTextBox>
            <SfButton OnClick="() => Grid.EndEditAsync()">Submit</SfButton>
        </div>
    </Template>
    <FooterTemplate>
        {{!-- empty: suppresses the default Save/Cancel buttons --}}
    </FooterTemplate>
</GridEditSettings>
```

> Use `<FooterTemplate>` when using tabbed dialog templates or any layout where default footer buttons would duplicate or conflict with custom action buttons.

## Caption Template

Customize the group caption row:

```razor
<GridGroupSettings>
    <CaptionTemplate>
        @{
            var caption = context as CaptionTemplateContext;
        }
        <span>@caption.HeaderText: @caption.Key — @caption.Count records</span>
    </CaptionTemplate>
</GridGroupSettings>
```

`CaptionTemplateContext` properties: `Field`, `HeaderText`, `Key`, `Count`

### Render Custom Blazor Component in Caption

Embed a reusable Blazor component inside `<CaptionTemplate>` for richer group header UI:

```razor
<GridGroupSettings>
    <CaptionTemplate>
        @{
            var caption = context as CaptionTemplateContext;
        }
        <GroupBadge Label="@caption.HeaderText" Value="@caption.Key.ToString()"
                    Count="@caption.Count" />
    </CaptionTemplate>
</GridGroupSettings>
```

Where `GroupBadge` is a custom component:

```razor
@* GroupBadge.razor *@
<span class="group-badge">
    <b>@Label:</b> @Value <span class="badge">@Count</span>
</span>

@code {
    [Parameter] public string Label  { get; set; }
    [Parameter] public string Value  { get; set; }
    [Parameter] public int    Count  { get; set; }
}
```

> Any Blazor component can be used inside `<CaptionTemplate>` — pass `CaptionTemplateContext` values as parameters for dynamic group-aware display.

### Caption Locale / Text Customization

The default group caption text format ("items" label) comes from the Grid's locale resources. To change the word "items" displayed after the count, override the locale key `GroupCaptionFormat` via `SfGrid.SetCultureInfoAsync` or by providing a custom locale JSON:

```json
// en-US locale override
{
  "grid": {
    "GroupDropArea": "Drag a column header here to group its column",
    "GroupCaptionFormat": "{0}: {1} - {2} records"
  }
}
```

> For simple text changes, prefer the `<CaptionTemplate>` approach — it avoids locale file management entirely.

## Pager Template

Custom pager UI:

```razor
<GridPageSettings>
    <Template>
        @{
            var pager = context as PagerTemplateContext;
        }
        <div>
            Page @pager.CurrentPage of @pager.TotalPages
            (@pager.TotalRecordsCount total records)
        </div>
    </Template>
</GridPageSettings>
```

`PagerTemplateContext` properties: `CurrentPage`, `PageSize`, `PageCount`, `TotalPages`, `TotalRecordsCount`

