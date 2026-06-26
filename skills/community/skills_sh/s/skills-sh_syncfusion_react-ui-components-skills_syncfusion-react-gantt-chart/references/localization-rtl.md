# Localization and RTL in Syncfusion React Gantt Chart

## Table of Contents
- [Overview](#overview)
- [Setting the Locale](#setting-the-locale)
- [Loading Custom Translations](#loading-custom-translations)
- [Gantt Locale Keys Reference](#gantt-locale-keys-reference)
- [RTL (Right-to-Left) Support](#rtl-right-to-left-support)
- [Column Number and Date Formatting](#column-number-and-date-formatting)
- [Common Pitfalls](#common-pitfalls)

---

## Overview

The Gantt component supports localization (translating built-in UI text) and RTL layout for global deployments. These are controlled via:

- `locale` prop — sets the active language/culture
- `L10n.load()` — registers translation strings for the `'gantt'` namespace
- `enableRtl` prop — flips the component layout direction

---

## Setting the Locale

Pass the locale string to the `locale` prop on `GanttComponent`:

```tsx
<GanttComponent
  locale='de'
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>
```

> Built-in locale strings for many languages are available from the `@syncfusion/ej2-locale` package. For custom translations, use `L10n.load()`.

---

## Loading Custom Translations

Use `L10n.load()` from `@syncfusion/ej2-base` to register translation strings before the component renders. Strings are scoped to the `'gantt'` namespace:

```tsx
import { L10n } from '@syncfusion/ej2-base';

// Call this BEFORE the component renders (e.g., at the top of your module)
L10n.load({
  'de': {
    'gantt': {
      'emptyRecord': 'Keine Daten vorhanden',
      'id': 'ID',
      'name': 'Name',
      'startDate': 'Startdatum',
      'endDate': 'Enddatum',
      'duration': 'Dauer',
      'progress': 'Fortschritt',
      'dependency': 'Abhängigkeit',
      'notes': 'Notizen',
      'addDialogTitle': 'Neue Aufgabe',
      'editDialogTitle': 'Aufgabe bearbeiten',
      'saveButton': 'Speichern',
      'cancelButton': 'Abbrechen',
      'deleteButton': 'Löschen',
      'add': 'Hinzufügen',
      'edit': 'Bearbeiten',
      'update': 'Aktualisieren',
      'delete': 'Löschen',
      'cancel': 'Abbrechen',
      'search': 'Suchen',
      'task': 'Aufgabe',
      'tasks': 'Aufgaben',
      'expandAll': 'Alle erweitern',
      'collapseAll': 'Alle reduzieren',
      'zoomIn': 'Vergrößern',
      'zoomOut': 'Verkleinern',
      'zoomToFit': 'Anpassen',
      'excelExport': 'Excel-Export',
      'csvExport': 'CSV-Export',
      'pdfExport': 'PDF-Export',
      'okText': 'OK',
      'confirmDelete': 'Möchten Sie den Datensatz wirklich löschen?',
      'from': 'Von',
      'to': 'Bis',
      'taskLink': 'Aufgabenverknüpfung',
      'lag': 'Verzögerung',
      'start': 'Start',
      'finish': 'Ende',
      'enterValue': 'Wert eingeben',
      'taskBeforePredecessor_FS': 'Sie haben "{0}" verschoben, bevor "{1}" fertig ist',
      'taskAfterPredecessor_FS': 'Sie haben "{0}" von "{1}" weg verschoben',
    }
  }
});

function App() {
  return (
    <GanttComponent
      locale='de'
      dataSource={data}
      taskFields={taskFields}
      height='450px'
    />
  );
}
```

> `L10n.load()` must be called **before** the component mounts. Place it at the module level (outside the component function), or in a bootstrap/setup file.

---

## Gantt Locale Keys Reference

These are the most commonly used keys in the `'gantt'` namespace:

| Key | Default (English) | Description |
|---|---|---|
| `emptyRecord` | `'No records to display'` | Empty data message |
| `id` | `'ID'` | Task ID column header |
| `name` | `'Name'` | Task Name column header |
| `startDate` | `'Start Date'` | Start Date column header |
| `endDate` | `'End Date'` | End Date column header |
| `duration` | `'Duration'` | Duration column header |
| `progress` | `'Progress'` | Progress column header |
| `dependency` | `'Dependency'` | Dependency column header |
| `notes` | `'Notes'` | Notes column header |
| `addDialogTitle` | `'New Task'` | Add dialog title |
| `editDialogTitle` | `'Task Information'` | Edit dialog title |
| `saveButton` | `'Save'` | Save button label |
| `cancelButton` | `'Cancel'` | Cancel button label |
| `deleteButton` | `'Delete'` | Delete button label |
| `add` | `'Add'` | Toolbar Add button |
| `edit` | `'Edit'` | Toolbar Edit button |
| `update` | `'Update'` | Toolbar Update button |
| `delete` | `'Delete'` | Toolbar Delete button |
| `cancel` | `'Cancel'` | Toolbar Cancel button |
| `search` | `'Search'` | Toolbar Search placeholder |
| `expandAll` | `'Expand All'` | Toolbar Expand All button |
| `collapseAll` | `'Collapse All'` | Toolbar Collapse All button |
| `zoomIn` | `'Zoom In'` | Toolbar Zoom In button |
| `zoomOut` | `'Zoom Out'` | Toolbar Zoom Out button |
| `zoomToFit` | `'Zoom To Fit'` | Toolbar Zoom to Fit button |
| `excelExport` | `'Excel Export'` | Toolbar Excel Export button |
| `csvExport` | `'CSV Export'` | Toolbar CSV Export button |
| `pdfExport` | `'PDF Export'` | Toolbar PDF Export button |
| `confirmDelete` | `'Are you sure you want to Delete Record?'` | Delete confirmation dialog |
| `from` | `'From'` | Dependency dialog From label |
| `to` | `'To'` | Dependency dialog To label |
| `taskLink` | `'Task Link'` | Dependency dialog title |
| `lag` | `'Lag'` | Dependency dialog Lag label |
| `start` | `'Start'` | Constraint start label |
| `finish` | `'Finish'` | Constraint finish label |

---

## RTL (Right-to-Left) Support

Enable RTL layout for Arabic, Hebrew, or other right-to-left languages:

```tsx
<GanttComponent
  enableRtl={true}
  locale='ar'
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>
```

> Set both `enableRtl={true}` **and** `locale='ar'` (or your target RTL locale) together for the full RTL experience — layout direction and translated UI text.

### What RTL Affects

- TreeGrid columns render right-to-left
- Column headers are right-aligned
- Toolbar items order is reversed
- Dialog fields are right-aligned
- Scrollbar appears on the left side
- Timeline reads right-to-left

---

## Column Number and Date Formatting

Apply display formats per column using the `format` prop on `ColumnDirective`:

### Date Formatting

```tsx
<ColumnDirective field='StartDate' format='yMd' />           {/* locale-aware short date */}
<ColumnDirective field='StartDate' format='dd/MM/yyyy' />    {/* custom pattern */}
<ColumnDirective field='StartDate' format={{ type: 'date', skeleton: 'full' }} />
```

### Number Formatting

```tsx
<ColumnDirective field='Cost'     format='C2' />   {/* currency, 2 decimals: $1,234.56 */}
<ColumnDirective field='Progress' format='P0' />   {/* percentage, 0 decimals: 75% */}
<ColumnDirective field='Rate'     format='N2' />   {/* number, 2 decimals: 1,234.56 */}
```

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| Translations not applied | `L10n.load()` called after component renders | Call `L10n.load()` at the module level before the component mounts |
| Partial translation | Missing keys in locale object | Add all required keys to the `'gantt'` namespace |
| RTL layout not applied | `enableRtl` not set | Set `enableRtl={true}` alongside `locale` |
| Date format not changing | `format` not set on `ColumnDirective` | Add `format='yMd'` or a custom pattern to the date column |
| Number format ignored | Wrong format string | Use EJ2 format strings: `'C2'`, `'N2'`, `'P0'` etc. |
