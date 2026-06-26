# Paging — Syncfusion Blazor DataGrid

## Table of Contents
- [Enable Paging](#enable-paging)
- [Page Size Dropdown](#page-size-dropdown)
- [Programmatic Page Navigation](#programmatic-page-navigation)
- [Pager Template](#pager-template)
- [External Pager (Pager at Top)](#external-pager-pager-at-top)
- [Dynamic Page Size Based on Container Height](#dynamic-page-size-based-on-container-height)
- [Paging Events](#paging-events)
  - [Grid pager events](#grid-pager-events)
  - [SfPager (external) events](#sfpager-external-events)

## Enable Paging

```razor
<SfGrid DataSource="@Orders" AllowPaging="true">
    <GridPageSettings PageSize="10" PageCount="5" CurrentPage="1"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

| Property | Default | Description |
|---|---|---|
| `PageSize` | 12 | Records per page |
| `PageCount` | 8 | Number of numeric pager buttons |
| `CurrentPage` | 1 | Active page (1-indexed) |

## Page Size Dropdown

Enable page size selector:

```razor
<GridPageSettings PageSizes="true"></GridPageSettings>
<!-- Default values: ["All","5","10","15","20"] -->

<!-- Custom values -->
<GridPageSettings PageSizes="@(new string[]{ \"10\",\"20\",\"50\",\"100\" })"></GridPageSettings>
```

## Programmatic Page Navigation

```razor
<SfGrid @ref="Grid" DataSource="@Orders" AllowPaging="true">
    <GridPageSettings PageSize="10"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
@code {
    SfGrid<Order> Grid;

    // Go to specific page
    await Grid.GoToPageAsync(3);

    // Change page size at runtime
    Grid.PageSettings.PageSize = 20;
    await Grid.Refresh();
}
```

## Pager Template

Customize the pager UI using `PagerTemplateContext`:

```razor
<SfGrid DataSource="@Orders" AllowPaging="true">
    <GridPageSettings PageSize="5">
        <Template>
            @{
                var pager = context as PagerTemplateContext;
                <div>
                    <span>Page @pager.CurrentPage of @pager.TotalPages</span>
                    <span>(@pager.TotalItemsCount total records)</span>
                </div>
            }
        </Template>
    </GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

`PagerTemplateContext` properties: `CurrentPage`, `PageSize`, `PageCount`, `TotalPages`, `TotalItemsCount`.

## External Pager (Pager at Top)

Use `SfPager` as an external component, disable built-in paging:

> **Note:** `SfPager.PageSizes` accepts `List<int>` (not `string[]`). This differs from `GridPageSettings.PageSizes` which takes `string[]`.

```razor
@using Syncfusion.Blazor.Navigations

<div @onkeydown="HandleKeyDown">
    <SfPager @ref="Pager" PageSize="@TakeValue"
             PageSizes="@pagesizes"
             ShowAllInPageSizes="true"
             NumericItemsCount="4"
             TotalItemsCount="@TotalCount"
             PageSizeChanged="OnPageSizeChanged"
             ItemClick="OnItemClick">
    </SfPager>
</div>

<SfGrid DataSource="@PagedOrders" AllowPaging="false">
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfPager Pager;
    int TakeValue = 5;
    int SkipValue = 0;
    int TotalCount;
    List<Order> AllOrders = new();
    List<Order> PagedOrders = new();
    // SfPager.PageSizes takes List<int> (not string[])
    public List<int> pagesizes = new List<int> { 5, 10, 12, 20 };

    protected override void OnInitialized()
    {
        AllOrders = GetOrders();
        TotalCount = AllOrders.Count;
        PagedOrders = AllOrders.Take(TakeValue).ToList();
    }

    void OnItemClick(PagerItemClickEventArgs args)
    {
        SkipValue = (args.CurrentPage * Pager.PageSize) - Pager.PageSize;
        TakeValue = Pager.PageSize;
    }

    void OnPageSizeChanged(PageSizeChangedArgs args)
    {
        TakeValue = Pager.PageSize;
        PagedOrders = AllOrders.Take(TakeValue).ToList();
    }

    void HandleKeyDown(KeyboardEventArgs args)
    {
        if (args.Code == "Enter" || args.Key == "Enter")
        {
            SkipValue = (Pager.CurrentPage * Pager.PageSize) - Pager.PageSize;
            TakeValue = Pager.PageSize;
        }
    }
}
```

| Property | Type | Description |
|---|---|---|
| `PageSize` | `int` | Records shown per page |
| `PageSizes` | `List<int>` | Page size dropdown options |
| `ShowAllInPageSizes` | `bool` | Adds "All" option to the page size dropdown |
| `NumericItemsCount` | `int` | Number of numeric page buttons |
| `TotalItemsCount` | `int` | Total record count |

## Dynamic Page Size Based on Container Height

```csharp
// Formula: PageSize = (GridHeight - (PagebarHeight + HeaderHeight)) / RowHeight
int pageSize = (int)((gridHeight - 130) / 36);
Grid.PageSettings.PageSize = pageSize;
```

## Paging Events

### Grid pager events

```razor
<GridEvents TValue="Order" PageChanging="PageChangingHandler" PageChanged="PageChangedHandler"></GridEvents>
@code {
    void PageChangingHandler(GridPageChangingEventArgs args)
    {
        // args.CurrentPage, args.PreviousPage
        // Cancel to prevent navigation: args.Cancel = true;
    }
    void PageChangedHandler(GridPageChangedEventArgs args)
    {
        // args.CurrentPage, args.CurrentPageSize, args.TotalPages
    }
}
```

### SfPager (external) events

| Event | Trigger |
|---|---|
| `Created` | Fired when the `SfPager` component is initialized |
| `ItemClick` | Fired when a numeric page button is clicked |
| `PageSizeChanged` | Fired when a page size is selected from the dropdown |

```razor
<SfPager Created="OnPagerCreated" ItemClick="OnItemClick" PageSizeChanged="OnPageSizeChanged" ...>
</SfPager>
@code {
    void OnPagerCreated() { /* runs once on init */ }
    void OnItemClick(PagerItemClickEventArgs args) { /* args.CurrentPage */ }
    void OnPageSizeChanged(PageSizeChangedArgs args) { /* args.PageSize */ }
}

