# Reset Image

## Overview

The `reset()` method reverts all edits and returns the image to its original state. Unlike `clearImage()`, which removes the image entirely, `reset()` preserves the loaded image but removes all modifications.

## Reset Image

### Basic Reset

```tsx
function resetImage(): void {
  imgObj.reset();
}
```

### Reset with Confirmation

```tsx
function resetWithConfirmation(): void {
  if (window.confirm('Reset all changes? Original image will be restored.')) {
    imgObj.reset();
  }
}
```

## Use Cases

### Discard All Edits

Cancel editing session:

```tsx
function discardEdits(): void {
  imgObj.reset();
  console.log('All edits discarded, image restored to original');
}
```

### Revert to Original

```tsx
const handleRevertClick = (): void => {
  imgObj.reset();
  updateUIState('edited', false);
};
```

### Start Fresh with Same Image

```tsx
function startOver(): void {
  // Preserve the loaded image, remove all edits
  imgObj.reset();
}
```

### Reset Before Export

```tsx
function exportOriginal(): void {
  // Reset to ensure original is exported
  imgObj.reset();
  
  imgObj.export('image/jpeg', 'original');
}
```

## Advanced Patterns

### Reset with State Tracking

```tsx
class EditorWithReset {
  private isModified: boolean = false;
  
  reset(): void {
    imgObj.reset();
    this.isModified = false;
    this.onResetCallback();
  }
  
  recordEdit(): void {
    this.isModified = true;
  }
  
  private onResetCallback(): void {
    console.log('Image reset to original state');
  }
  
  isEdited(): boolean {
    return this.isModified;
  }
}

const editor = new EditorWithReset();
editor.recordEdit();
editor.reset();
```

### Reset with Undo Alternative

```tsx
function undoAllChanges(): void {
  // Option 1: Reset (faster)
  imgObj.reset();
  
  // Option 2: Multiple undo (slower)
  // for (let i = 0; i < 16; i++) {
  //   imgObj.undo();
  // }
}
```

### Reset with Validation

```tsx
function safeReset(): void {
  const shapes = imgObj.getShapeSettings();
  
  if (shapes.length === 0) {
    console.log('No changes to reset');
    return;
  }
  
  const hasAnnotations = shapes.length > 0;
  
  if (hasAnnotations) {
    const message = 'This will remove all annotations. Continue?';
    if (!confirm(message)) {
      return;
    }
  }
  
  imgObj.reset();
}
```

### Reset with History

```tsx
class ResetHistory {
  private resetEvents: Array<{ timestamp: Date; message: string }> = [];
  
  reset(): void {
    imgObj.reset();
    this.recordReset();
  }
  
  private recordReset(): void {
    this.resetEvents.push({
      timestamp: new Date(),
      message: 'Image reset to original'
    });
  }
  
  getHistory(): string {
    return this.resetEvents
      .map(e => `${e.timestamp.toISOString()}: ${e.message}`)
      .join('\n');
  }
}

const history = new ResetHistory();
history.reset();
console.log(history.getHistory());
```

### Reset with Notification

```tsx
function resetWithNotification(): void {
  imgObj.reset();
  
  showNotification({
    type: 'success',
    message: 'Image reset to original',
    duration: 3000
  });
}

interface Notification {
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration: number;
}

function showNotification(notification: Notification): void {
  const element = document.createElement('div');
  element.className = `notification notification-${notification.type}`;
  element.textContent = notification.message;
  
  document.body.appendChild(element);
  
  setTimeout(() => element.remove(), notification.duration);
}
```

### Reset Specific Edits

```tsx
class SelectiveReset {
  resetAnnotations(): void {
    // Remove all annotations
    const shapes = imgObj.getShapeSettings();
    shapes.forEach(shape => {
      imgObj.deleteShape(shape.id);
    });
  }
  
  resetFilters(): void {
    // Reload without filters
    imgObj.reset();
  }
  
  resetTransforms(): void {
    // Reset rotation, flip, straighten
    imgObj.reset();
  }
  
  resetAll(): void {
    imgObj.reset();
  }
}

const selectiveReset = new SelectiveReset();
selectiveReset.resetAnnotations();
```

