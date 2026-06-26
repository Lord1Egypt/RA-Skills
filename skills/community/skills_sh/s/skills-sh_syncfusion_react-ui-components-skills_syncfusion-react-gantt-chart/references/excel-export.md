# Excel Export

## Table of Contents
- [Setup](#setup)
- [Export with Properties](#export-with-properties)
- [Custom Data Source Export](#custom-data-source-export)
- [Multiple Gantt Export](#multiple-gantt-export)
- [CSV Export](#csv-export)
- [Export Events](#export-events)
- [Common Pitfalls](#common-pitfalls)

---

## Setup

Enable Excel and CSV export with `allowExcelExport={true}` and inject `ExcelExport`.

```tsx
import { GanttComponent, Inject, Toolbar, ExcelExport, Selection } from '@syncfusion/ej2-react-gantt';
import { ClickEventArgs } from '@syncfusion/ej2-navigations';

function App() {
  const ganttRef = useRef<any>(null);

  const toolbarOptions = ['ExcelExport', 'CsvExport'];

  const toolbarClick = (args: ClickEventArgs) => {
    if (args.item.id === 'GanttExport_excelexport') {
      ganttRef.current.excelExport();
    } else if (args.item.id === 'GanttExport_csvexport') {
      ganttRef.current.csvExport();
    }
  };

  return (
    <GanttComponent
      id='GanttExport'
      ref={ganttRef}
      dataSource={data}
      taskFields={taskFields}
      toolbar={toolbarOptions}
      toolbarClick={toolbarClick}
      allowExcelExport={true}
      height='400px'
    >
      <Inject services={[Toolbar, ExcelExport, Selection]} />
    </GanttComponent>
  );
}
```

> **Toolbar item IDs** follow the pattern `{ganttId}_{action}` e.g. `GanttExport_excelexport`, `GanttExport_csvexport`.

---

## Export with Properties

Pass `ExcelExportProperties` to customize the export:

```tsx
import { ExcelExportProperties } from '@syncfusion/ej2-react-gantt';

const toolbarClick = (args: ClickEventArgs) => {
  if (args.item.id === 'GanttExport_excelexport') {
    const exportProps: ExcelExportProperties = {
      fileName: 'project-schedule.xlsx',
      dataSource: customData,       // optional: override data
      includeHiddenColumn: true     // include hidden columns
    };
    ganttRef.current.excelExport(exportProps);
  }
};
```

### `ExcelExportProperties` Key Options

| Property | Type | Description |
|---|---|---|
| `fileName` | string | Output file name |
| `dataSource` | object[] | Override data source for export |
| `includeHiddenColumn` | boolean | Export hidden columns |
| `theme` | object | Custom Excel theme/styling |

---

## Custom Data Source Export

Export a specific subset of data dynamically:

```tsx
const toolbarClick = (args: ClickEventArgs) => {
  if (args.item.id === 'GanttExport_excelexport') {
    const excelExportProperties: ExcelExportProperties = {
      dataSource: [data[0], data[1]]   // export only first two records
    };
    ganttRef.current.excelExport(excelExportProperties);
  }
};
```

---

## Multiple Gantt Export

Export data from multiple Gantt instances to the same Excel sheet or separate sheets.

### Same Sheet (AppendToSheet)

```tsx
const toolbarClick = (args: ClickEventArgs) => {
  if (args.item.id === 'FirstGantt_excelexport') {
    const appendProps: ExcelExportProperties = {
      multipleExport: { type: 'AppendToSheet', blankRows: 2 }
    };
    // Export first Gantt, then chain second export with shared workbook data
    const firstExport: Promise<any> = firstGanttRef.current.excelExport(appendProps, true);
    firstExport.then((workbookData: any) => {
      secondGanttRef.current.excelExport(appendProps, false, workbookData);
    });
  }
};
```

### New Sheet (NewSheet)

```tsx
const appendProps: ExcelExportProperties = {
  multipleExport: { type: 'NewSheet' }
};
const firstExport: Promise<any> = firstGanttRef.current.excelExport(appendProps, true);
firstExport.then((workbookData: any) => {
  secondGanttRef.current.excelExport(appendProps, false, workbookData);
});
```

**`multipleExport` options:**
| Property | Values | Description |
|---|---|---|
| `type` | `'AppendToSheet'` \| `'NewSheet'` | Export mode |
| `blankRows` | number | Blank rows between Gantt data (AppendToSheet only) |

### Multiple Export Setup
```tsx
// Each Gantt instance needs allowExcelExport={true} and ExcelExport injected
<GanttComponent id='FirstGantt' ref={firstGanttRef} allowExcelExport={true} toolbar={['ExcelExport']} toolbarClick={toolbarClick} ...>
  <Inject services={[Toolbar, ExcelExport, Selection]} />
</GanttComponent>

<GanttComponent id='SecondGantt' ref={secondGanttRef} allowExcelExport={true} ...>
  <Inject services={[ExcelExport, Selection]} />
</GanttComponent>
```

---

## CSV Export

CSV export uses the same `allowExcelExport` flag and `ExcelExport` module:

```tsx
const toolbarClick = (args: ClickEventArgs) => {
  if (args.item.id === 'GanttExport_csvexport') {
    ganttRef.current.csvExport();
  }
};
```

---

## Export Events

```tsx
<GanttComponent
  excelExportComplete={(args) => console.log('Export done', args)}
  excelQueryCellInfo={(args) => {
    // Customize individual cell styles/values before export
    if (args.column.field === 'Progress' && args.value > 80) {
      args.style = { backgroundColor: '#c8e6c9' };
    }
  }}
  ...
/>
```

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| Export not triggering | `ExcelExport` service not injected | Add `ExcelExport` to `services` |
| Export not triggering | `allowExcelExport` not set | Set `allowExcelExport={true}` |
| Wrong toolbar ID in click handler | Gantt `id` not matching | Toolbar item ID = `{ganttId}_excelexport` |
| Multiple export chaining fails | Not using Promise chain | Use `.then()` on first export's return value |
| CSV same as Excel | Same setup — `csvExport()` handles CSV format | Use `ganttRef.current.csvExport()` separately |
