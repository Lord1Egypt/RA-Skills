# Quick Access Toolbar

## Overview

The Quick Access toolbar provides frequently-used commands for rapid access without navigating the main toolbar.

## Enable Quick Access Toolbar

### Basic Setup

```tsx
const imageEditor = (
  <ImageEditorComponent
    quickAccessToolbar={['Undo', 'Redo', 'Save']}
  />
);
```

### Default Configuration

```tsx
const imageEditor = (
  <ImageEditorComponent
    quickAccessToolbar={['Undo', 'Redo', 'Open', 'Save']}
  />
);
```

## Configure Quick Access Items

### Select Frequently Used Commands

```tsx
const quickAccess = [
  'Undo',
  'Redo',
  'Crop',
  'Rotate Left',
  'Rotate Right',
  'Flip Horizontal',
  'Save'
];

const imageEditor = (
  <ImageEditorComponent quickAccessToolbar={quickAccess} />
);
```

### Organize by Workflow

```tsx
const imageEditor = (
  <ImageEditorComponent
    quickAccessToolbar={[
      'Open',
      'Crop',
      'Text',
      'Filters',
      'Save'
    ]}
  />
);
```

## Show/Hide Items

### Toggle Quick Access Toolbar

Dynamically show/hide toolbar:

```tsx
const [showQuickAccess, setShowQuickAccess] = useState(true);

const quickAccessToolbar = showQuickAccess
  ? ['Undo', 'Redo', 'Crop', 'Save']
  : [];

return (
  <>
    <button onClick={() => setShowQuickAccess(!showQuickAccess)}>
      Toggle Quick Access
    </button>
    <ImageEditorComponent quickAccessToolbar={quickAccessToolbar} />
  </>
);
```

### Conditional Items

Show items based on context:

```tsx
const [mode, setMode] = useState('basic');

const quickAccess = mode === 'basic'
  ? ['Open', 'Save', 'Undo', 'Redo']
  : ['Open', 'Save', 'Undo', 'Redo', 'Crop', 'Text', 'Filters', 'Fine-tune'];

return (
  <ImageEditorComponent quickAccessToolbar={quickAccess} />
);
```

## Custom Quick Access Items

### Add Custom Commands

```tsx
const customQuickAccess = [
  'Open',
  'Save',
  {
    id: 'quick-reset',
    tooltipText: 'Reset to Original',
    prefixIcon: 'e-icon-refresh'
  },
  {
    id: 'quick-grayscale',
    tooltipText: 'Apply Grayscale',
    prefixIcon: 'e-icon-filter'
  }
];

const handleQuickAccessClick = (args: any): void => {
  if (args.id === 'quick-reset') {
    imgObj.reset();
  } else if (args.id === 'quick-grayscale') {
    imgObj.applyImageFilter(ImageFilterOption.Grayscale);
  }
};

const imageEditor = (
  <ImageEditorComponent
    quickAccessToolbar={customQuickAccess}
    toolbarItemClick={handleQuickAccessClick}
  />
);
```

## Quick Access Events

### Item Click Handling

Capture quick access interactions:

```tsx
const handleQuickAccessItemClick = (args: ToolbarClickEventArgs): void => {
  console.log('Quick access item clicked:', args.id);
  
  // Log usage analytics
  logAnalytics({
    feature: 'quick-access',
    action: args.id,
    timestamp: new Date()
  });
};

const imageEditor = (
  <ImageEditorComponent
    quickAccessToolbar={['Undo', 'Redo', 'Save']}
    toolbarItemClick={handleQuickAccessItemClick}
  />
);
```

### State Tracking

Monitor quick access usage:

```tsx
const [quickAccessStats, setQuickAccessStats] = useState({
  undoClicks: 0,
  redoClicks: 0,
  saveClicks: 0
});

const handleQuickAccessClick = (args: ToolbarClickEventArgs): void => {
  if (args.id === 'Undo') {
    setQuickAccessStats(prev => ({ ...prev, undoClicks: prev.undoClicks + 1 }));
  } else if (args.id === 'Redo') {
    setQuickAccessStats(prev => ({ ...prev, redoClicks: prev.redoClicks + 1 }));
  } else if (args.id === 'Save') {
    setQuickAccessStats(prev => ({ ...prev, saveClicks: prev.saveClicks + 1 }));
  }
};

return (
  <>
    <ImageEditorComponent
      quickAccessToolbar={['Undo', 'Redo', 'Save']}
      toolbarItemClick={handleQuickAccessClick}
    />
    <div>Undo: {quickAccessStats.undoClicks} clicks</div>
  </>
);
```

## Quick Access Patterns

### Minimal Quick Access

Show only critical items:

```tsx
const imageEditor = (
  <ImageEditorComponent
    quickAccessToolbar={['Undo', 'Redo', 'Save']}
  />
);
```

