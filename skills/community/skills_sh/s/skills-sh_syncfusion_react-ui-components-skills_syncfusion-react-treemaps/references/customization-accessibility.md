# Customization, Accessibility & Export

## Table of Contents

- [Styling and Theming](#styling-and-theming)
  - [Built-in Themes](#built-in-themes)
  - [Available Themes](#available-themes)
  - [CSS Customization](#css-customization)
  - [CSS Variables](#css-variables)
  - [Dark Mode Support](#dark-mode-support)
- [Accessibility Features](#accessibility-features)
  - [WCAG 2.1 Compliance](#wcag-21-compliance)
  - [Keyboard Navigation](#keyboard-navigation)
  - [Screen Reader Support](#screen-reader-support)
  - [Color Contrast](#color-contrast)
  - [Focus Indicators](#focus-indicators)
- [RTL Support](#rtl-support)
  - [Enable Right-to-Left Layout](#enable-right-to-left-layout)
  - [RTL with Arabic Labels](#rtl-with-arabic-labels)
  - [Responsive RTL](#responsive-rtl)
- [Internationalization](#internationalization)
  - [Multi-Language Support](#multi-language-support)
  - [Number and Date Formatting](#number-and-date-formatting)
  - [Multi-Language Tooltips](#multi-language-tooltips)
- [Print and Export](#print-and-export)
  - [Export as Image](#export-as-image)
  - [Export Options](#export-options)
  - [Print TreeMap](#print-treemap)
  - [Export with Custom Styling](#export-with-custom-styling)
- [Performance Optimization](#performance-optimization)
  - [Data Aggregation for Performance](#data-aggregation-for-performance)
  - [Lazy Loading with Drill-Down](#lazy-loading-with-drill-down)
  - [Memoization for Performance](#memoization-for-performance)
- [Best Practices](#best-practices)
- [Accessibility Checklist](#accessibility-checklist)
- [Common Issues](#common-issues)
- [Next Steps](#next-steps)

## Styling and Theming

### Built-in Themes

Syncfusion TreeMap includes several built-in themes:

```jsx
import { TreeMapComponent } from '@syncfusion/ej2-react-treemap';

<TreeMapComponent
  dataSource={data}
  theme="Material"  // Material, Bootstrap, Fluent, Tailwind, HighContrast
/>
```

### Available Themes

| Theme | Use Case | Characteristics |
|-------|----------|-----------------|
| Material | Default, modern | Clean, material design |
| Bootstrap | Web apps | Professional, corporate |
| Fluent | Microsoft-like | Modern, accessible |
| Tailwind | Utility-first | Customizable, lightweight |
| HighContrast | Accessibility | High contrast for visibility |

### CSS Customization

```jsx
// Override TreeMap styles with CSS
const customCSS = `
  .e-treemap {
    font-family: 'Segoe UI', sans-serif;
  }

  .e-treemap-leaf {
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .e-treemap-label {
    font-weight: 500;
  }
`;

export function StyledTreeMap() {
  return (
    <>
      <style>{customCSS}</style>
      <TreeMapComponent
        dataSource={data}
        leafItemSettings={{ labelPath: 'Item' }}
      />
    </>
  );
}
```

### CSS Variables

```jsx
// Use CSS variables for dynamic theming
const root = document.documentElement;
root.style.setProperty('--treemap-bg-color', '#f5f5f5');
root.style.setProperty('--treemap-text-color', '#333');

// In CSS
.e-treemap {
  background-color: var(--treemap-bg-color);
  color: var(--treemap-text-color);
}
```

### Dark Mode Support

```jsx
export function DarkModeTreeMap() {
  const [isDarkMode, setIsDarkMode] = React.useState(false);

  React.useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('dark-mode');
      import('@syncfusion/ej2-base/styles/material-dark.css');
    } else {
      document.body.classList.remove('dark-mode');
      import('@syncfusion/ej2-base/styles/material.css');
    }
  }, [isDarkMode]);

  return (
    <div>
      <button onClick={() => setIsDarkMode(!isDarkMode)}>
        Toggle Dark Mode
      </button>
      <TreeMapComponent dataSource={data} />
    </div>
  );
}
```

## Accessibility Features

### WCAG 2.1 Compliance

TreeMap supports WCAG 2.1 Level AA guidelines:

```jsx
import { TreeMapComponent, Inject } from '@syncfusion/ej2-react-treemap';

<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelPath: 'Item',
    labelStyle: { size: '14px' }  // Readable font size
  }}
  tooltipSettings={{
    visible: true,
    format: '${Item}: ${Value}'  // Provide text alternatives
  }}
>
  <Inject services={[TreeMapSelection, TreeMapHighlight]} />
</TreeMapComponent>
```

### Keyboard Navigation

Enable keyboard navigation for assistive devices:

```jsx
<TreeMapComponent
  dataSource={data}
  enableKeyboardNavigation={true}  // Enable keyboard support
  selectionSettings={{
    mode: 'Item'
  }}
/>
```

**Keyboard shortcuts:**
- **Tab:** Navigate between items
- **Enter/Space:** Select/activate item
- **Arrow Keys:** Move between items
- **Escape:** Clear selection

### Screen Reader Support

```jsx
<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelPath: 'Product',
    labelFormat: '${Product}: ${Sales} units'  // Meaningful labels
  }}
  tooltipSettings={{
    visible: true,
    format: '${Product}\nCategory: ${Category}\nSales: ${Sales} units'
  }}
/>
```

### Color Contrast

Ensure sufficient contrast for visibility:

```jsx
const accessibleColors = [
  '#003f5c',  // Dark blue - 9.5:1 contrast
  '#bc5090',  // Purple - 4.5:1 contrast
  '#ffa600',  // Orange - 3.1:1 contrast
];

<TreeMapComponent
  palette={accessibleColors}
  leafItemSettings={{
    labelFontStyle: {
      color: '#000',  // High contrast text
      size: '14px'
    }
  }}
/>
```

### Focus Indicators

```jsx
const focusStyles = `
  .e-treemap-leaf:focus {
    outline: 3px solid #0066CC;
    outline-offset: 2px;
  }
`;

export function AccessibleTreeMap() {
  return (
    <>
      <style>{focusStyles}</style>
      <TreeMapComponent
        dataSource={data}
      />
    </>
  );
}
```

## RTL Support

### Enable Right-to-Left Layout

```jsx
import { TreeMapComponent } from '@syncfusion/ej2-react-treemap';

export function RTLTreeMap() {
  return (
    <TreeMapComponent
      dataSource={data}
      enableRtl={true}  // Enable RTL
      leafItemSettings={{
        labelPath: 'Item'  // Labels will be RTL-aware
      }}
      legendSettings={{
        visible: true,
        position: 'Left'  // Auto-adjusts for RTL
      }}
    />
  );
}
```

### RTL with Arabic Labels

```jsx
const arabicData = [
  { الفئة: 'الإلكترونيات', المبيعات: 45000 },
  { الفئة: 'الملابس', المبيعات: 28000 },
  { الفئة: 'الأثاث', المبيعات: 35000 }
];

<TreeMapComponent
  enableRtl={true}
  dataSource={arabicData}
  leafItemSettings={{
    labelPath: 'الفئة'
  }}
/>
```

### Responsive RTL

```jsx
export function ResponsiveRTL() {
  const [isRTL, setIsRTL] = React.useState(
    document.documentElement.lang === 'ar'
  );

  return (
    <TreeMapComponent
      enableRtl={isRTL}
      dataSource={data}
      leafItemSettings={{ labelPath: 'Item' }}
    />
  );
}
```

## Internationalization

### Multi-Language Support

```jsx
import { setCulture, loadCldr } from '@syncfusion/ej2-base';

// Load culture data
loadCldr(
  require('cldr-data/main/ar/numbers.json'),
  require('cldr-data/main/ar/currencies.json')
);

export function InternationalizedTreeMap() {
  // Set culture
  setCulture('ar');  // Arabic
  // or 'es' for Spanish, 'fr' for French, etc.

  return (
    <TreeMapComponent
      dataSource={data}
      locale="ar"
      leafItemSettings={{
        labelFormat: '${Item}\n{0:C2}'  // Currency format per locale
      }}
    />
  );
}
```

### Number and Date Formatting

```jsx
export function FormattedNumbers() {
  const data = [
    { Item: 'Product A', Sales: 1234567.89 },
    { Item: 'Product B', Sales: 987654.32 }
  ];

  return (
    <TreeMapComponent
      dataSource={data}
      locale="en-US"
      leafItemSettings={{
        labelFormat: '${Item}\n${Sales:C2}'  // Formatted currency
      }}
    />
  );
}
```

### Multi-Language Tooltips

```jsx
const translations = {
  'en': {
    item: 'Item',
    sales: 'Sales',
    category: 'Category'
  },
  'es': {
    item: 'Artículo',
    sales: 'Ventas',
    category: 'Categoría'
  },
  'ar': {
    item: 'عنصر',
    sales: 'مبيعات',
    category: 'فئة'
  }
};

export function MultiLanguageTreeMap() {
  const [language, setLanguage] = React.useState('en');
  const t = translations[language];

  return (
    <TreeMapComponent
      dataSource={data}
      enableRtl={language === 'ar'}
      tooltipSettings={{
        format: `${t.item}: \${Item}<br>${t.sales}: \${Sales}`
      }}
    />
  );
}
```

## Print and Export

### Export as Image

**Important:** Always include `allowImageExport={true}` prop and inject `ImageExport` service.

```jsx
import { TreeMapComponent, ImageExport, Inject } from '@syncfusion/ej2-react-treemap';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

export function ExportTreeMap() {
  let treeMapInstance;

  const handleExport = () => {
    if (treeMapInstance) {
      treeMapInstance.export('PNG', 'treemap');  // Export as PNG
    }
  };

  return (
    <div>
      <ButtonComponent onClick={handleExport}>
        Export as PNG
      </ButtonComponent>
      <TreeMapComponent 
        ref={g => treeMapInstance = g}
        allowImageExport={true}
        dataSource={data}
      >
        <Inject services={[ImageExport]} />
      </TreeMapComponent>
    </div>
  );
}
```

### Export Options

```jsx
// Export as SVG
treeMapInstance.export('SVG', 'treemap-chart');

// Export as PDF
treeMapInstance.export('PDF', 'treemap-document');

// Export with custom dimensions (for PNG)
treeMapInstance.export('PNG', 'treemap', 'Landscape', 1024, 768);
```

### Print TreeMap

**Important:** Always include `allowPrint={true}` prop and inject `Print` service.

```jsx
import { TreeMapComponent, Print, Inject } from '@syncfusion/ej2-react-treemap';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

export function PrintTreeMap() {
  let treeMapInstance;

  const handlePrint = () => {
    if (treeMapInstance) {
      treeMapInstance.print();
    }
  };

  return (
    <div>
      <ButtonComponent onClick={handlePrint}>
        Print
      </ButtonComponent>
      <TreeMapComponent 
        ref={g => treeMapInstance = g}
        allowPrint={true}
        dataSource={data}
      >
        <Inject services={[Print]} />
      </TreeMapComponent>
    </div>
  );
}
```

### Combined Print and Export

```jsx
import { TreeMapComponent, Print, ImageExport, Inject } from '@syncfusion/ej2-react-treemap';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

export function PrintAndExportTreeMap() {
  let treeMapInstance;

  const handlePrint = () => {
    if (treeMapInstance) {
      treeMapInstance.print();
    }
  };

  const handleExportPNG = () => {
    if (treeMapInstance) {
      treeMapInstance.export('PNG', 'treemap-report');
    }
  };

  const handleExportPDF = () => {
    if (treeMapInstance) {
      treeMapInstance.export('PDF', 'treemap-report');
    }
  };

  return (
    <div>
      <ButtonComponent onClick={handlePrint}>Print</ButtonComponent>
      <ButtonComponent onClick={handleExportPNG}>Export PNG</ButtonComponent>
      <ButtonComponent onClick={handleExportPDF}>Export PDF</ButtonComponent>
      
      <TreeMapComponent 
        ref={g => treeMapInstance = g}
        allowPrint={true}
        allowImageExport={true}
        dataSource={data}
        height="500px"
      >
        <Inject services={[Print, ImageExport]} />
      </TreeMapComponent>
    </div>
  );
}
```

## Performance Optimization

### Data Aggregation for Performance

```jsx
export function AggregatedData() {
  const rawData = /* large dataset */;
  
  // Aggregate similar items
  const aggregated = rawData.reduce((acc, item) => {
    const existing = acc.find(x => x.Category === item.Category);
    if (existing) {
      existing.Value += item.Value;
    } else {
      acc.push({ ...item });
    }
    return acc;
  }, []);

  return (
    <TreeMapComponent
      dataSource={aggregated}
      height="350px"
    />
  );
}
```

### Lazy Loading with Drill-Down

```jsx
export function LazyLoadTreeMap() {
  const [data, setData] = React.useState(initialData);

  const handleDrillStart = async (args) => {
    const childData = await fetchChildData(args.item.id);
    setData([...data, ...childData]);
  };

  return (
    <TreeMapComponent
      enableDrillDown={true}
      dataSource={data}
    >
      {/* Levels */}
    </TreeMapComponent>
  );
}
```

### Memoization for Performance

```jsx
export const OptimizedTreeMap = React.memo(function TreeMap({ data }) {
  return (
    <TreeMapComponent
      dataSource={data}
      leafItemSettings={{ labelPath: 'Item' }}
    />
  );
});
```

## Best Practices

1. **Accessibility:** Always include ARIA labels and keyboard navigation
2. **Color:** Use color-blind friendly palettes
3. **Contrast:** Maintain 4.5:1 minimum contrast ratio
4. **Performance:** Aggregate large datasets before rendering
5. **Export:** Provide export options for reports and sharing
6. **i18n:** Support multiple languages for global audiences
7. **RTL:** Test RTL functionality for Arabic/Hebrew users

## Accessibility Checklist

- [ ] Color contrast meets WCAG AA standards
- [ ] Keyboard navigation enabled
- [ ] ARIA labels provided
- [ ] Tooltips contain meaningful information
- [ ] Font size ≥ 12px for readability
- [ ] Focus indicators visible (3px outline)
- [ ] Screen reader tested
- [ ] Print/export functionality works

## Common Issues

**Issue:** RTL layout not applying
- **Solution:** Set `enableRtl={true}`, verify CSS loaded correctly

**Issue:** Export creates blank image
- **Solution:** Ensure TreeMap fully rendered before export, add delay if needed

**Issue:** Translation text not displaying
- **Solution:** Verify culture data loaded, locale property matches

## Next Steps

- **Color Mapping:** See [color-mapping.md](color-mapping.md) for accessible colors
- **Legends:** See [legends-tooltips-selection.md](legends-tooltips-selection.md) for legend alternatives
- **Data Binding:** See [data-binding.md](data-binding.md) for large dataset handling
