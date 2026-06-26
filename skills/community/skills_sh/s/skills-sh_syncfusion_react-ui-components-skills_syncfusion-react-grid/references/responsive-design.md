# Responsive Design in React Grid

## Table of Contents
- [Overview](#overview)
- [Adaptive Grid](#adaptive-grid)
- [Mobile Optimization](#mobile-optimization)
- [Column Visibility](#column-visibility)
- [Touch Interactions](#touch-interactions)
- [Breakpoints](#breakpoints)
- [Responsive Examples](#responsive-examples)

## Overview

Syncfusion Grid provides built-in responsive features for mobile and desktop devices, automatically adjusting layout and interactions based on screen size.

---

## Adaptive Grid

### Enable Adaptive UI

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Filter, Sort, Edit, Toolbar, Page } from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={data}
  enableAdaptiveUI={true}  // Enable adaptive mode
  allowFiltering={true}
  allowSorting={true}
  allowPaging={true}
  editSettings={{ mode: 'Dialog', allowEditing: true }}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='150' isPrimaryKey={true} />
    <ColumnDirective field='CustomerID' headerText='Customer' width='150' />
    <ColumnDirective field='Freight' headerText='Freight' width='150' format='C2' />
  </ColumnsDirective>
  <Inject services={[Filter, Sort, Edit, Toolbar, Page]} />
</GridComponent>
```

### Adaptive Dialog vs Inline

```tsx
<GridComponent
  dataSource={data}
  enableAdaptiveUI={true}
  editSettings={{
    mode: 'Dialog',  // Dialogs become full-screen on mobile
    allowEditing: true
  }}
>
  {/* Automatically adapts dialogs */}
</GridComponent>
```

### Vertical Row Rendering

Display rows vertically on mobile:

```tsx
<GridComponent
  dataSource={data}
  enableAdaptiveUI={true}
  rowRenderingMode='Vertical'  // Stack columns vertically
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='150' />
    <ColumnDirective field='CustomerID' headerText='Customer ID' width='150' />
    <ColumnDirective field='Freight' headerText='Freight' width='150' />
  </ColumnsDirective>
</GridComponent>
```

---

## Mobile Optimization

### Responsive Grid with Media Queries

```tsx
import React, { useState, useEffect } from 'react';

function ResponsiveGrid() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <GridComponent
      dataSource={data}
      enableAdaptiveUI={isMobile}
      height={isMobile ? '100vh' : '600px'}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width={isMobile ? '150' : '120'} />
      </ColumnsDirective>
    </GridComponent>
  );
}
```

### Touch-Optimized Rows

```tsx
const mobileStyles = `
  @media (max-width: 768px) {
    .e-grid .e-row {
      height: 44px;  /* Touch-friendly row height */
    }
    
    .e-grid .e-gridcontent td {
      padding: 12px 8px;  /* Larger touch targets */
    }
    
    .e-grid button {
      min-width: 48px;  /* iOS touch recommendation */
      min-height: 48px;
    }
  }
`;

<style>{mobileStyles}</style>
<GridComponent dataSource={data}>
  {/* columns */}
</GridComponent>
```

### Hide Secondary Columns on Mobile

```tsx
<GridComponent
  dataSource={data}
  enableAdaptiveUI={true}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective 
      field='CustomerID' 
      headerText='Customer' 
      width='100'
      hideAtMedia='(max-width: 768px)'  // Hide on mobile
    />
    <ColumnDirective 
      field='OrderDate' 
      headerText='Date' 
      width='100'
      hideAtMedia='(max-width: 600px)'  // Hide on small screens
    />
    <ColumnDirective field='Freight' headerText='Freight' width='100' />
  </ColumnsDirective>
</GridComponent>
```

---

## Column Visibility

### Show/Hide Columns Based on Screen Size

```tsx
import React, { useState, useEffect } from 'react';

function GridWithResponsiveColumns() {
  const [screenSize, setScreenSize] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setScreenSize(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const getVisibleColumns = () => {
    if (screenSize < 600) {
      return ['OrderID', 'Freight'];  // Mobile: essential columns only
    } else if (screenSize < 1024) {
      return ['OrderID', 'CustomerID', 'Freight'];  // tablet
    } else {
      return ['OrderID', 'CustomerID', 'OrderDate', 'Freight', 'Status'];  // Desktop
    }
  };

  const visibleColumns = getVisibleColumns();

  return (
    <GridComponent dataSource={data}>
      <ColumnsDirective>
        <ColumnDirective 
          field='OrderID' 
          visible ={!visibleColumns.includes('OrderID')} 
        />
        <ColumnDirective 
          field='CustomerID' 
          visible ={!visibleColumns.includes('CustomerID')} 
        />
        <ColumnDirective 
          field='OrderDate' 
          visible ={!visibleColumns.includes('OrderDate')} 
        />
        <ColumnDirective 
          field='Freight' 
          visible ={!visibleColumns.includes('Freight')} 
        />
        <ColumnDirective 
          field='Status' 
          visible ={!visibleColumns.includes('Status')} 
        />
      </ColumnsDirective>
    </GridComponent>
  );
}
```

### Column Chooser for Mobile

```tsx
<GridComponent
  dataSource={data}
  enableAdaptiveUI={true}
  toolbar={['ColumnChooser']}  // Users can select visible columns
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='OrderDate' headerText='Date' width='100' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' />
  </ColumnsDirective>
</GridComponent>
```

---

## Touch Interactions

### Touch-Friendly Selection

```tsx
<GridComponent
  dataSource={data}
  allowSelection={true}
  selectionSettings={{ type: 'Multiple', mode: 'Row' }}
>
  <ColumnsDirective>
    <ColumnDirective type='checkbox' width='60' />  {/* Easy touch target */}
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='100' />
  </ColumnsDirective>
</GridComponent>
```

### Swipe Actions (Custom)

```tsx
import React, { useRef } from 'react';

function GridWithSwipeActions() {
  const gridRef = useRef(null);
  const touchStartX = useRef(0);

  const handleTouchStart = (e) => {
    touchStartX.current = e.touches[0].clientX;
  };

  const handleTouchEnd = (e) => {
    const touchEndX = e.changedTouches[0].clientX;
    const diff = touchStartX.current - touchEndX;

    if (Math.abs(diff) > 50) {  // Swipe threshold
      if (diff > 0) {
        // Swiped left - show delete button
        console.log('Swiped left');
      } else {
        // Swiped right - show more options
        console.log('Swiped right');
      }
    }
  };

  return (
    <div 
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      <GridComponent ref={gridRef} dataSource={data}>
        {/* columns */}
      </GridComponent>
    </div>
  );
}
```

### Long Press for Context Menu

```tsx
import React, { useRef } from 'react';

function GridWithLongPress() {
  const longPressTimer = useRef(null);

  const handleMouseDown = () => {
    longPressTimer.current = setTimeout(() => {
      // Show context menu
      showContextMenu();
    }, 500);  // Long press duration
  };

  const handleMouseUp = () => {
    clearTimeout(longPressTimer.current);
  };

  return (
    <div 
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onTouchStart={handleMouseDown}
      onTouchEnd={handleMouseUp}
    >
      <GridComponent dataSource={data} contextMenuItems={['Copy', 'Edit', 'Delete']}>
        {/* columns */}
      </GridComponent>
    </div>
  );
}
```

---

## Breakpoints

### Device Breakpoints

```tsx
// Standard breakpoints
const breakpoints = {
  mobile: '(max-width: 600px)',      // < 600px
  tablet: '(min-width: 601px) and (max-width: 1024px)',  // 601-1024px
  desktop: '(min-width: 1025px)'     // > 1024px
};
```

### CSS Breakpoint Styles

```css
/* Mobile - small phones */
@media (max-width: 600px) {
  .e-grid {
    font-size: 14px;
  }
  
  .e-grid .e-row {
    height: 48px;
  }
  
  .e-grid .e-gridcontent td {
    padding: 12px 8px;
  }
}

/* Tablet */
@media (min-width: 601px) and (max-width: 1024px) {
  .e-grid {
    font-size: 15px;
  }
  
  .e-grid .e-row {
    height: 40px;
  }
}

/* Desktop */
@media (min-width: 1025px) {
  .e-grid {
    font-size: 14px;
  }
  
  .e-grid .e-row {
    height: 36px;
  }
}
```

---

## Responsive Examples

### Complete Responsive Grid

```tsx
import React, { useState, useEffect } from 'react';
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page, Sort, Filter, Edit, Toolbar } from '@syncfusion/ej2-react-grids';

function ResponsiveOrderGrid() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className='responsive-grid-container'>
      <style>{`
        @media (max-width: 768px) {
          .responsive-grid-container .e-grid {
            font-size: 13px;
          }
          
          .responsive-grid-container .e-grid .e-row {
            height: 44px;
          }
          
          .responsive-grid-container .e-grid .e-gridcontent td {
            padding: 10px 6px;
          }
        }
      `}</style>

      <GridComponent
        dataSource={data}
        enableAdaptiveUI={isMobile}
        allowPaging={true}
        allowSorting={true}
        allowFiltering={true}
        editSettings={{ mode: isMobile ? 'Dialog' : 'Inline' }}
        toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel', 'Search']}
        pageSettings={{ pageSize: isMobile ? 10 : 12 }}
        height={isMobile ? '100vh' : '600px'}
      >
        <ColumnsDirective>
          <ColumnDirective 
            type='checkbox' 
            width={isMobile ? '40' : '60'} 
          />
          <ColumnDirective 
            field='OrderID' 
            headerText='Order ID' 
            width={isMobile ? '80' : '100'}
            isPrimaryKey={true}
          />
          <ColumnDirective 
            field='CustomerID' 
            headerText='Customer' 
            width={isMobile ? '100' : '120'}
            hideAtMedia='(max-width: 600px)'
          />
          <ColumnDirective 
            field='Freight' 
            headerText='Freight' 
            width={isMobile ? '80' : '100'}
            format='C2'
          />
          <ColumnDirective 
            field='Status' 
            headerText='Status' 
            width={isMobile ? '80' : '100'}
            hideAtMedia='(max-width: 768px)'
          />
        </ColumnsDirective>
        <Inject services={[Page, Sort, Filter, Edit, Toolbar]} />
      </GridComponent>
    </div>
  );
}

export default ResponsiveOrderGrid;
```

### Fluid Width Grid

```tsx
<GridComponent
  dataSource={data}
  width='100%'  // 100% of container
  height='500px'
  allowPaging={true}
>
  <ColumnsDirective>
    <ColumnDirective 
      field='OrderID' 
      headerText='Order ID' 
      width='25%'  // Percentage width
    />
    <ColumnDirective 
      field='CustomerID' 
      headerText='Customer' 
      width='25%'
    />
    <ColumnDirective 
      field='Freight' 
      headerText='Freight' 
      width='25%'
    />
    <ColumnDirective 
      field='Status' 
      headerText='Status' 
      width='25%'
    />
  </ColumnsDirective>
  <Inject services={[Page]} />
</GridComponent>
```

### Horizontal Scroll on Mobile

```tsx
const responsiveStyles = `
  @media (max-width: 768px) {
    .e-grid {
      overflow-x: auto;
    }
    
    .e-grid .e-gridheader .e-headercell {
      min-width: 100px;
    }
    
    .e-grid .e-gridcontent td {
      min-width: 100px;
    }
  }
`;

<style>{responsiveStyles}</style>
<GridComponent dataSource={data}>
  <ColumnsDirective>
    {/* columns */}
  </ColumnsDirective>
</GridComponent>
```

---

## Best Practices

1. **Always enable adaptive UI** for mobile experience
2. **Test on real devices** (not just browser emulation)
3. **Use touch-friendly dimensions** (min 48x48px)
4. **Set explicit column widths** for narrow screens
5. **Hide non-essential columns** on mobile
6. **Adjust page size** based on screen size
7. **Use vertical layout** for mobile detail views
8. **Test landscape and portrait** orientations
9. **Optimize toolbar** for touchscreen
10. **Include skip navigation** for accessibility
