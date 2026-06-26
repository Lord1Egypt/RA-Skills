---
title: serialization-and-export
description: Save and load diagrams as JSON, export to image/SVG, print diagrams, import/export Visio files, and work with Mermaid syntax in the Syncfusion React Diagram component.
---

# Serialization and Export

## Overview

The Syncfusion React Diagram component supports full persistence through JSON serialization, image/SVG export, print output, Visio file import/export, and Mermaid syntax conversion. All export and print features require injecting the `PrintAndExport` module. Visio import/export requires injecting `ImportAndExportVisio`.

## Save and Load (JSON Serialization)

### Save a Diagram

Use `saveDiagram()` to serialize the entire diagram to a JSON string. Store it in localStorage, a database, or download as a file.

```tsx
// Save to string
const saveData: string = diagramInstance.saveDiagram();

// Store in localStorage
localStorage.setItem('myDiagram', saveData);

```

### Load a Diagram

Use `loadDiagram()` to restore a diagram from a previously saved JSON string. The existing diagram content is automatically cleared before loading.

```tsx
// Load from string
diagramInstance.loadDiagram(saveData);

// Handle load completion
<DiagramComponent
  loaded={(args) => {
    // Runs after all elements finish loading
    // Customize or validate elements here
  }}
/>
```

### Reduce Serialized File Size

Set `serializationSettings.preventDefaults` to `true` to exclude default-value properties from the JSON output. This significantly reduces file size for large diagrams.

```tsx
<DiagramComponent
  serializationSettings={{ preventDefaults: true }}
/>
```

### Load from File Upload

Use the `UploaderComponent` to let users select a saved JSON file, then pass the file contents to `loadDiagram()`.

```tsx
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function onUploadSuccess(args: { file: any }) {
  const reader = new FileReader();
  reader.readAsText(args.file.rawFile);
  reader.onloadend = (e: any) => {
    diagramInstance.loadDiagram(e.target.result);
  };
}

<UploaderComponent
  asyncSettings={{ saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save', removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove' }}
  success={onUploadSuccess}
/>
```

## Export to Image or SVG

Inject `PrintAndExport` and call `exportDiagram(options)` to export the diagram.

```tsx
import { DiagramComponent, Inject, PrintAndExport, IExportOptions } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent ...>
  <Inject services={[PrintAndExport]} />
</DiagramComponent>
```

### Export Formats

| Format | Description |
|--------|-------------|
| `'JPG'` | Compressed, suitable for complex color diagrams (default) |
| `'PNG'` | Lossless, ideal for transparency or sharp edges |
| `'SVG'` | Vector format, scales without quality loss |

```tsx
const options: IExportOptions = {
  format: 'PNG',           // 'JPG' | 'PNG' | 'SVG'
  fileName: 'MyDiagram',
  mode: 'Download',        // 'Download' | 'Data'
};
diagramInstance.exportDiagram(options);
```

### Export Modes

- **`'Download'`** — Automatically downloads the file to the user's device.
- **`'Data'`** — Returns a base64 string for programmatic processing.

```tsx
const options: IExportOptions = { mode: 'Data', format: 'SVG' };
const base64String = diagramInstance.exportDiagram(options) as string;
```

### Export Region

Control which part of the diagram is exported using the `region` property.

| Region | Description |
|--------|-------------|
| `'Content'` | Only the visible elements, excluding empty space |
| `'PageSettings'` | Based on configured page dimensions |
| `'CustomBounds'` | A user-defined rectangular area |

```tsx
import { Rect } from '@syncfusion/ej2-react-diagrams';

// Export only diagram content
diagramInstance.exportDiagram({ region: 'Content' });

// Export a custom region
diagramInstance.exportDiagram({
  region: 'CustomBounds',
  bounds: new Rect(0, 0, 400, 300),
});
```

### Export Options Reference

| Property | Type | Description |
|----------|------|-------------|
| `fileName` | string | Downloaded file name (default: `'Diagram'`) |
| `format` | string | `'JPG'` \| `'PNG'` \| `'SVG'` |
| `mode` | string | `'Download'` \| `'Data'` |
| `region` | enum | `'Content'` \| `'PageSettings'` \| `'CustomBounds'` |
| `bounds` | Rect | Required when `region` is `'CustomBounds'` |
| `margin` | object | Whitespace around exported content `{ left, top, right, bottom }` |
| `stretch` | enum | Adjust aspect ratio for better quality (`'Stretch'`) |
| `multiplePage` | boolean | Split across multiple pages when `true` |
| `pageWidth` | number | Page width for multi-page exports |
| `pageHeight` | number | Page height for multi-page exports |
| `pageOrientation` | enum | `'Portrait'` \| `'Landscape'` |

