# Responsive and Adaptive Design

## Table of Contents
- [Overview](#overview)
- [Responsive Behavior](#responsive-behavior)
- [Media Query Configuration](#media-query-configuration)
- [Breakpoints](#breakpoints)
- [Adaptive Layouts](#adaptive-layouts)
- [Mobile Considerations](#mobile-considerations)
- [Touch Device Support](#touch-device-support)
- [Testing Responsive Layouts](#testing-responsive-layouts)
- [Best Practices](#best-practices)

## Overview

Dashboard Layout includes built-in responsive behavior that automatically adapts panel arrangements based on viewport width. At smaller screen sizes, the layout transforms into a stacked arrangement with panels displayed vertically in a single column, optimizing the viewing experience for mobile and tablet devices.

### Responsive Features

- **Automatic Adaptation**: Layout changes based on viewport width
- **Configurable Breakpoints**: Set custom media query thresholds
- **Stacked Layout**: Panels arrange vertically on small screens
- **Column Adjustment**: Number of grid columns changes per breakpoint
- **Maintains State**: User customizations persist across resize

## Responsive Behavior

### Default Responsive Behavior

By default, Dashboard Layout automatically transforms to a stacked layout when viewport width drops to 600px or below:

```tsx
function DefaultResponsiveDashboard() {
  const panels = [
    {
      id: 'panel-1',
      header: 'Sales',
      content: '<div>Sales data</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2
    },
    {
      id: 'panel-2',
      header: 'Users',
      content: '<div>User data</div>',
      row: 0,
      col: 2,
      sizeX: 2,
      sizeY: 2
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      // Default: Responsive at <= 600px
    />
  );
}
```

### Responsive Layout Transformation

**Desktop (> 600px):**
```
┌──────────────────────────────────────┐
│ Panel 1          │ Panel 2           │ Multiple columns
│ (2x2)            │ (2x2)             │
└──────────────────────────────────────┘
```

**Mobile (<= 600px):**
```
┌─────────────────┐
│ Panel 1         │ Single column
│ (full width)    │
├─────────────────┤
│ Panel 2         │
│ (full width)    │
└─────────────────┘
```

## Media Query Configuration

### Custom Media Query Breakpoint

Use the `mediaQuery` property to customize the responsive breakpoint:

```typescript
// Property signature
mediaQuery: string;  // CSS media query string
```

### Examples

```tsx
function CustomMediaQueryDashboard() {
  return (
    <div>
      {/* Responsive at 800px */}
      <DashboardLayoutComponent
        id='dashboard-800'
        panels={panels}
        columns={5}
        mediaQuery='max-width: 800px'
      />

      {/* Responsive at 1000px */}
      <DashboardLayoutComponent
        id='dashboard-1000'
        panels={panels}
        columns={5}
        mediaQuery='max-width: 1000px'
      />

      {/* Responsive at landscape orientation */}
      <DashboardLayoutComponent
        id='dashboard-portrait'
        panels={panels}
        columns={5}
        mediaQuery='(max-width: 768px) and (orientation: portrait)'
      />

      {/* Multiple conditions */}
      <DashboardLayoutComponent
        id='dashboard-complex'
        panels={panels}
        columns={5}
        mediaQuery='(max-width: 768px) or (max-height: 600px)'
      />
    </div>
  );
}
```

## Breakpoints

### Standard Breakpoint System

```tsx
const breakpoints = {
  xs: '320px',   // Extra small (phones)
  sm: '576px',   // Small (landscape phones)
  md: '768px',   // Medium (tablets)
  lg: '992px',   // Large (desktops)
  xl: '1200px',  // Extra large (wide desktops)
  xxl: '1400px'  // Ultra wide
};

function MultiBreakpointDashboard() {
  const [breakpoint, setBreakpoint] = useState<keyof typeof breakpoints>('lg');

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      
      if (width < 576) setBreakpoint('xs');
      else if (width < 768) setBreakpoint('sm');
      else if (width < 992) setBreakpoint('md');
      else if (width < 1200) setBreakpoint('lg');
      else if (width < 1400) setBreakpoint('xl');
      else setBreakpoint('xxl');
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div>
      <p>Current Breakpoint: {breakpoint}</p>
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        mediaQuery={getMediaQueryForBreakpoint(breakpoint)}
      />
    </div>
  );
}

function getMediaQueryForBreakpoint(bp: string): string {
  const queries: Record<string, string> = {
    xs: 'max-width: 575px',
    sm: 'max-width: 767px',
    md: 'max-width: 991px',
    lg: 'max-width: 1199px',
    xl: 'max-width: 1399px',
    xxl: 'min-width: 1400px'
  };
  return queries[bp] || 'max-width: 600px';
}
```

## Adaptive Layouts

### Adaptive Column Configuration

Change the number of columns based on viewport size:

```tsx
function AdaptiveColumnDashboard() {
  const [columns, setColumns] = useState(5);

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;

      if (width < 640) setColumns(1);        // Mobile
      else if (width < 1024) setColumns(2);  // Tablet
      else if (width < 1280) setColumns(3);  // Small Desktop
      else if (width < 1536) setColumns(4);  // Desktop
      else setColumns(6);                    // Large Desktop
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={columns}
    />
  );
}
```

### Adaptive Panel Sizing

Adjust panel sizes for different screen sizes:

```tsx
function AdaptivePanelSizingDashboard() {
  const [screenSize, setScreenSize] = useState('desktop');
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;

      if (width < 640) {
        setScreenSize('mobile');
        // Single column layout
        dashboardRef.current!.panels = [
          { id: 'p1', sizeX: 1, sizeY: 1, row: 0, col: 0 },
          { id: 'p2', sizeX: 1, sizeY: 1, row: 1, col: 0 },
          { id: 'p3', sizeX: 1, sizeY: 1, row: 2, col: 0 }
        ];
      } else if (width < 1024) {
        setScreenSize('tablet');
        // Two column layout
        dashboardRef.current!.panels = [
          { id: 'p1', sizeX: 1, sizeY: 1, row: 0, col: 0 },
          { id: 'p2', sizeX: 1, sizeY: 1, row: 0, col: 1 },
          { id: 'p3', sizeX: 2, sizeY: 1, row: 1, col: 0 }
        ];
      } else {
        setScreenSize('desktop');
        // Multi-column layout
        dashboardRef.current!.panels = [
          { id: 'p1', sizeX: 2, sizeY: 2, row: 0, col: 0 },
          { id: 'p2', sizeX: 2, sizeY: 1, row: 0, col: 2 },
          { id: 'p3', sizeX: 1, sizeY: 2, row: 0, col: 4 }
        ];
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
    />
  );
}
```

## Mobile Considerations

### Mobile-First Approach

```tsx
function MobileFirstDashboard() {
  // Start with mobile layout (1 column)
  // Progressively enhance for larger screens
  const getMobileFriendlyConfig = () => {
    const width = window.innerWidth;

    return {
      columns: width < 640 ? 1 : width < 1024 ? 2 : 5,
      cellSpacing: width < 640 ? [5, 5] : [10, 10],
      allowDragging: width >= 1024,  // Disable on mobile
      allowResizing: width >= 768     // Disable on small tablets
    };
  };

  const config = getMobileFriendlyConfig();

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={config.columns}
      cellSpacing={config.cellSpacing}
      allowDragging={config.allowDragging}
      allowResizing={config.allowResizing}
      mediaQuery='max-width: 1023px'
    />
  );
}
```

### Mobile Touch Optimization

```tsx
function TouchOptimizedDashboard() {
  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={window.innerWidth < 768 ? 1 : 5}
      cellSpacing={[10, 10]}
      allowDragging={true}
      resizableHandles={['e-south-east']}  // Single resize handle on mobile
      // CSS adjusts handle size for touch
    />
  );
}

// CSS for touch-friendly handles
@media (max-width: 768px) {
  .e-panel .e-resize-handle {
    width: 50px !important;
    height: 50px !important;
    bottom: -15px;
    right: -15px;
  }
  
  .e-panel .e-panel-header {
    min-height: 48px;  /* Touch-friendly height */
    font-size: 16px;   /* Prevent iOS zoom */
  }
}
```

## Touch Device Support

### Detecting Touch Devices

```tsx
function TouchAwareDashboard() {
  const [isTouch, setIsTouch] = useState(false);

  useEffect(() => {
    const isTouchDevice = () => {
      return (
        (typeof window !== 'undefined' &&
          window.matchMedia('(hover: none)').matches) ||
        ('ontouchstart' in window) ||
        (navigator.maxTouchPoints > 0)
      );
    };

    setIsTouch(isTouchDevice());
  }, []);

  return (
    <div>
      {isTouch && <div className='touch-indicator'>Touch Device</div>}
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        allowDragging={!isTouch}  // Disable on touch for better UX
      />
    </div>
  );
}
```

### Touch-Friendly Interface

```css
/* Touch-optimized styling */
@media (hover: none) and (pointer: coarse) {
  /* Touch device */
  
  .e-panel .e-panel-header {
    padding: 16px;
    min-height: 56px;
  }

  .e-panel .e-resize-handle {
    width: 60px;
    height: 60px;
    opacity: 0.3;
  }

  .e-panel .e-resize-handle:active {
    opacity: 1;
  }

  /* Larger tap targets */
  .e-panel {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
}
```

## Testing Responsive Layouts

### Browser DevTools Testing

```tsx
function ResponsiveTestDashboard() {
  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      mediaQuery='max-width: 768px'
      // Test using Chrome DevTools:
      // 1. Open DevTools (F12)
      // 2. Toggle device toolbar (Ctrl+Shift+M)
      // 3. Select device and verify layout
    />
  );
}
```

### Programmatic Testing

```tsx
import { render } from '@testing-library/react';

describe('Responsive Dashboard', () => {
  test('should adapt to mobile viewport', () => {
    // Mock window size
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375
    });

    const { container } = render(
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        mediaQuery='max-width: 600px'
      />
    );

    // Assert mobile layout
    const dashboard = container.querySelector('.e-dashboard-layout');
    expect(dashboard).toBeInTheDocument();
  });

  test('should adapt to desktop viewport', () => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 1920
    });

    const { container } = render(
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
      />
    );

    const dashboard = container.querySelector('.e-dashboard-layout');
    expect(dashboard).toBeInTheDocument();
  });
});
```

### Visual Regression Testing

```tsx
import { screenshot } from 'playwright';

async function testResponsiveDesign() {
  const viewports = [
    { name: 'Mobile', width: 375, height: 667 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Desktop', width: 1920, height: 1080 }
  ];

  for (const viewport of viewports) {
    await page.setViewportSize(viewport);
    await screenshot(`dashboard-${viewport.name}.png`);
  }
}
```

## Best Practices

### 1. Define Clear Breakpoints

```tsx
// ✅ RECOMMENDED: Standard breakpoint system
const BREAKPOINTS = {
  mobile: 640,
  tablet: 1024,
  desktop: 1280,
  large: 1920
};

// ❌ AVOID: Arbitrary breakpoints
const badBreakpoints = [700, 1150, 1600];
```

### 2. Test on Real Devices

```tsx
// ✅ RECOMMENDED: Test on actual devices
// - iPhone (375px)
// - iPad (768px)
// - Android phone (360px)
// - Desktop monitors (1920px+)

// ❌ AVOID: Only testing in browser DevTools
```

### 3. Progressive Enhancement

```tsx
// ✅ RECOMMENDED: Start simple, enhance
function ProgressiveEnhancementDashboard() {
  const basicFeatures = {
    columns: 1,
    allowDragging: false,
    allowResizing: false
  };

  const enhancedFeatures = {
    columns: 5,
    allowDragging: true,
    allowResizing: true
  };

  const isSmallScreen = window.innerWidth < 1024;
  const config = isSmallScreen ? basicFeatures : enhancedFeatures;

  return <DashboardLayoutComponent {...config} />;
}
```

### 4. Handle Orientation Changes

```tsx
// ✅ RECOMMENDED: React to orientation changes
function OrientationAwareDashboard() {
  const [orientation, setOrientation] = useState('portrait');

  useEffect(() => {
    const handleOrientationChange = () => {
      setOrientation(window.innerHeight > window.innerWidth ? 'portrait' : 'landscape');
    };

    window.addEventListener('orientationchange', handleOrientationChange);
    return () => window.removeEventListener('orientationchange', handleOrientationChange);
  }, []);

  return (
    <div data-orientation={orientation}>
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={orientation === 'portrait' ? 1 : 5}
      />
    </div>
  );
}
```

### 5. Use Flexible Units

```tsx
// ✅ RECOMMENDED: Percentage/relative sizing
function FlexibleSizingDashboard() {
  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        // Dashboard expands to fill container
      />
    </div>
  );
}
```

### 6. Consider Viewport Meta Tag

```tsx
// HTML head configuration
function AppWithMetaTags() {
  useEffect(() => {
    // Ensure proper viewport settings
    const meta = document.querySelector('meta[name=viewport]');
    if (meta) {
      meta.setAttribute(
        'content',
        'width=device-width, initial-scale=1.0, maximum-scale=5.0'
      );
    }
  }, []);

  return <DashboardLayoutComponent id='dashboard' panels={panels} columns={5} />;
}

// Or in HTML
// <meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 7. Performance Optimization

```tsx
// ✅ RECOMMENDED: Debounce resize handling
function OptimizedResponsiveDashboard() {
  const timeoutRef = useRef<NodeJS.Timer>();

  const handleResize = useCallback(() => {
    clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => {
      // Update layout only after resize completes
      updateDashboardLayout();
    }, 250);
  }, []);

  useEffect(() => {
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      clearTimeout(timeoutRef.current);
    };
  }, [handleResize]);

  return <DashboardLayoutComponent id='dashboard' panels={panels} columns={5} />;
}
```
