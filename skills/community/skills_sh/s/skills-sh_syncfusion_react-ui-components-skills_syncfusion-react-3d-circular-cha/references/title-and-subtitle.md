# Title and Subtitle

This guide covers adding and customizing titles and subtitles for 3D Circular Charts, including positioning, styling, and responsive text configuration.

## Table of contents

- [Overview](title-and-subtitle.md#overview)
- [Adding a Title](title-and-subtitle.md#adding-a-title)
  - [Basic Title](title-and-subtitle.md#basic-title)
  - [Title for Different Contexts](title-and-subtitle.md#title-for-different-contexts)
- [Title Customization](title-and-subtitle.md#title-customization)
  - [Font and Size](title-and-subtitle.md#font-and-size)
  - [Color and Alignment](title-and-subtitle.md#color-and-alignment)
  - [Complete Title Styling](title-and-subtitle.md#complete-title-styling)
- [Adding a Subtitle](title-and-subtitle.md#adding-a-subtitle)
  - [Basic Subtitle](title-and-subtitle.md#basic-subtitle)
  - [Subtitle Customization](title-and-subtitle.md#subtitle-customization)
- [Title and Subtitle Together](title-and-subtitle.md#title-and-subtitle-together)
- [Text Alignment](title-and-subtitle.md#text-alignment)
- [Responsive Titles](title-and-subtitle.md#responsive-titles)
- [Dynamic Titles](title-and-subtitle.md#dynamic-titles)
- [Best Practices](title-and-subtitle.md#best-practices)
- [Complete Example](title-and-subtitle.md#complete-example)
- [Summary](title-and-subtitle.md#summary)

## Overview

Titles and subtitles provide context for your charts, helping users understand what data is being displayed. They appear at the top of the chart and can be fully customized.

## Adding a Title

### Basic Title

Add a title using the `title` property:

```tsx
function BasicTitle() {
  const data = [
    { category: 'Product A', sales: 35 },
    { category: 'Product B', sales: 28 },
    { category: 'Product C', sales: 22 },
    { category: 'Product D', sales: 15 }
  ];

  return (
    <CircularChart3DComponent
      id="chart"
      title="Product Sales Distribution"  // Chart title
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="sales"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Result**: "Product Sales Distribution" appears centered at the top of the chart.

### Title for Different Contexts

```tsx
// Dashboard widget
<CircularChart3DComponent title="Q4 2024 Revenue" />

// Report chart
<CircularChart3DComponent title="Customer Satisfaction Survey Results" />

// Analytics chart
<CircularChart3DComponent title="Browser Usage Statistics - March 2024" />
```

## Title Customization

Customize title appearance using the `titleStyle` property.

### Font and Size

```tsx
<CircularChart3DComponent
  title="Sales Analysis"
  titleStyle={{
    size: '18px',
    fontWeight: 'Bold',
    fontFamily: 'Arial'
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Color and Alignment

```tsx
function StyledTitle() {
  const data = [
    { region: 'North', revenue: 45 },
    { region: 'South', revenue: 30 },
    { region: 'East', revenue: 25 }
  ];

  return (
    <CircularChart3DComponent
      title="Regional Revenue Distribution"
      titleStyle={{
        size: '20px',
        fontWeight: 'Bold',
        color: '#2196F3',          // Blue title
        fontFamily: 'Segoe UI',
        textAlignment: 'Center',   // Options: Near, Center, Far
        textOverflow: 'Trim'       // Options: None, Trim, Wrap
      }}
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="region"
          yName="revenue"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Complete Title Styling

```tsx
function CompletelyStyledTitle() {
  const data = [
    { category: 'Electronics', value: 40 },
    { category: 'Clothing', value: 30 },
    { category: 'Home', value: 30 }
  ];

  return (
    <CircularChart3DComponent
      title="Department Sales - FY 2024"
      titleStyle={{
        size: '22px',
        fontWeight: '600',
        color: '#1976D2',
        fontFamily: '"Roboto", sans-serif',
        textAlignment: 'Center',
        fontStyle: 'Normal',        // Options: Normal, Italic, Oblique
        textOverflow: 'Wrap'
      }}
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="value"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Title Style Properties

- **`size`**: Font size (e.g., '16px', '20px', '1.5em')
- **`fontWeight`**: 'Normal', 'Bold', '400', '600', '700'
- **`color`**: Title text color (hex, rgb, or color name)
- **`fontFamily`**: Font name or font stack
- **`textAlignment`**: 'Near' (left), 'Center', 'Far' (right)
- **`fontStyle`**: 'Normal', 'Italic', 'Oblique'
- **`textOverflow`**: 'None', 'Trim', 'Wrap'

## Adding a Subtitle

### Basic Subtitle

Add a subtitle using the `subTitle` property:

```tsx
function WithSubtitle() {
  const data = [
    { product: 'Laptops', sales: 45 },
    { product: 'Phones', sales: 30 },
    { product: 'Tablets', sales: 25 }
  ];

  return (
    <CircularChart3DComponent
      title="Product Sales"
      subTitle="Q4 2024 Performance Report"  // Subtitle
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="product"
          yName="sales"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Result**: Subtitle appears below the title in a slightly smaller, lighter font.

### Subtitle Use Cases

```tsx
// Time period context
<CircularChart3DComponent
  title="Revenue Distribution"
  subTitle="January - March 2024"
/>

// Data source information
<CircularChart3DComponent
  title="Market Share"
  subTitle="Source: Industry Analytics Report"
/>

// Additional context
<CircularChart3DComponent
  title="Customer Feedback"
  subTitle="Based on 1,250 responses"
/>
```

## Subtitle Customization

Style subtitles independently using `subTitleStyle`.

### Basic Subtitle Styling

```tsx
<CircularChart3DComponent
  title="Sales Overview"
  subTitle="Quarterly Comparison"
  subTitleStyle={{
    size: '14px',
    color: '#757575',
    fontFamily: 'Arial'
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Complete Subtitle Styling

```tsx
function StyledSubtitle() {
  const data = [
    { category: 'Category A', value: 35 },
    { category: 'Category B', value: 30 },
    { category: 'Category C', value: 35 }
  ];

  return (
    <CircularChart3DComponent
      title="Data Distribution"
      subTitle="Updated: March 23, 2024"
      subTitleStyle={{
        size: '13px',
        fontWeight: 'Normal',
        color: '#9E9E9E',
        fontFamily: 'Segoe UI',
        textAlignment: 'Center',
        fontStyle: 'Italic'
      }}
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="value"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Title and Subtitle Together

### Balanced Design

```tsx
function BalancedTitleSubtitle() {
  const data = [
    { quarter: 'Q1', revenue: 45000 },
    { quarter: 'Q2', revenue: 52000 },
    { quarter: 'Q3', revenue: 48000 },
    { quarter: 'Q4', revenue: 55000 }
  ];

  return (
    <CircularChart3DComponent
      title="Quarterly Revenue Performance"
      titleStyle={{
        size: '20px',
        fontWeight: 'Bold',
        color: '#1976D2'
      }}
      subTitle="Fiscal Year 2024 - All Regions"
      subTitleStyle={{
        size: '13px',
        color: '#757575',
        fontStyle: 'Italic'
      }}
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="quarter"
          yName="revenue"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Professional Report Style

```tsx
function ProfessionalStyle() {
  const data = [
    { segment: 'Enterprise', customers: 450 },
    { segment: 'SMB', customers: 1200 },
    { segment: 'Individual', customers: 3500 }
  ];

  return (
    <CircularChart3DComponent
      title="Customer Segmentation Analysis"
      titleStyle={{
        size: '22px',
        fontWeight: '700',
        color: '#212121',
        fontFamily: '"Helvetica Neue", Arial, sans-serif'
      }}
      subTitle="Total Active Customers: 5,150 | Report Date: March 2024"
      subTitleStyle={{
        size: '12px',
        fontWeight: '400',
        color: '#616161',
        fontFamily: '"Helvetica Neue", Arial, sans-serif'
      }}
      width="700px"
      height="500px"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="segment"
          yName="customers"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Text Alignment

Control horizontal positioning of titles and subtitles.

### Alignment Options

```tsx
// Left-aligned
<CircularChart3DComponent
  title="Sales Report"
  titleStyle={{ textAlignment: 'Near' }}
  subTitle="Q1 2024"
  subTitleStyle={{ textAlignment: 'Near' }}
/>

// Center-aligned (default)
<CircularChart3DComponent
  title="Sales Report"
  titleStyle={{ textAlignment: 'Center' }}
  subTitle="Q1 2024"
  subTitleStyle={{ textAlignment: 'Center' }}
/>

// Right-aligned
<CircularChart3DComponent
  title="Sales Report"
  titleStyle={{ textAlignment: 'Far' }}
  subTitle="Q1 2024"
  subTitleStyle={{ textAlignment: 'Far' }}
/>
```

### Different Alignments

```tsx
function MixedAlignment() {
  const data = [
    { type: 'Type A', value: 40 },
    { type: 'Type B', value: 35 },
    { type: 'Type C', value: 25 }
  ];

  return (
    <CircularChart3DComponent
      title="Performance Metrics"
      titleStyle={{
        size: '18px',
        textAlignment: 'Near'  // Left-aligned
      }}
      subTitle="Last updated: 5 minutes ago"
      subTitleStyle={{
        size: '11px',
        textAlignment: 'Far',  // Right-aligned
        color: '#999'
      }}
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="type"
          yName="value"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Responsive Titles

### Adaptive Font Sizing

```tsx
function ResponsiveTitles() {
  const [chartWidth, setChartWidth] = React.useState('100%');
  
  const data = [
    { category: 'A', value: 35 },
    { category: 'B', value: 30 },
    { category: 'C', value: 35 }
  ];

  // Adjust title size based on container
  const titleSize = chartWidth === '100%' ? '20px' : '16px';
  const subtitleSize = chartWidth === '100%' ? '13px' : '11px';

  return (
    <CircularChart3DComponent
      title="Sales Distribution"
      titleStyle={{
        size: titleSize,
        fontWeight: 'Bold'
      }}
      subTitle="Current Period"
      subTitleStyle={{
        size: subtitleSize
      }}
      width={chartWidth}
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="value"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Dynamic Titles

### Updating Titles Based on Data

```tsx
function DynamicTitles() {
  const [selectedPeriod, setSelectedPeriod] = React.useState('Q1');
  
  const dataByPeriod = {
    Q1: [{ cat: 'A', val: 30 }, { cat: 'B', val: 40 }, { cat: 'C', val: 30 }],
    Q2: [{ cat: 'A', val: 35 }, { cat: 'B', val: 35 }, { cat: 'C', val: 30 }],
  };

  const currentData = dataByPeriod[selectedPeriod];
  const total = currentData.reduce((sum, item) => sum + item.val, 0);

  return (
    <div>
      <select onChange={(e) => setSelectedPeriod(e.target.value)} value={selectedPeriod}>
        <option value="Q1">Q1 2024</option>
        <option value="Q2">Q2 2024</option>
      </select>
      
      <CircularChart3DComponent
        title={`${selectedPeriod} Performance`}
        subTitle={`Total: ${total} units`}
        titleStyle={{ size: '18px', fontWeight: 'Bold' }}
        subTitleStyle={{ size: '13px', color: '#666' }}
      >
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={currentData}
            xName="cat"
            yName="val"
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>
    </div>
  );
}
```

## Best Practices

### Clear and Concise Titles

```tsx
// ✅ Good: Clear and specific
<CircularChart3DComponent
  title="Q4 2024 Product Sales"
  subTitle="Electronics Department"
/>

// ❌ Avoid: Too vague
<CircularChart3DComponent
  title="Chart"
  subTitle="Data"
/>
```

### Hierarchical Information

```tsx
// ✅ Good: Main info in title, details in subtitle
<CircularChart3DComponent
  title="Customer Satisfaction"
  subTitle="Survey conducted: March 2024 | Respondents: 1,247"
/>

// ❌ Avoid: Both too detailed
<CircularChart3DComponent
  title="Customer Satisfaction Survey Results from March 2024"
  subTitle="Based on 1,247 customer responses collected via email"
/>
```

### Consistent Styling

```tsx
// Create reusable style objects
const titleStyle = {
  size: '20px',
  fontWeight: 'Bold',
  color: '#212121',
  fontFamily: 'Roboto'
};

const subtitleStyle = {
  size: '13px',
  color: '#757575',
  fontFamily: 'Roboto'
};

// Apply consistently across charts
<CircularChart3DComponent
  title="Chart 1"
  titleStyle={titleStyle}
  subTitle="Details"
  subTitleStyle={subtitleStyle}
/>
```

## Complete Example

```tsx
function CompleteExample() {
  const salesData = [
    { region: 'North America', revenue: 450000, growth: '+15%' },
    { region: 'Europe', revenue: 380000, growth: '+8%' },
    { region: 'Asia Pacific', revenue: 520000, growth: '+22%' },
    { region: 'Latin America', revenue: 180000, growth: '+5%' }
  ];

  const totalRevenue = salesData.reduce((sum, item) => sum + item.revenue, 0);
  const formattedTotal = `$${(totalRevenue / 1000000).toFixed(2)}M`;

  return (
    <CircularChart3DComponent
      title="Global Revenue Distribution"
      titleStyle={{
        size: '24px',
        fontWeight: 'Bold',
        color: '#1976D2',
        fontFamily: '"Segoe UI", Arial, sans-serif',
        textAlignment: 'Center'
      }}
      subTitle={`FY 2024 Total: ${formattedTotal} | Year-over-Year Growth`}
      subTitleStyle={{
        size: '14px',
        fontWeight: 'Normal',
        color: '#616161',
        fontFamily: '"Segoe UI", Arial, sans-serif',
        textAlignment: 'Center',
        fontStyle: 'Italic'
      }}
      width="800px"
      height="600px"
      legendSettings={{ visible: true, position: 'Bottom' }}
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={salesData}
          xName="region"
          yName="revenue"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Summary

You've learned how to:
- ✅ Add titles with the `title` property
- ✅ Style titles with `titleStyle` (size, color, font, alignment)
- ✅ Add subtitles with the `subTitle` property
- ✅ Style subtitles independently with `subTitleStyle`
- ✅ Combine titles and subtitles effectively
- ✅ Align text (Near, Center, Far)
- ✅ Create responsive and dynamic titles
- ✅ Follow best practices for clear chart labeling

**Best Practices:**
- Keep titles concise and descriptive
- Use subtitles for context (dates, sources, totals)
- Maintain visual hierarchy (bold title, lighter subtitle)
- Align titles consistently across charts
- Update titles dynamically when data changes
- Consider responsive font sizes for different screen sizes