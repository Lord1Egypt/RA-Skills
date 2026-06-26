# Title and Subtitle

## Table of contents
- [Overview](title-and-subtitle.md#overview)
- [Enabling Title](title-and-subtitle.md#enabling-title)
- [Adding Subtitle](title-and-subtitle.md#adding-subtitle)
- [Title Trimming](title-and-subtitle.md#title-trimming)
  - [Enabling Title Trim](title-and-subtitle.md#enabling-title-trim)
  - [Maximum Width](title-and-subtitle.md#maximum-width)
  - [Subtitle Trimming](title-and-subtitle.md#subtitle-trimming)
- [Title Customization](title-and-subtitle.md#title-customization)
  - [Font Customization](title-and-subtitle.md#font-customization)
  - [Text Alignment](title-and-subtitle.md#text-alignment)
  - [Visibility Control](title-and-subtitle.md#visibility-control)
- [Complete Examples](title-and-subtitle.md#complete-examples)
  - [Comprehensive Title Configuration](title-and-subtitle.md#comprehensive-title-configuration)
  - [Title with Trimming](title-and-subtitle.md#title-with-trimming)
  - [Presentation-Style Titles](title-and-subtitle.md#presentation-style-titles)
  - [Dynamic Titles](title-and-subtitle.md#dynamic-titles)
  - [Aligned Titles](title-and-subtitle.md#aligned-titles)
- [Best Practices](title-and-subtitle.md#best-practices)
  - [Title Content](title-and-subtitle.md#title-content)
  - [Font Sizing](title-and-subtitle.md#font-sizing)
  - [Text Alignment](title-and-subtitle.md#text-alignment-1)
  - [Trimming Guidelines](title-and-subtitle.md#trimming-guidelines)
  - [Visibility](title-and-subtitle.md#visibility)
  - [Color and Contrast](title-and-subtitle.md#color-and-contrast)
- [Common Patterns](title-and-subtitle.md#common-patterns)
  - [Conditional Title Display](title-and-subtitle.md#conditional-title-display)
  - [Multi-Language Titles](title-and-subtitle.md#multi-language-titles)
  - [Data-Driven Titles](title-and-subtitle.md#data-driven-titles)

## Overview

Titles and subtitles describe the information about the data being plotted in the Smith Chart. They provide context and help users quickly understand what the visualization represents. By default, both title and subtitle visibility are enabled, and you can easily customize their appearance and behavior.

## Enabling Title

Set the title using the `text` property within the `title` object:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Transmission Line Impedance Analysis' }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective points={data} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Adding Subtitle

Add a subtitle using the `subtitle` property to provide additional context or details:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{
        text: 'RF Circuit S-Parameters',
        subtitle: {
          text: 'Measured at 2.4 GHz with 50Ω Reference'
        }
      }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective points={data} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Title Trimming

When titles or subtitles exceed a certain length, they can be trimmed automatically to fit within the chart area.

### Enabling Title Trim

Use the `enableTrim` property to enable automatic text trimming:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  const longTitle = 'Comprehensive Analysis of Transmission Line Impedance Characteristics Across Multiple Frequency Ranges';

  return (
    <SmithchartComponent
      id="smithchart"
      title={{
        text: longTitle,
        enableTrim: true
      }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective points={data} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Maximum Width

Control the maximum width for title trimming using the `maximumWidth` property:

```tsx
<SmithchartComponent
  id="smithchart"
  title={{
    text: 'Very Long Title Text That Needs To Be Trimmed',
    enableTrim: true,
    maximumWidth: 300  // Maximum width in pixels
  }}
>
  <SmithchartSeriesCollectionDirective>
    <SmithchartSeriesDirective points={data} />
  </SmithchartSeriesCollectionDirective>
</SmithchartComponent>
```

When `enableTrim` is true and text exceeds `maximumWidth`, an ellipsis (...) will be added.

### Subtitle Trimming

Subtitles can also be trimmed using the same properties:

```tsx
<SmithchartComponent
  id="smithchart"
  title={{
    text: 'Impedance Analysis',
    subtitle: {
      text: 'Detailed measurement results from laboratory testing at various frequency points',
      enableTrim: true,
      maximumWidth: 400
    }
  }}
>
  <SmithchartSeriesCollectionDirective>
    <SmithchartSeriesDirective points={data} />
  </SmithchartSeriesCollectionDirective>
</SmithchartComponent>
```

## Title Customization

### Font Customization

Customize title and subtitle fonts using the `font` property:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{
        text: 'Smith Chart Analysis',
        font: {
          size: '18px',
          fontFamily: 'Arial',
          fontWeight: 'Bold',
          color: '#2c3e50',
          opacity: 1
        },
        subtitle: {
          text: 'Transmission Line Measurements',
          font: {
            size: '14px',
            fontFamily: 'Arial',
            fontWeight: 'Normal',
            color: '#7f8c8d',
            opacity: 0.9
          }
        }
      }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective points={data} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

**Font properties:**
- `size` - Font size (e.g., '16px', '20px')
- `fontFamily` - Font family name (e.g., 'Arial', 'Roboto')
- `fontWeight` - Font weight ('Normal', 'Bold', 'Lighter')
- `color` - Text color (hex, rgb, named colors)
- `opacity` - Text opacity (0 to 1)

### Text Alignment

Control title and subtitle alignment using the `textAlignment` property:

**Available alignments:**
- `'Near'` - Left-aligned
- `'Center'` - Center-aligned (default)
- `'Far'` - Right-aligned

```tsx
<SmithchartComponent
  id="smithchart"
  title={{
    text: 'Impedance Measurements',
    textAlignment: 'Near'  // Left-aligned title
  }}
>
  <SmithchartSeriesCollectionDirective>
    <SmithchartSeriesDirective points={data} />
  </SmithchartSeriesCollectionDirective>
</SmithchartComponent>
```

### Visibility Control

Show or hide title and subtitle using the `visible` property:

```tsx
<SmithchartComponent
  id="smithchart"
  title={{
    text: 'Main Title',
    visible: true,  // Show title
    subtitle: {
      text: 'Subtitle Text',
      visible: false  // Hide subtitle
    }
  }}
>
  <SmithchartSeriesCollectionDirective>
    <SmithchartSeriesDirective points={data} />
  </SmithchartSeriesCollectionDirective>
</SmithchartComponent>
```

## Complete Examples

### Comprehensive Title Configuration

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const transmissionData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.2, reactance: 0.15 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 0.8, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{
        text: 'RF Circuit Impedance Analysis',
        enableTrim: false,
        textAlignment: 'Center',
        visible: true,
        font: {
          size: '20px',
          fontFamily: 'Segoe UI',
          fontWeight: 'Bold',
          color: '#34495e',
          opacity: 1
        },
        subtitle: {
          text: '50Ω Transmission Line | Frequency: 2.4 GHz | Temperature: 25°C',
          enableTrim: false,
          textAlignment: 'Center',
          visible: true,
          font: {
            size: '13px',
            fontFamily: 'Segoe UI',
            fontWeight: 'Normal',
            color: '#7f8c8d',
            opacity: 0.9
          }
        }
      }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Measured Impedance"
          points={transmissionData}
          fill="#3498db"
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Title with Trimming

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      width="600px"
      height="400px"
      title={{
        text: 'Comprehensive Transmission Line Impedance Analysis for RF Circuit Design and Optimization',
        enableTrim: true,
        maximumWidth: 500,
        font: {
          size: '16px',
          fontWeight: 'Bold',
          color: '#2c3e50'
        },
        subtitle: {
          text: 'Measured data from laboratory testing across multiple frequency ranges with various load conditions',
          enableTrim: true,
          maximumWidth: 500,
          font: {
            size: '12px',
            color: '#95a5a6'
          }
        }
      }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective points={data} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Presentation-Style Titles

High-contrast, large titles for presentations:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      width="1000px"
      height="700px"
      title={{
        text: 'S-Parameter Analysis',
        textAlignment: 'Center',
        font: {
          size: '28px',
          fontFamily: 'Arial',
          fontWeight: 'Bold',
          color: '#000000',
          opacity: 1
        },
        subtitle: {
          text: 'Input Impedance Measurements',
          textAlignment: 'Center',
          font: {
            size: '20px',
            fontFamily: 'Arial',
            fontWeight: 'Normal',
            color: '#333333',
            opacity: 1
          }
        }
      }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective points={data} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Dynamic Titles

Update titles based on user interactions or data changes:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const [frequency, setFrequency] = React.useState('2.4');
  
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div>
      <select value={frequency} onChange={(e) => setFrequency(e.target.value)}>
        <option value="2.4">2.4 GHz</option>
        <option value="5.0">5.0 GHz</option>
        <option value="10.0">10.0 GHz</option>
      </select>

      <SmithchartComponent
        id="smithchart"
        title={{
          text: 'Impedance Analysis',
          subtitle: {
            text: `Frequency: ${frequency} GHz | 50Ω Reference`
          }
        }}
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

### Aligned Titles

Different alignment options for various layouts:

```tsx
// Left-aligned (good for dashboard cards)
<SmithchartComponent
  id="smithchart"
  title={{
    text: 'Circuit Analysis',
    textAlignment: 'Near',
    subtitle: {
      text: 'Transmission Line Data',
      textAlignment: 'Near'
    }
  }}
>
  {/* series configuration */}
</SmithchartComponent>

// Center-aligned (default, balanced)
<SmithchartComponent
  id="smithchart"
  title={{
    text: 'Circuit Analysis',
    textAlignment: 'Center',
    subtitle: {
      text: 'Transmission Line Data',
      textAlignment: 'Center'
    }
  }}
>
  {/* series configuration */}
</SmithchartComponent>

// Right-aligned (special layouts)
<SmithchartComponent
  id="smithchart"
  title={{
    text: 'Circuit Analysis',
    textAlignment: 'Far',
    subtitle: {
      text: 'Transmission Line Data',
      textAlignment: 'Far'
    }
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

## Best Practices

### Title Content

**Do:**
- Keep titles concise and descriptive
- Use subtitles for additional context or parameters
- Include units, frequencies, or conditions in subtitle
- Use proper technical terminology
- Maintain consistency across related charts

**Don't:**
- Make titles overly verbose or technical jargon-heavy
- Include unnecessary details in the main title
- Use vague titles like "Chart 1" or "Data"
- Forget to update dynamic titles when data changes

### Font Sizing

**Title font sizes:**
- Small charts (400-600px): 14-16px
- Medium charts (600-800px): 16-20px
- Large charts (800-1200px): 20-24px
- Presentation charts: 24-32px

**Subtitle font sizes:**
- Typically 60-70% of title size
- Small charts: 11-13px
- Medium charts: 13-16px
- Large charts: 16-18px

### Text Alignment

- **Center**: Default, works for most cases
- **Near (Left)**: Dashboard cards, embedded charts
- **Far (Right)**: Special layouts, RTL languages

### Trimming Guidelines

- Enable trimming for dynamic content or user-generated titles
- Set `maximumWidth` to 80-90% of chart width
- Test with longest expected text
- Consider responsive behavior at different screen sizes

### Visibility

Hide titles when:
- Chart is part of a larger figure with external caption
- Space is extremely limited
- Multiple small charts in a grid (title in parent container)
- Chart is purely decorative

### Color and Contrast

- Ensure sufficient contrast with background (WCAG 2.1 AA: 4.5:1 minimum)
- Use darker colors for titles, lighter for subtitles
- Test in both light and dark themes if applicable
- Avoid colors that clash with series colors

## Common Patterns

### Conditional Title Display

```tsx
function App() {
  const [showTitle, setShowTitle] = React.useState(true);

  return (
    <>
      <button onClick={() => setShowTitle(!showTitle)}>
        Toggle Title
      </button>
      
      <SmithchartComponent
        id="smithchart"
        title={{
          text: 'Impedance Analysis',
          visible: showTitle
        }}
      >
        {/* series configuration */}
      </SmithchartComponent>
    </>
  );
}
```

### Multi-Language Titles

```tsx
const titles = {
  en: { title: 'Impedance Analysis', subtitle: 'Transmission Line Data' },
  es: { title: 'Análisis de Impedancia', subtitle: 'Datos de Línea de Transmisión' },
  fr: { title: 'Analyse d\'Impédance', subtitle: 'Données de Ligne de Transmission' }
};

function App() {
  const [lang, setLang] = React.useState('en');

  return (
    <SmithchartComponent
      id="smithchart"
      title={{
        text: titles[lang].title,
        subtitle: {
          text: titles[lang].subtitle
        }
      }}
    >
      {/* series configuration */}
    </SmithchartComponent>
  );
}
```

### Data-Driven Titles

```tsx
function App() {
  const [chartData, setChartData] = React.useState({
    title: 'Initial Analysis',
    subtitle: 'No data loaded',
    points: []
  });

  React.useEffect(() => {
    // Fetch data from API
    fetch('/api/impedance-data')
      .then(res => res.json())
      .then(data => setChartData({
        title: `Analysis: ${data.testName}`,
        subtitle: `${data.frequency} GHz | ${data.date}`,
        points: data.measurements
      }));
  }, []);

  return (
    <SmithchartComponent
      id="smithchart"
      title={{
        text: chartData.title,
        subtitle: {
          text: chartData.subtitle
        }
      }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective points={chartData.points} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}
```

This comprehensive guide covers all aspects of title and subtitle configuration in Smith Charts, enabling you to create clear, informative chart headers that effectively communicate your data context.
