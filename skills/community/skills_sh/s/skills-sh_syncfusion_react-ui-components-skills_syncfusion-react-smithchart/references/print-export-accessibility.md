# Print, Export, and Accessibility

## Table of contents
- [Printing Smith Charts](print-export-accessibility.md#printing-smith-charts)
  - [Basic Print Implementation](print-export-accessibility.md#basic-print-implementation)
  - [Keyboard Shortcut for Print](print-export-accessibility.md#keyboard-shortcut-for-print)
  - [Print Styling](print-export-accessibility.md#print-styling)
- [Exporting Smith Charts](print-export-accessibility.md#exporting-smith-charts)
  - [Supported Export Formats](print-export-accessibility.md#supported-export-formats)
  - [Basic Export Implementation](print-export-accessibility.md#basic-export-implementation)
  - [Export Method Parameters](print-export-accessibility.md#export-method-parameters)
  - [Custom File Names](print-export-accessibility.md#custom-file-names)
  - [Choosing the Right Format](print-export-accessibility.md#choosing-the-right-format)
- [Accessibility Features](print-export-accessibility.md#accessibility-features)
  - [Accessibility Standards Compliance](print-export-accessibility.md#accessibility-standards-compliance)
  - [Compliance Levels](print-export-accessibility.md#compliance-levels)
  - [WAI-ARIA Attributes](print-export-accessibility.md#wai-aria-attributes)
  - [Keyboard Navigation](print-export-accessibility.md#keyboard-navigation)
  - [Color Contrast](print-export-accessibility.md#color-contrast)
  - [Screen Reader Support](print-export-accessibility.md#screen-reader-support)
  - [Accessibility Testing Tools](print-export-accessibility.md#accessibility-testing-tools)
- [Complete Examples](print-export-accessibility.md#complete-examples)
  - [Full Print and Export Implementation](print-export-accessibility.md#full-print-and-export-implementation)
  - [Accessible Chart with All Features](print-export-accessibility.md#accessible-chart-with-all-features)
- [Best Practices](print-export-accessibility.md#best-practices)
  - [Print Optimization](print-export-accessibility.md#print-optimization)
  - [Export Recommendations](print-export-accessibility.md#export-recommendations)
  - [Accessibility Best Practices](print-export-accessibility.md#accessibility-best-practices)
  - [Mobile Accessibility](print-export-accessibility.md#mobile-accessibility)
- [Troubleshooting](print-export-accessibility.md#troubleshooting)
  - [Print Not Working](print-export-accessibility.md#print-not-working)
  - [Export Fails](print-export-accessibility.md#export-fails)
  - [Accessibility Issues](print-export-accessibility.md#accessibility-issues)

## Printing Smith Charts

The rendered Smith Chart can be printed directly from the browser by calling the public `print` method. The ID of the Smith Chart's div element must be passed as an argument.

### Basic Print Implementation

```tsx
import * as React from "react";
import { useRef } from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const chartRef = useRef(null);

  const handlePrint = () => {
    if (chartRef.current) {
      chartRef.current.print('smithchart');
    }
  };

  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div>
      <button onClick={handlePrint}>Print Chart</button>
      
      <SmithchartComponent
        ref={chartRef}
        id="smithchart"
        title={{ text: 'Transmission Line Analysis' }}
      >
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective points={data} />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

### Keyboard Shortcut for Print

The Smith Chart supports the `Ctrl+P` keyboard shortcut for printing, which works when the chart has focus.

### Print Styling

When printing, the chart maintains its current styling and dimensions. For best print results:

```tsx
<SmithchartComponent
  id="smithchart"
  width="700px"   // Standard print width
  height="525px"  // 4:3 aspect ratio
  title={{
    text: 'Impedance Analysis Report',
    font: { size: '16px', fontWeight: 'Bold', color: '#000000' }
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

## Exporting Smith Charts

The rendered Smith Chart can be exported to various image formats using the `export` method. This is useful for including charts in reports, presentations, or documentation.

### Supported Export Formats

- **JPEG** - Compressed raster image
- **PNG** - Lossless raster image
- **SVG** - Scalable vector graphics
- **PDF** - Portable document format

### Basic Export Implementation

```tsx
import * as React from "react";
import { useRef } from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const chartRef = useRef(null);

  const handleExport = (format) => {
    if (chartRef.current) {
      chartRef.current.export(format, 'smithchart');
    }
  };

  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => handleExport('PNG')}>Export as PNG</button>
        <button onClick={() => handleExport('JPEG')}>Export as JPEG</button>
        <button onClick={() => handleExport('SVG')}>Export as SVG</button>
        <button onClick={() => handleExport('PDF')}>Export as PDF</button>
      </div>
      
      <SmithchartComponent
        ref={chartRef}
        id="smithchart"
        title={{ text: 'RF Circuit Analysis' }}
      >
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective points={data} />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

### Export Method Parameters

The `export` method takes two parameters:

1. **type** (string): Export format - 'PNG', 'JPEG', 'SVG', or 'PDF'
2. **fileName** (string): Name of the exported file (without extension)

```tsx
chartRef.current.export('PNG', 'impedance-analysis');
// Creates: impedance-analysis.png
```

### Custom File Names

Use dynamic file names based on data or user input:

```tsx
import * as React from "react";
import { useRef, useState } from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const chartRef = useRef(null);
  const [fileName, setFileName] = useState('smithchart');

  const handleExport = () => {
    if (chartRef.current) {
      const timestamp = new Date().toISOString().slice(0, 10);
      const customName = `${fileName}-${timestamp}`;
      chartRef.current.export('PNG', customName);
    }
  };

  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div>
      <input
        type="text"
        value={fileName}
        onChange={(e) => setFileName(e.target.value)}
        placeholder="File name"
      />
      <button onClick={handleExport}>Export as PNG</button>
      
      <SmithchartComponent
        ref={chartRef}
        id="smithchart"
        title={{ text: 'Analysis Results' }}
      >
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective points={data} />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

### Choosing the Right Format

**PNG:**
- Best for web use and general documentation
- Lossless compression, good quality
- Supports transparency
- Recommended for most use cases

**JPEG:**
- Smaller file size than PNG
- Lossy compression (slight quality loss)
- Best for email attachments or size-constrained scenarios
- No transparency support

**SVG:**
- Vector format, scales infinitely without quality loss
- Editable in vector graphics software
- Best for printing and scaling
- Larger file size

**PDF:**
- Standard document format
- Best for formal reports and documentation
- Easy to share and view on any device
- Self-contained single file

## Accessibility Features

The Smith Chart component follows accessibility guidelines and standards, making it usable for people with disabilities.

### Accessibility Standards Compliance

The Smith Chart supports:

- **[ADA](https://www.ada.gov/)** - Americans with Disabilities Act
- **[Section 508](https://www.section508.gov/)** - US Federal accessibility requirements
- **[WCAG 2.2](https://www.w3.org/TR/WCAG22/)** - Web Content Accessibility Guidelines
- **[WAI-ARIA](https://www.w3.org/TR/wai-aria/)** - Accessible Rich Internet Applications

### Compliance Levels

| Accessibility Criteria | Compatibility |
|------------------------|---------------|
| WCAG 2.2 Support | Partial |
| Section 508 Support | Partial |
| Screen Reader Support | Partial |
| Color Contrast | Full |
| Mobile Device Support | Full |
| Keyboard Navigation | Partial |
| Accessibility Checker Validation | Full |
| Axe-core Validation | Full |

**Full** = All features meet the requirement  
**Partial** = Some features meet the requirement  

### WAI-ARIA Attributes

The Smith Chart component uses appropriate ARIA attributes:

**Roles:**
- `img` - Identifies the chart as an image
- `region` - Marks distinct regions of the chart

**Attributes:**
- `aria-label` - Provides accessible names for chart elements
- `aria-hidden` - Hides decorative elements from screen readers

These attributes are automatically applied to the chart elements.

### Keyboard Navigation

The Smith Chart supports the following keyboard shortcuts:

| Key | Action |
|-----|--------|
| `Tab` | Moves focus to the next element in the Smith Chart |
| `Shift + Tab` | Moves focus to the previous element |
| `Ctrl + P` | Prints the Smith Chart |

### Color Contrast

The Smith Chart component ensures sufficient color contrast for all visual elements, meeting WCAG 2.2 color contrast requirements. This makes charts readable for users with visual impairments.

**Best practices for color contrast:**

```tsx
<SmithchartComponent
  id="smithchart"
  title={{
    text: 'Impedance Analysis',
    font: {
      color: '#000000',  // High contrast with white background
      size: '16px',
      fontWeight: 'Bold'
    }
  }}
  horizontalAxis={{
    labelStyle: {
      color: '#333333',  // Sufficient contrast
      size: '12px'
    }
  }}
>
  <SmithchartSeriesCollectionDirective>
    <SmithchartSeriesDirective
      points={data}
      fill="#0066CC"  // WCAG AA compliant blue
      width={2}
    />
  </SmithchartSeriesCollectionDirective>
</SmithchartComponent>
```

### Screen Reader Support

While the Smith Chart has partial screen reader support, you can enhance accessibility by:

1. **Adding descriptive titles:**
```tsx
<SmithchartComponent
  id="smithchart"
  title={{ text: 'Transmission Line Impedance: 50 Ohms at 2.4 GHz' }}
>
  {/* series configuration */}
</SmithchartComponent>
```

2. **Providing text alternatives:**
```tsx
<div>
  <SmithchartComponent id="smithchart">
    {/* series configuration */}
  </SmithchartComponent>
  
  <div className="sr-only">
    {/* Screen reader only text description */}
    Chart showing impedance measurements: Resistance values range from 0 to 1.0 ohms,
    Reactance values range from 0.05 to 0.5 ohms.
  </div>
</div>
```

3. **Including data tables:**
```tsx
<div>
  <SmithchartComponent id="smithchart">
    {/* series configuration */}
  </SmithchartComponent>
  
  <details>
    <summary>View Data Table</summary>
    <table>
      <thead>
        <tr>
          <th>Point</th>
          <th>Resistance (Ω)</th>
          <th>Reactance (Ω)</th>
        </tr>
      </thead>
      <tbody>
        {data.map((point, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{point.resistance}</td>
            <td>{point.reactance}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </details>
</div>
```

### Accessibility Testing Tools

The Smith Chart has been validated with:

- **[accessibility-checker](https://www.npmjs.com/package/accessibility-checker)** - Automated accessibility testing
- **[axe-core](https://www.npmjs.com/package/axe-core)** - Industry-standard accessibility testing

You can view accessibility samples at: [Syncfusion Accessibility Demo](https://ej2.syncfusion.com/accessibility/smith-chart.html)

## Complete Examples

### Full Print and Export Implementation

```tsx
import * as React from "react";
import { useRef } from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const chartRef = useRef(null);

  const handlePrint = () => {
    if (chartRef.current) {
      chartRef.current.print('smithchart');
    }
  };

  const handleExport = (format) => {
    if (chartRef.current) {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      chartRef.current.export(format, `impedance-analysis-${timestamp}`);
    }
  };

  const transmissionData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.2, reactance: 0.15 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 0.8, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '15px' }}>
        <button onClick={handlePrint} style={{ marginRight: '10px' }}>
          Print Chart
        </button>
        <button onClick={() => handleExport('PNG')} style={{ marginRight: '10px' }}>
          Export PNG
        </button>
        <button onClick={() => handleExport('JPEG')} style={{ marginRight: '10px' }}>
          Export JPEG
        </button>
        <button onClick={() => handleExport('SVG')} style={{ marginRight: '10px' }}>
          Export SVG
        </button>
        <button onClick={() => handleExport('PDF')}>
          Export PDF
        </button>
      </div>

      <SmithchartComponent
        ref={chartRef}
        id="smithchart"
        width="800px"
        height="600px"
        title={{
          text: 'Transmission Line Impedance Analysis',
          font: { size: '18px', fontWeight: 'Bold' }
        }}
        legendSettings={{ visible: true, position: 'Bottom' }}
      >
        <Inject services={[SmithchartLegend]} />
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective
            name="50Ω Transmission Line"
            points={transmissionData}
            fill="#3498db"
            width={2}
            marker={{ visible: true, width: 10, height: 10 }}
          />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

### Accessible Chart with All Features

```tsx
import * as React from "react";
import { useRef } from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend, TooltipRender } from '@syncfusion/ej2-react-charts';

function App() {
  const chartRef = useRef(null);

  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.7, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  const handleExport = () => {
    if (chartRef.current) {
      chartRef.current.export('PNG', 'accessible-smith-chart');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>RF Circuit S-Parameter Analysis</h1>
      
      <button onClick={handleExport} style={{ marginBottom: '15px' }}>
        Export Chart (PNG)
      </button>

      <SmithchartComponent
        ref={chartRef}
        id="smithchart"
        width="700px"
        height="600px"
        title={{
          text: 'Input Impedance at 2.4 GHz',
          font: { size: '16px', fontWeight: 'Bold', color: '#000000' }
        }}
        legendSettings={{
          visible: true,
          position: 'Bottom'
        }}
        horizontalAxis={{
          labelStyle: { color: '#333333', size: '12px' }
        }}
        radialAxis={{
          labelStyle: { color: '#333333', size: '12px' }
        }}
      >
        <Inject services={[SmithchartLegend, TooltipRender]} />
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective
            name="Measured Impedance"
            points={data}
            fill="#0066CC"
            width={2}
            marker={{
              visible: true,
              width: 10,
              height: 10
            }}
            tooltip={{ visible: true }}
          />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>

      {/* Accessible data table */}
      <details style={{ marginTop: '20px' }}>
        <summary>View Data Table (Accessible Format)</summary>
        <table style={{ borderCollapse: 'collapse', marginTop: '10px' }}>
          <thead>
            <tr>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Point #</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Resistance (Ω)</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Reactance (Ω)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((point, index) => (
              <tr key={index}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{index + 1}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{point.resistance}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{point.reactance}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </details>

      {/* Text description for screen readers */}
      <div style={{ marginTop: '15px', fontSize: '14px', color: '#666' }}>
        <p>
          <strong>Chart Description:</strong> This Smith Chart displays input impedance measurements
          at 2.4 GHz frequency. The data shows 4 measurement points with resistance values ranging
          from 0 to 1.0 ohms and reactance values from 0.05 to 0.5 ohms.
        </p>
      </div>
    </div>
  );
}

export default App;
```

## Best Practices

### Print Optimization

1. **Use appropriate dimensions:** 700×525px (4:3) or 800×600px
2. **High-contrast colors:** Black/dark colors for lines, clear backgrounds
3. **Readable fonts:** Minimum 12px for labels, 16px for titles
4. **Test print preview:** Always check before final print

### Export Recommendations

**For documentation:**
- Use PNG or PDF
- High resolution (800×600px or larger)
- Include descriptive titles and legends

**For presentations:**
- Use PNG or SVG
- Large, readable fonts
- High-contrast colors

**For web embedding:**
- Use PNG or JPEG
- Optimize file size
- Consider responsive dimensions

### Accessibility Best Practices

1. **Always provide text alternatives** for screen reader users
2. **Use sufficient color contrast** (WCAG AA: 4.5:1 minimum)
3. **Include data tables** as accessible alternatives
4. **Test with keyboard navigation** (Tab, Shift+Tab, Ctrl+P)
5. **Add descriptive titles** and subtitles
6. **Test with accessibility tools** (axe-core, NVDA, JAWS)
7. **Avoid color-only distinctions** - use shapes, patterns, or labels

### Mobile Accessibility

- Ensure touch targets are at least 44×44px
- Test on actual mobile devices
- Provide alternative input methods
- Consider simplified views for small screens

## Troubleshooting

### Print Not Working

- Verify chart reference is correctly set
- Ensure chart ID matches the parameter passed to `print()`
- Check that chart is fully rendered before printing
- Test browser print settings

### Export Fails

- Confirm chart reference exists and is mounted
- Verify export format is valid ('PNG', 'JPEG', 'SVG', 'PDF')
- Check browser console for errors
- Ensure file name doesn't contain invalid characters

### Accessibility Issues

- Run automated tests with axe-core or accessibility-checker
- Test with actual screen readers (NVDA, JAWS, VoiceOver)
- Verify keyboard navigation works as expected
- Check color contrast ratios with online tools

This comprehensive guide covers printing, exporting, and accessibility features of Smith Charts, enabling you to create charts that are shareable, printable, and accessible to all users.
