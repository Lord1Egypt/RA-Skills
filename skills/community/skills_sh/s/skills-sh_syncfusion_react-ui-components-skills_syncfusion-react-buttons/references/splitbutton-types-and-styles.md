# SplitButton Types and Styles

## Table of Contents
- [Button Styles](#button-styles)
- [Button Types](#button-types)
- [Icon Positioning](#icon-positioning)
- [Size Variations](#size-variations)
- [Styled Anchor Elements](#styled-anchor-elements)
- [RTL Support](#rtl-support)
- [Best Practices](#best-practices)

## Button Styles

Apply different visual styles to SplitButtons using the `cssClass` property.

### Primary Style

Used for primary/main actions that need emphasis.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function PrimaryButton() {
  const items = [
    { text: 'Save' },
    { text: 'Save As' },
    { text: 'Save All' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
    >
      Save
    </SplitButtonComponent>
  );
}

export default PrimaryButton;
```

**Use cases:** Primary actions, main workflows, confirm dialogs

### Success Style

Green color, used for positive/successful actions.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function SuccessButton() {
  const items = [
    { text: 'Deploy Live' },
    { text: 'Deploy Staging' },
    { text: 'Deploy Preview' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-success"
      iconCss="e-icons e-deploy"
    >
      Deploy
    </SplitButtonComponent>
  );
}

export default SuccessButton;
```

**Use cases:** Approve, confirm, deploy, publish actions

### Info Style

Cyan/blue color for informational or secondary actions.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function InfoButton() {
  const items = [
    { text: 'View Details' },
    { text: 'View History' },
    { text: 'View Related' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-info"
      iconCss="e-icons e-info"
    >
      More
    </SplitButtonComponent>
  );
}

export default InfoButton;
```

**Use cases:** Information, help, additional options

### Warning Style

Orange color for actions requiring caution.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function WarningButton() {
  const items = [
    { text: 'Archive' },
    { text: 'Move to Archive' },
    { text: 'Archive All' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-warning"
      iconCss="e-icons e-archive"
    >
      Archive
    </SplitButtonComponent>
  );
}

export default WarningButton;
```

**Use cases:** Warning, caution, archive, suspend operations

### Danger Style

Red color for destructive actions.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function DangerButton() {
  const items = [
    { text: 'Delete' },
    { text: 'Delete Permanently' },
    { text: 'Delete All' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-danger"
      iconCss="e-icons e-delete"
    >
      Delete
    </SplitButtonComponent>
  );
}

export default DangerButton;
```

**Use cases:** Delete, remove, clear, dangerous actions

### Link Style

Appears as a text link, used for less prominent actions.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function LinkButton() {
  const items = [
    { text: 'View Profile' },
    { text: 'View Settings' },
    { text: 'View History' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-link"
    >
      View
    </SplitButtonComponent>
  );
}

export default LinkButton;
```

**Use cases:** Less important actions, inline actions, secondary options

### Style Color Reference

| Style | Color | Use Case |
|-------|-------|----------|
| (default) | Gray | Secondary actions, neutral |
| `e-primary` | Blue | Main actions, emphasis |
| `e-success` | Green | Approve, confirm, positive |
| `e-info` | Cyan | Information, help, details |
| `e-warning` | Orange | Warning, caution, critical |
| `e-danger` | Red | Delete, remove, destructive |
| `e-link` | Blue link | Less prominent, inline |

## Button Types

Control button appearance with type classes.

### Flat Button

Minimal styling, most subtle appearance.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function FlatButtons() {
  const items = [{ text: 'Save' }, { text: 'Save As' }];

  return (
    <div>
      {/* Flat primary */}
      <SplitButtonComponent
        items={items}
        cssClass="e-flat e-primary"
      >
        Save
      </SplitButtonComponent>

      {/* Flat danger */}
      <SplitButtonComponent
        items={items}
        cssClass="e-flat e-danger"
        style={{ marginLeft: '10px' }}
      >
        Delete
      </SplitButtonComponent>
    </div>
  );
}

export default FlatButtons;
```

**Characteristics:**
- Minimal styling
- No background color (inherits theme)
- Color applied to text and hover effect
- Best for toolbar actions

### Outline Button

Button with border, no fill.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function OutlineButtons() {
  const items = [{ text: 'Save' }, { text: 'Save As' }];

  return (
    <div>
      {/* Outline primary */}
      <SplitButtonComponent
        items={items}
        cssClass="e-outline e-primary"
      >
        Save
      </SplitButtonComponent>

      {/* Outline warning */}
      <SplitButtonComponent
        items={items}
        cssClass="e-outline e-warning"
        style={{ marginLeft: '10px' }}
      >
        Archive
      </SplitButtonComponent>
    </div>
  );
}

export default OutlineButtons;
```

**Characteristics:**
- Bordered appearance
- No background fill
- Good contrast and visibility
- Best for secondary actions

### Round Button

Fully rounded appearance.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function RoundButtons() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' }
  ];

  return (
    <div>
      {/* Round with icons */}
      <SplitButtonComponent
        items={items}
        cssClass="e-round e-primary"
        iconCss="e-icons e-save"
      >
        Save
      </SplitButtonComponent>

      {/* Icon-only round button */}
      <SplitButtonComponent
        items={items}
        cssClass="e-round e-primary"
        iconCss="e-icons e-settings"
        style={{ marginLeft: '10px' }}
        title="Settings"
      />
    </div>
  );
}

export default RoundButtons;
```

**Characteristics:**
- Fully rounded corners
- Often used with icons
- Good for icon-only buttons
- Modern appearance

### Button Type Combinations

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function CombinedTypes() {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
      {/* Flat + Primary */}
      <SplitButtonComponent items={items} cssClass="e-flat e-primary">
        Flat Primary
      </SplitButtonComponent>

      {/* Outline + Success */}
      <SplitButtonComponent items={items} cssClass="e-outline e-success">
        Outline Success
      </SplitButtonComponent>

      {/* Round + Danger */}
      <SplitButtonComponent items={items} cssClass="e-round e-danger">
        Round Danger
      </SplitButtonComponent>

      {/* Round + Flat + Info */}
      <SplitButtonComponent items={items} cssClass="e-round e-flat e-info">
        Round Flat Info
      </SplitButtonComponent>
    </div>
  );
}

export default CombinedTypes;
```

### Type Reference

| Type | Class | Appearance |
|------|-------|-----------|
| Default | (none) | Filled with color |
| Flat | `e-flat` | Minimal styling, text color |
| Outline | `e-outline` | Bordered, no fill |
| Round | `e-round` | Fully rounded corners |

## Icon Positioning

Control where icons appear relative to text.

### Left Position (Default)

Icon appears to the left of text.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function LeftIconButton() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      iconCss="e-icons e-save"
      iconPosition="Left"
      cssClass="e-primary"
    >
      Save
    </SplitButtonComponent>
  );
}

export default LeftIconButton;
```

**Best for:** Most UI designs, left-to-right languages

### Right Position

Icon appears to the right of text.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function RightIconButton() {
  const items = [
    { text: 'Next', iconCss: 'e-icons e-chevron-right' },
    { text: 'Skip', iconCss: 'e-icons e-skip-right' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      iconCss="e-icons e-chevron-right"
      iconPosition="Right"
      cssClass="e-primary"
    >
      Next
    </SplitButtonComponent>
  );
}

export default RightIconButton;
```

**Best for:** Navigation forward, chevron indicators

### Top Position

Icon appears above text, stacked vertically.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function TopIconButton() {
  const items = [
    { text: 'Download', iconCss: 'e-icons e-download' },
    { text: 'Export', iconCss: 'e-icons e-export' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      iconCss="e-icons e-download"
      iconPosition="Top"
      cssClass="e-primary"
    >
      Download
    </SplitButtonComponent>
  );
}

export default TopIconButton;
```

**Best for:** Toolbar buttons with text

### Bottom Position

Icon appears below text, stacked vertically.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function BottomIconButton() {
  const items = [
    { text: 'Settings', iconCss: 'e-icons e-settings' },
    { text: 'Config', iconCss: 'e-icons e-config' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      iconCss="e-icons e-settings"
      iconPosition="Bottom"
      cssClass="e-primary"
    >
      Settings
    </SplitButtonComponent>
  );
}

export default BottomIconButton;
```

**Best for:** Specialized UI layouts

## Size Variations

Control button and icon size with CSS classes.

### Small Button

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function SmallButton() {
  const items = [{ text: 'Save' }, { text: 'Save As' }];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-small e-primary"
      iconCss="e-icons e-save"
    >
      Save
    </SplitButtonComponent>
  );
}

export default SmallButton;
```

**Use cases:** Compact toolbars, dense UI, mobile

### Normal Button (Default)

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function NormalButton() {
  const items = [{ text: 'Save' }, { text: 'Save As' }];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
      iconCss="e-icons e-save"
    >
      Save
    </SplitButtonComponent>
  );
}

export default NormalButton;
```

**Use cases:** Default button sizing, dialogs

### Large Button

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function LargeButton() {
  const items = [{ text: 'Save' }, { text: 'Save As' }];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-large e-primary"
      iconCss="e-icons e-save"
    >
      Save
    </SplitButtonComponent>
  );
}

export default LargeButton;
```

**Use cases:** Prominent actions, mobile buttons, accessibility

## Styled Anchor Elements

Apply Syncfusion SplitButton classes to native HTML anchor elements.

### Anchor as Primary Button

```tsx
function StyledAnchors() {
  return (
    <div>
      {/* Anchor as primary button */}
      <a 
        href="/dashboard" 
        className="e-btn e-primary"
      >
        Dashboard
      </a>

      {/* Anchor with icon */}
      <a 
        href="/settings" 
        className="e-btn e-primary e-outline"
        style={{ marginLeft: '10px' }}
      >
        Settings
      </a>

      {/* Anchor as link button */}
      <a 
        href="https://example.com" 
        className="e-btn e-link"
        target="_blank"
        rel="noopener noreferrer"
        style={{ marginLeft: '10px' }}
      >
        External Link
      </a>
    </div>
  );
}

export default StyledAnchors;
```

### Anchor with Dropdown

```tsx
function AnchorWithDropdown() {
  return (
    <div style={{ padding: '20px' }}>
      <a 
        href="#" 
        className="e-btn e-primary"
        onClick={(e) => e.preventDefault()}
      >
        Download
      </a>
      <div className="e-dropdown-menu" style={{ display: 'none' }}>
        <ul>
          <li><a href="#">PDF</a></li>
          <li><a href="#">Excel</a></li>
          <li><a href="#">CSV</a></li>
        </ul>
      </div>
    </div>
  );
}

export default AnchorWithDropdown;
```

## RTL Support

Enable right-to-left mode for Arabic, Hebrew, and other RTL languages.

### RTL Button

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function RTLButton() {
  const items = [
    { text: 'حفظ', iconCss: 'e-icons e-save' },
    { text: 'حفظ باسم', iconCss: 'e-icons e-save-as' },
    { text: 'حفظ الكل', iconCss: 'e-icons e-save-all' }
  ];

  return (
    <div dir="rtl" style={{ padding: '20px' }}>
      <SplitButtonComponent
        items={items}
        enableRtl={true}
        cssClass="e-primary"
        iconCss="e-icons e-save"
      >
        حفظ
      </SplitButtonComponent>
    </div>
  );
}

export default RTLButton;
```

### RTL with Icon Position

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function RTLIconPositions() {
  const items = [
    { text: 'السابق' },
    { text: 'التالي' }
  ];

  return (
    <div dir="rtl" style={{ padding: '20px' }}>
      {/* Icon on left in RTL mode (appears left) */}
      <SplitButtonComponent
        items={items}
        enableRtl={true}
        iconCss="e-icons e-chevron-left"
        iconPosition="Left"
        cssClass="e-primary"
      >
        السابق
      </SplitButtonComponent>

      {/* Icon on right in RTL mode (appears right) */}
      <SplitButtonComponent
        items={items}
        enableRtl={true}
        iconCss="e-icons e-chevron-right"
        iconPosition="Right"
        cssClass="e-primary"
        style={{ marginTop: '10px' }}
      >
        التالي
      </SplitButtonComponent>
    </div>
  );
}

export default RTLIconPositions;
```

### Global RTL Setup

```tsx
import React from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { enableRtl } from '@syncfusion/ej2-base';

// Enable RTL globally for entire app
enableRtl(true);

function App() {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <div dir="rtl">
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
      >
        إجراء
      </SplitButtonComponent>
    </div>
  );
}

export default App;
```

## Best Practices

### Style Guidelines

1. **Use consistent styling** - Pick a style scheme and use it consistently
2. **Emphasize important actions** - Use primary/success for critical actions
3. **Warn about destructive actions** - Use danger style for delete/remove
4. **Group similar styles** - Keep related buttons with same style
5. **Consider accessibility** - Ensure sufficient color contrast

### Color Contrast Example

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function AccessibleColors() {
  const items = [{ text: 'Option' }];

  return (
    <div style={{ padding: '20px' }}>
      {/* Good contrast - accessible */}
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
      >
        Primary
      </SplitButtonComponent>

      {/* High contrast - most accessible */}
      <SplitButtonComponent
        items={items}
        cssClass="e-primary e-outline"
        style={{ marginLeft: '10px' }}
      >
        Outline Primary
      </SplitButtonComponent>
    </div>
  );
}

export default AccessibleColors;
```

### Icon Selection Best Practices

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function IconBestPractices() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Delete', iconCss: 'e-icons e-delete' }
  ];

  return (
    <div style={{ padding: '20px' }}>
      {/* ✓ Meaningful icon for context */}
      <SplitButtonComponent
        items={items}
        iconCss="e-icons e-save"
        cssClass="e-primary"
      >
        Save
      </SplitButtonComponent>

      {/* ✓ Consistent icon usage */}
      <SplitButtonComponent
        items={items}
        iconCss="e-icons e-delete"
        cssClass="e-danger"
        style={{ marginLeft: '10px' }}
      >
        Delete
      </SplitButtonComponent>
    </div>
  );
}

export default IconBestPractices;
```

## Next Steps

- **Features** → Read [splitbutton-features.md](splitbutton-features.md) for event handling and advanced features
- **API Reference** → Read [api-reference.md](api-reference.md) for complete property documentation
- **Customization** → Read [customization.md](customization.md) for advanced styling
