# Nested Items - File Manager Inside Other Components

The React File Manager component can be rendered inside other Syncfusion components like Dialog, Tab, Splitter, and more. This enables creating advanced UI layouts where file management is embedded within other interactive elements.

## Table of Contents

1. [File Manager in Dialog](#file-manager-in-dialog)
2. [File Manager in Tab](#file-manager-in-tab)
3. [File Manager in Splitter](#file-manager-in-splitter)
4. [File Manager in Modal](#file-manager-in-modal)
5. [Best Practices](#best-practices)

## File Manager in Dialog

### Pattern 1: Simple Dialog with File Manager

```typescript
import React, { useRef } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function FileManagerInDialogExample() {
  const dialogRef = useRef(null);
  const fileManagerRef = useRef(null);
  const hostUrl = "url";

  const handleOpenDialog = () => {
    dialogRef.current?.show?.();
  };

  const handleDialogClose = () => {
    // Reset file manager when dialog closes
    fileManagerRef.current?.path = "/";
    fileManagerRef.current?.refresh?.();
  };

  return (
    <div className="control-section">
      <ButtonComponent onClick={handleOpenDialog} cssClass='e-success'>
        Open File Browser
      </ButtonComponent>

      <DialogComponent
        ref={dialogRef}
        width='800px'
        height='600px'
        header="File Browser"
        content="Select a file from the File Manager"
        showCloseIcon={true}
        close={handleDialogClose}
      >
        <FileManagerComponent
          ref={fileManagerRef}
          id="file-manager-in-dialog"
          height="500px"
          view="Details"
          ajaxSettings={{
            url: hostUrl + 'api/FileManager/FileOperations',
            downloadUrl: hostUrl + 'api/FileManager/Download',
            uploadUrl: hostUrl + 'api/FileManager/Upload',
            getImageUrl: hostUrl + 'api/FileManager/GetImage'
          }}
        >
          <Inject services={[NavigationPane, DetailsView, Toolbar]} />
        </FileManagerComponent>
      </DialogComponent>
    </div>
  );
}

export default FileManagerInDialogExample;
```

### Pattern 2: File Selector with Dialog

```typescript
import React, { useRef, useState } from 'react';
import { DialogComponent, AnimationSettingsModel } from '@syncfusion/ej2-react-popups';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function FileSelectorDialogExample() {
  const dialogRef = useRef(null);
  const fileManagerRef = useRef(null);
  const uploaderRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const hostUrl = "url";
  const animationSettings = { effect: 'None' };

  const handleFileOpen = (args) => {
    const file = args.fileDetails;
    
    // Only select files, not folders
    if (file.isFile) {
      args.cancel = true;
      
      // Set file to uploader
      if (file.size <= 0) file.size = 10000;
      uploaderRef.current.files = [{
        name: file.name,
        size: file.size,
        type: file.type
      }];
      
      // Close dialog and show uploader
      dialogRef.current?.hide?.();
      setSelectedFile(file.name);
    }
  };

  const handleOpenDialog = () => {
    dialogRef.current?.show?.();
    fileManagerRef.current.path = "/";
    fileManagerRef.current?.refresh?.();
  };

  const handleDialogClose = () => {
    // Dialog closed
  };

  return (
    <div className="control-section">
      <div style={{ marginBottom: '20px' }}>
        <div style={{ marginBottom: '10px' }}>
          <label>Selected File: <strong>{selectedFile || 'None'}</strong></label>
        </div>
        <ButtonComponent onClick={handleOpenDialog} cssClass='e-success'>
          Browse Files
        </ButtonComponent>
      </div>

      <UploaderComponent
        ref={uploaderRef}
        id="file-upload"
        type="file"
      />

      <DialogComponent
        ref={dialogRef}
        width='900px'
        height='650px'
        header="Select a File"
        target="body"
        showCloseIcon={true}
        visible={false}
        open={() => {}}
        close={handleDialogClose}
        animationSettings={animationSettings}
      >
        <FileManagerComponent
          ref={fileManagerRef}
          id="dialog-file-manager"
          height="500px"
          view="Details"
          allowMultiSelection={false}
          ajaxSettings={{
            url: hostUrl + 'api/FileManager/FileOperations',
            downloadUrl: hostUrl + 'api/FileManager/Download',
            uploadUrl: hostUrl + 'api/FileManager/Upload',
            getImageUrl: hostUrl + 'api/FileManager/GetImage'
          }}
          fileOpen={handleFileOpen}
          toolbarSettings={{
            items: ['NewFolder', 'Upload', 'Delete', 'Cut', 'Copy', 'Rename', 'SortBy', 'Refresh', 'View', 'Details']
          }}
        >
          <Inject services={[NavigationPane, DetailsView, Toolbar]} />
        </FileManagerComponent>
      </DialogComponent>
    </div>
  );
}

export default FileSelectorDialogExample;
```

## File Manager in Tab

### Pattern 1: Separate Tab for File Manager

```typescript
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function FileManagerInTabExample() {
  const hostUrl = "url";

  return (
    <div className="control-section">
      <TabComponent>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Overview' }} content="Welcome to the application" />
          
          <TabItemDirective header={{ text: 'File Manager' }}>
            <FileManagerComponent
              id="tab-file-manager"
              height="500px"
              view="Details"
              ajaxSettings={{
                url: hostUrl + 'api/FileManager/FileOperations',
                downloadUrl: hostUrl + 'api/FileManager/Download',
                uploadUrl: hostUrl + 'api/FileManager/Upload',
                getImageUrl: hostUrl + 'api/FileManager/GetImage'
              }}
            >
              <Inject services={[NavigationPane, DetailsView, Toolbar]} />
            </FileManagerComponent>
          </TabItemDirective>
          
          <TabItemDirective header={{ text: 'Settings' }} content="Application Settings" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}

export default FileManagerInTabExample;
```

## File Manager in Splitter

### Pattern 1: File Manager in Splitter Pane

```typescript
import React from 'react';
import { SplitterComponent, SplitterItemsDirective, SplitterItemDirective } from '@syncfusion/ej2-react-layouts';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function FileManagerInSplitterExample() {
  const hostUrl = "url";

  return (
    <div className="control-section">
      <SplitterComponent style={{ height: '600px' }}>
        <SplitterItemsDirective>
          <SplitterItemDirective size='40%' min='200px' max='600px' collapsible={true}>
            <div style={{ padding: '10px' }}>
              <h3>Preview</h3>
              <div style={{ height: '400px', border: '1px solid #ddd', padding: '10px' }}>
                Preview content will appear here
              </div>
            </div>
          </SplitterItemDirective>
          
          <SplitterItemDirective size='60%' min='300px' collapsible={true}>
            <FileManagerComponent
              id="splitter-file-manager"
              height="550px"
              view="Details"
              ajaxSettings={{
                url: hostUrl + 'api/FileManager/FileOperations',
                downloadUrl: hostUrl + 'api/FileManager/Download',
                uploadUrl: hostUrl + 'api/FileManager/Upload',
                getImageUrl: hostUrl + 'api/FileManager/GetImage'
              }}
            >
              <Inject services={[NavigationPane, DetailsView, Toolbar]} />
            </FileManagerComponent>
          </SplitterItemDirective>
        </SplitterItemsDirective>
      </SplitterComponent>
    </div>
  );
}

export default FileManagerInSplitterExample;
```

## File Manager in Modal

### Pattern 1: Bootstrap Modal with File Manager

```typescript
import React, { useRef } from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function FileManagerInModalExample() {
  const fileManagerRef = useRef(null);
  const hostUrl = "url";

  const handleOpenModal = () => {
    const modal = document.getElementById('fileManagerModal');
    modal?.classList?.add('show');
    modal?.style?.setProperty('display', 'block');
  };

  const handleCloseModal = () => {
    const modal = document.getElementById('fileManagerModal');
    modal?.classList?.remove('show');
    modal?.style?.setProperty('display', 'none');
  };

  return (
    <div className="control-section">
      <ButtonComponent onClick={handleOpenModal} cssClass='e-success'>
        Open File Manager Modal
      </ButtonComponent>

      {/* Modal */}
      <div
        id="fileManagerModal"
        style={{
          display: 'none',
          position: 'fixed',
          zIndex: '1000',
          left: '0',
          top: '0',
          width: '100%',
          height: '100%',
          backgroundColor: 'rgba(0,0,0,0.4)',
          paddingTop: '50px'
        }}
      >
        <div style={{
          backgroundColor: '#fefefe',
          margin: 'auto',
          padding: '0',
          border: '1px solid #888',
          width: '900px',
          height: '600px',
          borderRadius: '4px',
          display: 'flex',
          flexDirection: 'column'
        }}>
          {/* Modal Header */}
          <div style={{
            padding: '20px',
            borderBottom: '1px solid #ddd',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <h2>File Manager</h2>
            <button
              style={{
                fontSize: '28px',
                fontWeight: 'bold',
                border: 'none',
                backgroundColor: 'transparent',
                cursor: 'pointer'
              }}
              onClick={handleCloseModal}
            >
              ×
            </button>
          </div>

          {/* Modal Body */}
          <div style={{ flex: '1', overflow: 'hidden', padding: '10px' }}>
            <FileManagerComponent
              ref={fileManagerRef}
              id="modal-file-manager"
              height="calc(100% - 20px)"
              view="Details"
              ajaxSettings={{
                url: hostUrl + 'api/FileManager/FileOperations',
                downloadUrl: hostUrl + 'api/FileManager/Download',
                uploadUrl: hostUrl + 'api/FileManager/Upload',
                getImageUrl: hostUrl + 'api/FileManager/GetImage'
              }}
            >
              <Inject services={[NavigationPane, DetailsView, Toolbar]} />
            </FileManagerComponent>
          </div>

          {/* Modal Footer */}
          <div style={{
            padding: '15px',
            borderTop: '1px solid #ddd',
            textAlign: 'right'
          }}>
            <ButtonComponent onClick={handleCloseModal} cssClass='e-danger'>
              Close
            </ButtonComponent>
          </div>
        </div>
      </div>
    </div>
  );
}

export default FileManagerInModalExample;
```

## Complete Example - Multi-Panel Layout

```typescript
import React, { useRef, useState } from 'react';
import { SplitterComponent, SplitterItemsDirective, SplitterItemDirective } from '@syncfusion/ej2-react-layouts';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function AdvancedNestedLayoutExample() {
  const fileManagerRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const hostUrl = "url";

  const handleFileSelect = (args) => {
    const selectedItems = fileManagerRef.current?.getSelectedFiles?.();
    if (selectedItems?.length === 1) {
      setSelectedFile(selectedItems[0]);
    }
  };

  const treeData = [
    {
      nodeId: 'root',
      nodeText: 'My Files',
      expanded: true,
      child: [
        { nodeId: 'documents', nodeText: 'Documents' },
        { nodeId: 'images', nodeText: 'Images' },
        { nodeId: 'videos', nodeText: 'Videos' },
        { nodeId: 'downloads', nodeText: 'Downloads' },
        { nodeId: 'archive', nodeText: 'Archive' }
      ]
    }
  ];

  return (
    <div className="control-section" style={{ height: '700px' }}>
      <SplitterComponent style={{ height: '100%' }}>
        <SplitterItemsDirective>
          {/* Left Sidebar */}
          <SplitterItemDirective size='20%' min='150px' max='400px' collapsible={true}>
            <div style={{ padding: '10px', height: '100%', overflow: 'auto' }}>
              <h4>Navigation</h4>
              <TreeViewComponent
                fields={{ dataSource: treeData, id: 'nodeId', text: 'nodeText', child: 'child' }}
              />
            </div>
          </SplitterItemDirective>

          {/* Main Content */}
          <SplitterItemDirective size='80%' min='400px'>
            <TabComponent>
              <TabItemsDirective>
                <TabItemDirective header={{ text: 'Files' }}>
                  <FileManagerComponent
                    ref={fileManagerRef}
                    id="nested-file-manager"
                    height="550px"
                    view="Details"
                    allowMultiSelection={true}
                    ajaxSettings={{
                      url: hostUrl + 'api/FileManager/FileOperations',
                      downloadUrl: hostUrl + 'api/FileManager/Download',
                      uploadUrl: hostUrl + 'api/FileManager/Upload',
                      getImageUrl: hostUrl + 'api/FileManager/GetImage'
                    }}
                    fileSelect={handleFileSelect}
                  >
                    <Inject services={[NavigationPane, DetailsView, Toolbar]} />
                  </FileManagerComponent>
                </TabItemDirective>

                <TabItemDirective header={{ text: 'Details' }}>
                  <div style={{ padding: '20px' }}>
                    <h3>File Details</h3>
                    {selectedFile ? (
                      <div>
                        <p><strong>File Name:</strong> {selectedFile}</p>
                        <p><strong>Path:</strong> {fileManagerRef.current?.path || '/'}</p>
                      </div>
                    ) : (
                      <p>Select a file to view details</p>
                    )}
                  </div>
                </TabItemDirective>

                <TabItemDirective header={{ text: 'Preview' }}>
                  <div style={{ padding: '20px' }}>
                    <h3>File Preview</h3>
                    <div style={{
                      border: '1px solid #ddd',
                      padding: '20px',
                      minHeight: '300px',
                      backgroundColor: '#f9f9f9'
                    }}>
                      {selectedFile ? (
                        <p>Preview for: {selectedFile}</p>
                      ) : (
                        <p>Select a file to preview</p>
                      )}
                    </div>
                  </div>
                </TabItemDirective>
              </TabItemsDirective>
            </TabComponent>
          </SplitterItemDirective>
        </SplitterItemsDirective>
      </SplitterComponent>
    </div>
  );
}

export default AdvancedNestedLayoutExample;
```

## Best Practices

1. **Container Height** - Always set explicit heights for nested components
2. **Refresh on Open** - Reset file manager path when opening parent component
3. **Single Selection** - Use allowMultiSelection={false} in dialogs
4. **State Management** - Properly manage selected items and paths
5. **Performance** - Avoid rendering multiple file managers unnecessarily
6. **Responsive Design** - Ensure nested layouts work on different screen sizes

## Related Topics

- [Customization](customization.md)
- [Views and Navigation](views-and-navigation.md)
- [File Operations](file-operations.md)
- [Getting Started](getting-started.md)
