# Virtualization – Syncfusion React AutoComplete

## Table of Contents
- [Overview](#overview)
- [Local Data Virtualization](#local-data-virtualization)
- [Remote Data Virtualization](#remote-data-virtualization)
- [Customizing Item Count](#customizing-item-count)
- [Grouping with Virtualization](#grouping-with-virtualization)

---

## Overview

Virtual scrolling renders only the visible DOM elements from a large dataset, recycling them as the user scrolls. This dramatically improves performance when working with hundreds or thousands of items.

**Enable with:**
- `enableVirtualization={true}` on the component
- `<Inject services={[VirtualScroll]} />` inside the component

The `actionBegin` event fires before data is fetched; `actionComplete` fires after successful retrieval — both also fire during virtual scroll data requests.

> When `enableVirtualization` is enabled, any `skip`/`take` set directly in the `Query` at the component's initial state will be ignored, as the virtual scroll manages pagination internally based on popup height and item height.

---

## Local Data Virtualization

```tsx
import { AutoCompleteComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default class App extends React.Component<{}, {}> {
  private fields: object = { value: 'text' };
  private records: { [key: string]: Object }[] = [];

  constructor(props: {}) {
    super(props);
    this.records = Array.from({ length: 150 }, (_, i) => ({
      id: `id${i + 1}`,
      text: `Item ${i + 1}`,
    }));
  }

  public render() {
    return (
      <AutoCompleteComponent
        id="datas"
        dataSource={this.records}
        fields={this.fields}
        enableVirtualization={true}
        popupHeight="200px"
        placeholder="e.g. Item 1"
      >
        <Inject services={[VirtualScroll]} />
      </AutoCompleteComponent>
    );
  }
}
```

---

## Remote Data Virtualization

For remote data, the AutoComplete triggers additional fetch requests as the user scrolls, firing `actionBegin` and `actionComplete` each time:

```tsx
import { AutoCompleteComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';
import * as React from 'react';

export default class App extends React.Component<{}, {}> {
  private customerField: object = { value: 'OrderID' };
  private customerData: DataManager = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor,
    crossDomain: true
  });

  public render() {
    return (
      <AutoCompleteComponent
        id="datas"
        dataSource={this.customerData}
        fields={this.customerField}
        enableVirtualization={true}
        popupHeight="200px"
        placeholder="OrderID"
      >
        <Inject services={[VirtualScroll]} />
      </AutoCompleteComponent>
    );
  }
}
```

---

## Customizing Item Count

When `enableVirtualization` is enabled, pass a `Query` with `take()` to control how many items are loaded per page. The internal calculation ensures at least enough items to fill the popup:

```tsx
import { AutoCompleteComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';
import { Query } from '@syncfusion/ej2-data';
import * as React from 'react';

export default class App extends React.Component<{}, {}> {
  private fields: object = { value: 'text' };
  private records: { [key: string]: Object }[] = [];
  private query: Query = new Query().take(40);

  constructor(props: {}) {
    super(props);
    this.records = Array.from({ length: 150 }, (_, i) => ({
      id: `id${i + 1}`,
      text: `Item ${i + 1}`,
    }));
  }

  public render() {
    return (
      <AutoCompleteComponent
        id="datas"
        dataSource={this.records}
        fields={this.fields}
        query={this.query}
        enableVirtualization={true}
        popupHeight="200px"
        placeholder="e.g. Item 1"
      >
        <Inject services={[VirtualScroll]} />
      </AutoCompleteComponent>
    );
  }
}
```

> If the provided `take` value is less than the minimum items needed to fill the popup, the user-provided value is ignored.

---

## Grouping with Virtualization

Grouping works with virtualization. For remote data with grouping, an initial request fetches all data for grouping purposes, after which virtual scrolling is applied as with local data:

```tsx
import { AutoCompleteComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default class App extends React.Component<{}, {}> {
  private fields: object = { groupBy: 'group', value: 'text' };
  private records: { [key: string]: Object }[] = [];

  constructor(props: {}) {
    super(props);
    const groups = ['Group A', 'Group B', 'Group C', 'Group D'];
    this.records = Array.from({ length: 150 }, (_, i) => ({
      id: `id${i + 1}`,
      text: `Item ${i + 1}`,
      group: groups[Math.floor(Math.random() * groups.length)],
    }));
  }

  public render() {
    return (
      <AutoCompleteComponent
        id="datas"
        dataSource={this.records}
        fields={this.fields}
        enableVirtualization={true}
        popupHeight="200px"
        placeholder="e.g. Item 1"
      >
        <Inject services={[VirtualScroll]} />
      </AutoCompleteComponent>
    );
  }
}
```
