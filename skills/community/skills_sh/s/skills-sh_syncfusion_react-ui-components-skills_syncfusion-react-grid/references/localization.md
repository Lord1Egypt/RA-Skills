# Localization & Globalization in React Grid

## Table of Contents
- [Overview](#overview)
- [Localization Setup](#localization-setup)
- [Culture Configuration](#culture-configuration)
- [Number Formatting](#number-formatting)
- [Date Formatting](#date-formatting)
- [Currency Formatting](#currency-formatting)
- [RTL Support](#rtl-support)
- [Custom Localization](#custom-localization)

## Overview

Syncfusion React Grid supports 60+ languages and locales, providing automatic formatting based on culture settings.

---

## Localization Setup

### Set Grid Locale

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';
import { setLocale } from '@syncfusion/ej2-base';

// Set locale for all Syncfusion components
setLocale('de');  // German
// setLocale('fr');  // French
// setLocale('es');  // Spanish
// setLocale('ja');  // Japanese
// setLocale('zh');  // Chinese
// setLocale('ar');  // Arabic
// setLocale('pt');  // Portuguese

<GridComponent
  dataSource={data}
  locale='de'
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
  </ColumnsDirective>
</GridComponent>
```

### Available Locales

```tsx
// Common locales
const locales = [
  'en',      // English
  'de',      // German
  'fr',      // French
  'es',      // Spanish
  'it',      // Italian
  'pt-BR',   // Portuguese (Brazil)
  'ja',      // Japanese
  'zh',      // Chinese Simplified
  'zh-TW',   // Chinese Traditional
  'ko',      // Korean
  'ru',      // Russian
  'ar',      // Arabic
  'he',      // Hebrew
  'fa',      // Farsi
  'hi',      // Hindi
  'vi',      // Vietnamese
  'th',      // Thai
  'tr',      // Turkish
  'pl',      // Polish
  'nl',      // Dutch
];

const handleLocaleChange = (locale) => {
  setLocale(locale);
  // Grid updates automatically
};
```

---

## Culture Configuration

### Date Culture Settings

```tsx
import { GridComponent, ColumnsDirective, ColumnDirectiveInjection, Page } from '@syncfusion/ej2-react-grids';
import { setCulture } from '@syncfusion/ej2-base';

// Set culture (automatically sets locale, date/number format)
setCulture('de-DE');  // German - Germany
setCulture('en-US');  // English - United States
setCulture('ja-JP');  // Japanese - Japan
setCulture('zh-CN');  // Chinese - China

<GridComponent
  dataSource={data}
  locale='de-DE'
>
  <ColumnsDirective>
    <ColumnDirective
      field='OrderDate'
      headerText='Order Date'
      type='date'
      format='dd/MM/yyyy'  // German format
    />
  </ColumnsDirective>
  <Inject services={[Page]} />
</GridComponent>
```

### Browser Locale Auto-Detection

```tsx
import { getCulture } from '@syncfusion/ej2-base';

function GridWithAutoCulture() {
  const browserLocale = navigator.language;  // e.g., 'en-US'
  
  return (
    <GridComponent dataSource={data} locale={browserLocale}>
      <ColumnsDirective>
        <ColumnDirective field='OrderDate' type='date' format='short' />
      </ColumnsDirective>
    </GridComponent>
  );
}
```

---

## Number Formatting

### Automatic Culture-Based Formatting

```tsx
// German (de-DE): Uses comma as decimal separator
// En-US: Uses period as decimal separator

<ColumnDirective
  field='Freight'
  headerText='Freight'
  type='number'
  format='N2'  // 2 decimal places
/>

// Results:
// de-DE: 1.234,56 EUR
// en-US: 1,234.56 USD
// fr-FR: 1 234,56 €
```

### Number Format Examples

```tsx
<GridComponent locale='de-DE'>
  <ColumnsDirective>
    {/* Percentage */}
    <ColumnDirective
      field='Discount'
      type='number'
      format='P2'  // 15,50% (German format)
    />
    
    {/* Currency */}
    <ColumnDirective
      field='Freight'
      type='number'
      format='C2'  // €1.234,56 (German format)
    />
    
    {/* Large numbers */}
    <ColumnDirective
      field='Amount'
      type='number'
      format='N0'  // 1.234.567 (German thousands separator)
    />
  </ColumnsDirective>
</GridComponent>
```

---

## Date Formatting

### Culture-Aware Date Formats

```tsx
// Different formats by culture
<GridComponent locale='en-US'>
  <ColumnDirective field='OrderDate' type='date' format='short' />
  {/* Result: 3/15/2023 */}
</GridComponent>

<GridComponent locale='de-DE'>
  <ColumnDirective field='OrderDate' type='date' format='short' />
  {/* Result: 15.03.2023 */}
</GridComponent>

<GridComponent locale='ja-JP'>
  <ColumnDirective field='OrderDate' type='date' format='short' />
  {/* Result: 2023/3/15 */}
</GridComponent>
```

### Date Format Codes

```tsx
<GridComponent>
  <ColumnsDirective>
    <ColumnDirective 
      field='OrderDate' 
      type='date' 
      format='yMd'  // Combined format code
    />
    <ColumnDirective 
      field='OrderDate' 
      type='date' 
      format='MMM/dd/yyyy'  // Custom pattern
    />
    <ColumnDirective 
      field='OrderDate' 
      type='datetime' 
      format='MM/dd/yyyy hh:mm a'  // Date + time
    />
  </ColumnsDirective>
</GridComponent>
```

### Date Picker Locale

```tsx
import { GridComponent, Inject, Edit } from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={data}
  locale='de-DE'
  editSettings={{ mode: 'Dialog' }}
>
  <ColumnsDirective>
    <ColumnDirective
      field='OrderDate'
      headerText='Order Date'
      type='date'
      edit={{
        params: {
          locale: 'de-DE'  // DatePicker uses German locale
        }
      }}
    />
  </ColumnsDirective>
  <Inject services={[Edit]} />
</GridComponent>
```

---

## Currency Formatting

### Automatic Currency by Locale

```tsx
// Format as currency with automatic symbol
<ColumnDirective
  field='Freight'
  type='number'
  format='C2'  // Currency with 2 decimals
/>

// Results by locale:
// en-US: $1,234.56
// de-DE: 1.234,56 €
// fr-FR: 1 234,56 €
// ja-JP: ¥1234
// gb: £1,234.56
```

### Custom Currency Format

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-grids';

function GridWithCurrency() {
  const userCurrency = getUserCurrency();  // 'USD', 'EUR', 'GBP', etc.

  const currencyFormat = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: userCurrency,
      minimumFractionDigits: 2
    }).format(value);
  };

  return (
    <GridComponent dataSource={data}>
      <ColumnsDirective>
        <ColumnDirective
          field='Freight'
          headerText='Freight'
          template={(props) => currencyFormat(props.Freight)}
        />
      </ColumnsDirective>
      <Inject services={[Page]} />
    </GridComponent>
  );
}
```

---

## RTL Support

### Enable Right-to-Left Layout

```tsx
import { enableRtl } from '@syncfusion/ej2-base';

// Enable RTL globally
enableRtl(true);

<GridComponent
  dataSource={data}
  locale='ar'  // Arabic
  enableRtl={true}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='معرّف الطلب' width='100' />
    <ColumnDirective field='CustomerID' headerText='معرّف العميل' width='120' />
  </ColumnsDirective>
</GridComponent>
```

### Conditional RTL

```tsx
import React, { useState } from 'react';
import { enableRtl } from '@syncfusion/ej2-base';

function GridWithRTLToggle() {
  const [isRTL, setIsRTL] = useState(false);

  const toggleRTL = () => {
    enableRtl(!isRTL);
    setIsRTL(!isRTL);
  };

  return (
    <div>
      <button onClick={toggleRTL}>
        {isRTL ? 'LTR' : 'RTL'}
      </button>

      <GridComponent
        dataSource={data}
        enableRtl={isRTL}
        locale={isRTL ? 'ar' : 'en'}
      >
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default GridWithRTLToggle;
```

### RTL CSS

```css
/* Apply RTL styles */
[data-rtl='true'] .e-grid {
  direction: rtl;
  text-align: right;
}

[data-rtl='true'] .e-grid .e-gridheader {
  text-align: right;
}

[data-rtl='true'] .e-grid .e-gridcontent td {
  text-align: right;
}

[data-rtl='true'] .e-grid .e-sortindicator::before {
  left: auto;
  right: 2px;
}
```

---

## Custom Localization

### Override Default Messages

```tsx
import { GridComponent } from '@syncfusion/ej2-react-grids';
import { L10n } from '@syncfusion/ej2-base';

// Define custom locale strings
L10n.load({
  'de': {
    'grid': {
      'EmptyRecord': 'Keine Datensätze gefunden',
      'Pagerformat': '{0} to {1} von {2} Elementen',
      'BatchSaveConfirm': 'Möchten Sie die Änderungen speichern?',
      'BatchDeleteConfirm': 'Möchten Sie die ausgewählten Datensätze löschen?'
    }
  }
});

<GridComponent dataSource={data} locale='de'>
  {/* columns */}
</GridComponent>
```

### Custom Messages Examples

```tsx
L10n.load({
  'en': {
    'grid': {
      // Paging
      'Pagerformat': 'Showing {0} to {1} of {2} records',
      'PagerItemsPerPage': 'Items per page',
      
      // Sorting
      'SortAscending': 'Sort Ascending',
      'SortDescending': 'Sort Descending',
      
      // Filtering
      'NoRecordsToDisplay': 'No records to display',
      'SerialNumberColumn': '#',
      
      // Editing
      'EditOperationAlert': 'No records selected for edit operation',
      'DeleteOperationAlert': 'No records selected for delete operation',
      'SaveButton': 'Save',
      'CancelButton': 'Cancel',
      'EditButton': 'Edit',
      'DeleteButton': 'Delete',
      
      // Grouping  
      'GroupDropArea': 'Drag a column header here to group its column',
      
      // Export
      'ExcelExport': 'Excel Export',
      'PdfExport': 'PDF Export',
      'CsvExport': 'CSV Export'
    }
  }
});
```

### Language Switcher

```tsx
import React, { useState } from 'react';
import { setLocale } from '@syncfusion/ej2-base';

function GridWithLanguageSelector() {
  const [language, setLanguage] = useState('en');

  const handleLanguageChange = (newLanguage) => {
    setLocale(newLanguage);
    setLanguage(newLanguage);
  };

  const languages = {
    'en': 'English',
    'de': 'Deutsch',
    'fr': 'Français',
    'es': 'Español',
    'ja': '日本語',
    'ar': 'العربية'
  };

  return (
    <div>
      <select 
        value={language} 
        onChange={(e) => handleLanguageChange(e.target.value)}
      >
        {Object.entries(languages).map(([code, name]) => (
          <option key={code} value={code}>{name}</option>
        ))}
      </select>

      <GridComponent dataSource={data} locale={language}>
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default GridWithLanguageSelector;
```

---

## Best Practices

1. **Use locale codes** (en-US, de-DE, etc.)
2. **Set culture early** in application
3. **Test all locales** with real data
4. **Use format codes** for automatic locale formatting
5. **Provide language switcher** if needed
6. **Support RTL languages** properly
7. **Test with special characters** in each locale
8. **Document locale support** for users
9. **Use browser locale** as default
10. **Cache locale settings** in user preferences
