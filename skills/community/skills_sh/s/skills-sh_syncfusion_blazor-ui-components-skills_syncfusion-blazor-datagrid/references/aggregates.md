# Aggregates — Syncfusion Blazor DataGrid

## Table of Contents
- [Basic Aggregate Structure](#basic-aggregate-structure)
- [Built-in Aggregate Types](#built-in-aggregate-types)
- [Multiple Aggregate Types on One Column](#multiple-aggregate-types-on-one-column)
- [Boolean Column Aggregates](#boolean-column-aggregates)
- [Date Column Aggregates](#date-column-aggregates)
- [Custom Aggregate](#custom-aggregate)
- [Reactive Aggregates (Batch Editing)](#reactive-aggregates-batch-editing)
- [Notes](#notes)

## Basic Aggregate Structure

Use `GridAggregates` > `GridAggregate` > `GridAggregateColumns` > `GridAggregateColumn` with a template:

```razor
<SfGrid DataSource="@Orders" AllowPaging="true" AllowGrouping="true">
    <GridGroupSettings Columns="@(new string[]{ "ShipCountry" })"></GridGroupSettings>
    <GridAggregates>
        <!-- Footer aggregate -->
        <GridAggregate>
            <GridAggregateColumns>
                <GridAggregateColumn Field="Freight" Type="AggregateType.Sum" Format="C2">
                    <FooterTemplate>
                        @{
                            var agg = context as AggregateTemplateContext;
                        }
                        <span>Sum: @agg.Sum</span>
                    </FooterTemplate>
                </GridAggregateColumn>
            </GridAggregateColumns>
        </GridAggregate>
        <!-- Group footer aggregate -->
        <GridAggregate>
            <GridAggregateColumns>
                <GridAggregateColumn Field="Freight" Type="AggregateType.Average" Format="C2">
                    <GroupFooterTemplate>
                        @{
                            var agg = context as AggregateTemplateContext;
                        }
                        <span>Avg: @agg.Average</span>
                    </GroupFooterTemplate>
                </GridAggregateColumn>
            </GridAggregateColumns>
        </GridAggregate>
        <!-- Group caption aggregate -->
        <GridAggregate>
            <GridAggregateColumns>
                <GridAggregateColumn Field="Freight" Type="AggregateType.Max" Format="C2">
                    <GroupCaptionTemplate>
                        @{
                            var agg = context as AggregateTemplateContext;
                        }
                        <span>Max: @agg.Max</span>
                    </GroupCaptionTemplate>
                </GridAggregateColumn>
            </GridAggregateColumns>
        </GridAggregate>
    </GridAggregates>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer" Width="150"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" TextAlign="TextAlign.Right" Width="120"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

> Group footer and group caption aggregates appear only when grouping is enabled.

## Built-in Aggregate Types

| AggregateType | Description | Access Property |
|---|---|---|
| `Sum` | Sum of numeric values | `agg.Sum` |
| `Average` | Average of numeric values | `agg.Average` |
| `Min` | Minimum value | `agg.Min` |
| `Max` | Maximum value | `agg.Max` |
| `Count` | Row count | `agg.Count` |
| `TrueCount` | Count of `true` boolean values | `agg.TrueCount` |
| `FalseCount` | Count of `false` boolean values | `agg.FalseCount` |
| `Custom` | User-defined calculation | Use template directly |

## Multiple Aggregate Types on One Column

Use separate `GridAggregate` blocks per aggregate:

```razor
<GridAggregates>
    <GridAggregate>
        <GridAggregateColumns>
            <GridAggregateColumn Field="Freight" Type="AggregateType.Sum" Format="C2">
                <FooterTemplate>
                    @{ var agg = context as AggregateTemplateContext; }
                    <span>Sum: @agg.Sum</span>
                </FooterTemplate>
            </GridAggregateColumn>
        </GridAggregateColumns>
    </GridAggregate>
    <GridAggregate>
        <GridAggregateColumns>
            <GridAggregateColumn Field="Freight" Type="AggregateType.Max" Format="C2">
                <FooterTemplate>
                    @{ var agg = context as AggregateTemplateContext; }
                    <span>Max: @agg.Max</span>
                </FooterTemplate>
            </GridAggregateColumn>
        </GridAggregateColumns>
    </GridAggregate>
</GridAggregates>
```

## Boolean Column Aggregates

```razor
<GridAggregateColumn Field="IsActive" Type="AggregateType.TrueCount">
    <FooterTemplate>
        @{ var agg = context as AggregateTemplateContext; }
        <span>Active: @agg.TrueCount</span>
    </FooterTemplate>
</GridAggregateColumn>
```

## Date Column Aggregates

```razor
<GridAggregateColumn Field="OrderDate" Type="AggregateType.Max" Format="d">
    <FooterTemplate>
        @{ var agg = context as AggregateTemplateContext; }
        <span>Latest: @agg.Max</span>
    </FooterTemplate>
</GridAggregateColumn>
```

## Custom Aggregate

Use `AggregateType.Custom` when built-in types don't fit:

```razor
<GridAggregateColumn Field="ShipCountry" Type="AggregateType.Custom">
    <FooterTemplate>
        <span>Brazil Orders: @GetBrazilCount()</span>
    </FooterTemplate>
</GridAggregateColumn>

@code {
    private int GetBrazilCount()
    {
        return Orders.Count(x => x.ShipCountry == "Brazil");
    }
}
```

## Reactive Aggregates (Batch Editing)

Aggregates auto-update when editing in `EditMode.Batch` — no extra configuration needed:

```razor
<SfGrid DataSource="@Orders" Toolbar="@(new List<string>{ "Update","Cancel" })">
    <GridEditSettings AllowEditing="true" AllowAdding="true" AllowDeleting="true"
                      Mode="EditMode.Batch">
    </GridEditSettings>
    <GridAggregates>
        <GridAggregate>
            <GridAggregateColumns>
                <GridAggregateColumn Field="Freight" Type="AggregateType.Sum" Format="C2">
                    <FooterTemplate>
                        @{ var agg = context as AggregateTemplateContext; }
                        <span>Sum: @agg.Sum</span>
                    </FooterTemplate>
                </GridAggregateColumn>
            </GridAggregateColumns>
        </GridAggregate>
    </GridAggregates>
    ...
</SfGrid>
```

## Notes

- With **local data**: aggregates compute over the entire bound dataset
- With **remote data + paging**: footer aggregates reflect the current page only (unless the server returns total summaries)
- `AggregateTemplateContext` properties: `Sum`, `Average`, `Min`, `Max`, `Count`, `TrueCount`, `FalseCount`
- Use `Format` property (e.g., `"C2"`, `"d"`) for culture-aware display
- Multiple aggregate types for a single column are supported only when one of the aggregate templates is used.