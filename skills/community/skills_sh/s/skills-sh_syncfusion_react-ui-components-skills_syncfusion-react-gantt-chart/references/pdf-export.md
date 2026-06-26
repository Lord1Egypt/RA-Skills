# PDF Export

## Table of Contents
- [Setup](#setup)
- [Export Properties](#export-properties)
- [Header and Footer](#header-and-footer)
- [Gantt Style Customization](#gantt-style-customization)
- [Data Markers / Indicators in PDF Export](#data-markers--indicators-in-pdf-export)
- [Complete Example](#complete-example)
- [Common Pitfalls](#common-pitfalls)

---

## Setup

Enable PDF export with `allowPdfExport={true}` and inject `PdfExport`.

> **Note:** Manually scheduled tasks are not supported in PDF export.

```tsx
import { GanttComponent, Inject, Toolbar, PdfExport, Selection } from '@syncfusion/ej2-react-gantt';
import { ClickEventArgs } from '@syncfusion/ej2-navigations';

function App() {
  const ganttRef = useRef<any>(null);

  const toolbarOptions = ['PdfExport'];

  const toolbarClick = (args: ClickEventArgs) => {
    if (args.item.text === 'PDF export') {
      ganttRef.current.pdfExport();
    }
  };

  return (
    <GanttComponent
      id='root'
      ref={ganttRef}
      dataSource={data}
      taskFields={taskFields}
      toolbar={toolbarOptions}
      toolbarClick={toolbarClick}
      allowPdfExport={true}
      height='400px'
    >
      <Inject services={[Toolbar, PdfExport, Selection]} />
    </GanttComponent>
  );
}
```

---

## Export Properties

Pass `PdfExportProperties` to `pdfExport()` to customize the output:

```tsx
import { PdfExportProperties } from '@syncfusion/ej2-react-gantt';

const toolbarClick = (args: ClickEventArgs) => {
  if (args.item.text === 'PDF export') {
    const exportProps: PdfExportProperties = {
      fileName: 'project-schedule.pdf',
      pageOrientation: 'Portrait',    // default: 'Landscape'
      pageSize: 'A3',
      fitToWidthSettings: {
        isFitToWidth: true
      }
    };
    ganttRef.current.pdfExport(exportProps);
  }
};
```

### `PdfExportProperties` Key Options

| Property | Type / Values | Description |
|---|---|---|
| `fileName` | string | Output file name |
| `pageOrientation` | `'Portrait'` \| `'Landscape'` | Page orientation (default: Landscape) |
| `pageSize` | `'A3'` \| `'A4'` \| `'Letter'` etc. | Page size |
| `fitToWidthSettings` | `{ isFitToWidth: boolean }` | Fit chart to page width |
| `header` | `PdfHeader` | Custom header configuration |
| `footer` | `PdfFooter` | Custom footer configuration |
| `ganttStyle` | `PdfGanttStyle` | Customize fonts, colors, taskbar appearance |

---

## Header and Footer

Add text, lines, images, and page numbers to headers/footers.

### Text in Header
```tsx
const exportProps: PdfExportProperties = {
  header: {
    fromTop: 0,
    height: 130,
    contents: [
      {
        type: 'Text',
        value: 'Project Schedule Report',
        position: { x: 200, y: 10 },
        style: { textBrushColor: '#C25050', fontSize: 20 }
      }
    ]
  }
};
```

### Line in Header
```tsx
contents: [
  {
    type: 'Line',
    style: { penColor: '#000080', penSize: 2, dashStyle: 'Solid' },
    points: { x1: 0, y1: 4, x2: 685, y2: 4 }
  }
]
```

**Supported `dashStyle` values:** `'Solid'`, `'Dash'`, `'Dot'`, `'DashDot'`, `'DashDotDot'`

### Page Number in Footer
```tsx
const exportProps: PdfExportProperties = {
  footer: {
    fromBottom: 160,
    height: 150,
    contents: [
      {
        type: 'PageNumber',
        pageNumberType: 'Arabic',           // '1', '2', ...
        format: 'Page {$current} of {$total}',
        position: { x: 0, y: 25 },
        style: { textBrushColor: '#000000', fontSize: 12 }
      }
    ]
  }
};
```

**`pageNumberType` values:** `'Arabic'`, `'LowerLatin'`, `'UpperLatin'`, `'LowerRoman'`, `'UpperRoman'`

### Image in Header
```tsx
contents: [
  {
    type: 'Image',
    src: base64ImageString,       // base64 encoded image
    position: { x: 40, y: 10 },
    size: { height: 100, width: 250 }
  }
]
```

---

## Gantt Style Customization

Customize fonts, colors, and taskbar appearance:
```tsx
import { PdfColor, PdfTrueTypeFont } from '@syncfusion/ej2-pdf-export';

const exportProps: PdfExportProperties = {
  ganttStyle: {
    taskbar: {
      taskColor: new PdfColor(240, 128, 128),
      progressColor: new PdfColor(205, 92, 92),
      taskBorderColor: new PdfColor(205, 92, 92)
    },
    label: {
      fontColor: new PdfColor(0, 0, 0)
    },
    columnHeader: {
      backgroundColor: new PdfColor(179, 219, 255)
    },
    chartRow: {
      backgroundColor: new PdfColor(240, 248, 255)
    }
  }
};
```

---

## Data Markers / Indicators in PDF Export

Add image-based indicators to tasks in exported PDFs using `base64` image in data source:
```typescript
const data = [
  {
    TaskID: 1, TaskName: 'Planning',
    StartDate: new Date('04/02/2019'), EndDate: new Date('04/21/2019'),
    Indicators: [
      {
        date: new Date('04/10/2019'),
        base64: '/9j/4AAQSkZJRg...',   // base64 image string
        name: 'review',
        tooltip: 'Review Meeting'
      }
    ]
  }
];

const taskFields = {
  ...
  indicators: 'Indicators'
};
```

---

## Complete Example

```tsx
import React, { useRef } from 'react';
import { GanttComponent, Inject, Toolbar, PdfExport, Selection } from '@syncfusion/ej2-react-gantt';
import { ClickEventArgs } from '@syncfusion/ej2-navigations';
import { PdfExportProperties } from '@syncfusion/ej2-react-gantt';

function App() {
  const ganttRef = useRef<any>(null);

  const taskFields = {
    id: 'TaskID', name: 'TaskName',
    startDate: 'StartDate', duration: 'Duration',
    progress: 'Progress', child: 'subtasks'
  };

  const toolbarClick = (args: ClickEventArgs) => {
    if (args.item.text === 'PDF export') {
      const exportProps: PdfExportProperties = {
        fileName: 'schedule.pdf',
        pageOrientation: 'Landscape',
        header: {
          fromTop: 0, height: 80,
          contents: [
            { type: 'Text', value: 'Project Plan', position: { x: 200, y: 10 },
              style: { textBrushColor: '#2563EB', fontSize: 18 } }
          ]
        },
        footer: {
          fromBottom: 100, height: 60,
          contents: [
            { type: 'PageNumber', pageNumberType: 'Arabic',
              format: 'Page {$current} of {$total}',
              position: { x: 0, y: 10 },
              style: { textBrushColor: '#666666', fontSize: 10 } }
          ]
        }
      };
      ganttRef.current.pdfExport(exportProps);
    }
  };

  return (
    <GanttComponent
      id='ganttPdf'
      ref={ganttRef}
      dataSource={data}
      taskFields={taskFields}
      toolbar={['PdfExport']}
      toolbarClick={toolbarClick}
      allowPdfExport={true}
      height='400px'
    >
      <Inject services={[Toolbar, PdfExport, Selection]} />
    </GanttComponent>
  );
}

export default App;
```

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| PDF export not working | `PdfExport` service not injected | Add `PdfExport` to `services` |
| PDF export not working | `allowPdfExport` not set | Set `allowPdfExport={true}` |
| Manual tasks missing in PDF | Not supported | Convert to auto-scheduled or exclude them |
| Toolbar click not matching | Wrong `args.item.text` check | Use `args.item.text === 'PDF export'` (case-sensitive) |
| Image not showing in header | Invalid base64 or wrong `src` field | Ensure valid base64 image data |
| Portrait vs Landscape | Default is Landscape | Set `pageOrientation: 'Portrait'` explicitly if needed |
