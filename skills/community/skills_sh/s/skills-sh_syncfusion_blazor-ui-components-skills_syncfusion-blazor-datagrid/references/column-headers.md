# Column Headers — Syncfusion Blazor DataGrid

## Table of Contents
1. [Header Text](#header-text)
2. [Header Template](#header-template)
3. [Stacked Headers](#stacked-headers)
4. [Header Text Alignment](#header-text-alignment)
5. [Auto-wrap Header Text](#auto-wrap-header-text)

---

## Header Text

Override the default header text displayed from the Field value using the `HeaderText` property:

```razor
<GridColumn Field="CustomerID" HeaderText="Customer Name" Width="150"></GridColumn>
<GridColumn Field="OrderDate" HeaderText="Order Date" Format="d" Width="130"></GridColumn>
```

> If `HeaderText` is not defined, the column's `Field` value is used as the header text.

---

## Header Template

Customize the header element using the `HeaderTemplate` property to render custom HTML or Blazor components:

```razor
<GridColumn Field="CustomerID" HeaderText="Customer Name">
    <HeaderTemplate>
        <div>
            <span class="e-icons e-user" style="font-size:14px"></span>
            Customer
        </div>
    </HeaderTemplate>
</GridColumn>
```

Header templates support:
- Custom HTML elements
- Blazor components
- Icons and dropdowns
- Switches and interactive controls

> The `HeaderTemplate` property is applicable only to columns that have a header element. Any HTML or Blazor component can be used in the header template.

---

## Stacked Headers

Group multiple columns under a common header by nesting GridColumn directives:

```razor
<GridColumns>
    <GridColumn HeaderText="Order Details" TextAlign="TextAlign.Center">
        <ChildContent>
            <GridColumns>
                <GridColumn Field="OrderDate" HeaderText="Order Date" Width="130" Format="d"></GridColumn>
                <GridColumn Field="Freight" HeaderText="Freight ($)" Width="135" Format="C2"></GridColumn>
            </GridColumns>
        </ChildContent>
    </GridColumn>
    <GridColumn HeaderText="Ship Details" TextAlign="TextAlign.Center">
        <ChildContent>
            <GridColumns>
                <GridColumn Field="ShipCity" HeaderText="Ship City" Width="140"></GridColumn>
                <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="140"></GridColumn>
            </GridColumns>
        </ChildContent>
    </GridColumn>
</GridColumns>
```

Benefits:
- Better data organization
- Improved readability
- Structured column grouping

---

## Header Text Alignment

Align header text horizontally using the `HeaderTextAlign` property:

```razor
<GridColumn Field="OrderID" HeaderText="Order ID" HeaderTextAlign="TextAlign.Right" Width="120"></GridColumn>
<GridColumn Field="CustomerID" HeaderText="Customer ID" HeaderTextAlign="TextAlign.Center" Width="150"></GridColumn>
<GridColumn Field="Freight" HeaderText="Freight" HeaderTextAlign="TextAlign.Right" Format="C2" Width="120"></GridColumn>
```

Alignment options:
- **Left**: Aligns the text to the left (default)
- **Center**: Aligns the text to the center
- **Right**: Aligns the text to the right
- **Justify**: Justifies the header text

> The `HeaderTextAlign` property only changes the alignment of header text, not the cell content. Use `TextAlign` to align cell content and `HeaderTextAlign` for header alignment.

---

## Auto-wrap Header Text

Enable text wrapping for header text when it exceeds column width using `AllowTextWrap` property:

```razor
<SfGrid DataSource="@Orders" AllowTextWrap="true">
    <GridTextWrapSettings WrapMode="WrapMode.Header"></GridTextWrapSettings>
    <GridColumns>
        <GridColumn Field="Inventor" HeaderText="Inventor Name" Width="70"></GridColumn>
        <GridColumn Field="PatentFamilies" HeaderText="Number of Patent Families" Width="80"></GridColumn>
        <GridColumn Field="Invention" HeaderText="Main Fields Of Invention" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Wrap mode options:
- **Both**: Wraps both header text and content (default)
- **Header**: Wraps only header text
- **Content**: Wraps only content

> Specify appropriate column widths using the `Width` property to ensure proper wrapping. Header text without white space does not wrap.

