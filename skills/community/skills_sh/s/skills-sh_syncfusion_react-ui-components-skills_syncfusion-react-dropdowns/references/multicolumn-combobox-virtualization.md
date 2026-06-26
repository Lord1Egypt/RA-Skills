# Virtualization — Syncfusion React MultiColumn ComboBox

## Overview

Virtualization enables efficient rendering of very large datasets in the popup list. Instead of rendering every item in the DOM, it creates a fixed number of elements and reuses them as the user scrolls. This technique dramatically reduces memory usage and improves scroll performance.

Enable it with `enableVirtualization={true}`.

---

## Virtualization with Local Data

Generate or load large local datasets and enable virtualization. The component only renders visible rows in the DOM at any time.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  // Generate 150 items programmatically
  const generateData = (count: number) => {
    const names = ['John', 'Alice', 'Bob', 'Mario Pontes', 'Yang Wang', 'Michael', 'Nancy', 'Robert King'];
    const hours = [8, 12, 16];
    const status = ['Pending', 'Completed', 'In Progress'];
    const designation = ['Engineer', 'Manager', 'Tester'];
    const result: object[] = [];
    for (let i = 0; i < count; i++) {
      result.push({
        TaskID: i + 1,
        Engineer: names[Math.floor(Math.random() * names.length)],
        Designation: designation[Math.floor(Math.random() * designation.length)],
        Estimation: hours[Math.floor(Math.random() * hours.length)],
        Status: status[Math.floor(Math.random() * status.length)]
      });
    }
    return result;
  };

  const fields = { text: 'Engineer', value: 'TaskID' };

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={generateData(150)}
      fields={fields}
      placeholder="Select an engineer"
      popupHeight={230}
      gridSettings={{ rowHeight: 40 }}
      enableVirtualization={true}
    >
      <ColumnsDirective>
        <ColumnDirective field='TaskID' header='Employee ID' width={100} />
        <ColumnDirective field='Engineer' header='Name' width={140} />
        <ColumnDirective field='Designation' header='Designation' width={130} />
        <ColumnDirective field='Estimation' header='Estimation' width={120} />
        <ColumnDirective field='Status' header='Status' width={120} />
      </ColumnsDirective>
    </MultiColumnComboBoxComponent>
  );
}
```

---

## Virtualization with Remote Data

When using `DataManager` with virtualization, the component initially fetches all data from the server, then performs virtual scrolling against the locally-stored result.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

function App() {
  const dataSource = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor(),
    crossDomain: true
  });
  const fields = { text: 'ShipCountry', value: 'CustomerID' };

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={dataSource}
      fields={fields}
      popupHeight="230px"
      placeholder="Select a country"
      gridSettings={{ rowHeight: 40 }}
      enableVirtualization={true}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' header='OrderID' width={120} />
        <ColumnDirective field='CustomerID' header='CustomerID' width={130} />
        <ColumnDirective field='ShipCountry' header='ShipCountry' width={120} />
      </ColumnsDirective>
    </MultiColumnComboBoxComponent>
  );
}
```

---

## Best Practices for Virtualization

- Set `gridSettings={{ rowHeight: N }}` to a fixed value — virtualization relies on consistent row heights for accurate position calculations.
- Set an explicit `popupHeight` — the component needs a defined viewport for virtual rendering.
- Combine with `popupHeight` to keep the popup at a manageable size (e.g., `230px` or `300px`).
- Virtualization is most beneficial for datasets with 100+ items.

---

## Key Property

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enableVirtualization` | `boolean` | `false` | Enables virtual scrolling in the popup list |
