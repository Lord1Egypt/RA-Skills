# Clear Image

## Overview

The `clearImage()` method resets the Image Editor to a blank state, removing all images and clearing the canvas.

## Clear Image

### Basic Clear

```tsx
function clearCurrentImage(): void {
  imgObj.clearImage();
}
```

### With Confirmation

```tsx
function clearWithConfirmation(): void {
  if (window.confirm('Are you sure you want to clear the image? This action cannot be undone.')) {
    imgObj.clearImage();
  }
}
```

## Use Cases

### Reset After Save

Clear image after exporting:

```tsx
async function exportAndClear(): Promise<void> {
  // Save image
  imgObj.export('image/png', 'edited-image');
  
  // Clear editor
  imgObj.clearImage();
}
```

### Prepare for New Image

Clear before opening new file:

```tsx
function openNewImage(imageUrl: string): void {
  // Clear existing
  imgObj.clearImage();
  
  // Load new
  imgObj.open(imageUrl);
}
```

### Undo All Changes

Reset to blank state:

```tsx
function clearAllChanges(): void {
  imgObj.clearImage();
}
```

## Advanced Patterns

### Clear with Dialog Confirmation

```tsx
function clearImageWithDialog(): void {
  const userChoice = confirm(
    'Clear current image?\n\nThis will remove all edits and annotations.'
  );
  
  if (userChoice) {
    imgObj.clearImage();
    logAction('Image cleared');
  }
}
```

### Clear Specific Elements

```tsx
// Clear all annotations but keep the image
function clearAnnotations(): void {
  const shapes = imgObj.getShapeSettings();
  shapes.forEach(shape => {
    imgObj.deleteShape(shape.id);
  });
}

// Clear specific shape types
function clearRectangles(): void {
  const shapes = imgObj.getShapeSettings();
  shapes
    .filter(s => s.type === 'Rectangle')
    .forEach(s => imgObj.deleteShape(s.id));
}
```

### Clear with Undo Support

```tsx
function clearImageWithUndo(): void {
  // Image Editor's undo will handle this
  imgObj.clearImage();
  
  // User can press Ctrl+Z to redo
}
```

### Batch Clear

```tsx
function clearMultipleEditors(editors: ImageEditor[]): void {
  editors.forEach(editor => {
    editor.clearImage();
  });
}
```

### Smart Clear with Shape Check

```tsx
function smartClear(): void {
  const shapes = imgObj.getShapeSettings();
  
  if (shapes.length === 0) {
    // Already empty
    console.log('Nothing to clear');
    return;
  }
  
  if (!confirm('Clear all content?')) {
    return;
  }
  
  imgObj.clearImage();
}
```

### Clear with State Tracking

```tsx
class EditorState {
  private hasContent: boolean = false;
  
  setContent(hasContent: boolean): void {
    this.hasContent = hasContent;
  }
  
  clear(): void {
    if (this.hasContent) {
      imgObj.clearImage();
      this.hasContent = false;
    }
  }
  
  hasContent(): boolean {
    return this.hasContent;
  }
}

const state = new EditorState();
state.setContent(true);
state.clear();
```

### Dialog-Based Editor Pattern

```tsx
interface DialogEditorConfig {
  containerId: string;
  dialogId: string;
  reuseEditor: boolean;
}

function renderImageEditorDialog(config: DialogEditorConfig): void {
  const dialogElement = document.getElementById(config.dialogId);
  
  if (!dialogElement) return;
  
  // Create or reuse editor instance
  if (config.reuseEditor) {
    // Clear existing content
    imgObj.clearImage();
  } else {
    // Create new instance
    // imgObj = new ImageEditor();
  }
  
  // Show dialog
  if ('show' in dialogElement && typeof dialogElement.show === 'function') {
    (dialogElement as any).show();
  }
}

// Usage
const editorConfig: DialogEditorConfig = {
  containerId: 'editor-container',
  dialogId: 'editor-dialog',
  reuseEditor: true
};

renderImageEditorDialog(editorConfig);
```

### Auto-Clear on Timer

```tsx
function autoClearAfterDelay(delayMs: number = 300000): void {
  // Auto-clear after 5 minutes of inactivity
  let timeoutId: NodeJS.Timeout | null = null;
  
  const resetTimer = (): void => {
    if (timeoutId) clearTimeout(timeoutId);
    
    timeoutId = setTimeout(() => {
      if (confirm('Clear inactive editor?')) {
        imgObj.clearImage();
      }
    }, delayMs);
  };
  
  document.addEventListener('mousemove', resetTimer);
  document.addEventListener('keypress', resetTimer);
}
```

### Clear with Notification

```tsx
function clearImageWithNotification(): void {
  imgObj.clearImage();
  
  // Notify user
  showNotification({
    type: 'info',
    message: 'Image cleared',
    duration: 3000
  });
}

interface Notification {
  type: 'info' | 'warning' | 'error' | 'success';
  message: string;
  duration: number;
}

function showNotification(notification: Notification): void {
  const element = document.createElement('div');
  element.className = `notification notification-${notification.type}`;
  element.textContent = notification.message;
  element.setAttribute('role', 'status');
  element.setAttribute('aria-live', 'polite');
  
  document.body.appendChild(element);
  
  setTimeout(() => element.remove(), notification.duration);
}
```

### Conditional Clear

```tsx
interface ClearConditions {
  hasAnnotations: boolean;
  hasShapes: boolean;
}

function getClearConditions(): ClearConditions {
  const shapes = imgObj.getShapeSettings();
  
  return {
    hasAnnotations: shapes.length > 0,
    hasShapes: shapes.length > 0
  };
}

function conditionalClear(): void {
  const conditions = getClearConditions();
  
  if (conditions.hasAnnotations) {
    if (confirm('Clear all annotations?')) {
      imgObj.clearImage();
    }
  } else {
    console.log('No annotations to clear');
  }
}
```

### Clear with History Export

```tsx
class EditorWithHistory {
  private history: Array<{ timestamp: Date; action: string }> = [];
  
  clear(): void {
    this.history.push({
      timestamp: new Date(),
      action: 'Image cleared'
    });
    
    imgObj.clearImage();
  }
  
  exportHistory(): string {
    return this.history
      .map(entry => `${entry.timestamp.toISOString()}: ${entry.action}`)
      .join('\n');
  }
}

const editorWithHistory = new EditorWithHistory();
editorWithHistory.clear();
console.log(editorWithHistory.exportHistory());
```
