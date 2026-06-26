````markdown
# Sankey Examples Reference

This file collects example patterns referenced from `SKILL.md`:

## basic-usage

```tsx
<SankeyComponent width="90%" height="420px" title="Energy Flow" tooltip={{ enable: true }}>
  <SankeyNodesCollectionDirective>
    <SankeyNodeDirective id="Solar" label={{ text: 'Solar' }} />
    <SankeyNodeDirective id="Generation" label={{ text: 'Generation' }} />
    <SankeyNodeDirective id="Consumption" label={{ text: 'Consumption' }} />
  </SankeyNodesCollectionDirective>
  <SankeyLinksCollectionDirective>
    <SankeyLinkDirective sourceId="Solar" targetId="Generation" value={450} />
    <SankeyLinkDirective sourceId="Generation" targetId="Consumption" value={400} />
  </SankeyLinksCollectionDirective>
  <Inject services={[SankeyTooltip, SankeyLegend, SankeyExport]} />
</SankeyComponent>
```

## custom-node-styles

```tsx
<SankeyComponent
  linkStyle={{ opacity: 0.6, curvature: 0.55, colorType: 'Source' }}
  nodeWidth={12}
  nodePadding={10}
>
  {/* nodes & links */}
</SankeyComponent>
```

## tooltip-template

```tsx
<SankeyComponent
  tooltip={{ enable: true, template: `<div>{source} → {target}: {value}</div>` }}
  tooltipRender={(args) => { args.text = `${args.data.source} → ${args.data.target}: ${args.data.value}`; }}
>
  {/* nodes & links */}
</SankeyComponent>
```

## export-and-print

```tsx
const ref = useRef(null);
<button onClick={() => ref.current?.export('PNG', 'sankey')}>Export</button>
<SankeyComponent ref={ref} /* ... */ />
```

````