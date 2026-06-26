# Data Binding in React Bullet Chart

Data binding connects your data source to the Bullet Chart component, allowing it to display actual values (feature measures) and target values (comparative measures).

## Table of contents

- [Overview](#overview)
- [dataSource Property](#datasource-property)
- [valueField Property](#valuefield-property)
- [targetField Property](#targetfield-property)
- [Complete Data Binding Example](#complete-data-binding-example)
- [Local Data Binding](#local-data-binding)
- [Data Structure Requirements](#data-structure-requirements)
- [Dynamic Data Binding](#dynamic-data-binding)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

## Overview

The Bullet Chart uses three key properties for data binding:
- **`dataSource`**: The array of data objects
- **`valueField`**: The property name in your data that contains the actual/feature measure
- **`targetField`**: The property name in your data that contains the target/comparative measure

## dataSource Property

The `dataSource` property accepts a collection of values as input. This data helps display actual measurements and compare them to target values.

### Basic Data Structure

Your data should be an array of objects, where each object contains at least:
- A property for the actual value (e.g., `value`)
- A property for the target value (e.g., `target`)

**Example:**
```javascript
const data = [
    { value: 270, target: 250 }
];
```

## valueField Property

The `valueField` property specifies which property from your data source should be used as the actual bar (feature measure) value.

### Example

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { actual: 270, goal: 250 }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="actual"    // Maps to the 'actual' property
            targetField="goal"     // Maps to the 'goal' property
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

In this example, the actual bar will display the value `270` from the `actual` property.

## targetField Property

The `targetField` property specifies which property from your data source should be used as the target bar (comparative measure) value.

### Example

```tsx
const salesData = [
    { revenue: 180, target: 200 }
];

<BulletChartComponent
    dataSource={salesData}
    valueField="revenue"    // Actual revenue: 180
    targetField="target"    // Target revenue: 200
    minimum={0}
    maximum={250}
/>
```

The target bar will display at position `200`, providing a comparison point for the actual value of `180`.

## Complete Data Binding Example

Here's a comprehensive example with multiple data points:

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";
import * as React from "react";

function App() {
    const salesData = [
        { 
            value: 270, 
            target: 250,
            category: "Product A"
        },
        { 
            value: 180, 
            target: 200,
            category: "Product B"
        },
        { 
            value: 220, 
            target: 210,
            category: "Product C"
        }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={salesData}
            valueField="value"
            targetField="target"
            categoryField="category"
            title="Sales Performance by Product"
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}

export default App;
```

## Local Data Binding

### Single Data Point

For a single metric (most common use case):

```tsx
const data = [
    { value: 100, target: 80 }
];

<BulletChartComponent
    dataSource={data}
    valueField="value"
    targetField="target"
    minimum={0}
    maximum={150}
/>
```

### Multiple Data Points

For displaying multiple bullet charts or using category labels:

```tsx
const data = [
    { value: 100, target: 80 },
    { value: 200, target: 180 },
    { value: 300, target: 280 }
];

<BulletChartComponent
    dataSource={data}
    valueField="value"
    targetField="target"
    minimum={0}
    maximum={400}
/>
```

## Data Structure Requirements

### Minimum Required Fields

At minimum, your data objects must have:
```javascript
{ 
    value: number,    // For valueField
    target: number    // For targetField
}
```

### Extended Data Structure

You can include additional fields for advanced features:

```javascript
{
    value: number,           // Actual value
    target: number,          // Target value
    category: string,        // For category labels
    valueColor: string,      // Dynamic value bar color
    targetColor: string      // Dynamic target bar color
}
```

**Example with extended fields:**
```tsx
const data = [
    { 
        value: 270, 
        target: 250,
        category: "Q1 Revenue",
        valueColor: "#5B5FC7",
        targetColor: "#646464"
    }
];

<BulletChartComponent
    dataSource={data}
    valueField="value"
    targetField="target"
    categoryField="category"
    valueFill="valueColor"       // Bind color from data
    targetColor="targetColor"    // Bind target color from data
/>
```

## Dynamic Data Binding

### From State

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";
import { useState, useEffect } from "react";

function App() {
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        // Fetch or compute data
        const fetchedData = [
            { value: 270, target: 250 }
        ];
        setChartData(fetchedData);
    }, []);

    return (
        <BulletChartComponent
            dataSource={chartData}
            valueField="value"
            targetField="target"
            minimum={0}
            maximum={300}
        />
    );
}
```

### From API

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";
import { useState, useEffect } from "react";

function App() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/metrics')
            .then(response => response.json())
            .then(jsonData => {
                setData(jsonData);
                setLoading(false);
            });
    }, []);

    if (loading) return <div>Loading...</div>;

    return (
        <BulletChartComponent
            dataSource={data}
            valueField="value"
            targetField="target"
            minimum={0}
            maximum={500}
        />
    );
}
```

## Common Patterns

### KPI Dashboard with Multiple Metrics

```tsx
const metrics = [
    { name: "Revenue", actual: 270, goal: 250 },
    { name: "Profit", actual: 85, goal: 100 },
    { name: "Sales", actual: 180, goal: 150 }
];

<div>
    {metrics.map((metric, index) => (
        <BulletChartComponent
            key={index}
            dataSource={[metric]}
            valueField="actual"
            targetField="goal"
            title={metric.name}
            minimum={0}
            maximum={300}
        />
    ))}
</div>
```

### Percentage-Based Data

```tsx
const performanceData = [
    { 
        completion: 85,      // 85% complete
        target: 100,         // 100% target
        metric: "Project Progress"
    }
];

<BulletChartComponent
    dataSource={performanceData}
    valueField="completion"
    targetField="target"
    categoryField="metric"
    minimum={0}
    maximum={100}
    labelFormat="{value}%"
/>
```

## Troubleshooting

**Issue: Bars not displaying**
- Verify property names in `valueField` and `targetField` match your data exactly (case-sensitive)
- Check that data values are numbers, not strings
- Ensure `minimum` and `maximum` encompass your data range

**Issue: Wrong values displayed**
- Double-check the property names in `valueField` and `targetField`
- Verify your data structure matches the expected format
- Console.log your dataSource to inspect the actual data

**Issue: Multiple data points not showing**
- For multiple separate charts, map over your data and create multiple BulletChartComponent instances
- For category-based grouping, use the `categoryField` property

**Issue: Data updates not reflecting**
- Ensure you're updating state correctly in React
- Check that the dataSource reference changes when data updates
- Use proper React state management (useState, useEffect)
