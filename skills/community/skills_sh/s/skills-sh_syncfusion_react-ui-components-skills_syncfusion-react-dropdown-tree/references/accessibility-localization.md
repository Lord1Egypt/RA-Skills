# Accessibility & Localization

## Table of Contents

- [Accessibility Overview](#accessibility-overview)
- [WCAG Compliance](#wcag-compliance)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [Localization](#localization)
- [RTL Support](#rtl-support)

## Accessibility Overview

The Dropdown Tree component follows accessibility guidelines to ensure usability for all users, including those with disabilities.

### Compliance Standards

| Standard | Support | Notes |
|----------|---------|-------|
| **WCAG 2.2** | Partial | Most features meet guidelines |
| **Section 508** | Partial | Sufficient for most scenarios |
| **Screen Readers** | Full | Complete support with ARIA |
| **Keyboard Navigation** | Full | All features accessible via keyboard |
| **Color Contrast** | Full | Meets WCAG AA standards |
| **Mobile Devices** | Full | Touch-friendly interfaces |
| **RTL Languages** | Full | Full right-to-left support |

### WCAG 2.2

Dropdown Tree meets WCAG 2.2 Level AA standards for:
- Perceivable: Content is visible and distinguishable
- Operable: Keyboard accessible, sufficient time for interactions
- Understandable: Clear labels, error prevention
- Robust: Compatible with assistive technologies

### Section 508

Complies with U.S. Section 508 accessibility requirements for federal information technology.

## WAI-ARIA Attributes

The component uses WAI-ARIA (Web Accessibility Initiative - Accessible Rich Internet Applications) attributes to communicate with assistive technologies.

### ARIA Roles and Attributes

| Attribute | Element | Purpose |
|-----------|---------|---------|
| `role="listbox"` | Dropdown container | Identifies list functionality |
| `role="tree"` | Tree structure | Identifies hierarchical tree |
| `role="treeitem"` | Tree node | Identifies individual nodes |
| `role="group"` | Node children | Groups child elements |
| `role="checkbox"` | Checkbox input | Identifies checkbox control |
| `aria-disabled` | Input/Items | Indicates disabled state |
| `aria-expanded` | Expandable items | Shows expanded/collapsed state |
| `aria-selected` | Selected items | Marks selected nodes |
| `aria-checked` | Checkboxes | Indicates checkbox state |
| `aria-owns` | Input | References popup list |
| `aria-haspopup` | Input | Indicates popup availability |
| `aria-activedescendant` | Input | References active list item |
| `aria-label` | Input/Checkboxes | Provides accessible labels |
| `aria-describedby` | Input | Links to description element |
| `aria-labelledby` | Input | References label element |
| `aria-level` | Tree items | Indicates nesting level |
| `aria-multiselectable` | Tree | Indicates multi-select capability |

### Using Labels

```jsx
// Provide accessible label
<div>
  <label htmlFor="deptSelect" id="deptLabel">
    Select Department:
  </label>
  <DropDownTreeComponent
    id="deptSelect"
    aria-labelledby="deptLabel"
    fields={{...}}
  />
</div>
```

### Using Descriptions

```jsx
<div>
  <DropDownTreeComponent
    id="tree"
    aria-describedby="treeHelp"
    fields={{...}}
  />
  <small id="treeHelp">
    Select one or more items from the tree. Use arrow keys to navigate.
  </small>
</div>
```

## Keyboard Navigation

All Dropdown Tree features are accessible via keyboard.

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Alt + Down** | Open popup |
| **Alt + Up** | Close popup |
| **Escape** | Close popup |
| **Arrow Up** | Select previous item |
| **Arrow Down** | Select next item |
| **Arrow Right** | Expand current item |
| **Arrow Left** | Collapse current item |
| **Home** | Go to first item |
| **End** | Go to last item |
| **Enter** | Select focused item |
| **Space** | Check/uncheck focused item (with checkboxes) |
| **Tab** | Move to next control |
| **Shift + Tab** | Move to previous control |

### Keyboard Interaction Example

```
1. User presses Tab to focus Dropdown Tree input
2. User presses Alt+Down to open popup
3. User presses Arrow Down to navigate items
4. User presses Arrow Right to expand category
5. User presses Space to check item (if checkboxes enabled)
6. User presses Escape to close popup
7. Selection is maintained in input field
```

### Testing Keyboard Access

```jsx
// Component properly receives keyboard events
<DropDownTreeComponent
  id="tree"
  fields={{...}}
  // Component handles all keyboard interactions automatically
/>
```

## Screen Reader Support

Screen readers (NVDA, JAWS, VoiceOver) announce component state, structure, and changes.

### What Screen Readers Announce

- **Component type**: "List box" or "Tree view"
- **Item information**: Item text, nesting level, expanded state
- **Selection state**: "Selected" or "Checked"
- **Checkbox status**: "Checked", "Unchecked", "Partially checked"
- **Interactive instructions**: "Press Space to check"
- **Error messages**: Validation or state change notifications

### Best Practices

**1. Use Semantic Labels**

```jsx
// Good: Clear label for screen readers
<div>
  <label htmlFor="categoryTree">Select Category</label>
  <DropDownTreeComponent id="categoryTree" {...props} />
</div>

// Avoid: No label
<DropDownTreeComponent {...props} />
```

**2. Provide Help Text**

```jsx
<div>
  <DropDownTreeComponent 
    id="tree"
    aria-describedby="help"
    {...props}
  />
  <p id="help">
    Select one item. Use arrow keys to navigate.
  </p>
</div>
```

**3. Use Clear Item Text**

```jsx
// Good: Descriptive item names
const data = [
  { id: 1, name: 'Electronics - 25 items', parentId: null },
  { id: 2, name: 'Laptops (subcategory)', parentId: 1 },
];

// Less helpful: Vague names
const data = [
  { id: 1, name: 'Item 1', parentId: null },
  { id: 2, name: 'Item 1.1', parentId: 1 },
];
```

## Localization

Dropdown Tree supports multiple languages and cultures through localization.

### Localization Keys

Default text for English (`en` culture):

| Key | Default Text | Use Case |
|-----|--------------|----------|
| `noRecordsTemplate` | No records found | Displayed when no data matches filter |
| `actionFailureTemplate` | Request failed | Shown on data loading errors |
| `overflowCountTemplate` | +${count} more.. | Shows count of additional selected items |
| `totalCountTemplate` | ${count} selected | Shows total selected items count |

### Customize Localization Text

```jsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';

// Define custom locale
const customLocale = {
  'en': {
    'dropdowntree': {
      'noRecordsTemplate': 'No items found',
      'actionFailureTemplate': 'Connection error. Please try again.',
      'overflowCountTemplate': 'and ${count} more',
      'totalCountTemplate': '${count} items selected',
    }
  },
  'es': {
    'dropdowntree': {
      'noRecordsTemplate': 'No hay registros encontrados',
      'actionFailureTemplate': 'Error de conexión',
      'overflowCountTemplate': 'y ${count} más',
      'totalCountTemplate': '${count} elementos seleccionados',
    }
  }
};

// Register locale
// L10n.load(customLocale); // If using Syncfusion's localization system

<DropDownTreeComponent
  fields={{...}}
  noRecordsTemplate="No items found"
  actionFailureTemplate="Connection error"
/>
```

### Multi-Language Support

```jsx
const [language, setLanguage] = useState('en');

const translations = {
  en: {
    placeholder: 'Select item',
    selectAll: 'Select All',
    noRecords: 'No records found',
  },
  es: {
    placeholder: 'Seleccionar elemento',
    selectAll: 'Seleccionar todo',
    noRecords: 'No se encontraron registros',
  },
  fr: {
    placeholder: 'Sélectionner un élément',
    selectAll: 'Sélectionner tout',
    noRecords: 'Aucun enregistrement trouvé',
  }
};

const current = translations[language];

<DropDownTreeComponent
  fields={{...}}
  placeholder={current.placeholder}
  selectAllText={current.selectAll}
  noRecordsTemplate={current.noRecords}
  showCheckBox={true}
  showSelectAll={true}
/>
```

### Common Translations

**English (en):**
```
Select Item
Select All / Unselect All
No Records Found
Request Failed
Loading...
```

**Spanish (es):**
```
Seleccionar elemento
Seleccionar todo / Deseleccionar todo
No se encontraron registros
Error en la solicitud
Cargando...
```

**French (fr):**
```
Sélectionner un élément
Sélectionner tout / Désélectionner tout
Aucun enregistrement trouvé
Erreur de la demande
Chargement...
```

**German (de):**
```
Element auswählen
Alles auswählen / Alles abwählen
Keine Datensätze gefunden
Anfragefehler
Wird geladen...
```

**Portuguese (pt):**
```
Selecionar elemento
Selecionar tudo / Desselecionar tudo
Nenhum registro encontrado
Erro na solicitação
Carregando...
```

**Japanese (ja):**
```
アイテムを選択
すべて選択 / すべての選択を解除
レコードが見つかりません
リクエストエラー
読み込み中...
```

**Italian (it):**
```
Seleziona elemento
Seleziona tutto / Deseleziona tutto
Nessun record trovato
Errore della richiesta
Caricamento...
```

**Arabic (ar):**
```
اختر عنصراً
تحديد الكل / إلغاء تحديد الكل
لم يتم العثور على سجلات
فشل الطلب
جاري التحميل...
```

### Comprehensive Localization Setup

```jsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import { L10n } from '@syncfusion/ej2-base';
import React, { useState } from 'react';

// Define comprehensive locale for all languages
L10n.load({
  'es': {
    'dropdowntree': {
      'noRecordsTemplate': 'No se encontraron registros',
      'actionFailureTemplate': 'Error al cargar datos',
      'overflowCountTemplate': 'y ${count} más',
      'totalCountTemplate': '${count} elementos seleccionados'
    }
  },
  'fr': {
    'dropdowntree': {
      'noRecordsTemplate': 'Aucun enregistrement trouvé',
      'actionFailureTemplate': 'Erreur de chargement des données',
      'overflowCountTemplate': 'et ${count} plus',
      'totalCountTemplate': '${count} éléments sélectionnés'
    }
  },
  'de': {
    'dropdowntree': {
      'noRecordsTemplate': 'Keine Datensätze gefunden',
      'actionFailureTemplate': 'Fehler beim Laden von Daten',
      'overflowCountTemplate': 'und ${count} weitere',
      'totalCountTemplate': '${count} Elemente ausgewählt'
    }
  },
  'pt': {
    'dropdowntree': {
      'noRecordsTemplate': 'Nenhum registro encontrado',
      'actionFailureTemplate': 'Erro ao carregar dados',
      'overflowCountTemplate': 'e mais ${count}',
      'totalCountTemplate': '${count} elementos selecionados'
    }
  },
  'ja': {
    'dropdowntree': {
      'noRecordsTemplate': 'レコードが見つかりません',
      'actionFailureTemplate': 'データの読み込みに失敗しました',
      'overflowCountTemplate': '他に${count}件',
      'totalCountTemplate': '${count}件選択'
    }
  },
  'ar': {
    'dropdowntree': {
      'noRecordsTemplate': 'لم يتم العثور على سجلات',
      'actionFailureTemplate': 'خطأ في تحميل البيانات',
      'overflowCountTemplate': 'و ${count} أكثر',
      'totalCountTemplate': '${count} عناصر محددة'
    }
  }
});

function MultiLocaleDropdownTree() {
  const [locale, setLocale] = useState('en');

  const localeInfo = {
    'en': { label: 'English', flag: '🇺🇸' },
    'es': { label: 'Español', flag: '🇪🇸' },
    'fr': { label: 'Français', flag: '🇫🇷' },
    'de': { label: 'Deutsch', flag: '🇩🇪' },
    'pt': { label: 'Português', flag: '🇵🇹' },
    'ja': { label: '日本語', flag: '🇯🇵' },
    'ar': { label: 'العربية', flag: '🇸🇦' }
  };

  const demoData = [
    { id: 1, name: 'Electronics', parentId: null, expanded: true },
    { id: 2, name: 'Computers', parentId: 1 },
    { id: 3, name: 'Mobile Devices', parentId: 1 },
    { id: 4, name: 'Accessories', parentId: 1 },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h2>Multi-Language Dropdown Tree</h2>
      
      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        {Object.entries(localeInfo).map(([code, { label, flag }]) => (
          <button
            key={code}
            onClick={() => setLocale(code)}
            style={{
              padding: '8px 12px',
              backgroundColor: locale === code ? '#007bff' : '#f0f0f0',
              color: locale === code ? 'white' : 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: locale === code ? 'bold' : 'normal'
            }}
          >
            {flag} {label}
          </button>
        ))}
      </div>

      <DropDownTreeComponent
        id="dropdowntree"
        fields={{
          dataSource: demoData,
          value: 'id',
          text: 'name',
          parentValue: 'parentId'
        }}
        locale={locale}
        showCheckBox={true}
        showSelectAll={true}
        allowFiltering={true}
        placeholder="Select an item"
      />
    </div>
  );
}

export default MultiLocaleDropdownTree;
```

### Runtime Locale Switching

```jsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import { L10n, setCulture } from '@syncfusion/ej2-base';

// Pre-define locales
L10n.load({...localeDefinitions...});

function App() {
  const [culture, setCultureState] = useState('en');

  const handleCultureChange = (newCulture) => {
    setCultureState(newCulture);
    setCulture(newCulture); // Update global culture
  };

  return (
    <div>
      <select onChange={(e) => handleCultureChange(e.target.value)}>
        <option value="en">English</option>
        <option value="fr">Français</option>
        <option value="de">Deutsch</option>
      </select>

      <DropDownTreeComponent
        locale={culture}
        fields={{...}}
      />
    </div>
  );
}
```

## RTL Support

Full Right-to-Left (RTL) language support for Arabic, Hebrew, Urdu, and other RTL languages.

### Enable RTL

```jsx
import { enableRtl } from '@syncfusion/ej2-base';

// Enable RTL globally
enableRtl(true);

<DropDownTreeComponent
  fields={{...}}
/>
```

### HTML Level RTL

```html
<html dir="rtl" lang="ar">
  <body>
    <div id="root"></div>
  </body>
</html>
```

### Component-Level RTL

```jsx
<DropDownTreeComponent
  fields={{...}}
  enableRtl={true}
/>
```

### RTL Example - Arabic

```jsx
const arabicData = [
  { id: 1, name: 'الإلكترونيات', parentId: null, expanded: true },
  { id: 2, name: 'أجهزة الكمبيوتر', parentId: 1 },
  { id: 3, name: 'الهواتف الذكية', parentId: 1 },
];

function App() {
  return (
    <div dir="rtl" lang="ar">
      <DropDownTreeComponent
        fields={{
          dataSource: arabicData,
          value: 'id',
          text: 'name',
          parentValue: 'parentId',
        }}
        placeholder="اختر عنصرا"
        enableRtl={true}
      />
    </div>
  );
}
```

### Testing RTL

Verify that:
- Text flows right to left
- Dropdown arrow aligns correctly
- Checkboxes appear on right side
- Expand/collapse arrows point correctly
- Keyboard navigation works properly

## Complete Accessible Example

```jsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import { enableRtl } from '@syncfusion/ej2-base';
import '@syncfusion/ej2-dropdowns/styles/material.css';

function AccessibleDropdownTree() {
  const departmentData = [
    { id: 1, name: 'Engineering (25 people)', expanded: true },
    { id: 2, name: 'Frontend Team (10 people)', parentId: 1 },
    { id: 3, name: 'Backend Team (15 people)', parentId: 1 },
    { id: 4, name: 'Sales (12 people)' },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <form>
        <fieldset>
          <legend>Select Your Department</legend>
          
          <label htmlFor="deptSelect" id="deptLabel">
            Department Selection <span aria-label="required">*</span>
          </label>
          
          <DropDownTreeComponent
            id="deptSelect"
            ref={treeRef}
            fields={{
              dataSource: departmentData,
              value: 'id',
              text: 'name',
              parentValue: 'parentId',
            }}
            placeholder="Select your department"
            aria-labelledby="deptLabel"
            aria-describedby="deptHelp"
            showCheckBox={true}
            showSelectAll={true}
            treeSettings={{ autoCheck: true }}
          />
          
          <small id="deptHelp">
            Use arrow keys to navigate. Press Space to select. 
            Press Alt+Down to open, Escape to close.
          </small>
        </fieldset>
      </form>
    </div>
  );
}

export default AccessibleDropdownTree;
```
