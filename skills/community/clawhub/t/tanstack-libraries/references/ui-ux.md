# UI & UX

> Table / Form / Hotkeys

---

## Table

Headless — provides logic/state/API, no markup or styling.

```bash
npm i @tanstack/react-table  # adapters: react/vue/solid/svelte/angular/qwik/lit
```

```ts
const table = useReactTable({
  data, columns,
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
})

// Rendering: table.getHeaderGroups() → <thead>, table.getRowModel().rows → <tbody>
// flexRender(header.column.columnDef.header, header.getContext())
```

### Column Definition

```ts
const columnHelper = createColumnHelper<Person>()

const columns = [
  columnHelper.display({ id: 'actions', cell: props => <RowActions row={props.row} /> }),  // No data model
  columnHelper.group({ header: 'Name', columns: [
    columnHelper.accessor('firstName', { header: 'First Name' }),         // Object key
    columnHelper.accessor(row => row.lastName, { id: 'lastName' }),       // Function (requires id)
  ]}),
  columnHelper.accessor('age', { cell: props => <span>{props.getValue()}</span> }),
]
```

Three column types: Accessor (has data model) | Display (pure display) | Group (grouping)

### Features

| Feature | Configuration |
|---------|---------------|
| Sorting | `getSortedRowModel: getSortedRowModel()`, `state: { sorting }` |
| Pagination | `getPaginationRowModel: getPaginationRowModel()` |
| Filtering | `getFilteredRowModel: getFilteredRowModel()`, `state: { columnFilters }` |
| Row Selection | `enableRowSelection: true`, `state: { rowSelection }`, `getRowId: row => row.uuid` |
| Aggregation | `aggregationFn: 'sum'`, `getAggregatedRowModel` |

Server-side mode: `manualSorting/Filtering/Pagination: true` + `rowCount: totalRows`

### Styling

- No built-in styles — 50+ community styling solutions available (shadcn/ui, Mantine, Chakra, Ant Design, etc.)
- TanStack Start projects have built-in `@tanstack/react-table` integration

---

## Form

Headless form state management, supports nested fields and async validation.

```bash
npm i @tanstack/react-form  # adapters: react/vue/angular/solid/lit/preact
```

```tsx
import { useForm } from '@tanstack/react-form'

const form = useForm({
  defaultValues: { name: '', age: 0 },
  onSubmit: async ({ value }) => { await api.submit(value) },
})

<form.Field name="name" validators={{ onChange: ({ value }) => !value ? 'Required' : undefined }}>
  {(field) => <input value={field.state.value} onChange={e => field.handleChange(e.target.value)} />}
</form.Field>
```

- Validation: `onChange`/`onBlur`/`onSubmit` three levels, supports Zod/Yup/Superstruct adapters
- Array fields: `form.useField({ name: 'items' })` + `.push/.remove/.move/.swap`
- Plugin system: `@tanstack/zod-form-adapter`, etc.

---

## Hotkeys (Alpha)

Type-safe keyboard shortcuts. `npm i @tanstack/hotkeys`

```ts
import { useHotkeys } from '@tanstack/react-hotkeys'
useHotkeys({
  'meta+k': () => openSearch(),
  'ctrl+s': () => save(),
  'shift+?': () => showPalette(),
  'a b c': () => konami(),  // Sequence
})
```
Supports recording/replay, platform awareness (Ctrl vs ⌘).