# Infinite Scrolling — Syncfusion Blazor DataGrid

## Table of Contents
- [Enable Infinite Scrolling](#enable-infinite-scrolling)
- [GridInfiniteScrollSettings](#gridinfinitescrollsettings)
- [Cache Mode](#cache-mode)
- [Limitations](#limitations)
  - [Incompatible features](#incompatible-features)
  - [Selection](#selection)
  - [Grouping](#grouping)
  - [Aggregates](#aggregates)
  - [Row drag and drop](#row-drag-and-drop)

## Enable Infinite Scrolling

Loads data in blocks as the scrollbar reaches the bottom:

```razor
<SfGrid DataSource="@Orders" Height="400" EnableInfiniteScrolling="true">
    <GridPageSettings PageSize="50"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

- `Height` is **required** (a fixed container height must be set; using `100%` only works if the Grid **and** its parent container both have explicit heights)
- `PageSize` defines block size (auto-calculated from viewport if not set)
- New rows are appended to the DOM as you scroll down
- The combined height of the initially loaded rows must exceed the viewport height for scrolling to work

> **Browser limitation:** The maximum number of records the Grid can load is constrained by browser element height limits.

## GridInfiniteScrollSettings

```razor
<SfGrid DataSource="@Orders" Height="400" EnableInfiniteScrolling="true">
    <GridInfiniteScrollSettings InitialBlocks="3" EnableCache="false" MaximumBlocks="3">
    </GridInfiniteScrollSettings>
    <GridPageSettings PageSize="50"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

| Property | Default | Description |
|---|---|---|
| `InitialBlocks` | 3 | Number of blocks loaded on initial render |
| `EnableCache` | `false` | Reuse cached blocks (limits DOM row count) |
| `MaximumBlocks` | 3 | Max cached blocks in DOM when `EnableCache=true` |

## Cache Mode

When `EnableCache="true"`, only `MaximumBlocks * PageSize` rows are kept in DOM. Older blocks are replaced:

```razor
<GridInfiniteScrollSettings EnableCache="true" MaximumBlocks="5">
</GridInfiniteScrollSettings>
```

> **Cache mode limitations:**
> - Cell selection is not persisted across cached blocks.
> - Group records **cannot be collapsed** in cache mode.
> - Lazy load grouping with infinite scrolling **does not support cache mode**; infinite scrolling applies only to parent-level caption rows in that scenario.
> - In cache mode, the Grid refreshes automatically if the number of `<tr>` elements exceeds the cache limit after a row drag-and-drop action.

Use `Refresh()` after toggling cache settings to apply changes:

```razor
private void Change(ChangeEventArgs<bool> args)
{
    IsEnabled = args.Checked;
    Grid.Refresh();
}
```

## Limitations

### Incompatible features
- **Not compatible with:** batch editing, normal editing (inline), row template, row virtual scrolling, detail template, hierarchy, autofill

### Selection
- `SelectRowAsync` / `SelectRowsAsync` programmatic row selection is not supported
- Cell selection is not persisted in cache mode

### Grouping
- Group records cannot be collapsed in cache mode
- In **normal grouping**, infinite scrolling is not supported for child items during expand/collapse — all child items load when caption rows are toggled
- **Lazy load grouping** with infinite scrolling does not support cache mode; infinite scrolling applies only to parent-level caption rows

### Aggregates
- Aggregates and total group items reflect only the **current view items** (expected behavior with on-demand data loading)

### Row drag and drop
- Copy-paste and drag-and-drop apply only to items within the current viewport
- In cache mode, the Grid auto-refreshes if content `<tr>` count exceeds cache limit after a drop
- With lazy load grouping, the Grid auto-refreshes after row drag and drop
- For **remote data**, drag-and-drop changes apply only in the UI and are lost after refresh unless persisted to the server — use the `RowDropped` event to commit changes server-side before refreshing:

```razor
<GridEvents TValue="TaskDetails" RowDropped="RowDropHandler"></GridEvents>

@code {
    public async Task RowDropHandler(RowDroppedEventArgs<TaskDetails> args)
    {
        // Persist dropped row changes to server here, then refresh
        await Grid.Refresh();
    }
}

