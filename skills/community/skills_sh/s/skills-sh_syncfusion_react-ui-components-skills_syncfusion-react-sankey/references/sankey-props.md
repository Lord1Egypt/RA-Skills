````markdown
# Sankey Props Reference

Source: [SankeyComponent API](https://ej2.syncfusion.com/react/documentation/api/sankey/index-default)

This file lists primary props for the `SankeyComponent`. Complex/nested props link to their model pages on the official Syncfusion docs.

## Props

- `accessibility` — [AccessibilityModel](https://ej2.syncfusion.com/react/documentation/api/sankey/accessibilitymodel) — Accessibility options for the component.
- `allowExport` — `boolean` — default: `false` — Enables export in specific scenarios. See component API.
- `animation` — [AnimationModel](https://ej2.syncfusion.com/react/documentation/api/sankey/animationmodel) — Animation configuration for render transitions.
- `background` — `string` — default: `null` — Background color value.
- `backgroundImage` — `string` — default: `null` — URL for background image.
- `border` — [BorderModel](https://ej2.syncfusion.com/react/documentation/api/sankey/bordermodel) — Outer border configuration.
- `enableExport` — `boolean` — default: `true` — When true, enables export of the diagram into supported formats.
- `enablePersistence` — `boolean` — default: `false` — Persist component state between reloads.
- `enableRtl` — `boolean` — default: `false` — Enable right-to-left rendering.
- `focusBorderColor` — `string` — default: `null` — Focus border color for interactive elements.
- `focusBorderMargin` — `number` — default: `0` — Focus border margin.
- `focusBorderWidth` — `number` — default: `1.5` — Focus border width.
- `height` — `string` — default: `null` — Component height (e.g., `"420px"` or `"100%"`).
- `labelSettings` — [SankeyLabelSettingsModel](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylabelsettingsmodel) — Configure node and link labels.
- `legendSettings` — [SankeyLegendSettingsModel](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylegendsettingsmodel) — Legend configuration.
- `linkStyle` — [SankeyLinkSettingsModel](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylinksettingsmodel) — Global link styling (opacity, colorType, curvature).
- `links` — [SankeyLinkModel[]](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeylinkmodel) — default: `[]` — Collection of link definitions (source / target / value).
- `locale` — `string` — default: `''` — Culture/locale override for this component.
- `margin` — [MarginModel](https://ej2.syncfusion.com/react/documentation/api/sankey/marginmodel) — Margin configuration around the component.
- `nodeLayoutMap` — `{ [key: string]: SankeyNodeLayout }` — Computed node layout map (internal structure).
- `nodeStyle` — [SankeyNodeSettingsModel](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeynodesettingsmodel) — Node style configuration (size, color, text alignment).
- `nodes` — [SankeyNodeModel[]](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeynodemodel) — default: `[]` — Collection of node definitions.
- `orientation` — `Orientation` — default: `Horizontal` — Diagram orientation (see API: [orientation](https://ej2.syncfusion.com/react/documentation/api/sankey/index-default#orientation)).
- `subTitle` — `string` — default: `''` — Subtitle text.
- `subTitleStyle` — [SankeyTitleStyleModel](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeytitlestylemodel) — Subtitle style options.
- `theme` — [ChartTheme](https://ej2.syncfusion.com/react/documentation/api/sankey/charttheme) — default: `Material` — Component theme.
- `title` — `string` — default: `''` — Main title text.
- `titleStyle` — [SankeyTitleStyleModel](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeytitlestylemodel) — Title style options.
- `tooltip` — [SankeyTooltipSettingsModel](https://ej2.syncfusion.com/react/documentation/api/sankey/sankeytooltipsettingsmodel) — Tooltip configuration (enable/template/format).
- `width` — `string` — default: `null` — Component width (e.g., `"90%"` or `"800px"`).

## Notes

- This summary links to model pages for complex/nested props — follow those links for full property shapes and examples.
- Numeric defaults and enum token names (if you require absolute precision) should be verified against the official API live page: https://ej2.syncfusion.com/react/documentation/api/sankey/index-default

````