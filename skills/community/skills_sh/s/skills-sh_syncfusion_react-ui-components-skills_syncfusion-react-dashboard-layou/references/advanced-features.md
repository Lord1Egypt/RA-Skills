# Dashboard Layout Advanced Features

## Table of Contents
- [Dynamic Panel Creation](#dynamic-panel-creation)
- [Custom Styling & CSS](#custom-styling--css)
- [Panel Templates](#panel-templates)
- [Accessibility & RTL](#accessibility--rtl)
- [Performance Optimization](#performance-optimization)
- [Integration Patterns](#integration-patterns)

## Dynamic Panel Creation

### Add Panels at Runtime

Add panels dynamically after component initialization:

```tsx
import { useRef } from 'react';
import { DashboardLayoutComponent, PanelModel } from '@syncfusion/ej2-react-layouts';

export const DynamicPanelManager = () => {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const addNewPanel = () => {
    const newPanel: PanelModel = {
      id: `panel-${Date.now()}`,
      header: 'New Panel',
      content: '<div style="padding: 20px;">New panel content</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 1
    };

    dashboardRef.current?.addPanel(newPanel);
  };

  return (
    <>
      <button onClick={addNewPanel}>Add New Panel</button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        columns={5}
        panels={[]}
      >
      </DashboardLayoutComponent>
    </>
  );
};
```

### Remove Panels at Runtime

Remove specific panels or all panels:

```tsx
const removePanel = (panelId: string) => {
  dashboardRef.current?.removePanel(panelId);
};

const clearAllPanels = () => {
  dashboardRef.current?.removeAll();
};
```

### Batch Panel Operations

Add/remove multiple panels efficiently:

```tsx
const addMultiplePanels = (panelConfigs: PanelModel[]) => {
  panelConfigs.forEach(config => {
    dashboardRef.current?.addPanel(config);
  });
};

const replaceAllPanels = (newPanels: PanelModel[]) => {
  dashboardRef.current?.removeAll();
  newPanels.forEach(panel => {
    dashboardRef.current?.addPanel(panel);
  });
};
```

## Custom Styling & CSS

### Custom CSS Classes

Apply custom classes to panels:

```tsx
const styledPanels: PanelModel[] = [
  {
    id: 'premium-panel',
    header: 'Premium Panel',
    cssClass: 'custom-premium highlight',
    content: 'Premium content',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 1
  },
  {
    id: 'alert-panel',
    header: 'Alert',
    cssClass: 'custom-alert',
    content: 'Alert content',
    row: 0,
    col: 2,
    sizeX: 2,
    sizeY: 1
  }
];

// CSS
const styles = `
.custom-premium {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.custom-alert {
  background-color: #fee;
  border-left: 4px solid #f44;
}

.highlight {
  border: 2px solid gold;
}
`;
```

### Panel Header Customization

```tsx
const customHeaderCSS = `
.e-dashboardlayout.e-control .e-panel .e-panel-container .e-panel-header {
  background: linear-gradient(90deg, #667eea, #764ba2);
  color: white;
  font-weight: bold;
  padding: 12px;
  border-radius: 4px 4px 0 0;
}

.e-dashboardlayout.e-control .e-panel .e-panel-container .e-panel-header .e-icons {
  color: white;
}
`;
```

### Panel Content Styling

```tsx
const customContentCSS = `
.e-dashboardlayout.e-control .e-panel .e-panel-container .e-panel-content {
  background-color: #f8f9fa;
  padding: 20px;
  border: 1px solid #dee2e6;
  min-height: 100px;
}

.e-dashboardlayout.e-control .e-panel:hover .e-panel-container .e-panel-content {
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
`;
```

### Resize Handle Styling

```tsx
const customResizeCSS = `
.e-dashboardlayout.e-control .e-panel .e-panel-container .e-resize.e-double {
  background-color: #667eea;
  color: white;
  font-size: 16px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-items: center;
}

.e-dashboardlayout.e-control .e-panel .e-panel-container .e-resize.e-double:hover {
  background-color: #764ba2;
  cursor: grab;
}
`;
```

## Panel Templates

### Header Templates

Create custom header content:

```tsx
const headerTemplate = () => {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span>📊 Analytics</span>
      <span style={{ fontSize: '12px', color: '#666' }}>Last updated: now</span>
    </div>
  );
};

const panelWithCustomHeader: PanelModel = {
  id: 'analytics-panel',
  header: headerTemplate,  // Function returns JSX
  content: '<div>Chart content</div>',
  row: 0,
  col: 0,
  sizeX: 2,
  sizeY: 2
};
```

### Content Templates

Create complex panel content:

```tsx
const contentTemplate = () => {
  return (
    <div style={{ padding: '20px' }}>
      <h3>Sales Dashboard</h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        <div>
          <p>Total Sales</p>
          <h2>$45,000</h2>
        </div>
        <div>
          <p>Growth</p>
          <h2 style={{ color: 'green' }}>+12%</h2>
        </div>
      </div>
      <button>View Details</button>
    </div>
  );
};

const panelWithComplexContent: PanelModel = {
  id: 'sales-panel',
  header: 'Sales',
  content: contentTemplate,  // Function returns JSX
  row: 0,
  col: 0,
  sizeX: 2,
  sizeY: 2
};
```

### HTML String Templates

Use HTML strings for simple content:

```tsx
const panelWithHTML: PanelModel = {
  id: 'html-panel',
  header: 'HTML Content',
  content: `
    <div style="padding: 20px;">
      <h3>Dashboard Stats</h3>
      <ul>
        <li>Metric 1: 100</li>
        <li>Metric 2: 200</li>
        <li>Metric 3: 300</li>
      </ul>
    </div>
  `,
  row: 0,
  col: 0,
  sizeX: 2,
  sizeY: 1
};
```

## Accessibility & RTL

### Accessibility (WCAG)

Enable keyboard navigation and screen reader support:

```tsx
<DashboardLayoutComponent
  id='accessible-dashboard'
  panels={panels}
  enableHtmlSanitizer={true}  // Sanitize for security
>
</DashboardLayoutComponent>
```

**Keyboard Shortcuts:**
- Tab: Navigate between panels
- Enter/Space: Interact with focused elements
- Arrow Keys: Move focus
- Escape: Cancel drag/resize operations

### ARIA Attributes

Panels automatically include ARIA labels. For custom content:

```tsx
const accessiblePanel: PanelModel = {
  id: 'accessible-panel',
  header: 'Sales Report',
  content: `
    <div aria-label="Sales Report Dashboard">
      <h3 aria-level="3">Q4 Sales</h3>
      <table role="table" aria-label="Quarterly sales data">
        <tr>
          <th>Month</th>
          <th>Sales</th>
        </tr>
        <tr>
          <td>October</td>
          <td>$45,000</td>
        </tr>
      </table>
    </div>
  `,
  row: 0,
  col: 0,
  sizeX: 2,
  sizeY: 1
};
```

### Right-to-Left (RTL) Layout

Enable RTL for Arabic, Hebrew, and other RTL languages:

```tsx
<DashboardLayoutComponent
  enableRtl={true}        // Enable RTL rendering
  mediaQuery='max-width:600px'
  columns={5}
  panels={panels}
>
</DashboardLayoutComponent>
```

**RTL CSS:**
```tsx
const rtlStyles = `
.e-dashboardlayout.e-rtl {
  direction: rtl;
}

.e-dashboardlayout.e-rtl .e-panel .e-panel-header {
  text-align: right;
}
`;
```

## Performance Optimization

### Virtual Scrolling (Large Datasets)

For dashboards with many panels:

```tsx
// Lazy load panels
const LazyDashboard = () => {
  const [visiblePanels, setVisiblePanels] = useState<PanelModel[]>([]);

  useEffect(() => {
    // Load only visible panels
    const loadedPanels = allPanels.slice(0, 10);
    setVisiblePanels(loadedPanels);

    // Load more on scroll
    const handleScroll = () => {
      if (scrollPosition > threshold) {
        setVisiblePanels(prev => [...prev, ...allPanels.slice(prev.length, prev.length + 5)]);
      }
    };

    return () => {};
  }, []);

  return (
    <DashboardLayoutComponent
      columns={5}
      panels={visiblePanels}
    >
    </DashboardLayoutComponent>
  );
};
```

### Memoization

Prevent unnecessary re-renders:

```tsx
import { memo, useMemo } from 'react';

const DashboardMemo = memo(({ panels }) => {
  const memoizedPanels = useMemo(() => panels, [panels]);

  return (
    <DashboardLayoutComponent
      columns={5}
      panels={memoizedPanels}
    >
    </DashboardLayoutComponent>
  );
});
```

### Debounce Layout Changes

Reduce event firing:

```tsx
import { useCallback, useRef } from 'react';

const DashboardWithDebounce = () => {
  const debounceTimer = useRef<NodeJS.Timeout>();

  const handleChange = useCallback((args: any) => {
    clearTimeout(debounceTimer.current);
    debounceTimer.current = setTimeout(() => {
      console.log('Layout changed:', args);
      saveLayout(args);
    }, 300);
  }, []);

  return (
    <DashboardLayoutComponent
      panels={panels}
      change={handleChange}
    >
    </DashboardLayoutComponent>
  );
};
```

## Integration Patterns

### Redux Integration

Manage dashboard state with Redux:

```tsx
import { useSelector, useDispatch } from 'react-redux';

const ReduxDashboard = () => {
  const dispatch = useDispatch();
  const panels = useSelector((state: any) => state.dashboard.panels);

  const handleChange = (args: any) => {
    dispatch({
      type: 'UPDATE_DASHBOARD_LAYOUT',
      payload: args.changedPanels
    });
  };

  return (
    <DashboardLayoutComponent
      panels={panels}
      change={handleChange}
    >
    </DashboardLayoutComponent>
  );
};
```

### API Integration

Load and save layouts from server:

```tsx
const APIIntegratedDashboard = () => {
  const [panels, setPanels] = useState<PanelModel[]>([]);

  useEffect(() => {
    // Load layout from API
    fetch('/api/dashboard/layout')
      .then(res => res.json())
      .then(data => setPanels(data))
      .catch(err => console.error('Failed to load layout:', err));
  }, []);

  const saveLayout = (newLayout: PanelModel[]) => {
    fetch('/api/dashboard/layout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newLayout)
    }).catch(err => console.error('Failed to save layout:', err));
  };

  return (
    <DashboardLayoutComponent
      panels={panels}
      change={(args) => saveLayout(args.changedPanels)}
    >
    </DashboardLayoutComponent>
  );
};
```

### Context API Integration

Share dashboard state across components:

```tsx
import { createContext, useContext } from 'react';

const DashboardContext = createContext<any>(null);

export const DashboardProvider = ({ children }: any) => {
  const [panels, setPanels] = useState<PanelModel[]>([]);

  return (
    <DashboardContext.Provider value={{ panels, setPanels }}>
      {children}
    </DashboardContext.Provider>
  );
};

export const useDashboard = () => {
  const context = useContext(DashboardContext);
  if (!context) {
    throw new Error('useDashboard must be used within DashboardProvider');
  }
  return context;
};

// Usage
const Dashboard = () => {
  const { panels, setPanels } = useDashboard();

  return (
    <DashboardLayoutComponent
      panels={panels}
      change={(args) => setPanels(args.changedPanels)}
    >
    </DashboardLayoutComponent>
  );
};
```
