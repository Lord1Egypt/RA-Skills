# Advanced Features

## Table of Contents
- [Virtual Scrolling](#virtual-scrolling)
- [Internationalization (i18n)](#internationalization-i18n)
- [RTL Support](#rtl-support)
- [Accessibility (WCAG)](#accessibility-wcag)
- [Disabled Items](#disabled-items)
- [Keyboard Navigation](#keyboard-navigation)

---

## Virtual Scrolling

### Enable Virtual Scrolling for Large Datasets

Virtual scrolling renders only visible items, dramatically improving performance with 10,000+ items.

> **Important:** `enableVirtualization` requires injecting the `VirtualScroll` module via `<Inject services={[VirtualScroll]} />` inside the component.

```tsx
import { ComboBoxComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  // 50,000 items
  const largeDataset = Array.from({ length: 50000 }, (_, i) => ({
    id: i + 1,
    name: `Item ${i + 1}`
  }));

  return (
    <ComboBoxComponent 
      id="large-combo"
      dataSource={largeDataset}
      fields={{ text: 'name', value: 'id' }}
      enableVirtualization={true}      // ← Enable virtual scrolling
      allowFiltering={true}
      popupHeight="300px"
      placeholder="Searching 50,000 items efficiently..."
    >
      <Inject services={[VirtualScroll]} />
    </ComboBoxComponent>
  );
}
```

**Benefits:**
- ✅ Handles 50,000+ items without lag
- ✅ Smooth scrolling with filtering
- ✅ Reduced memory usage
- ✅ Faster initial render

**When to use:**
- >5,000 items
- Large remote datasets
- Performance-critical applications

### Performance Comparison

| Scenario | Without Virtual Scroll | With Virtual Scroll |
|----------|----------------------|-------------------|
| 1,000 items | 50ms render | 45ms render |
| 10,000 items | 500ms render | 80ms render |
| 50,000 items | 3,000ms+ (lag) | 120ms render |

---

## Internationalization (i18n)

### Change Language/Locale

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { setDefaultCulture } from '@syncfusion/ej2-base';

// Set default culture before rendering
setDefaultCulture('es-ES');  // Spanish - Spain

export default function App() {
  return (
    <ComboBoxComponent 
      id="combo"
      dataSource={items}
      placeholder="Seleccionar..."    // Spanish placeholder
    />
  );
}
```

**Supported locales:**
- `en-US` - English (USA)
- `es-ES` - Spanish
- `fr-FR` - French
- `de-DE` - German
- `ar-AE` - Arabic
- `ja-JP` - Japanese
- `zh-CN` - Chinese (Simplified)
- And 20+ more...

### Custom Localization

Create custom locale messages:

```tsx
import { L10n } from '@syncfusion/ej2-base';

// Define custom translations
L10n.load({
  'es': {
    'combobox': {
      'noRecordsTemplate': 'Sin resultados encontrados',
      'actionFailureTemplate': 'Error al cargar datos'
    }
  },
  'fr': {
    'combobox': {
      'noRecordsTemplate': 'Aucun résultat trouvé',
      'actionFailureTemplate': 'Erreur de chargement des données'
    }
  }
});

<ComboBoxComponent 
  dataSource={items}
  locale="es"    // Use Spanish
/>
```

---

## RTL Support

### Enable Right-to-Left Layout

For Arabic, Hebrew, and other RTL languages:

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { enableRtl } from '@syncfusion/ej2-base';

// Enable RTL globally
enableRtl(true);

export default function App() {
  const arabicItems = ['عنصر 1', 'عنصر 2', 'عنصر 3'];

  return (
    <ComboBoxComponent 
      id="arabic-combo"
      dataSource={arabicItems}
      placeholder="اختر..."    // Arabic placeholder
    />
  );
}
```

### RTL-Specific Styling

```css
/* RTL Layout */
.e-combobox[dir="rtl"] .e-input {
  text-align: right;
  direction: rtl;
}

.e-combobox[dir="rtl"] .e-clear-icon {
  left: 10px;   /* Swap left/right */
  right: auto;
}

.e-combobox[dir="rtl"] .e-dropdown-icon {
  right: 10px;
  left: auto;
}
```

---

## Accessibility (WCAG)

### WCAG 2.1 Compliance

ComboBox is built with accessibility in mind:

```tsx
<ComboBoxComponent 
  id="accessible-combo"
  dataSource={items}
  fields={{ text: 'name', value: 'id' }}
  placeholder="Choose an option"
  aria-label="Select an item from the list"
  aria-describedby="combo-help"
/>

<small id="combo-help">Use arrow keys to navigate, Enter to select</small>
```

### Keyboard Navigation

| Key | Action |
|-----|--------|
| `↓` | Move to next item |
| `↑` | Move to previous item |
| `Home` | Go to first item |
| `End` | Go to last item |
| `Enter` | Select highlighted item |
| `Escape` | Close dropdown |
| `Tab` | Move to next field |
| `Shift+Tab` | Move to previous field |

### Screen Reader Support

ComboBox announces changes to screen readers:

```tsx
export default function App() {
  return (
    <div>
      <label htmlFor="items-combo" className="sr-only">
        Select an item
      </label>
      <ComboBoxComponent 
        id="items-combo"
        dataSource={items}
        role="combobox"
        aria-expanded={isOpen}
        aria-owns="items-list"
      />
    </div>
  );
}
```

---

## Disabled Items

### Disable Specific Items

Some items should not be selectable:

```tsx
export default function App() {
  const items = [
    { id: 1, name: 'Available', disabled: false },
    { id: 2, name: 'Unavailable', disabled: true },
    { id: 3, name: 'Available', disabled: false }
  ];

  const itemTemplate = (props) => {
    return (
      <div className={props.disabled ? 'item-disabled' : 'item'}>
        {props.name}
      </div>
    );
  };

  const filtering = (e) => {
    // Exclude disabled items from search results
    const searchText = e.text.toLowerCase();
    const filtered = items.filter(item =>
      !item.disabled && item.name.toLowerCase().includes(searchText)
    );
    e.updateData(filtered);
  };

  return (
    <ComboBoxComponent 
      dataSource={items}
      fields={{ text: 'name', value: 'id' }}
      allowFiltering={true}
      itemTemplate={itemTemplate}
      filtering={filtering}
    />
  );
}
```

**CSS:**
```css
.item-disabled {
  color: #ccc;
  opacity: 0.6;
  pointer-events: none;
}
```

### Disable Entire Component

Prevent interaction:

```tsx
<ComboBoxComponent 
  dataSource={items}
  enabled={false}              // Disabled state
  placeholder="This is disabled"
/>
```

---

## Keyboard Navigation

### Responding to Selection via Keyboard

Use the `select` and `change` events to respond when a user picks an item through keyboard navigation:

```tsx
export default function App() {
  const handleSelect = (e) => {
    // Fires when item is highlighted via keyboard and confirmed
    console.log('Item selected:', e.itemData);
  };

  const handleChange = (e) => {
    // Fires when value changes (keyboard or mouse)
    console.log('Value changed to:', e.value);
  };

  return (
    <ComboBoxComponent 
      dataSource={items}
      select={handleSelect}
      change={handleChange}
    />
  );
}
```

---

## Common Advanced Patterns

### Pattern 1: Conditional Disabling Based on Selection

```tsx
export default function App() {
  const [selected, setSelected] = useState('');

  const items = [
    { id: 1, name: 'Option A' },
    { id: 2, name: 'Option B' }
  ];

  const handleChange = (e) => {
    setSelected(e.value);
  };

  return (
    <div>
      <ComboBoxComponent 
        dataSource={items}
        change={handleChange}
        placeholder="First selection"
      />
      
      <button disabled={!selected}>
        Submit {selected && `(${selected})`}
      </button>
    </div>
  );
}
```

### Pattern 2: Large Dataset with Filtering & Virtual Scrolling

```tsx
import { ComboBoxComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const largeDataset = Array.from({ length: 100000 }, (_, i) => ({
    id: i + 1,
    name: `Item ${i + 1}`,
    category: `Category ${(i % 10) + 1}`
  }));

  return (
    <ComboBoxComponent 
      id="mega-combo"
      dataSource={largeDataset}
      fields={{ text: 'name', value: 'id', groupBy: 'category' }}
      enableVirtualization={true}      // Critical for performance
      allowFiltering={true}
      filterType="Contains"
      popupHeight="400px"
      placeholder="Search 100,000 items..."
    >
      <Inject services={[VirtualScroll]} />
    </ComboBoxComponent>
  );
}
```

### Pattern 3: Accessibility-First Implementation

```tsx
export default function App() {
  const [selectedValue, setSelectedValue] = useState('');

  return (
    <div>
      <label htmlFor="accessible-combo">
        Select a priority level
        <abbr title="required">*</abbr>
      </label>
      
      <ComboBoxComponent 
        id="accessible-combo"
        dataSource={['Low', 'Medium', 'High']}
        value={selectedValue}
        change={(e) => setSelectedValue(e.value)}
        placeholder="Choose priority..."
        aria-required={true}
        aria-label="Select priority level for task"
        aria-describedby="combo-help"
      />
      
      <small id="combo-help" className="help-text">
        Use arrow keys to navigate options, press Enter to select
      </small>
    </div>
  );
}
```

---

## Advanced Features Checklist

- [ ] Virtual scrolling enabled for large datasets (>5000 items) — `enableVirtualization={true}` with `<Inject services={[VirtualScroll]} />`
- [ ] Locale/culture set appropriately for audience
- [ ] RTL layout tested in browser
- [ ] Keyboard navigation verified (arrow keys, Enter, Escape)
- [ ] Screen reader tested with NVDA or JAWS
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Focus indicators visible and clear
- [ ] Disabled state handled properly
- [ ] Performance tested with actual data volume

---

## Next Steps

- **Styling the component?** → See [styling-and-theming.md](styling-and-theming.md)
- **Having performance issues?** → Check virtual scrolling section above
- **Troubleshooting?** → Visit [troubleshooting.md](troubleshooting.md)
- **Need localization details?** → See [Syncfusion i18n docs](https://ej2.syncfusion.com/react/documentation/common/localization)
