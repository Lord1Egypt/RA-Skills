# 3D Chart Types

## Table of contents
- [Column Chart](chart-types.md#column-chart)
- [Bar Chart](chart-types.md#bar-chart)
- [Stacked Column Chart](chart-types.md#stacked-column-chart)
- [Stacked Bar Chart](chart-types.md#stacked-bar-chart)
- [100% Stacked Column Chart](chart-types.md#100-stacked-column-chart)
- [100% Stacked Bar Chart](chart-types.md#100-stacked-bar-chart)
- [Choosing the Right Chart Type](chart-types.md#choosing-the-right-chart-type)

Syncfusion React 3D Charts support six chart types, each suited for different data visualization scenarios.

## Column Chart

**Use when:** Comparing values across categories, showing changes over time with discrete intervals.

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Legend3D, Tooltip3D } from '@syncfusion/ej2-react-charts';

function ColumnChart() {
  const data = [
    { country: 'USA', gold: 46, silver: 37, bronze: 38 },
    { country: 'China', gold: 38, silver: 32, bronze: 18 },
    { country: 'Japan', gold: 27, silver: 14, bronze: 17 },
    { country: 'UK', gold: 22, silver: 21, bronze: 22 }
  ];

  return (
    <Chart3DComponent
      id='column-chart'
      title='Olympic Medals by Country'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{ title: 'Medals' }}
      enableRotation={true}
      rotation={7}
      tilt={10}
      depth={100}
    >
      <Inject services={[ColumnSeries3D, Category3D, Legend3D, Tooltip3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='country'
          yName='gold'
          type='Column'
          name='Gold'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='country'
          yName='silver'
          type='Column'
          name='Silver'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='country'
          yName='bronze'
          type='Column'
          name='Bronze'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key features:**
- Vertical bars representing values
- Ideal for comparing discrete categories
- Supports multiple series for grouped comparison
- Works best with 3-15 categories

## Bar Chart

**Use when:** Comparing values where labels are long, or when emphasizing rank/order.

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, BarSeries3D, Category3D } from '@syncfusion/ej2-react-charts';

function BarChart() {
  const data = [
    { department: 'Marketing', budget: 120000 },
    { department: 'Research & Development', budget: 180000 },
    { department: 'Sales', budget: 150000 },
    { department: 'Human Resources', budget: 90000 },
    { department: 'IT Infrastructure', budget: 140000 }
  ];

  return (
    <Chart3DComponent
      id='bar-chart'
      title='Department Budgets'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{ title: 'Budget ($)' }}
      rotation={22}
      tilt={0}
    >
      <Inject services={[BarSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='department'
          yName='budget'
          type='Bar'
          name='Budget'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key features:**
- Horizontal bars representing values
- Better readability for long category names
- Natural left-to-right reading direction
- Ideal for ranking data

## Stacked Column Chart

**Use when:** Showing part-to-whole relationships over categories, comparing contribution of each part.

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, StackingColumnSeries3D, Category3D, Legend3D } from '@syncfusion/ej2-react-charts';

function StackedColumnChart() {
  const data = [
    { quarter: 'Q1', mobile: 30, tablet: 15, desktop: 25 },
    { quarter: 'Q2', mobile: 35, tablet: 18, desktop: 22 },
    { quarter: 'Q3', mobile: 40, tablet: 20, desktop: 20 },
    { quarter: 'Q4', mobile: 45, tablet: 22, desktop: 18 }
  ];

  return (
    <Chart3DComponent
      id='stacked-column-chart'
      title='Device Sales by Quarter'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{ title: 'Units Sold (Thousands)' }}
    >
      <Inject services={[StackingColumnSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='quarter'
          yName='mobile'
          type='StackingColumn'
          name='Mobile'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='quarter'
          yName='tablet'
          type='StackingColumn'
          name='Tablet'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='quarter'
          yName='desktop'
          type='StackingColumn'
          name='Desktop'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key features:**
- Series stacked vertically
- Shows total and individual contributions
- Emphasizes cumulative totals
- All series share the same categories

## Stacked Bar Chart

**Use when:** Showing part-to-whole with long category names, horizontal orientation preferred.

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, StackingBarSeries3D, Category3D, Legend3D } from '@syncfusion/ej2-react-charts';

function StackedBarChart() {
  const data = [
    { project: 'Website Redesign', planning: 20, development: 40, testing: 15 },
    { project: 'Mobile App', planning: 15, development: 50, testing: 20 },
    { project: 'API Integration', planning: 10, development: 35, testing: 12 },
    { project: 'Database Migration', planning: 25, development: 45, testing: 18 }
  ];

  return (
    <Chart3DComponent
      id='stacked-bar-chart'
      title='Project Time Distribution (Hours)'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{ title: 'Hours' }}
      rotation={22}
    >
      <Inject services={[StackingBarSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='project'
          yName='planning'
          type='StackingBar'
          name='Planning'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='project'
          yName='development'
          type='StackingBar'
          name='Development'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='project'
          yName='testing'
          type='StackingBar'
          name='Testing'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key features:**
- Series stacked horizontally
- Better for long project/category names
- Shows time/resource allocation clearly

## 100% Stacked Column Chart

**Use when:** Comparing percentage contribution over categories, emphasizing proportions rather than absolute values.

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, StackingColumnSeries3D, Category3D, Legend3D, DataLabel3D } from '@syncfusion/ej2-react-charts';

function HundredPercentStackedColumn() {
  const data = [
    { year: '2020', renewable: 25, nuclear: 20, fossil: 55 },
    { year: '2021', renewable: 30, nuclear: 18, fossil: 52 },
    { year: '2022', renewable: 35, nuclear: 17, fossil: 48 },
    { year: '2023', renewable: 40, nuclear: 15, fossil: 45 }
  ];

  return (
    <Chart3DComponent
      id='hundred-percent-stacked-column'
      title='Energy Sources Distribution (%)'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{ title: 'Percentage', labelFormat: '{value}%' }}
    >
      <Inject services={[StackingColumnSeries3D, Category3D, Legend3D, DataLabel3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='year'
          yName='renewable'
          type='StackingColumn100'
          name='Renewable'
          dataLabel= {{ visible: true, position: 'Middle' }}
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='year'
          yName='nuclear'
          type='StackingColumn100'
          name='Nuclear'
          dataLabel= {{ visible: true, position: 'Middle' }}
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='year'
          yName='fossil'
          type='StackingColumn100'
          name='Fossil Fuels'
          dataLabel= {{ visible: true, position: 'Middle' }}
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key features:**
- Y-axis always 0-100%
- Shows relative proportions, not absolute values
- Each stack totals 100%
- Ideal for composition analysis

## 100% Stacked Bar Chart

**Use when:** Showing percentage contribution with horizontal orientation, long category names.

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, StackingBarSeries3D, Category3D, Legend3D } from '@syncfusion/ej2-react-charts';

function HundredPercentStackedBar() {
  const data = [
    { region: 'North America', electronics: 30, clothing: 25, food: 45 },
    { region: 'Europe', electronics: 35, clothing: 30, food: 35 },
    { region: 'Asia Pacific', electronics: 40, clothing: 20, food: 40 },
    { region: 'Latin America', electronics: 20, clothing: 35, food: 45 }
  ];

  return (
    <Chart3DComponent
      id='hundred-percent-stacked-bar'
      title='Sales Distribution by Region (%)'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{ title: 'Percentage', labelFormat: '{value}%' }}
      rotation={22}
    >
      <Inject services={[StackingBarSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='region'
          yName='electronics'
          type='StackingBar100'
          name='Electronics'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='region'
          yName='clothing'
          type='StackingBar100'
          name='Clothing'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='region'
          yName='food'
          type='StackingBar100'
          name='Food & Beverage'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key features:**
- Horizontal 100% stacked bars
- Comparison of proportions across regions/categories
- Natural reading direction for long names

## Choosing the Right Chart Type

| Chart Type | Best For | Avoid When |
|------------|----------|-----------|
| **Column** | Comparing discrete values, time series | >15 categories, long labels |
| **Bar** | Long category names, ranking | Short labels, time progression |
| **Stacked Column** | Part-to-whole, cumulative totals | Need exact comparisons between parts |
| **Stacked Bar** | Part-to-whole with long labels | Comparing totals across categories |
| **100% Stacked Column** | Proportion comparison, composition | Absolute values matter |
| **100% Stacked Bar** | Proportion comparison, long labels | Totals differ significantly |

**General guidelines:**
- Use **Column/Bar** for straightforward comparisons
- Use **Stacked** to show both parts and totals
- Use **100% Stacked** to emphasize proportions over absolute values
- Choose **Bar** when labels are >15 characters
- Limit categories to 3-12 for readability in stacked charts

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
