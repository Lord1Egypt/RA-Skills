````markdown
# Sankey Events Reference

Source: [SankeyComponent API events](https://ej2.syncfusion.com/react/documentation/api/sankey/index-default#events)

Below are events exposed by `SankeyComponent`. Complex event argument types link to their API pages.

- `afterExport(args)` — (see component exports) — Fired after export completes.
- `beforeExport(args)` — [SankeyExportEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeyexporteventargs) — Fired before export starts; cancelable.
- `beforePrint(args)` — [SankeyPrintEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeyprinteventargs) — Fired before print starts.
- `exportCompleted(args)` — [SankeyExportedEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeyexportedeventargs) — Fired after export completes.
- `labelRendering(args)` — [SankeyLabelRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylabelrendereventargs) — Fired before a label is rendered; allows customization.
- `legendItemHover(args)` — [SankeyLegendItemHoverEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylegenditemhovereventargs) — When mouse hovers a legend item.
- `legendItemRendering(args)` — [SankeyLegendRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylegendrendereventargs) — Fired before a legend item renders; customize label/shape.
- `linkClick(args)` — [SankeyLinkEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylinkeventargs) — Fired when a link is clicked.
- `linkEnter(args)` — [SankeyLinkEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylinkeventargs) — Fired when mouse enters a link.
- `linkLeave(args)` — [SankeyLinkEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylinkeventargs) — Fired when mouse leaves a link.
- `linkRendering(args)` — [SankeyLinkRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylinkrendereventargs) — Fired before a link is rendered; allows style overrides.
- `load(args)` — [SankeyLoadedEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeyloadedeventargs) — Fired before the sankey loads; use to modify initial config.
- `loaded(args)` — [SankeyLoadedEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeyloadedeventargs) — Fired after the sankey fully loads.
- `nodeClick(args)` — [SankeyNodeEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeynodeeventargs) — Fired when a node is clicked.
- `nodeEnter(args)` — [SankeyNodeEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeynodeeventargs) — Fired when mouse enters a node.
- `nodeLeave(args)` — [SankeyNodeEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeynodeeventargs) — Fired when mouse leaves a node.
- `nodeRendering(args)` — [SankeyNodeRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeynoderendereventargs) — Fired before a node renders; allows customization.
- `sizeChanged(args)` — [SankeySizeChangedEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeysizechangedeventargs) — Fired when chart size changes.
- `tooltipRendering(args)` — [SankeyTooltipRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeytooltiprendereventargs) — Fired before a tooltip is shown.

## Usage

Attach handlers directly to the component:

```tsx
<SankeyComponent
  beforeExport={(args) => {/* ... */}}
  linkClick={(args) => {/* ... */}}
  tooltipRendering={(args) => {/* ... */}}
>
  {/* ... */}
</SankeyComponent>
```

Follow linked argument pages for full `args` object shapes and available fields.

````