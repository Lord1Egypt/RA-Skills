# Render Image Editor in Dialog

## Table of Contents

- [Dialog Setup](#dialog-setup)
- [Integration](#integration)
- [Content Template](#content-template)
- [Advanced Patterns](#advanced-patterns)

## Dialog Setup

### Basic Dialog Integration

```tsx
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import { ImageEditorComponent } from '@syncfusion/ej2-react-image-editor';

const ImageEditorDialog = (): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open Editor</button>
      
      <DialogComponent
        visible={isOpen}
        onClose={() => setIsOpen(false)}
        header="Image Editor"
        width="800px"
        height="600px"
      >
        <ImageEditorComponent />
      </DialogComponent>
    </>
  );
};
```

### Dialog with Toolbar

```tsx
const EditorDialogWithToolbar = (): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <>
      <button onClick={() => setIsOpen(true)}>Edit Image</button>
      
      <DialogComponent
        visible={isOpen}
        onClose={() => setIsOpen(false)}
        header="Image Editor"
        width="1000px"
        height="700px"
      >
        <div className="dialog-toolbar">
          <button>Open</button>
          <button>Save</button>
          <button>Close</button>
        </div>
        
        <ImageEditorComponent />
      </DialogComponent>
    </>
  );
};
```

## Integration

### Open Image in Dialog

```tsx
interface DialogEditorProps {
  imageUrl?: string;
  onSave?: (base64: string) => void;
  onClose?: () => void;
}

const ImageEditorDialog: React.FC<DialogEditorProps> = ({
  imageUrl,
  onSave,
  onClose
}) => {
  const [isOpen, setIsOpen] = useState(false);
  let imgObj: ImageEditor;
  
  const handleOpen = (): void => {
    setIsOpen(true);
  };
  
  const handleImageOpened = (): void => {
    if (imageUrl) {
      imgObj.open(imageUrl);
    }
  };
  
  const handleSave = (): void => {
    // Export the current image
    imgObj.export('image/png', 'edited-image');
    if (onSave) {
      // Note: Use getImageData() for direct data access
      const imageData = imgObj.getImageData();
    }
    setIsOpen(false);
  };
  
  const handleClose = (): void => {
    if (onClose) {
      onClose();
    }
    setIsOpen(false);
  };
  
  return (
    <>
      <button onClick={handleOpen}>Edit Image</button>
      
      <DialogComponent
        visible={isOpen}
        onClose={handleClose}
        header="Image Editor"
        width="900px"
        height="700px"
        buttons={[
          {
            buttonModel: { content: 'Save' },
            onClick: handleSave
          },
          {
            buttonModel: { content: 'Cancel' },
            onClick: handleClose
          }
        ]}
      >
        <ImageEditorComponent
          ref={(img) => { imgObj = img; }}
          fileOpened={handleImageOpened}
          width="100%"
          height="100%"
        />
      </DialogComponent>
    </>
  );
};

// Usage
<ImageEditorDialog
  imageUrl="image.jpg"
  onSave={(base64) => console.log('Saved:', base64)}
  onClose={() => console.log('Closed')}
/>
```

### Modal Dialog Pattern

```tsx
const ModalImageEditor = (): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  const [imageData, setImageData] = useState<string | null>(null);
  let imgObj: ImageEditor;
  
  const handleOpen = (imageUrl: string): void => {
    setImageData(imageUrl);
    setIsOpen(true);
  };
  
  const handleApply = (): void => {
    imgObj.export('image/png', 'edited-image');
    console.log('Changes applied and exported');
    setIsOpen(false);
  };
  
  return (
    <>
      <button onClick={() => handleOpen('image.jpg')}>Edit</button>
      
      <DialogComponent
        visible={isOpen}
        onClose={() => setIsOpen(false)}
        isModal={true}
        header="Image Editor"
        width="900px"
        height="700px"
      >
        <ImageEditorComponent
          ref={(img) => { imgObj = img; }}
          created={() => {
            if (imageData) imgObj.open(imageData);
          }}
        />
        
        <div style={{ marginTop: '10px' }}>
          <button onClick={handleApply}>Apply</button>
          <button onClick={() => setIsOpen(false)}>Cancel</button>
        </div>
      </DialogComponent>
    </>
  );
};
```

## Content Template

### Custom Dialog Layout

```tsx
const CustomDialogLayout = (): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  let imgObj: ImageEditor;
  
  return (
    <DialogComponent
      visible={isOpen}
      onClose={() => setIsOpen(false)}
      header="Image Editor"
      width="1200px"
      height="800px"
    >
      <div style={{ display: 'flex', gap: '10px', height: '100%' }}>
        {/* Sidebar */}
        <aside style={{ width: '200px', borderRight: '1px solid #ccc' }}>
          <h3>Tools</h3>
          <ul>
            <li><button>Crop</button></li>
            <li><button>Rotate</button></li>
            <li><button>Text</button></li>
            <li><button>Filters</button></li>
          </ul>
        </aside>
        
        {/* Main Editor */}
        <main style={{ flex: 1 }}>
          <ImageEditorComponent
            ref={(img) => { imgObj = img; }}
            width="100%"
            height="100%"
          />
        </main>
      </div>
    </DialogComponent>
  );
};
```

### Dialog with Preview

```tsx
const DialogWithPreview = (): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  let imgObj: ImageEditor;
  
  const handlePreview = (): void => {
    const imageData = imgObj.getImageData();
    setPreview(imageData ? 'image-data-captured' : null);
  };
  
  return (
    <>
      <DialogComponent
        visible={isOpen}
        onClose={() => setIsOpen(false)}
        header="Image Editor"
        width="1000px"
        height="600px"
      >
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          {/* Editor */}
          <div>
            <ImageEditorComponent
              ref={(img) => { imgObj = img; }}
              width="100%"
              height="500px"
            />
          </div>
          
          {/* Preview */}
          <div>
            <h3>Preview</h3>
            {preview && <img src={preview} alt="Preview" style={{ maxWidth: '100%' }} />}
            <button onClick={handlePreview}>Update Preview</button>
          </div>
        </div>
      </DialogComponent>
    </>
  );
};
```

## Advanced Patterns

### Reusable Dialog Editor

```tsx
class DialogEditorManager {
  private dialog: DialogComponent | null = null;
  private editor: ImageEditor | null = null;
  
  initialize(dialogId: string): void {
    this.dialog = document.querySelector(`#${dialogId}`) as any;
  }
  
  open(imageUrl: string): void {
    if (this.editor) {
      this.editor.open(imageUrl);
    }
    this.dialog?.show?.();
  }
  
  close(): void {
    this.dialog?.hide?.();
  }
  
  exportImage(filename: string = 'edited-image'): void {
    this.editor?.export('image/png', filename);
  }
  
  clear(): void {
    this.editor?.clearImage();
  }
}

const manager = new DialogEditorManager();
manager.initialize('editor-dialog');
manager.open('image.jpg');
```

### Multiple Dialogs

```tsx
interface EditorDialogState {
  id: string;
  isOpen: boolean;
  imageUrl: string;
}

const MultipleDialogEditor = (): JSX.Element => {
  const [dialogs, setDialogs] = useState<EditorDialogState[]>([]);
  
  const addDialog = (): void => {
    setDialogs([
      ...dialogs,
      { id: `dialog-${Date.now()}`, isOpen: true, imageUrl: '' }
    ]);
  };
  
  return (
    <>
      <button onClick={addDialog}>Add Editor</button>
      
      {dialogs.map(dialog => (
        <DialogComponent
          key={dialog.id}
          visible={dialog.isOpen}
          onClose={() => {
            setDialogs(dialogs.filter(d => d.id !== dialog.id));
          }}
        >
          <ImageEditorComponent width="100%" height="100%" />
        </DialogComponent>
      ))}
    </>
  );
};
```

### Dialog with Upload

```tsx
const DialogWithUpload = (): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  let imgObj: ImageEditor;
  
  const handleFileUpload = (e: ChangeEvent<HTMLInputElement>): void => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        imgObj.open(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };
  
  return (
    <>
      <DialogComponent
        visible={isOpen}
        onClose={() => setIsOpen(false)}
        header="Image Editor"
      >
        <input
          type="file"
          accept="image/*"
          onChange={handleFileUpload}
        />
        
        <ImageEditorComponent
          ref={(img) => { imgObj = img; }}
          width="100%"
          height="500px"
        />
      </DialogComponent>
    </>
  );
};
```

### Dialog with Tabs

```tsx
const DialogWithTabs = (): JSX.Element => {
  const [activeTab, setActiveTab] = useState(0);
  let imgObj: ImageEditor;
  
  return (
    <DialogComponent header="Image Editor" width="900px" height="700px">
      <div className="tabs">
        <button
          className={activeTab === 0 ? 'active' : ''}
          onClick={() => setActiveTab(0)}
        >
          Editor
        </button>
        <button
          className={activeTab === 1 ? 'active' : ''}
          onClick={() => setActiveTab(1)}
        >
          Effects
        </button>
        <button
          className={activeTab === 2 ? 'active' : ''}
          onClick={() => setActiveTab(2)}
        >
          Settings
        </button>
      </div>
      
      {activeTab === 0 && (
        <ImageEditorComponent
          ref={(img) => { imgObj = img; }}
          width="100%"
          height="500px"
        />
      )}
      
      {activeTab === 1 && (
        <div>
          <p>Filter Controls</p>
          {/* Filter UI */}
        </div>
      )}
      
      {activeTab === 2 && (
        <div>
          <p>Settings</p>
          {/* Settings UI */}
        </div>
      )}
    </DialogComponent>
  );
};
```

### Dialog Size Management

```tsx
interface DialogSize {
  width: string;
  height: string;
}

const ResponsiveDialog = (): JSX.Element => {
  const [size, setSize] = useState<DialogSize>({ width: '80%', height: '80vh' });
  
  const getDialogSize = (): DialogSize => {
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    if (width < 768) {
      return { width: '95%', height: '95vh' };
    } else if (width < 1024) {
      return { width: '85%', height: '85vh' };
    } else {
      return { width: '80%', height: '80vh' };
    }
  };
  
  useEffect(() => {
    setSize(getDialogSize());
    const handleResize = (): void => setSize(getDialogSize());
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  return (
    <DialogComponent
      width={size.width}
      height={size.height}
      header="Image Editor"
    >
      <ImageEditorComponent width="100%" height="100%" />
    </DialogComponent>
  );
};
```

### Dialog State Persistence

```tsx
const PersistentDialog = (): JSX.Element => {
  const [dialogState, setDialogState] = useState(() => {
    const saved = localStorage.getItem('editorDialogState');
    return saved ? JSON.parse(saved) : { isOpen: false };
  });
  
  const updateDialogState = (state: any): void => {
    setDialogState(state);
    localStorage.setItem('editorDialogState', JSON.stringify(state));
  };
  
  return (
    <DialogComponent
      visible={dialogState.isOpen}
      onClose={() => updateDialogState({ isOpen: false })}
      onOpen={() => updateDialogState({ isOpen: true })}
    >
      <ImageEditorComponent width="100%" height="100%" />
    </DialogComponent>
  );
};
```
