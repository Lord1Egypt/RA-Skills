# Excel Export Reference - Syncfusion React Pivot Table

## Overview

The Pivot Table supports exporting data to **Excel** (.xlsx) and **CSV** formats. Enable export by setting `allowExcelExport` to **true** and injecting `ExcelExport` module.

### Key Features
- **Excel Export**: Export to .xlsx format preserving formatting
- **CSV Export**: Lightweight plain text format
- **Multiple Tables**: Export multiple pivot tables to single file
- **Custom Styling**: Apply custom headers, footers, themes
- **Page Export**: Export only current viewport (virtualization/paging)

## Basic Setup

```typescript
import { PivotViewComponent, ExcelExport, Inject } from '@syncfusion/ej2-react-pivotview';
import { pivotData } from './datasource';

function App() {
  return (
    <PivotViewComponent
      id="PivotView"
      dataSourceSettings={{ dataSource: pivotData }}
      allowExcelExport={true}
    >
      <Inject services={[ExcelExport]} />
    </PivotViewComponent>
  );
}

export default App;
```

## Export Methods

### Excel Export

Call `excelExport()` method to export data to Excel:

```typescript
function btnClick(): void {
  pivotObj.excelExport();
}
```

### CSV Export

Call `csvExport()` method to export data to CSV:

```typescript
function btnClick(): void {
  pivotObj.csvExport();
}
```

## Multiple Pivot Tables

### Export to Same Worksheet

Use `multipleExport.type: AppendToSheet` to append tables to same sheet:

```typescript
let excelExportProperties: ExcelExportProperties = {
  multipleExport: { type: AppendToSheet, blankRows: 2 },
  pivotTableIds: ['PivotView', 'PivotView1']
};
pivotObj.excelExport(excelExportProperties, true);
```

### Export to New Worksheet

Use `multipleExport.type: NewSheet` for separate worksheets:

```typescript
let excelExportProperties: ExcelExportProperties = {
  multipleExport: { type: NewSheet },
  pivotTableIds: ['PivotView', 'PivotView1']
};
pivotObj.excelExport(excelExportProperties, true);
```

## Export Customization

### Before Export Event

Use `beforeExport` event to customize data before export:

```typescript
function beforeExport(args: BeforeExportEventArgs): void {
  pivotObj.setProperties(
    { dataSourceSettings: { expandAll: true, drilledMembers: [] } },
    true
  );
  pivotObj.engineModule.generateGridData(pivotObj.dataSourceSettings, true);
  args.dataCollections = [pivotObj.engineModule.pivotValues];
  pivotObj.setProperties(
    { dataSourceSettings: { expandAll: false, drilledMembers: member } },
    true
  );
}
```

### Custom Aggregates

Define custom aggregate types for export:

```typescript
const SummaryType: string[] = [
  Sum, Count, DistinctCount, Avg,
  CustomAggregateType1, CustomAggregateType2
];

function dataBound(): void {
  pivotObj.getAllSummaryType = function () {
    return SummaryType as AggregateTypes[];
  };
}

function aggregateCell(args: AggregateEventArgs): void {
  if (args.aggregateType === CustomAggregateType1 as SummaryTypes) {
    args.value = args.value as number * 100;
  }
}
```

### Custom Date Format

Use `formatSettings` with `type: date` for date formatting:

```typescript
formatSettings: [{ name: Date, type: date, format: EEE, MMM d, ''yy }]
```

> Note: The `Group_Data` export should be included in your datasource file.

### Remove Row Headers

Use `beforeExport` event to exclude row headers from export:

```typescript
function beforeExport(args: BeforeExportEventArgs): void {
  for (let i: number = 0; i < args.dataCollections.length; i++) {
    const pivotValue: IAxisSet[] = args.dataCollections[i];
    for (let j: number = 0; j < pivotValue.length; j++) {
      pivotValue[j] = pivotValue[j].filter((item: any) => {
        return item !== null && (item.axis !== row);
      });
    }
  }
}
```

### Exclude Hidden Columns

Set `includeHiddenColumn: false` in export properties:

```typescript
let excelExportProperties: ExcelExportProperties = {
  includeHiddenColumn: false
};
pivotObj.excelExport(excelExportProperties);
```

## Styling Options

### Rotate Cell Text

Use `excelHeaderQueryCellInfo` and `excelQueryCellInfo` events:

```typescript
function excelHeaderQueryCellInfo(args: ExcelHeaderQueryCellInfoEventArgs): void {
  args.style.rotation = 45;
}
```

### Conditional Styling

Apply styles based on cell values:

```typescript
function excelQueryCellInfo(args: ExcelQueryCellInfoEventArgs): void {
  if (args.column.field === Sold) {
    args.style.backColor = args.value < 700 ? #ff0000 : #00ff00;
  }
}
```

### Theme and Colors

Define theme settings for export:

```typescript
let excelExportProperties: ExcelExportProperties = {
  theme: { header: { fontColor: #FF0000 } }
};
```

### Header and Footer

Add header/footer content to exported file:

```typescript
let excelExportProperties: ExcelExportProperties = {
  header: { content: Sales Report },
  footer: { content: Generated:  + new Date().toLocaleDateString() }
};
```

### Custom File Name

Set custom file name using `fileName` property:

```typescript
let excelExportProperties: ExcelExportProperties = {
  fileName: custom-export.xlsx
};
```

## Events

### excelQueryCellInfo

Triggered for each row/value cell during export. Provides `value`, `column`, `data`, and `style` arguments.

### excelHeaderQueryCellInfo

Triggered for each header cell. Provides `cell` and `style` arguments.

### exportComplete

Triggered after export completes. Use `isBlob` parameter to get blob data:

```typescript
function exportComplete(args: ExportCompleteEventArgs): void {
  args.promise.then((e: { blobData: Blob }) => {
    console.log(e.blobData);
  });
}

pivotObj.excelExport(excelExportProperties, false, null, true);
```

## Performance Tips

1. **Virtual Scrolling**: Enable to efficiently export large datasets
2. **Current Page Only**: Set `exportAllPages: false` to export only visible data
3. **CSV Format**: For very large datasets, prefer CSV over Excel format

## Best Practices

✅ **Do:**
- Use `exportAllPages: false` with virtualization for better performance
- Use CSV format for datasets exceeding Excel's 1,048,576 row limit
- Set `isBlob: true` when you need to process the exported file programmatically

❌ **Don't:**
- Export millions of records to Excel (use CSV instead)
- Forget to inject `ExcelExport` module
- Use full URLs - reference API names in backticks like `excelExport`

## Common Issues

**Export not working?**
- Verify `ExcelExport` is in the `Inject` services array
- Check `allowExcelExport` is set to **true**

**Large file sizes?**
- Use `exportAllPages: false` to export only current viewport
- Consider CSV format for large datasets

**Styling not applied?**
- Ensure event handlers are properly bound
- Check that `gridSettings` is passed to PivotViewComponent

## Related Features

- **PDF Export**: Export to PDF format
- **Toolbar**: Export options in toolbar UI
- **Virtualization**: Handle large datasets efficiently