### Reset with Auto-save

```tsx
async function resetWithAutoSave(): Promise<void> {
  // Save current state before reset
  const imageData = imgObj.getImageData();
  await saveToBackup(imageData);
  
  // Reset
  imgObj.reset();
}

async function saveToBackup(): Promise<void> {
  // Export and backup current state
  imgObj.export('image/png', 'backup-image');
  
  // Or save metadata
  const dimension = imgObj.getImageDimension();
  localStorage.setItem('backup_metadata', JSON.stringify({
    width: dimension?.width,
    height: dimension?.height,
    timestamp: new Date().toISOString()
  }));
}
```

### Reset in Batch Operations

```tsx
function batchResetEditors(editors: ImageEditor[]): void {
  editors.forEach(editor => {
    editor.reset();
  });
}

// Usage
const editors = [imgObj1, imgObj2, imgObj3];
batchResetEditors(editors);
```

### Reset with Keyboard Shortcut

```tsx
function setupResetShortcut(): void {
  document.addEventListener('keydown', (e: KeyboardEvent) => {
    // Ctrl+Shift+Z or Cmd+Shift+Z
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'z') {
      e.preventDefault();
      resetImage();
    }
  });
}
```

### Reset Timer

```tsx
class AutoResetManager {
  private timer: NodeJS.Timeout | null = null;
  private resetAfterMs: number;
  
  constructor(resetAfterMs: number = 3600000) { // 1 hour
    this.resetAfterMs = resetAfterMs;
  }
  
  start(): void {
    this.timer = setTimeout(() => {
      imgObj.reset();
      console.log('Auto-reset triggered');
    }, this.resetAfterMs);
  }
  
  stop(): void {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
  }
  
  restart(): void {
    this.stop();
    this.start();
  }
}

const autoReset = new AutoResetManager(600000); // 10 minutes
autoReset.start();
```

### Reset with UI Update

```tsx
function resetAndUpdateUI(): void {
  // Reset image
  imgObj.reset();
  
  // Update UI state
  updateEditButton(false);
  updateCancelButton(false);
  updateSaveButton(false);
  clearAnnotationPanel();
  clearHistoryPanel();
  
  setEditMode(false);
}

function updateEditButton(enabled: boolean): void {
  const button = document.querySelector('[data-action="edit"]');
  if (button) {
    (button as HTMLButtonElement).disabled = !enabled;
  }
}
```

### Reset Before/After Lifecycle

```tsx
const handleBeforeReset = (): void => {
  console.log('About to reset...');
};

const handleAfterReset = (): void => {
  console.log('Reset complete');
};

function resetWithLifecycle(): void {
  handleBeforeReset();
  imgObj.reset();
  handleAfterReset();
}
```

### Conditional Reset

```tsx
interface ResetConditions {
  hasChanges: boolean;
  hasAnnotations: boolean;
  hasFilters: boolean;
}

function getResetConditions(): ResetConditions {
  const shapes = imgObj.getShapeSettings();
  
  return {
    hasChanges: shapes.length > 0,
    hasAnnotations: shapes.some(obj => obj.type !== 'Image'),
    hasFilters: false // Would track actual filter state
  };
}

function conditionalReset(): void {
  const conditions = getResetConditions();
  
  if (!conditions.hasChanges) {
    console.log('No changes to reset');
    return;
  }
  
  if (conditions.hasAnnotations) {
    const message = 'Reset will remove annotations. Continue?';
    if (!confirm(message)) {
      return;
    }
  }
  
  imgObj.reset();
}
```

### Reset and Export Comparison

```tsx
class ImageComparison {
  revertToOriginal(): void {
    imgObj.reset();
  }
  
  exportEdited(): void {
    imgObj.export('image/png', 'edited-image');
  }
  
  getDimension(): void {
    const dim = imgObj.getImageDimension();
    console.log('Image dimensions:', dim.width, 'x', dim.height);
  }
}

const comparison = new ImageComparison();
comparison.getDimension();
// ... user edits ...
comparison.exportEdited();
comparison.revertToOriginal();
```