### Multi-Page Export

```tsx
diagramInstance.exportDiagram({
  multiplePage: true,
  region: 'PageSettings',
});
// Also configure pageSettings on the diagram:
// pageSettings={{ width: 400, height: 300, multiplePage: true, showPageBreaks: true }}
```

## Print Diagram

Inject `PrintAndExport` and call `print(options)`.

```tsx
import { IPrintOptions } from '@syncfusion/ej2-react-diagrams';

const printOptions: IPrintOptions = {
  region: 'PageSettings',       // 'Content' | 'PageSettings'
  multiplePage: true,
  pageOrientation: 'Portrait',  // 'Portrait' | 'Landscape'
  pageWidth: 816,
  pageHeight: 1056,
  margin: { left: 10, top: 10, right: 10, bottom: 10 },
};
diagramInstance.print(printOptions);
```

`IPrintOptions` supports the same `region`, `margin`, `stretch`, `multiplePage`, `pageWidth`, `pageHeight`, and `pageOrientation` properties as `IExportOptions`.

## Mermaid Syntax

### Save as Mermaid

Supported layouts: Flowchart, MindMap, UML Sequence Diagram.

```tsx
const mermaidString: string = diagramInstance.saveDiagramAsMermaid();
```

### Load from Mermaid

```tsx
import { Inject, FlowchartLayout } from '@syncfusion/ej2-react-diagrams';

const mermaidData = `flowchart TD
  A[Start] --> B(Process)
  B --> C{Decision}
  C --Yes--> D[Plan 1]
  C --No--> E[Plan 2]`;

diagramInstance.loadDiagramFromMermaid(mermaidData);

// DiagramComponent must have appropriate layout and inject:
<DiagramComponent layout={{ type: 'Flowchart' }}>
  <Inject services={[FlowchartLayout]} />
</DiagramComponent>
```

> Mermaid serialization only supports Flowchart, MindMap, and UML Sequence Diagram layouts.

## Visio Import and Export

> Visio import/export support is currently **experimental**. Inject `ImportAndExportVisio`.

### Import a Visio File

```tsx
import { ImportAndExportVisio, IImportingEventArgs } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  diagramImporting={(args: IImportingEventArgs) => {
    if (args.status === 'started') {
      // Select a specific page from multi-page Visio files:
      // args.selectedPage = args.pages[0];
      // Cancel import: args.cancel = true;
    } else if (args.status === 'completed') { /* hide loader */ }
    else if (args.status === 'failed') { console.error(args); }
  }}
>
  <Inject services={[ImportAndExportVisio]} />
</DiagramComponent>

// Trigger import with a File object:
const warnings = await diagramInstance.importFromVisio(fileObject, { pageIndex: 0 });
```

**Import options:**

| Property | Description |
|----------|-------------|
| `pageIndex` | Zero-based page index to import (default: `0`) |

### Export to Visio

```tsx
import { VisioExportOptions, IExportingEventArgs } from '@syncfusion/ej2-react-diagrams';

const exportOptions: VisioExportOptions = {
  fileName: 'diagram.vsdx',
  pageName: 'Page-1',
};
diagramInstance.exportToVisio(exportOptions);
```

**`diagramExporting` event arguments:** `status` (`'started'` | `'completed'` | `'failed'`), `cancel` (set to `true` to abort), `logs`.

## Best Practices

- Enable `preventDefaults` in `serializationSettings` for large diagrams to reduce JSON payload size.
- Use `mode: 'Data'` when you need to process or upload the exported image server-side.
- For Visio round-trips, verify supported shape types — gradient fills, rich text, and compound line styles are not preserved.
- Always inject `PrintAndExport` before calling `exportDiagram()` or `print()`; calls without injection will silently fail.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `exportDiagram` or `print` has no effect | Ensure `PrintAndExport` is injected via `<Inject services={[PrintAndExport]} />` |
| HTML/native nodes missing from export | Browser security prevents this; use Syncfusion PDF library with Blink renderer |
| Visio import produces incorrect layout | Ruler origin differences (Visio = bottom-left, Diagram = top-left); adjust offsets post-import |
| Large JSON file slowing saves | Set `serializationSettings={{ preventDefaults: true }}` |
| Mermaid load fails | Confirm diagram type is Flowchart, MindMap, or UML Sequence; other layouts are unsupported |
