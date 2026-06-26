# Accessibility & Internationalization

## Table of contents

- [WCAG 2.1 Compliance](#wcag-21-compliance)
  - [ARIA Support](#aria-support)
  - [ARIA Live Regions](#aria-live-regions)
  - [Tab Navigation](#tab-navigation)
- [Keyboard Navigation](#keyboard-navigation)
  - [Enable Keyboard Support](#enable-keyboard-support)
  - [Keyboard Shortcuts](#keyboard-shortcuts)
- [Screen Reader Support](#screen-reader-support)
  - [Semantic HTML](#semantic-html)
  - [Accessible Annotations](#accessible-annotations)
  - [Text Alternatives](#text-alternatives)
- [Color Contrast](#color-contrast)
  - [Sufficient Contrast Ratios](#sufficient-contrast-ratios)
  - [High Contrast Theme](#high-contrast-theme)
  - [Focus Indicators](#focus-indicators)
- [RTL (Right-to-Left) Support](#rtl-right-to-left-support)
  - [Enable RTL](#enable-rtl)
  - [RTL Example with Arabic](#rtl-example-with-arabic)
- [Internationalization (i18n)](#internationalization-i18n)
  - [Locale Settings](#locale-settings)
  - [Number Formatting](#number-formatting)
  - [Currency Formatting](#currency-formatting)
  - [Date/Time Culture](#datetime-culture)
  - [Multi-Language Example](#multi-language-example)
- [Accessibility Checklist](#accessibility-checklist)
- [Tips and Best Practices](#tips-and-best-practices)

See the API quick reference: [api-reference.md](api-reference.md) for prop names, event args and methods.

## WCAG 2.1 Compliance

### ARIA Support

Add accessible labels and descriptions:

```tsx
import * as React from "react";
import { createRoot } from 'react-dom/client';
import { CircularGaugeComponent, AxesDirective, AxisDirective, PointersDirective, PointerDirective } from '@syncfusion/ej2-react-circulargauge';
export function App() {
  return(
    <CircularGaugeComponent
    aria-label="Speed Gauge"
    description="A speedometer gauge showing vehicle speed from 0 to 240 km/h"
  >
    <AxesDirective>
      <AxisDirective
        aria-label="Speed Gauge"
      >
        <PointersDirective>
          <PointerDirective
            aria-label="Current Speed: 85 km/h"
            value={85}
          />
        </PointersDirective>
      </AxisDirective>
    </AxesDirective>
  </CircularGaugeComponent>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<App />);
```

### ARIA Live Regions

Announce value changes to screen readers:

```tsx
<div aria-live="polite" aria-atomic="true">
  <span>Current speed: {currentValue} km/h</span>
</div>

<CircularGaugeComponent>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Tab Navigation

Ensure keyboard navigation works:

```tsx
<div tabIndex={0} role="group" aria-label="Performance Metrics">
  <CircularGaugeComponent
    tabIndex={0}
    aria-label="Performance Gauge"
  >
    {/* gauge content */}
  </CircularGaugeComponent>
</div>
```

---

## Screen Reader Support

### Semantic HTML

Wrap gauge with proper landmarks:

```tsx
<section aria-label="Performance Dashboard">
  <h2>System Performance Metrics</h2>
  
  <article aria-label="CPU Usage Gauge">
    <CircularGaugeComponent
      aria-label="CPU usage gauge"
      role="img"
      aria-describedby="cpu-description"
    >
      {/* gauge content */}
    </CircularGaugeComponent>
    <p id="cpu-description">
      Shows current CPU usage percentage. Green indicates optimal (0-30%), yellow indicates normal (30-60%), red indicates high usage (60-100%).
    </p>
  </article>
</section>
```

### Accessible Annotations

```tsx
<AnnotationDirective
  content="75% - Above Normal"
  textStyle={{ size: '14px' }}
  role="status"
  aria-label="Current CPU usage is 75 percent, above normal"
/>
```

### Text Alternatives

Provide text descriptions for visual elements:

```tsx
<div>
  <div style={{ height: '400px' }}>
    <CircularGaugeComponent
      aria-label="CPU Usage Gauge"
      role="img"
    >
      {/* gauge */}
    </CircularGaugeComponent>
  </div>
  
  <div role="status" aria-live="polite">
    <p>CPU Usage: {value}%</p>
    {value > 80 && <p>Warning: High CPU usage detected.</p>}
  </div>
</div>
```

---

## Color Contrast

### Sufficient Contrast Ratios

Ensure text and elements meet WCAG AA standards (4.5:1 for normal text):

```tsx
// ✅ Good contrast
import { CircularGaugeComponent, AxesDirective, AxisDirective, RangesDirective, RangeDirective } from '@syncfusion/ej2-react-circulargauge';
export function App() {
  return(
    <CircularGaugeComponent
    titleStyle={{
      color: '#1976d2',  // Dark blue
    }}
    background='#ffffff'  // White
  >
    <AxesDirective>
      <AxisDirective
        labelStyle={{
          color: '#424242',  // Dark gray
        }}
        lineStyle={{
          color: '#1976d2'   // Dark blue
        }}
      >
        <RangesDirective>
          {/* Dark colors for ranges */}
          <RangeDirective start={0} end={30} color='#1b5e20' />
          <RangeDirective start={30} end={60} color='#f57f17' />
          <RangeDirective start={60} end={100} color='#b71c1c' />
        </RangesDirective>
      </AxisDirective>
    </AxesDirective>
  </CircularGaugeComponent>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<App />);

// ❌ Poor contrast (avoid)
<AxisDirective
  labelStyle={{ color: '#ffff00' }}  // Yellow on white - not enough contrast
  background='#ffffff'
/>
```

### High Contrast Theme

```tsx
<CircularGaugeComponent
  background='#000000'  // Black background
  titleStyle={{ color: '#ffffff' }}  // White text
>
  <AxesDirective>
    <AxisDirective
      lineStyle={{ color: '#ffffff' }}
      labelStyle={{ color: '#ffffff' }}
      majorTicks={{ color: '#ffffff' }}
    >
      <RangesDirective>
        <RangeDirective start={0} end={33} color='#00ff00' />
        <RangeDirective start={33} end={66} color='#ffff00' />
        <RangeDirective start={66} end={100} color='#ff0000' />
      </RangesDirective>
      <PointersDirective>
        <PointerDirective value={50} color='#00ffff' />
      </PointersDirective>
    </AxisDirective>
  </AxesDirective>
</CircularGaugeComponent>
```

### Focus Indicators

```tsx

// Add custom CSS for focus indicators
const styles = `
  .e-circulargauge:focus {
    outline: 3px solid #1976d2;
    outline-offset: 2px;
  }

  .e-circulargauge:focus-visible {
    outline: 3px dashed #1976d2;
  }
`;
```

---

## RTL (Right-to-Left) Support

### Enable RTL

```tsx
<CircularGaugeComponent
  enableRtl={true}
  direction='AntiClockWise'  // Common for RTL languages
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### RTL Example with Arabic

```tsx
import * as React from "react";
import { createRoot } from 'react-dom/client';
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  RangesDirective,
  RangeDirective,
  PointersDirective,
  PointerDirective,
  AnnotationDirective,
  AnnotationsDirective
} from '@syncfusion/ej2-react-circulargauge';

export function App() {
  return (
    <CircularGaugeComponent
      enableRtl={true}
      title="مقياس الأداء"
      titleStyle={{ size: '20px' }}
    >
      <AxesDirective>
        <AxisDirective
          minimum={0}
          maximum={100}
          direction="AntiClockWise"
        >
          <RangesDirective>
            <RangeDirective start={0} end={30} color="#4caf50" label="جيد" />
            <RangeDirective start={30} end={60} color="#fbc02d" label="عادي" />
            <RangeDirective start={60} end={100} color="#f44336" label="سيء" />
          </RangesDirective>

          <PointersDirective>
            <PointerDirective value={65} />
          </PointersDirective>

          <AnnotationsDirective>
            <AnnotationDirective
              content="القيمة الحالية"
              radius="120%"
              angle={90}
            />
          </AnnotationsDirective>

        </AxisDirective>
      </AxesDirective>
    </CircularGaugeComponent>
  );
}

const root = createRoot(document.getElementById('container'));
root.render(<App />);
```

---

## Internationalization (i18n)

### Locale Settings

```tsx
import { setCulture } from '@syncfusion/ej2-base';

// Set culture for number formatting
setCulture('de-DE');

<CircularGaugeComponent locale="de-DE">
  <AxesDirective>
    <AxisDirective
      labelStyle={{
        format: '{value}'
      }}
    />
  </AxesDirective>
</CircularGaugeComponent>
```

---

### Number Formatting

```tsx
// Different number formats by culture
<AxisDirective
  labelStyle={{
    format: '{value}'  // Uses current culture
  }}
  minimum={0}
  maximum={1000}
/>

// US: 1,000.50
// Germany: 1.000,50
// France: 1 000,50
```

---

### Currency Formatting

```tsx
<AxisDirective
  labelStyle={{
    format: '${value}'  // Manual prefix (not culture-aware)
  }}
  minimum={0}
  maximum={1000}
/>

// Alternative formats
// format: '€{value}'
// format: '¥{value}'
// format: '£{value}'
```

---

### Multi-Language Example

```tsx
import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { setCulture } from '@syncfusion/ej2-base';
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  RangesDirective,
  RangeDirective,
  PointersDirective,
  PointerDirective
} from '@syncfusion/ej2-react-circulargauge';

export function MultiLanguageGauge() {
  const [language, setLanguage] = useState('en-US');

  const labels: { [key: string]: any } = {
    'en-US': {
      title: 'Performance Gauge',
      good: 'Good',
      normal: 'Normal',
      poor: 'Poor'
    },
    'de-DE': {
      title: 'Leistungsmesser',
      good: 'Gut',
      normal: 'Normal',
      poor: 'Schlecht'
    },
    'fr-FR': {
      title: 'Jauge de Performance',
      good: 'Bon',
      normal: 'Normal',
      poor: 'Mauvais'
    }
  };

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang);
    setCulture(lang);
  };

  const currentLabels = labels[language];

  return (
    <div>
      <div>
        <select onChange={(e) => handleLanguageChange(e.target.value)}>
          <option value="en-US">English</option>
          <option value="de-DE">Deutsch</option>
          <option value="fr-FR">Français</option>
        </select>
      </div>

      <CircularGaugeComponent
        locale={language}
        title={currentLabels.title}
      >
        <AxesDirective>
          <AxisDirective minimum={0} maximum={100}>
            <RangesDirective>
              <RangeDirective 
                start={0} 
                end={30} 
                color='#4caf50'
                label={currentLabels.good}
              />
              <RangeDirective 
                start={30} 
                end={60} 
                color='#fbc02d'
                label={currentLabels.normal}
              />
              <RangeDirective 
                start={60} 
                end={100} 
                color='#f44336'
                label={currentLabels.poor}
              />
            </RangesDirective>
            <PointersDirective>
              <PointerDirective value={65} />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );
}

const root = createRoot(document.getElementById('container')!);
root.render(<MultiLanguageGauge />);
```

---

## Accessibility Checklist

* [ ] Gauge has `aria-label` or `aria-describedby`
* [ ] Text has sufficient color contrast (4.5:1 minimum)
* [ ] Keyboard navigation works (custom implementation required)
* [ ] Focus indicators are visible
* [ ] Screen reader announcements for value changes
* [ ] Semantic HTML structure
* [ ] Text alternatives for complex visualizations
* [ ] RTL support enabled for right-to-left languages
* [ ] Number formats respect user locale
* [ ] Labels are readable (not too small)
* [ ] No color as sole differentiator (use patterns/labels)

---

## Tips and Best Practices

* **Always provide descriptions:** Don't rely only on visual representation
* **Use aria-live:** For real-time updates, announce changes to screen readers
* **Test with screen readers:** NVDA (Windows), JAWS, VoiceOver (Mac)
* **Keyboard first:** Ensure all functionality works without mouse
* **Focus management:** Keep focus visible during interactions
* **Localization:** Plan for text expansion in translations (German is ~20% longer than English)
* **Symbols:** Use consistent symbols/icons across cultures
* **Testing:** Include accessibility in your testing strategy

---

## Notes

* `locale` must be used along with `setCulture()` for proper formatting
* `setCulture()` sets global culture; `locale` applies it to the component
* Currency formats like `${value}` are manual and not locale-aware
* CircularGauge supports numeric formatting only (no date/time axis)
