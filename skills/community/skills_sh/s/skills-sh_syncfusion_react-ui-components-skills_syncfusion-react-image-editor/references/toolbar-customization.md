# Toolbar Customization

## Built-in Toolbar Items

The Image Editor includes these default toolbar items:

- **File**: Open, Save
- **Edit**: Undo, Redo
- **Transform**: Rotate, Flip, Straighten
- **Zoom**: Zoom In/Out, Fit to Width/Height, Reset
- **Crop & Resize**: Crop, Resize
- **Annotation**: Text, Shapes (Rectangle, Ellipse, Line, Arrow), Freehand
- **Filters**: Chrome, Cold, Warm, Grayscale, Sepia, Invert
- **Fine-tune**: Brightness, Contrast, Saturation, Hue, Exposure, Blur, Opacity
- **Other**: Frame, Z-Order, Redact

## Customize Built-in Items

### Show/Hide Items

Control toolbar visibility:

```tsx
const imageEditor = (
  <ImageEditorComponent
    toolbar={['Open', 'Save', 'Undo', 'Redo', 'Crop', 'Rotate', 'Flip']}
  />
);
```

### Item Arrangement

Reorder toolbar items:

```tsx
const imageEditor = (
  <ImageEditorComponent
    toolbar={[
      'Open',
      'Save',
      'Undo',
      'Redo',
      'Zoom In',
      'Zoom Out',
      'Reset Transform',
      'Crop',
      'Text',
      'Shapes',
      'Filters'
    ]}
  />
);
```

### Grouped Items

Use separators:

```tsx
const imageEditor = (
  <ImageEditorComponent
    toolbar={[
      'Open',
      'Save',
      '|', // Separator
      'Undo',
      'Redo',
      '|',
      'Crop',
      'Rotate',
      'Flip'
    ]}
  />
);
```

## Custom Toolbar Items

### Add Custom Button

Insert custom actions:

```tsx
const customToolbar = [
  'Open',
  'Save',
  {
    id: 'custom-reset',
    tooltipText: 'Reset to Original',
    text: 'Reset',
    prefixIcon: 'e-icon-refresh'
  },
  {
    id: 'custom-export',
    tooltipText: 'Export as PNG',
    text: 'Export',
    prefixIcon: 'e-icon-export'
  }
];

const imageEditor = (
  <ImageEditorComponent toolbar={customToolbar} />
);
```

### Custom Button with Event

Handle custom toolbar actions:

```tsx
const handleCustomAction = (args: any): void => {
  switch (args.id) {
    case 'custom-reset':
      imgObj.reset();
      break;
    case 'custom-export':
      imgObj.export('image/png', 'edited-image');
      break;
  }
};

const customToolbar = [
  {
    id: 'custom-reset',
    text: 'Reset',
    prefixIcon: 'e-icon-refresh'
  }
];

const imageEditor = (
  <ImageEditorComponent
    toolbar={customToolbar}
    toolbarItemClick={handleCustomAction}
  />
);
```

### Custom Icon

Use custom SVG or CSS class:

```tsx
const customToolbar = [
  {
    id: 'custom-print',
    tooltipText: 'Print Image',
    prefixIcon: 'custom-print-icon', // Custom CSS class
    align: 'Left'
  },
  {
    id: 'custom-email',
    text: 'Email',
    prefixIcon: 'e-icon-email'
  }
];

// CSS
const styles = `
  .custom-print-icon::before {
    content: '🖨️';
  }
`;
```

## Contextual Toolbar

### Show/Hide Based on State

Toggle toolbar items dynamically:

```tsx
const [editMode, setEditMode] = useState(false);
const [showAdvanced, setShowAdvanced] = useState(false);

const baseToolbar = ['Open', 'Save', 'Undo', 'Redo'];
const editingToolbar = [...baseToolbar, 'Crop', 'Rotate', 'Flip', 'Text'];
const advancedToolbar = [
  ...editingToolbar,
  'Filters',
  'Fine-tune',
  'Frame'
];

const currentToolbar = showAdvanced ? advancedToolbar : editMode ? editingToolbar : baseToolbar;

return (
  <>
    <ImageEditorComponent toolbar={currentToolbar} />
    <button onClick={() => setEditMode(!editMode)}>Toggle Edit Mode</button>
    <button onClick={() => setShowAdvanced(!showAdvanced)}>Toggle Advanced</button>
  </>
);
```

### Context-Sensitive Items

