# Performance Monitoring & Optimization

## Table of Contents
- [Overview](#overview)
- [Measure Grid Performance](#measure-grid-performance)
- [Identify Bottlenecks](#identify-bottlenecks)
- [Optimization Checklist](#optimization-checklist)

---

## Overview

Monitor grid performance to optimize rendering, data binding, and interactions. Key metrics:

- **Load time**: Time to first render all rows
- **Sort/filter time**: Time to complete operations
- **Memory usage**: Grid state and data size
- **Interaction latency**: Time between user action and grid response

---

## Measure Grid Performance

Use the Performance API to track grid operations.

```tsx
import React, { useRef, useState } from 'react';
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-grids';

function GridPerformanceMonitor() {
  const gridRef = useRef(null);
  const [metrics, setMetrics] = useState({
    loadTime: 0,
    renderTime: 0,
    sortTime: 0,
    filterTime: 0
  });

  const startTimer = (name) => {
    return performance.now();
  };

  const endTimer = (name, startTime) => {
    const duration = performance.now() - startTime;
    console.log(`${name}: ${duration.toFixed(2)}ms`);
    return duration;
  };

  // Measure initial load
  const handleGridCreated = () => {
    const startTime = performance.now();
    const loadTime = endTimer('Grid Created', startTime);
    
    setMetrics(prev => ({ ...prev, loadTime }));
  };

  const handleActionComplete = (args) => {
    const startTime = performance.now();

    switch (args.requestType) {
      case 'sorting':
        endTimer('Sort Operation', startTime);
        break;
      case 'filtering':
        endTimer('Filter Operation', startTime);
        break;
      case 'paging':
        endTimer('Page Navigation', startTime);
        break;
      case 'grouping':
        endTimer('Grouping', startTime);
        break;
      default:
        break;
    }
  };

  // Generate large dataset for testing
  const generateLargeDataset = (count) => {
    const data = [];
    for (let i = 0; i < count; i++) {
      data.push({
        OrderID: 10248 + i,
        CustomerID: `CUST${i % 100}`,
        Freight: Math.random() * 1000,
        OrderDate: new Date(2024, Math.floor(Math.random() * 12), Math.floor(Math.random() * 28)),
        Status: ['Completed', 'Pending', 'Cancelled'][Math.floor(Math.random() * 3)]
      });
    }
    return data;
  };

  return (
    <div>
      <h3>Performance Monitoring</h3>

      <div style={{
        backgroundColor: '#f5f5f5',
        padding: '10px',
        marginBottom: '15px',
        borderRadius: '4px',
        fontSize: '12px'
      }}>
        <div><strong>Load Time:</strong> {metrics.loadTime.toFixed(2)}ms</div>
        <div><strong>Render Time:</strong> {metrics.renderTime.toFixed(2)}ms</div>
        <div><strong>Sort Time:</strong> {metrics.sortTime.toFixed(2)}ms</div>
        <div><strong>Filter Time:</strong> {metrics.filterTime.toFixed(2)}ms</div>
      </div>

      <GridComponent
        ref={gridRef}
        dataSource={generateLargeDataset(1000)}
        created={handleGridCreated}
        actionComplete={handleActionComplete}
        allowPaging={true}
        pageSettings={{ pageSize: 50 }}
        allowSorting={true}
        allowFiltering={true}
      >
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='80' />
          <ColumnDirective field='CustomerID' headerText='Customer' width='100' />
          <ColumnDirective field='Freight' headerText='Freight' format='C2' width='80' />
          <ColumnDirective field='OrderDate' headerText='Date' type='date' format='yMd' width='100' />
          <ColumnDirective field='Status' headerText='Status' width='100' />
        </ColumnsDirective>
        <Inject services={[Page]} />
      </GridComponent>
    </div>
  );
}

export default GridPerformanceMonitor;
```

---

## Identify Bottlenecks

Use browser DevTools Performance tab to identify slow operations.

```tsx
// Mark performance boundaries
const markPerformance = (label) => {
  performance.mark(`${label}-start`);
};

const measurePerformance = (label) => {
  performance.mark(`${label}-end`);
  performance.measure(label, `${label}-start`, `${label}-end`);
  
  const measure = performance.getEntriesByName(label)[0];
  console.log(`${label}: ${measure.duration.toFixed(2)}ms`);
};

// Example: Measure data binding
const handleDataBound = () => {
  markPerformance('data-binding');
  
  gridRef.current.query = new Query().select(['OrderID', 'CustomerID']);
  
  window.requestAnimationFrame(() => {
    measurePerformance('data-binding');
  });
};
```

**DevTools Steps:**
1. Open Chrome DevTools → Performance tab
2. Click record
3. Interact with grid (sort, filter, scroll)
4. Stop recording
5. Analyze timeline - look for long tasks (>50ms)

---

## Memory Usage Tracking

Monitor grid memory footprint.

```tsx
// Estimate grid memory
const estimateGridMemory = (gridRef) => {
  if (!gridRef.current || !gridRef.current.dataSource) return 0;

  const data = gridRef.current.dataSource;
  const estimatedSize = JSON.stringify(data).length;
  
  return (estimatedSize / 1024).toFixed(2); // In KB
};

// Check memory in browser console
if (performance.memory) {
  console.log('Used Memory:', (performance.memory.usedJSHeapSize / 1048576).toFixed(2), 'MB');
  console.log('Total Memory:', (performance.memory.totalJSHeapSize / 1048576).toFixed(2), 'MB');
}
```

---
