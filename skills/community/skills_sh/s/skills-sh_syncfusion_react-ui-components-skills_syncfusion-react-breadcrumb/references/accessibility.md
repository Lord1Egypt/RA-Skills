# Accessibility

## Table of Contents
- [Compliance Standards](#compliance-standards)
- [ARIA Attributes](#aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [Best Practices](#best-practices)

## Compliance Standards

The Syncfusion React Breadcrumb component meets all major accessibility standards and guidelines:

| Accessibility Standard | Support | Details |
|---|---|---|
| WCAG 2.2 | ✓ Full Support | Web Content Accessibility Guidelines Level AA and AAA compliance |
| Section 508 | ✓ Full Support | U.S. federal accessibility requirements |
| ADA | ✓ Full Support | Americans with Disabilities Act compliance |
| Right-to-Left (RTL) | ✓ Full Support | Supports RTL languages like Arabic and Hebrew |
| Screen Reader | ✓ Full Support | Compatible with JAWS, NVDA, VoiceOver |
| Keyboard Navigation | ✓ Full Support | Full keyboard access to all features |
| Color Contrast | ✓ Full Support | Meets WCAG color contrast requirements |
| Mobile Support | ✓ Full Support | Touch-accessible on mobile devices |

**Third-Party Validation:**
- Accessibility Checker - Validated ✓
- Axe-core - Validated ✓

## ARIA Attributes

The Breadcrumb component automatically applies proper ARIA attributes for accessibility:

### aria-label

The `aria-label` attribute indicates the breadcrumb item text for screen readers:

```html
<a class="e-breadcrumb-item" aria-label="Home">
  <span class="e-icons e-home"></span>
</a>
```

**Automatically Applied:** No additional configuration required.

### aria-disabled

The `aria-disabled` attribute indicates when a breadcrumb item is disabled:

```html
<a class="e-breadcrumb-item" aria-disabled="true">
  <span>Current Page</span>
</a>
```

**When Applied:** 
- Last breadcrumb item (active) when `enableActiveItemNavigation={false}`
- Disabled items

## Keyboard Navigation

The Breadcrumb component supports full keyboard navigation for users who don't use a mouse:

| Keyboard Key | Action |
|---|---|
| <kbd>Tab</kbd> | Navigate to the next breadcrumb item and also navigate within dropdown menus in overflow mode |
| <kbd>Shift + Tab</kbd> | Navigate to the previous breadcrumb item and also navigate within dropdown menus in overflow mode |
| <kbd>Enter</kbd> | Activate the breadcrumb item (navigate to URL) in normal mode |
| <kbd>Enter</kbd> on overflow menu | Open the menu dropdown or expand collapsed items |

### Example: Keyboard Navigation Workflow

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function AccessibleBreadcrumb() {
  return (
    <BreadcrumbComponent enableNavigation={true}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" />
        <BreadcrumbItemDirective text="Products" url="/products" />
        <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**User Flow:**
1. User presses <kbd>Tab</kbd> to focus on breadcrumb
2. User presses <kbd>Tab</kbd> again to move between items
3. User presses <kbd>Enter</kbd> to navigate to item URL
4. Screen reader announces each item's text via `aria-label`

## Screen Reader Support

The Breadcrumb component is fully compatible with screen readers including:
- **JAWS** (Job Access With Speech)
- **NVDA** (NonVisual Desktop Access)
- **VoiceOver** (Apple)
- **Narrator** (Windows)

### How Screen Readers Interact

1. **Component Discovery:** Screen reader recognizes navigation component
2. **Item Announcement:** Each breadcrumb item text is announced via `aria-label`
3. **State Indication:** Current/active item status is communicated
4. **Navigation:** Users navigate items using Tab key
5. **Action:** Users select items using Enter key

### Example: Semantic HTML Structure

The component generates accessible HTML:

```html
<nav class="e-breadcrumb" role="navigation" aria-label="Breadcrumb">
  <ol class="e-breadcrumb-list">
    <li class="e-breadcrumb-item">
      <a href="/" aria-label="Home">Home</a>
    </li>
    <li class="e-breadcrumb-item">
      <a href="/products" aria-label="Products">Products</a>
    </li>
    <li class="e-breadcrumb-item" aria-current="page">
      <span aria-label="Electronics">Electronics</span>
    </li>
  </ol>
</nav>
```

## Best Practices

### 1. Always Provide Text for Icons

When using icons-only breadcrumbs, ensure screen readers can identify items:

```tsx
// ❌ Poor: Icon-only, no text context
<BreadcrumbItemDirective iconCss="e-icons e-home" />

// ✓ Good: Icon with descriptive text
<BreadcrumbItemDirective iconCss="e-icons e-home" text="Home" />

// ✓ Also Good: Icon with aria-label via beforeItemRender
function beforeItemRenderHandler(args: BreadcrumbBeforeItemRenderEventArgs): void {
  if (args.element.children[0]) {
    args.element.children[0].title = "Home";
    args.element.children[0].setAttribute("aria-label", "Home");
  }
}
```

### 2. Use Meaningful URL Patterns

Breadcrumb URLs should match the site structure:

```tsx
// ✓ Good: URLs match navigation hierarchy
<BreadcrumbItemDirective text="Products" url="/products" />
<BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
<BreadcrumbItemDirective text="Phones" url="/products/electronics/phones" />

// ❌ Poor: URLs don't reflect structure
<BreadcrumbItemDirective text="Products" url="/p" />
<BreadcrumbItemDirective text="Electronics" url="/e" />
```

### 3. Make Navigation Optional

Allow users to disable navigation if needed:

```tsx
// ✓ Good: enableNavigation prop allows control
<BreadcrumbComponent enableNavigation={true}>
  {/* items */}
</BreadcrumbComponent>
```

### 4. Ensure Sufficient Color Contrast

Use colors that meet WCAG AAA standards (at least 7:1 contrast ratio):

```css
/* ✓ Good: High contrast */
.e-breadcrumb .e-breadcrumb-item a {
  color: #0078d4;  /* Dark blue on light background */
}

/* ❌ Poor: Insufficient contrast */
.e-breadcrumb .e-breadcrumb-item a {
  color: #b3d9ff;  /* Light blue on light background */
}
```

### 5. Support RTL Languages

The component automatically supports RTL:

```tsx
<BreadcrumbComponent enableNavigation={false} dir="rtl">
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="الصفحة الرئيسية" url="/" />
    <BreadcrumbItemDirective text="المنتجات" url="/products" />
    <BreadcrumbItemDirective text="الإلكترونيات" url="/products/electronics" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

### 6. Use Semantic Separators

Avoid ambiguous separators that screen readers might not announce clearly:

```tsx
// ✓ Good: Clear icon separator
function separatorTemplate(): JSX.Element {
  return (
    <span className="e-icons e-arrow" aria-hidden="true"></span>
  );
}

// Use aria-hidden for decorative icons
<BreadcrumbComponent separatorTemplate={separatorTemplate}>
  {/* items */}
</BreadcrumbComponent>
```

### 7. Implement Overflow Accessibly

For overflow modes, ensure hidden items remain accessible:

```tsx
<BreadcrumbComponent 
  maxItems={3} 
  overflowMode='Menu' 
  enableNavigation={false}
>
  {/* All items remain accessible through menu */}
</BreadcrumbComponent>
```

### 8. Test with Real Assistive Technologies

- Test keyboard navigation with Tab, Shift+Tab, Enter keys
- Test with screen readers (NVDA on Windows, VoiceOver on Mac)
- Verify announcements are clear and logical
- Test with browser zoom at 200%
- Test on mobile with touch navigation

## Accessibility Testing Tools

Use these tools to validate accessibility:

```bash
# Install accessibility checker
npm install accessibility-checker

# Install axe-core
npm install axe-core

# Install WAVE extension browser addon
# Available for Chrome, Firefox, Edge
```

## Example: Fully Accessible Breadcrumb

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbBeforeItemRenderEventArgs } from '@syncfusion/ej2-navigations';

export default function AccessibleBreadcrumb() {
  function beforeItemRenderHandler(args: BreadcrumbBeforeItemRenderEventArgs): void {
    // Ensure items have proper ARIA labels
    if (args.element.children[0]) {
      args.element.children[0].setAttribute('role', 'link');
    }
  }

  return (
    <nav aria-label="Breadcrumb">
      <BreadcrumbComponent 
        enableNavigation={true}
        beforeItemRender={beforeItemRenderHandler}
      >
        <BreadcrumbItemsDirective>
          <BreadcrumbItemDirective iconCss="e-icons e-home" text="Home" url="/" />
          <BreadcrumbItemDirective text="Products" url="/products" />
          <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
          <BreadcrumbItemDirective text="Smartphones" url="/products/electronics/smartphones" />
        </BreadcrumbItemsDirective>
      </BreadcrumbComponent>
    </nav>
  );
}
```

This implementation ensures:
- Proper semantic HTML with `<nav>` element
- Clear navigation context with `aria-label`
- Icon with descriptive text
- Full keyboard navigation support
- Screen reader compatibility
- WCAG 2.2 compliance
