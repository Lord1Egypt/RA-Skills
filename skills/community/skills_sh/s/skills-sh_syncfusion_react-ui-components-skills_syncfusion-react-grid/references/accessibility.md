# Accessibility (WCAG 2.2 & Section 508) in React Grid

## Table of Contents
- [Overview](#overview)
- [Keyboard Navigation](#keyboard-navigation)
- [WCAG 2.2 Compliance](#wcag-22-compliance)
- [WAI-ARIA Implementation](#wai-aria-implementation)
- [Screen Reader Support](#screen-reader-support)
- [Color Contrast](#color-contrast)
- [Focus Management](#focus-management)
- [Accessibility Testing](#accessibility-testing)

## Overview

Syncfusion React Grid is built with accessibility as a core principle, supporting:
- **WCAG 2.2** (Web Content Accessibility Guidelines Level AA)
- **Section 508** (U.S. accessibility standards)
- **WAI-ARIA 1.2** (Web Accessibility Initiative - Accessible Rich Internet Applications)
- **Keyboard-only navigation**
- **Screen reader compatibility**

---

## Keyboard Navigation

### Grid Navigation Keys

| Key | Action |
|-----|--------|
| **Tab** | Move to next cell/control |
| **Shift + Tab** | Move to previous cell/control |
| **Arrow Keys** | Navigate within rows/columns |
| **Ctrl + Home** | Go to first cell |
| **Ctrl + End** | Go to last cell |
| **Page Up** | Previous page (paging enabled) |
| **Page Down** | Next page (paging enabled) |
| **Space** | Select row/check checkbox |
| **Enter** | Edit cell / Confirm action |
| **Escape** | Cancel edit / Close dialog |
| **Ctrl + A** | Select all |
| **Ctrl + C** | Copy (with clipboard enabled) |
| **Ctrl + X** | Cut (with clipboard enabled) |
| **Ctrl + V** | Paste (with clipboard enabled) |

### Enable Keyboard Navigation

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={data}
  allowKeyboard={true}  // Enable keyboard navigation (default: true)
  allowPaging={true}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
  </ColumnsDirective>
  <Inject services={[Page]} />
</GridComponent>
```

### Keyboard Event Handling

```tsx
const gridRef = useRef(null);

const handleKeyDown = (event) => {
  if (event.key === 'F2') {
    // Custom action on F2
    const selectedRows = gridRef.current.getSelectedRows();
    if (selectedRows.length > 0) {
      gridRef.current.startEdit(selectedRows[0]);
    }
  }
};

return (
  <div onKeyDown={handleKeyDown}>
    <GridComponent ref={gridRef} dataSource={data}>
      {/* columns */}
    </GridComponent>
  </div>
);
```

---

## WCAG 2.2 Compliance

### Perceivable

Information must be presentable to users:

```tsx
// ✅ Provide text alternatives for images
<ColumnDirective
  field='Photo'
  headerText='Employee Photo'
  template={(props) => (
    <img
      src={props.Photo}
      alt={`Photo of ${props.FirstName} ${props.LastName}`}
      style={{ width: '32px', height: '32px' }}
    />
  )}
/>

// ✅ Use semantic HTML
<GridComponent
  dataSource={data}
  ariaLabel='Employee data grid'
>
  {/* columns */}
</GridComponent>

// ✅ Sufficient contrast ratios (4.5:1 for normal text)
<div style={{ color: '#000000', backgroundColor: '#FFFFFF' }}>
  High contrast text
</div>
```

### Operable

Users must be able to navigate and interact:

```tsx
// ✅ Keyboard accessible
<GridComponent
  dataSource={data}
  allowKeyboard={true}
  allowSelection={true}
>
  {/* columns */}
</GridComponent>

// ✅ Provide skip links
function App() {
  return (
    <>
      <a href='#main-grid' className='skip-link'>Skip to grid</a>
      <GridComponent id='main-grid' dataSource={data}>
        {/* columns */}
      </GridComponent>
    </>
  );
}
```

### Understandable

Content must be clear and predictable:

```tsx
// ✅ Use clear labels
<ColumnDirective
  field='OrderDate'
  headerText='Order Date'
  type='date'
  format='MM/dd/yyyy'
/>

// ✅ Predictable behavior
const handleActionBegin = (args) => {
  if (args.requestType === 'save') {
    console.log('Data saved');  // Confirm action
  }
};

<GridComponent actionBegin={handleActionBegin}>
  {/* columns */}
</GridComponent>

// ✅ Clear instructions
<div>
  <label htmlFor='grid-filter'>Filter by customer:</label>
  <GridComponent
    id='grid-filter'
    dataSource={data}
    allowFiltering={true}
  >
    {/* columns */}
  </GridComponent>
</div>
```

---

## WAI-ARIA Implementation

### ARIA Attributes

Syncfusion Grid automatically adds ARIA attributes:

```tsx
// Automatically added by Grid:
// role='grid'
// role='row' for each row
// role='gridcell' for each cell
// role='button' for headers (clickable)
// aria-selected='true/false'
// aria-sort='ascending/descending/none'
// aria-expanded='true/false' (for detail rows)
// aria-disabled='true/false'
// aria-readonly='true/false'

<GridComponent
  dataSource={data}
  allowSorting={true}
  detailTemplate={detailTemplate}
>
  {/* columns */}
</GridComponent>
```

### Custom ARIA Labels

```tsx
<GridComponent
  dataSource={data}
  ariaLabel='Employee database'
  rowTemplate={(props) => (
    <tr aria-label={`Employee ${props.FirstName} ${props.LastName}`}>
      <td>{props.FirstName}</td>
      <td>{props.LastName}</td>
    </tr>
  )}
>
  {/* columns */}
</GridComponent>
```

### ARIA Live Regions

Announce dynamic content changes:

```tsx
import React, { useRef, useState } from 'react';

function GridWithAnnouncements() {
  const gridRef = useRef(null);
  const [announcement, setAnnouncement] = useState('');

  const handleRowAction = (action) => {
    setAnnouncement(`${action} performed`);
    
    // Clear announcement after screen reader reads it
    setTimeout(() => setAnnouncement(''), 1000);
  };

  return (
    <div>
      <div
        role='status'
        aria-live='polite'
        aria-atomic='true'
        className='sr-only'
      >
        {announcement}
      </div>

      <GridComponent
        ref={gridRef}
        dataSource={data}
        recordDoubleClick={() => handleRowAction('Row opened')}
      >
        {/* columns */}
      </GridComponent>
    </div>
  );
}
```

---

## Screen Reader Support

### Test with NVDA/JAWS

1. Install NVDA (free) or JAWS
2. Enable screen reader
3. Tab through grid
4. Verify announcements

### Announce Selection

```tsx
<GridComponent
  dataSource={data}
  selectionSettings={{ type: 'Multiple', mode: 'Row' }}
  rowSelected={(args) => {
    const announcement = `Row ${args.data.OrderID} selected`;
    announceToScreenReader(announcement);
  }}
>
  {/* columns */}
</GridComponent>

const announceToScreenReader = (message) => {
  const announcement = document.createElement('div');
  announcement.setAttribute('role', 'status');
  announcement.setAttribute('aria-live', 'polite');
  announcement.className = 'sr-only';
  announcement.textContent = message;
  document.body.appendChild(announcement);
  
  setTimeout(() => announcement.remove(), 1000);
};
```

### Describe Complex Cells

```tsx
// Add descriptions for complex content
<ColumnDirective
  field='Status'
  headerText='Status'
  template={(props) => (
    <div>
      <span
        style={{
          backgroundColor: props.Status === 'Active' ? 'green' : 'red',
          color: 'white',
          padding: '4px 8px',
          borderRadius: '4px'
        }}
        aria-label={`Status: ${props.Status}`}
      >
        {props.Status}
      </span>
    </div>
  )}
/>
```

### Header Descriptions

```tsx
<ColumnDirective
  field='Freight'
  headerText='Freight Cost'
  template={() => (
    <div>
      <span>Freight Cost (USD)</span>
      <span className='sr-only'>Shipping cost in US dollars</span>
    </div>
  )}
/>
```

---

## Color Contrast

### WCAG AA Requirements

- **Normal text**: 4.5:1 ratio
- **Large text** (18+ or 14+ bold): 3:1 ratio

### Contrast Check

```tsx
// ✅ Good contrast (Black on White = 21:1)
<div style={{ color: '#000000', backgroundColor: '#FFFFFF' }}>
  Text with excellent contrast
</div>

// ✅ Good for large text (3:1)
<div style={{ color: '#0066CC', backgroundColor: '#FFFFFF', fontSize: '18px', fontWeight: 'bold' }}>
  Large blue text
</div>

// ❌ Bad contrast (Gray on White = 1.5:1)
<div style={{ color: '#CCCCCC', backgroundColor: '#FFFFFF' }}>
  Poor contrast text (fail)
</div>
```

### Apply to Grid

```tsx
// Custom theme with good contrast
const gridStyles = `
  .e-grid .e-gridcontent td {
    color: #000000;  /* High contrast */
    background-color: #FFFFFF;
  }
  
  .e-grid .e-headercell {
    color: #FFFFFF;
    background-color: #0066CC;  /* 4.5:1 ratio */
  }
  
  .e-grid .e-selectionbackground {
    background-color: #0066CC;
    color: #FFFFFF;
  }
`;

<style>{gridStyles}</style>
<GridComponent dataSource={data}>
  {/* columns */}
</GridComponent>
```

---

## Focus Management

### Visible Focus Indicator

```tsx
const focusStyles = `
  .e-grid .e-gridcontent td:focus,
  .e-grid .e-headercell:focus {
    outline: 3px solid #4A90E2;
    outline-offset: 2px;
  }
`;

<style>{focusStyles}</style>
<GridComponent dataSource={data}>
  {/* columns */}
</GridComponent>
```

### Restore Focus on Dialog Close

```tsx
import React, { useRef } from 'react';

function GridWithDialog() {
  const gridRef = useRef(null);
  const previousFocusRef = useRef(null);

  const handleEditStart = () => {
    previousFocusRef.current = document.activeElement;
  };

  const handleEditComplete = () => {
    // Restore focus to previously focused element
    if (previousFocusRef.current) {
      previousFocusRef.current.focus();
    }
  };

  return (
    <GridComponent
      ref={gridRef}
      dataSource={data}
      editSettings={{ mode: 'Dialog', allowEditing: true }}
      actionBegin={(args) => {
        if (args.requestType === 'beginEdit') handleEditStart();
      }}
      actionComplete={(args) => {
        if (args.requestType === 'save') handleEditComplete();
      }}
    >
      {/* columns */}
    </GridComponent>
  );
}

export default GridWithDialog;
```

---

## Accessibility Testing

### Automated Testing with axe DevTools

```tsx
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('grid should be accessible', async () => {
  const { container } = render(<GridApp />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Testing Checklist

- [ ] All features keyboard accessible
- [ ] Tab order is logical
- [ ] Focus indicators visible
- [ ] No keyboard traps
- [ ] Color not only differentiator
- [ ] Contrast ratios met (4.5:1)
- [ ] Headings properly structured
- [ ] Labels associated with inputs
- [ ] Form validation messages clear
- [ ] Dynamic content announced
- [ ] Images have alt text
- [ ] Links have descriptive text
- [ ] No auto-playing audio/video
- [ ] Resizable text works
- [ ] Works with screen readers
- [ ] Responsive on mobile with zoom

### Browser Extensions for Testing

- **axe DevTools**: Accessibility checker
- **WAVE**: Web accessibility tool
- **Lighthouse**: Built-in Chrome audit
- **NVDA**: Free screen reader (Windows)
- **JAWS**: Professional screen reader

### Test Report Template

```
Grid Accessibility Audit - [Date]

✅ Keyboard Navigation
 - All functions accessible
 - Logical tab order
 - No keyboard traps

✅ WCAG 2.2 Compliance
 - Level A: PASSED
 - Level AA: PASSED

✅ Screen Reader Support
 - NVDA: PASSED
 - JAWS: PASSED

✅ Color & Contrast
 - Text: 4.5:1
 - UI Components: 3:1

Notes:
- [Any issues found]
```

---

## Best Practices Summary

1. **Always enable keyboard navigation**
   ```tsx
   allowKeyboard={true}
   ```

2. **Use semantic HTML**
   ```tsx
   <ColumnDirective ariaLabel='...' />
   ```

3. **Maintain color contrast**
   - 4.5:1 for normal text
   - 3:1 for large text

4. **Provide clear labels and instructions**
   ```tsx
   <label htmlFor='grid-id'>Instructions here</label>
   ```

5. **Test with assistive technology**
   - Use NVDA or JAWS
   - Use axe automation

6. **Implement focus management**
   - Show focus indicator
   - Maintain logical focus order

7. **Use ARIA appropriately**
   - Let Grid handle automatic ARIA
   - Add custom ARIA when needed

8. **Make dynamic changes announcements**
   - Use aria-live regions
   - Announce data updates

9. **Ensure print-friendly**
   ```tsx
   @media print {
     .grid { /* print styles */ }
   }
   ```

10. **Document accessibility features**
    - Include in user guide
    - Provide keyboard shortcuts