### Extended Quick Access

Show comprehensive quick access:

```tsx
const imageEditor = (
  <ImageEditorComponent
    quickAccessToolbar={[
      'Undo',
      'Redo',
      'Open',
      'Crop',
      'Rotate Left',
      'Rotate Right',
      'Flip Horizontal',
      'Text',
      'Filters',
      'Save'
    ]}
  />
);
```

### Task-Based Quick Access

Organize by workflow:

```tsx
interface WorkflowQuickAccess {
  basic: string[];
  editing: string[];
  publishing: string[];
}

const workflowAccess: WorkflowQuickAccess = {
  basic: ['Open', 'Undo', 'Redo'],
  editing: ['Crop', 'Rotate', 'Flip', 'Text', 'Filters'],
  publishing: ['Save', 'Export']
};

interface WorkflowState {
  currentPhase: 'basic' | 'editing' | 'publishing';
}

function getQuickAccess(workflow: WorkflowState): string[] {
  return workflowAccess[workflow.currentPhase];
}

const [workflow, setWorkflow] = useState<WorkflowState>({ currentPhase: 'basic' });

return (
  <>
    <ImageEditorComponent
      quickAccessToolbar={getQuickAccess(workflow)}
    />
    <button onClick={() => setWorkflow({ currentPhase: 'editing' })}>
      Enter Edit Mode
    </button>
  </>
);
```

### Role-Based Quick Access

Tailor for user roles:

```tsx
type UserRole = 'viewer' | 'editor' | 'admin';

interface RoleQuickAccess {
  [role in UserRole]: string[];
}

const roleAccess: RoleQuickAccess = {
  viewer: ['Open', 'Zoom In', 'Zoom Out'],
  editor: ['Open', 'Undo', 'Redo', 'Crop', 'Text', 'Save'],
  admin: [
    'Open',
    'Undo',
    'Redo',
    'Crop',
    'Text',
    'Filters',
    'Fine-tune',
    'Frame',
    'Z-Order',
    'Save'
  ]
};

function renderEditor(role: UserRole): JSX.Element {
  return (
    <ImageEditorComponent
      quickAccessToolbar={roleAccess[role]}
    />
  );
}
```

### Contextual Quick Access

Update based on selected tool:

```tsx
const [selectedTool, setSelectedTool] = useState('basic');

const toolQuickAccess: { [key: string]: string[] } = {
  basic: ['Undo', 'Redo', 'Open', 'Save'],
  crop: ['Undo', 'Redo', 'Crop', 'Save'],
  annotate: ['Undo', 'Redo', 'Text', 'Shapes', 'Save'],
  filter: ['Undo', 'Redo', 'Filters', 'Fine-tune', 'Save']
};

return (
  <>
    <div className="tool-selector">
      <button onClick={() => setSelectedTool('basic')}>Basic</button>
      <button onClick={() => setSelectedTool('crop')}>Crop</button>
      <button onClick={() => setSelectedTool('annotate')}>Annotate</button>
      <button onClick={() => setSelectedTool('filter')}>Filter</button>
    </div>
    <ImageEditorComponent
      quickAccessToolbar={toolQuickAccess[selectedTool]}
    />
  </>
);
```

### Keyboard Support

Add keyboard access to quick access items:

```tsx
const quickAccessMap: { [key: string]: () => void } = {
  'Ctrl+U': () => imgObj.undo(),
  'Ctrl+R': () => imgObj.redo(),
  'Ctrl+O': () => openImageDialog(),
  'Ctrl+S': () => saveImage()
};

const handleGlobalKeyDown = (e: KeyboardEvent): void => {
  const shortcut = `${e.ctrlKey ? 'Ctrl+' : ''}${e.key.toUpperCase()}`;
  if (quickAccessMap[shortcut]) {
    e.preventDefault();
    quickAccessMap[shortcut]();
  }
};

useEffect(() => {
  window.addEventListener('keydown', handleGlobalKeyDown);
  return () => window.removeEventListener('keydown', handleGlobalKeyDown);
}, []);
```

## Best Practices

### Recommended Quick Access

Start with these essential items:

```tsx
const recommendedQuickAccess = [
  'Open',
  'Undo',
  'Redo',
  'Crop',
  'Save'
];
```

### Avoid Quick Access Overload

Keep to 5-7 most-used items:

```tsx
// Good - focused on essentials
const goodQuickAccess = ['Undo', 'Redo', 'Crop', 'Save'];

// Avoid - too many items
const poorQuickAccess = [
  'Open', 'Save', 'Undo', 'Redo', 'Crop', 'Rotate',
  'Flip', 'Text', 'Shapes', 'Filters', 'Fine-tune'
];
```

### Performance Optimization

Minimize items in frequently-updated scenarios:

```tsx
const performanceOptimized = ['Undo', 'Redo', 'Save'];
```
