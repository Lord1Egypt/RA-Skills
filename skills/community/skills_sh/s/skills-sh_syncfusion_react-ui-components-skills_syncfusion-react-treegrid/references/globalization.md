---
name: globalization
description: 'Globalization in React TreeGrid - internationalization (i18n), localization (l10n), RTL support, date and number formatting per locale.'
---

# Globalization

## Table of Contents
- [Internationalization (i18n)](#internationalization)
- [Localization (l10n)](#localization)
- [RTL Support](#rtl-support)
- [Date and Number Formatting](#date-and-number-formatting)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Internationalization

Internationalize UI text:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Locale } from '@syncfusion/ej2-react-treegrid';
import { locale } from '@syncfusion/ej2-base';

// Add custom locale
locale.setLocale('es');  // Spanish
locale['es'] = {
  'grid': {
    'Add': 'Añadir',
    'Edit': 'Editar',
    'Delete': 'Eliminar',
    'Update': 'Actualizar',
    'Cancel': 'Cancelar'
  }
};

export default function App() {
  const data = [ { TaskID: 1, TaskName: 'Planning', Children: [] } ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      locale="es"
      editSettings={{ allowEditing: true, allowAdding: true }}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
    </TreeGridComponent>
  );
}
```

## Localization

Localize UI elements for specific cultures:

```tsx

import { locale } from '@syncfusion/ej2-base';

// Set German locale
locale.setLocale('de');

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  locale="de"
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

**Supported Locales**: en (English), de (German), fr (French), es (Spanish), ja (Japanese), zh (Chinese), etc.

## RTL Support

Right-to-left language support:

```tsx
import { enableRtl } from '@syncfusion/ej2-base';

// Enable RTL globally
enableRtl(true);

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  locale="ar"  // Arabic
  enableRtl={true}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Date and Number Formatting

Localize date and number formats:

```tsx

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  locale="ja"  // Japanese
>
  <ColumnsDirective>
    <ColumnDirective 
      field="StartDate" 
      headerText="Start Date" 
      type="date" 
      format="yMd"  // Locale-aware format
      width={120}
    />
    <ColumnDirective 
      field="Budget" 
      headerText="Budget" 
      type="number" 
      format="C"  // Locale-specific currency
      width={120}
    />
  </ColumnsDirective>
</TreeGridComponent>
```

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `locale` | string | Set locale (e.g., 'en', 'de', 'ja') |
| `enableRtl` | boolean | Enable right-to-left layout |
| `setLocale` | method | Set locale globally |
| `format` | string | Date/number format per locale |

## Common Patterns

1. **Multi-language Support**: Dynamically switch between locales
2. **Culture-specific Formatting**: Date and currency per locale
3. **RTL Layouts**: Support Arabic, Hebrew, Persian
4. **User Preferences**: Save language preference