Enable/disable based on selection:

```tsx
const handleSelectionChange = (args: any): void => {
  // Update toolbar based on selection
  const hasText = checkForTextAnnotations();
  const toolbar = hasText
    ? ['Open', 'Save', 'Delete Selection', 'Edit Text', 'Filters']
    : ['Open', 'Save', 'Crop', 'Rotate'];
};
```

## Toolbar Positioning

### Align Items

Set item alignment:

```tsx
const customToolbar = [
  {
    id: 'open',
    text: 'Open',
    align: 'Left'
  },
  {
    id: 'undo',
    text: 'Undo',
    align: 'Left'
  },
  {
    id: 'help',
    text: 'Help',
    align: 'Right'
  }
];

const imageEditor = (
  <ImageEditorComponent toolbar={customToolbar} />
);
```

## Toolbar Events

### Toolbar Item Click

Capture toolbar interactions:

```tsx
const handleToolbarClick = (args: ToolbarClickEventArgs): void => {
  console.log('Toolbar item clicked:', args.id);
  
  if (args.id === 'open') {
    openImageDialog();
  } else if (args.id === 'save') {
    saveImage();
  }
};

const imageEditor = (
  <ImageEditorComponent toolbarItemClick={handleToolbarClick} />
);
```

### Before Toolbar Render

Modify toolbar before display:

```tsx
const handleBeforeRender = (args: any): void => {
  // Add custom properties or modify items
  args.toolbarItems.forEach((item: any) => {
    if (item.id === 'custom-reset') {
      item.enabled = false; // Disable initially
    }
  });
};
```

## Advanced Toolbar Patterns

### Dynamic Toolbar

Update toolbar based on loaded image:

```tsx
const [imageLoaded, setImageLoaded] = useState(false);
let imgObj: ImageEditor;

const handleImageOpened = (): void => {
  setImageLoaded(true);
  // Show editing tools only after image loads
};

const toolbar = imageLoaded
  ? ['Open', 'Save', 'Undo', 'Redo', 'Crop', 'Rotate', 'Text', 'Filters']
  : ['Open'];

return (
  <ImageEditorComponent
    toolbar={toolbar}
    fileOpened={handleImageOpened}
    ref={(img) => { imgObj = img; }}
  />
);
```

### Toolbar with Dropdowns

Multi-option toolbar items:

```tsx
const customToolbar = [
  {
    id: 'open',
    text: 'Open',
    prefixIcon: 'e-icon-open'
  },
  {
    id: 'transform-menu',
    text: 'Transform',
    prefixIcon: 'e-icon-transform',
    items: [
      { id: 'rotate-90', text: 'Rotate 90°' },
      { id: 'rotate-180', text: 'Rotate 180°' },
      { id: 'flip-h', text: 'Flip Horizontal' }
    ]
  }
];

const handleDropdownSelect = (args: any): void => {
  switch (args.id) {
    case 'rotate-90':
      imgObj.rotate(90);
      break;
    case 'rotate-180':
      imgObj.rotate(180);
      break;
  }
};
```

### Keyboard Shortcuts for Toolbar

Map keyboard to toolbar:

```tsx
const handleKeyDown = (e: KeyboardEvent): void => {
  if (e.ctrlKey) {
    switch (e.key) {
      case 'o':
        e.preventDefault();
        // Trigger open action
        break;
      case 's':
        e.preventDefault();
        // Trigger save action
        break;
      case 'e':
        e.preventDefault();
        // Trigger export action
        break;
    }
  }
};

document.addEventListener('keydown', handleKeyDown);
```

### Conditional Toolbar Loading

Load toolbar based on permissions:

```tsx
interface UserPermissions {
  canEdit: boolean;
  canDelete: boolean;
  canExport: boolean;
}

function getToolbarForUser(permissions: UserPermissions): string[] {
  const toolbar = ['Open', 'Undo', 'Redo'];
  
  if (permissions.canEdit) {
    toolbar.push('Crop', 'Rotate', 'Flip', 'Text');
  }
  
  if (permissions.canDelete) {
    toolbar.push('Delete');
  }
  
  if (permissions.canExport) {
    toolbar.push('Save');
  }
  
  return toolbar;
}

const userPermissions: UserPermissions = {
  canEdit: true,
  canDelete: false,
  canExport: true
};

const toolbar = getToolbarForUser(userPermissions);
const imageEditor = (
  <ImageEditorComponent toolbar={toolbar} />
);
```
