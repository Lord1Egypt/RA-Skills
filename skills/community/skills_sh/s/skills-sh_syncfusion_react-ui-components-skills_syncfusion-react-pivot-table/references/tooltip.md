# Tooltip Configuration & Customization

## Basic Tooltip Setup

```typescript
<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  showTooltip={true}
/>
```

## Tooltip Configuration

### Enable Tooltip

Tooltips are enabled by setting the `showTooltip` property to `true`. When enabled, tooltips automatically display cell information on hover.

```typescript
<PivotViewComponent 
  showTooltip={true}
  dataSourceSettings={dataSourceSettings}
/>
```

### Disable Tooltip

```typescript
<PivotViewComponent
  showTooltip={false}
  dataSourceSettings={dataSourceSettings}
/>
```

## Custom Tooltip Templates

### Simple Template

```typescript
function tooltipTemplate(args: any) {
  const { value, rowHeaders, columnHeaders } = args;
  
  return `
    <div style="padding: 8px; background: white; border: 1px solid #ccc;">
      <p><strong>Value:</strong> ${value}</p>
      <p><strong>Row:</strong> ${rowHeaders}</p>
      <p><strong>Column:</strong> ${columnHeaders}</p>
    </div>
  `;
}

<PivotViewComponent tooltipTemplate={tooltipTemplate} />
```

### Advanced Template with Styling

```typescript
function advancedTooltipTemplate(args: any) {
  const isHighValue = args.value > 10000;
  const bgColor = isHighValue ? '#4CAF50' : '#2196F3';
  
  return (
    <div style={{
      padding: '12px',
      backgroundColor: bgColor,
      color: 'white',
      borderRadius: '4px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
      fontSize: '12px'
    }}>
      <div><strong>${args.value.toLocaleString()}</strong></div>
      <div style={{ fontSize: '11px', marginTop: '4px' }}>
        {args.rowHeaders} × {args.columnHeaders}
      </div>
    </div>
  );
}

<PivotViewComponent tooltipTemplate={advancedTooltipTemplate} />
```

## Tooltip Formatting

### Number Format in Tooltip

```typescript
function formattedTooltip(args: any) {
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  });
  
  return `Value: ${formatter.format(args.value)}`;
}

<PivotViewComponent tooltipTemplate={formattedTooltip} />
```

### Percentage Format

```typescript
function percentageTooltip(args: any) {
  const percentage = (args.value * 100).toFixed(2);
  return `${percentage}%`;
}
```

## Conditional Tooltips

### Context-Based Tooltips

```typescript
function contextTooltip(args: any) {
  let message = '';
  
  if (args.value > 50000) {
    message = '⚠️ High Value - Review Recommended';
  } else if (args.value < 1000) {
    message = 'ℹ️ Low Value';
  } else {
    message = '✓ Normal Value';
  }
  
  return `
    <div style={{ padding: '8px' }}>
      <div>${args.value}</div>
      <div style={{ fontSize: '10px', color: '#666' }}>${message}</div>
    </div>
  `;
}

<PivotViewComponent tooltipTemplate={contextTooltip} />
```

## Complete Tooltip Example

```typescript
function PivotWithTooltips() {
  function richTooltipTemplate(args: any) {
    const value = typeof args.value === 'number' 
      ? args.value.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
      : args.value;

    return (
      <div style={{
        padding: '12px',
        backgroundColor: '#1976D2',
        color: 'white',
        borderRadius: '4px',
        minWidth: '200px'
      }}>
        <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>
          Cell Information
        </div>
        <div style={{ fontSize: '12px' }}>
          <div><strong>Value:</strong> {value}</div>
          <div><strong>Row:</strong> {args.rowHeaders || 'N/A'}</div>
          <div><strong>Column:</strong> {args.columnHeaders || 'N/A'}</div>
          <div style={{ marginTop: '8px', fontSize: '10px', opacity: 0.8 }}>
            {new Date().toLocaleString()}
          </div>
        </div>
      </div>
    );
  }

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      showTooltip={true}
      tooltipTemplate={richTooltipTemplate}
      height={400}
    />
  );
}
```

## Common Tooltip Properties

The tooltip displays the following information by default:
- **Value**: The aggregated cell value
- **Row Headers**: The row header information
- **Column Headers**: The column header information

To customize what information appears, use the `tooltipTemplate` property with custom logic.
