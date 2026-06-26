# Foreign Key Column — Syncfusion Blazor DataGrid

## Table of Contents
1. [Foreign Key Column Overview](#foreign-key-column-overview)
2. [Bind Local Data](#bind-local-data)
3. [Bind Remote Data](#bind-remote-data)
4. [Edit Template in Foreign Key Column](#edit-template-in-foreign-key-column)
5. [Filter Template](#filter-template)
6. [Custom Aggregation](#custom-aggregation)

---

## Foreign Key Column Overview

Use the `GridForeignColumn` directive to display related data from a foreign key data source instead of displaying raw ID values:

```razor
<GridForeignColumn Field="EmployeeID" 
                 HeaderText="Employee Name" 
                 ForeignKeyValue="FirstName" 
                 ForeignDataSource="@Employees" 
                 Width="150">
</GridForeignColumn>
```

Key properties:
- **Field**: Column field name in the Grid data source (typically the ID)
- **ForeignKeyValue**: Property to display from the foreign data source (the descriptive value)
- **ForeignDataSource**: Data source containing the related data
- **ForeignKeyField**: Maps the column field to the foreign data source key (optional)

> If `ForeignKeyField` is not defined, the Grid uses the `Field` property to match with the foreign data source.

---

## Bind Local Data

Display foreign key values from a local in-memory data source:

```razor
<SfGrid DataSource="@Orders" Height="315">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" TextAlign="TextAlign.Right" Width="120"></GridColumn>
        <GridForeignColumn Field="EmployeeID" 
                         HeaderText="Employee Name" 
                         ForeignKeyValue="FirstName" 
                         ForeignDataSource="@Employees" 
                         Width="150">
        </GridForeignColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="120"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    public List<OrderDetails> Orders { get; set; }
    public List<EmployeeDetails> Employees { get; set; }
    
    protected override void OnInitialized()
    {
        Orders = OrderDetails.GetAllRecords();
        Employees = EmployeeDetails.GetAllRecords();
    }
}
```

Benefits:
- Improved readability (names instead of IDs)
- Automatic mapping of foreign key IDs to display values
- Works seamlessly with filtering and sorting

---

## Bind Remote Data

Display foreign key values from a remote data source using `SfDataManager`:

```razor
<SfGrid DataSource="@Orders" Height="315">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
        <GridForeignColumn TValue="EmployeeData" 
                         Field="EmployeeID" 
                         HeaderText="Employee Name" 
                         ForeignKeyValue="FirstName" 
                         Width="150">
            <SfDataManager Url="https://services.odata.org/V4/Northwind/Northwind.svc/Employees" 
                         CrossDomain="true" 
                         Adaptor="ODataV4Adaptor">
            </SfDataManager>
        </GridForeignColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    public List<OrderDetails> Orders { get; set; }
    
    protected override void OnInitialized()
    {
        Orders = OrderDetails.GetAllRecords();
    }
}
```

Important notes for remote data:
- **Sorting and grouping** are performed on the `ForeignKeyField` (ID), not the display value
- Remote queries use OData, REST API, or other remote endpoints
- Support for cross-domain requests

---

## Edit Template in Foreign Key Column

Customize the editor for foreign key columns by defining an `EditTemplate`:

```razor
<SfGrid DataSource="@Orders" 
        Height="315" 
        Toolbar="@(new List<string>() { "Add", "Edit", "Delete", "Update", "Cancel" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true">
    </GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true" Width="120"></GridColumn>
        <GridForeignColumn Field="EmployeeID" 
                         HeaderText="Employee Name" 
                         ForeignKeyValue="FirstName" 
                         ForeignDataSource="@Employees" 
                         Width="150">
            <EditTemplate>
                <SfComboBox TValue="int?" TItem="EmployeeData" 
                          @bind-Value="@((context as OrderData).EmployeeID)" 
                          DataSource="Employees">
                    <ComboBoxFieldSettings Value="EmployeeID" Text="FirstName">
                    </ComboBoxFieldSettings>
                </SfComboBox>
            </EditTemplate>
        </GridForeignColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Edit template benefits:
- Use custom components (ComboBox, AutoComplete, DropDownList)
- Default: DropDownList renders for foreign key columns
- Full control over editing experience

---

## Filter Template

Customize the filtering UI for foreign key columns:

```razor
<SfGrid DataSource="@Orders" Height="315" AllowFiltering="true">
    <GridFilterSettings Type="FilterType.Menu"></GridFilterSettings>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
        <GridForeignColumn Field="EmployeeID" 
                         HeaderText="Employee Name" 
                         ForeignKeyValue="FirstName" 
                         ForeignDataSource="@Employees" 
                         Width="150">
            <FilterTemplate>
                <SfDropDownList Placeholder="Employee Name" 
                              @bind-Value="@((context as PredicateModel<string>).Value)" 
                              TItem="EmployeeDetails" 
                              TValue="string" 
                              DataSource="@Employees">
                    <DropDownListFieldSettings Value="FirstName" Text="FirstName">
                    </DropDownListFieldSettings>
                </SfDropDownList>
            </FilterTemplate>
        </GridForeignColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Filter template features:
- Custom dropdown for filtering foreign key values
- Works with different filter types (Menu, FilterBar, Excel)
- Provides intuitive filtering experience

---

## Custom Aggregation

Implement custom aggregation for foreign key columns:

```razor
<SfGrid DataSource="@OrderData" Height="315">
    <GridAggregates>
        <GridAggregate>
            <GridAggregateColumns>
                <GridAggregateColumn Field="EmployeeID" Type="AggregateType.Custom">
                    <FooterTemplate Context="data">
                        Count of Margaret: @CustomAggregateFn()
                    </FooterTemplate>
                </GridAggregateColumn>
            </GridAggregateColumns>
        </GridAggregate>
    </GridAggregates>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true" Width="100"></GridColumn>
        <GridForeignColumn Field="EmployeeID" 
                         HeaderText="Employee Name" 
                         ForeignKeyValue="FirstName" 
                         ForeignDataSource="@EmployeeData" 
                         Width="120">
        </GridForeignColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    public List<OrderDetails> OrderData { get; set; }
    public List<EmployeeDetails> EmployeeData { get; set; }
    
    protected override void OnInitialized()
    {
        OrderData = OrderDetails.GetAllRecords();
        EmployeeData = EmployeeDetails.GetAllRecords();
    }
    
    private int CustomAggregateFn()
    {
        return OrderData.Count(order => 
            EmployeeData.FirstOrDefault(emp => emp.EmployeeID == order.EmployeeID)
            ?.FirstName == "Margaret");
    }
}
```

Custom aggregation capabilities:
- Aggregate based on foreign key display values
- Use LINQ queries to calculate custom values
- Display in footer template

