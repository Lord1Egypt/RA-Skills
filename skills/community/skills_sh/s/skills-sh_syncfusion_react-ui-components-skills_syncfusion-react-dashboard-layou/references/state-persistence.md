# State Persistence and Serialization

## Table of Contents
- [Overview](#overview)
- [Serialize Method](#serialize-method)
- [Save State Pattern](#save-state-pattern)
- [Restore State Pattern](#restore-state-pattern)
- [localStorage Integration](#localstorage-integration)
- [sessionStorage Integration](#sessionstorage-integration)
- [Database Integration](#database-integration)
- [Advanced State Management](#advanced-state-management)
- [Best Practices](#best-practices)

## Overview

Dashboard Layout provides powerful state persistence capabilities, allowing you to save and restore layout configurations across sessions. The `serialize()` method captures the complete dashboard state as JSON, enabling flexible storage and recovery strategies.

### Why Persist State?

- **User Experience**: Users see their customized layout when returning
- **Productivity**: No need to reconfigure after page refresh
- **Collaboration**: Share dashboard configurations across team members
- **Backup**: Create snapshots of critical layouts
- **Compliance**: Maintain audit trails of layout changes

### Serialization Scope

The `serialize()` method captures:
- ✅ Panel positions (row, col)
- ✅ Panel sizes (sizeX, sizeY)
- ✅ Panel properties (minSize, maxSize)
- ✅ Panel order in DOM
- ✅ Component settings (allowDragging, allowResizing, etc.)

Does NOT capture:
- ❌ Panel content/data
- ❌ Component internal state (filters, sorting)
- ❌ Custom styles (apply separately)

## Serialize Method

### Method Signature

```typescript
serialize(): object[]
```

### Return Value

Returns an array of `PanelModel` objects representing the current layout:

```typescript
interface SerializedPanel {
  id?: string;
  header?: string;
  content?: string;
  row?: number;
  col?: number;
  sizeX?: number;
  sizeY?: number;
  minSizeX?: number;
  minSizeY?: number;
  maxSizeX?: number;
  maxSizeY?: number;
}
```

### Basic Usage

```tsx
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';
import { useRef } from 'react';

function Dashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const saveLayout = () => {
    const layoutState = dashboardRef.current?.serialize();
    console.log('Saved layout:', layoutState);
    // Output:
    // [
    //   { id: 'panel-1', row: 0, col: 0, sizeX: 2, sizeY: 2, ... },
    //   { id: 'panel-2', row: 0, col: 2, sizeX: 2, sizeY: 1, ... },
    //   ...
    // ]
  };

  return (
    <>
      <button onClick={saveLayout}>Save Layout</button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
      />
    </>
  );
}
```

## Save State Pattern

### Pattern 1: Save to Variable

```tsx
function DashboardWithStateSaving() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [savedLayouts, setSavedLayouts] = useState<any[]>([]);

  const saveCurrentLayout = () => {
    const currentState = dashboardRef.current?.serialize();
    setSavedLayouts(prev => [...prev, {
      name: `Snapshot ${new Date().toLocaleTimeString()}`,
      layout: currentState,
      timestamp: Date.now()
    }]);
  };

  const getLayoutSummary = () => {
    const state = dashboardRef.current?.serialize();
    return {
      panelCount: state?.length || 0,
      firstPanel: state?.[0]?.id,
      gridLayout: `${state?.[0]?.sizeX} x ${state?.[0]?.sizeY}`
    };
  };

  return (
    <div>
      <button onClick={saveCurrentLayout}>Save Snapshot</button>
      <div>Total Snapshots: {savedLayouts.length}</div>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
      />
    </div>
  );
}
```

### Pattern 2: Save on Panel Change

```tsx
function AutoSaveDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [lastSave, setLastSave] = useState<number>(0);

  const handlePanelChange = () => {
    const now = Date.now();
    
    // Debounce: Only save if 2+ seconds have passed
    if (now - lastSave < 2000) return;

    const layoutState = dashboardRef.current?.serialize();
    localStorage.setItem('dashboard-layout', JSON.stringify(layoutState));
    setLastSave(now);
    console.log('Layout auto-saved');
  };

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      change={handlePanelChange}
      dragStop={handlePanelChange}
      resizeStop={handlePanelChange}
    />
  );
}
```

### Pattern 3: Timed Auto-Save

```tsx
function TimedAutoSaveDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [saveInterval, setSaveInterval] = useState<NodeJS.Timer | null>(null);

  useEffect(() => {
    // Auto-save every 30 seconds
    const interval = setInterval(() => {
      const layoutState = dashboardRef.current?.serialize();
      const metadata = {
        layout: layoutState,
        timestamp: new Date().toISOString(),
        version: '1.0'
      };
      localStorage.setItem('dashboard-autosave', JSON.stringify(metadata));
    }, 30000);

    setSaveInterval(interval);

    return () => clearInterval(interval);
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

## Restore State Pattern

### Pattern 1: Restore from Variable

```tsx
function DashboardWithRestore() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [savedState, setSavedState] = useState<any[] | null>(null);

  const saveLayout = () => {
    const state = dashboardRef.current?.serialize();
    setSavedState(state);
    alert('Layout saved!');
  };

  const restoreLayout = () => {
    if (savedState && dashboardRef.current) {
      dashboardRef.current.panels = savedState;
      alert('Layout restored!');
    }
  };

  return (
    <div>
      <button onClick={saveLayout}>Save Layout</button>
      <button onClick={restoreLayout} disabled={!savedState}>
        Restore Layout
      </button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
      />
    </div>
  );
}
```

### Pattern 2: Restore with Merge

```tsx
function DashboardWithMerge() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const savedLayoutRef = useRef<any[] | null>(null);

  const saveLayout = () => {
    savedLayoutRef.current = dashboardRef.current?.serialize();
  };

  const restoreLayoutPartial = () => {
    if (!savedLayoutRef.current) return;

    const currentPanels = dashboardRef.current?.serialize() || [];
    const restored = savedLayoutRef.current;

    // Merge: Keep new panels, restore positions of old ones
    const merged = currentPanels.map(panel => {
      const savedPanel = restored.find(p => p.id === panel.id);
      return savedPanel ? { ...panel, row: savedPanel.row, col: savedPanel.col } : panel;
    });

    dashboardRef.current!.panels = merged;
  };

  return (
    <div>
      <button onClick={saveLayout}>Save Layout</button>
      <button onClick={restoreLayoutPartial}>Restore (Keep New Panels)</button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
      />
    </div>
  );
}
```

### Pattern 3: Conditional Restore

```tsx
function ConditionalRestoreDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  useEffect(() => {
    // Check if saved layout exists on component mount
    const savedLayout = localStorage.getItem('user-dashboard-layout');
    
    if (savedLayout) {
      try {
        const parsed = JSON.parse(savedLayout);
        
        // Validate before restore
        if (isValidLayout(parsed)) {
          dashboardRef.current!.panels = parsed;
          console.log('Layout restored from storage');
        }
      } catch (error) {
        console.error('Failed to restore layout:', error);
      }
    }
  }, []);

  const isValidLayout = (layout: any): boolean => {
    return Array.isArray(layout) && 
           layout.every(panel => 
             typeof panel.row === 'number' && 
             typeof panel.col === 'number'
           );
  };

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

## localStorage Integration

### Persist to localStorage

```tsx
function PersistentDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const STORAGE_KEY = 'dashboard-layout-v1';

  // Save to localStorage
  const saveToStorage = () => {
    const layoutState = dashboardRef.current?.serialize();
    if (layoutState) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(layoutState));
      console.log('Saved to localStorage');
    }
  };

  // Restore from localStorage
  const loadFromStorage = () => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const layoutState = JSON.parse(stored);
        dashboardRef.current!.panels = layoutState;
        console.log('Restored from localStorage');
      } catch (error) {
        console.error('Error loading from localStorage:', error);
      }
    }
  };

  useEffect(() => {
    // Load on mount
    loadFromStorage();

    // Save on window close (optional)
    const handleBeforeUnload = () => {
      saveToStorage();
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, []);

  return (
    <div>
      <button onClick={saveToStorage}>Save to Storage</button>
      <button onClick={loadFromStorage}>Load from Storage</button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
        dragStop={saveToStorage}
        resizeStop={saveToStorage}
      />
    </div>
  );
}
```

### localStorage JSON Structure

```json
{
  "layout": [
    {
      "id": "panel-1",
      "header": "Sales Chart",
      "row": 0,
      "col": 0,
      "sizeX": 2,
      "sizeY": 2,
      "minSizeX": 1,
      "minSizeY": 1
    },
    {
      "id": "panel-2",
      "header": "User Analytics",
      "row": 0,
      "col": 2,
      "sizeX": 3,
      "sizeY": 2
    }
  ],
  "metadata": {
    "version": "1.0",
    "savedAt": "2024-01-15T10:30:00Z",
    "userId": "user-123"
  }
}
```

## sessionStorage Integration

For temporary, session-scoped persistence:

```tsx
function SessionDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const SESSION_KEY = 'dashboard-temp-layout';

  const saveToSession = () => {
    const state = dashboardRef.current?.serialize();
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(state));
  };

  const restoreFromSession = () => {
    const stored = sessionStorage.getItem(SESSION_KEY);
    if (stored) {
      dashboardRef.current!.panels = JSON.parse(stored);
    }
  };

  useEffect(() => {
    restoreFromSession();
  }, []);

  return (
    <div>
      <button onClick={saveToSession}>Save Session</button>
      <button onClick={restoreFromSession}>Restore Session</button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
        dragStop={saveToSession}
      />
    </div>
  );
}
```

## Database Integration

### Save to Backend API

```tsx
function DashboardWithAPI() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [isSaving, setIsSaving] = useState(false);

  const saveLayoutToDatabase = async () => {
    const layoutState = dashboardRef.current?.serialize();
    
    setIsSaving(true);
    try {
      const response = await fetch('/api/dashboard/layout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: getCurrentUserId(),
          layout: layoutState,
          timestamp: new Date().toISOString()
        })
      });

      if (response.ok) {
        console.log('Layout saved to database');
        showNotification('Layout saved successfully');
      }
    } catch (error) {
      console.error('Error saving layout:', error);
      showNotification('Failed to save layout', 'error');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div>
      <button onClick={saveLayoutToDatabase} disabled={isSaving}>
        {isSaving ? 'Saving...' : 'Save to Database'}
      </button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
      />
    </div>
  );
}
```

### Load from Backend API

```tsx
function LoadDashboardLayout() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadLayout = async () => {
      try {
        const response = await fetch(
          `/api/dashboard/layout/${getUserId()}`
        );
        const data = await response.json();

        if (data.layout) {
          dashboardRef.current!.panels = data.layout;
        }
      } catch (error) {
        console.error('Error loading layout:', error);
      } finally {
        setLoading(false);
      }
    };

    loadLayout();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;

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

## Advanced State Management

### Redux Integration

```tsx
import { useSelector, useDispatch } from 'react-redux';

function ReduxDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const dispatch = useDispatch();
  const layoutState = useSelector(state => state.dashboard.layout);

  const handleLayoutChange = () => {
    const newLayout = dashboardRef.current?.serialize();
    dispatch({
      type: 'DASHBOARD_LAYOUT_CHANGED',
      payload: newLayout
    });
  };

  useEffect(() => {
    if (layoutState) {
      dashboardRef.current!.panels = layoutState;
    }
  }, [layoutState]);

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      dragStop={handleLayoutChange}
      resizeStop={handleLayoutChange}
    />
  );
}
```

### Context API with Hooks

```tsx
const DashboardContext = createContext<any>(null);

function DashboardProvider({ children }) {
  const [layout, setLayout] = useState<any[]>([]);

  const saveLayout = useCallback((newLayout: any[]) => {
    setLayout(newLayout);
    localStorage.setItem('dashboard-layout', JSON.stringify(newLayout));
  }, []);

  const restoreLayout = useCallback(() => {
    const saved = localStorage.getItem('dashboard-layout');
    if (saved) {
      const parsed = JSON.parse(saved);
      setLayout(parsed);
      return parsed;
    }
    return null;
  }, []);

  return (
    <DashboardContext.Provider value={{ layout, saveLayout, restoreLayout }}>
      {children}
    </DashboardContext.Provider>
  );
}

function UseDashboardLayout() {
  return useContext(DashboardContext);
}
```

## Best Practices

### 1. Versioning Your Layout

```tsx
interface LayoutSnapshot {
  version: '1.0' | '1.1' | '1.2';
  layout: any[];
  timestamp: string;
  userId: string;
}

function versionedSaveLayout(version: string) {
  const state: LayoutSnapshot = {
    version: version as any,
    layout: dashboardRef.current?.serialize() || [],
    timestamp: new Date().toISOString(),
    userId: getCurrentUserId()
  };

  localStorage.setItem('dashboard-layout', JSON.stringify(state));
}
```

### 2. Validate Before Restore

```tsx
function validateLayout(layout: any[]): boolean {
  if (!Array.isArray(layout)) return false;
  
  return layout.every(panel => {
    return (
      typeof panel.id === 'string' &&
      typeof panel.row === 'number' &&
      typeof panel.col === 'number' &&
      typeof panel.sizeX === 'number' &&
      typeof panel.sizeY === 'number' &&
      panel.row >= 0 &&
      panel.col >= 0 &&
      panel.sizeX > 0 &&
      panel.sizeY > 0
    );
  });
}
```

### 3. Handle Migration

```tsx
function migrateLayout(oldLayout: any[], fromVersion: string): any[] {
  if (fromVersion === '1.0') {
    // Add new properties for v1.1
    return oldLayout.map(panel => ({
      ...panel,
      locked: false,
      minSizeX: 1,
      minSizeY: 1
    }));
  }
  return oldLayout;
}
```

### 4. Error Recovery

```tsx
function safeSaveLayout() {
  try {
    const state = dashboardRef.current?.serialize();
    const backup = localStorage.getItem('dashboard-layout-backup');
    
    // Save current as backup
    if (backup) {
      localStorage.setItem('dashboard-layout-backup2', backup);
    }
    
    // Save new
    localStorage.setItem('dashboard-layout-backup', JSON.stringify(state));
    localStorage.setItem('dashboard-layout', JSON.stringify(state));
  } catch (error) {
    console.error('Error saving layout:', error);
  }
}
```

### 5. Performance Optimization

```tsx
function DebouncedSave() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const timeoutRef = useRef<NodeJS.Timer>();

  const debouncedSave = useCallback(() => {
    // Clear previous timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Set new timeout
    timeoutRef.current = setTimeout(() => {
      const state = dashboardRef.current?.serialize();
      localStorage.setItem('dashboard-layout', JSON.stringify(state));
    }, 1000); // Save 1 second after last change
  }, []);

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      dragStop={debouncedSave}
      resizeStop={debouncedSave}
    />
  );
}
```
