---
name: file-attachments
description: Enable file attachments in Chat-UI with upload, download, file type restrictions, and custom templates.
---

# File Attachments

## Table of Contents
- [Enable Attachments](#enable-attachments)
- [Configure Upload Endpoints](#configure-upload-endpoints)
- [File Type Restrictions](#file-type-restrictions)
- [File Size Restrictions](#file-size-restrictions)
- [Attachment Templates](#attachment-templates)
- [Attachment Click Event](#attachment-click-event)
- [Drag and Drop](#drag-and-drop)

## Enable Attachments

### Basic Attachment Support

Enable file attachment functionality:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
        />
    );
}
```

## Configure Upload Endpoints

### Set Save and Remove URLs

Configure server endpoints for file operations:

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove'
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

### Custom Server Implementation

```tsx
// Example backend endpoint for Node.js/Express
app.post('/api/upload', (req, res) => {
    // Handle file upload
    const file = req.files.upload;
    const uploadPath = path.join(__dirname, 'uploads', file.name);
    
    file.mv(uploadPath, (err) => {
        if (err) {
            res.status(500).json({ error: 'Upload failed' });
        } else {
            res.json({ name: file.name, size: file.size, url: `/uploads/${file.name}` });
        }
    });
});

app.post('/api/remove', (req, res) => {
    // Handle file removal
    const fileName = req.body.fileName;
    const filePath = path.join(__dirname, 'uploads', fileName);
    
    fs.unlink(filePath, (err) => {
        if (err) {
            res.status(500).json({ error: 'Delete failed' });
        } else {
            res.json({ success: true });
        }
    });
});
```

## File Type Restrictions

### Allowed File Types

Restrict uploads to specific file types:

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        allowedFileTypes: '.pdf, .docx, .xlsx, .txt, .jpg, .png'
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

### Images Only

```tsx
const attachmentSettings: FileAttachmentSettingsModel = {
    allowedFileTypes: '.jpg, .jpeg, .png, .gif, .webp'
};
```

### Documents Only

```tsx
const attachmentSettings: FileAttachmentSettingsModel = {
    allowedFileTypes: '.pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx'
};
```

## File Size Restrictions

### Maximum File Size

Limit upload file size (in bytes):

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        maxFileSize: 5242880  // 5MB
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

### Common Size Limits

```tsx
// 1MB
maxFileSize: 1048576

// 10MB
maxFileSize: 10485760

// 50MB
maxFileSize: 52428800

// 100MB
maxFileSize: 104857600
```

### Maximum File Count

Limit number of files per message:

```tsx
const attachmentSettings: FileAttachmentSettingsModel = {
    maximumCount: 5  // Maximum 5 files per upload
};
```

## Attachment Templates

### Preview Template

Customize how attachments appear before upload:

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const PreviewTemplate = (props: { selectedFile: any }) => {
        const file = props.selectedFile;
        const isImage = file.type?.startsWith('image/');
        
        return (
            <div style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '12px',
                marginBottom: '8px'
            }}>
                <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>
                    {file.name}
                </div>
                {isImage && (
                    <img 
                        src={file.fileSource} 
                        alt={file.name}
                        style={{ maxWidth: '200px', maxHeight: '200px' }}
                    />
                )}
                <div style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>
                    Size: {(file.size / 1024).toFixed(2)} KB
                </div>
            </div>
        );
    };

    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        previewTemplate: PreviewTemplate
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

### Attachment Display Template

Customize how attachments appear in messages:

```tsx
const AttachmentTemplate = (props: { selectedFile: any }) => {
    const file = props.selectedFile;
    const isImage = file.type?.startsWith('image/');
    const isVideo = file.type?.startsWith('video/');

    return (
        <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '8px',
            backgroundColor: '#f5f5f5',
            borderRadius: '8px'
        }}>
            {isImage && (
                <img src={file.fileSource} alt={file.name} style={{ 
                    width: '40px', 
                    height: '40px', 
                    borderRadius: '4px' 
                }} />
            )}
            {isVideo && (
                <span className="e-icons e-video" style={{ fontSize: '24px' }}></span>
            )}
            {!isImage && !isVideo && (
                <span className="e-icons e-file" style={{ fontSize: '24px' }}></span>
            )}
            <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 'bold', fontSize: '14px' }}>
                    {file.name}
                </div>
                <div style={{ fontSize: '12px', color: '#999' }}>
                    {(file.size / 1024).toFixed(2)} KB
                </div>
            </div>
        </div>
    );
};
```

### Footer Attachment Template

Customize how attachments appear in the footer area before sending:

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const FooterAttachmentTemplate = (props: { selectedFiles: any[] }) => {
        return (
            <div style={{ padding: '8px' }}>
                <div style={{ fontSize: '12px', color: '#666', marginBottom: '8px' }}>
                    Selected Files ({props.selectedFiles.length}):
                </div>
                {props.selectedFiles.map((file, index) => (
                    <div key={index} style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '6px',
                        backgroundColor: '#f5f5f5',
                        borderRadius: '6px',
                        marginBottom: '6px'
                    }}>
                        <span className="e-icons e-file" style={{ fontSize: '18px' }}></span>
                        <div style={{ flex: 1 }}>
                            <div style={{ fontSize: '13px', fontWeight: '500' }}>
                                {file.name}
                            </div>
                            <div style={{ fontSize: '11px', color: '#999' }}>
                                {(file.size / 1024).toFixed(1)} KB
                            </div>
                        </div>
                        <button 
                            style={{
                                background: 'transparent',
                                border: 'none',
                                cursor: 'pointer',
                                fontSize: '16px'
                            }}
                        >
                            <span className="e-icons e-close"></span>
                        </button>
                    </div>
                ))}
            </div>
        );
    };

    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        attachmentTemplate: FooterAttachmentTemplate  // Custom footer template
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

## Attachment Click Event

### Handle Attachment Clicks

Respond when user clicks on an attachment (either before sending or after sent):

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel, ChatAttachmentClickEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const handleAttachmentClick = (args: ChatAttachmentClickEventArgs) => {
        console.log('Attachment clicked:', args.file.name);
        console.log('File type:', args.file.type);
        console.log('File size:', args.file.size);
        
        // Open file in new tab
        if (args.file.url) {
            window.open(args.file.url, '_blank');
        }
        
        // Cancel default behavior if needed
        // args.cancel = true;
    };

    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        attachmentClick: handleAttachmentClick
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

### Preview Image Attachments

```tsx
const handleAttachmentClick = (args: ChatAttachmentClickEventArgs) => {
    const file = args.file;
    
    // Check if it's an image
    if (file.type?.startsWith('image/')) {
        // Show image in modal/preview
        showImagePreview(file.url || file.fileSource);
        args.cancel = true;  // Prevent default action
    } else if (file.type === 'application/pdf') {
        // Open PDF in new tab
        window.open(file.url, '_blank');
        args.cancel = true;
    }
    // For other files, use default behavior (download)
};

const showImagePreview = (imageUrl: string) => {
    // Implementation for image preview modal
    const modal = document.createElement('div');
    modal.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: rgba(0,0,0,0.8); display: flex; align-items: center; 
                    justify-content: center; z-index: 9999;">
            <img src="${imageUrl}" style="max-width: 90%; max-height: 90%;" />
        </div>
    `;
    modal.onclick = () => modal.remove();
    document.body.appendChild(modal);
};
```

### Download Attachment

```tsx
const handleAttachmentClick = (args: ChatAttachmentClickEventArgs) => {
    const file = args.file;
    
    // Trigger download
    const link = document.createElement('a');
    link.href = file.url || file.fileSource;
    link.download = file.name;
    link.click();
    
    // Cancel default behavior
    args.cancel = true;
    
    console.log('Downloading:', file.name);
};
```

### Event Arguments Details

The `ChatAttachmentClickEventArgs` provides:

| Property | Type | Description |
|----------|------|-------------|
| `cancel` | boolean | Set to `true` to prevent default preview rendering |
| `event` | Event | The underlying click event object |
| `file` | FileInfo | Complete file information (name, type, size, url) |
| `name` | string | Name of the event ('attachmentClick') |

### Complete Attachment Click Example

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel, ChatAttachmentClickEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

function App() {
    const [previewFile, setPreviewFile] = useState<any>(null);

    const handleAttachmentClick = (args: ChatAttachmentClickEventArgs) => {
        const file = args.file;
        
        console.log('Attachment clicked:', {
            name: file.name,
            type: file.type,
            size: file.size,
            url: file.url
        });

        // Handle different file types
        if (file.type?.startsWith('image/')) {
            // Show image preview
            setPreviewFile(file);
            args.cancel = true;
        } else if (file.type === 'application/pdf') {
            // Open PDF in new window
            window.open(file.url, '_blank');
            args.cancel = true;
        } else if (file.type?.startsWith('video/')) {
            // Show video player
            setPreviewFile(file);
            args.cancel = true;
        }
        // For documents, allow default download behavior
    };

    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        allowedFileTypes: '.jpg, .png, .pdf, .mp4, .doc, .docx',
        maxFileSize: 10485760,  // 10MB
        attachmentClick: handleAttachmentClick
    };

    return (
        <div>
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                enableAttachments={true}
                attachmentSettings={attachmentSettings}
            />
            
            {/* Preview Modal */}
            {previewFile && (
                <div 
                    style={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        background: 'rgba(0,0,0,0.9)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        zIndex: 9999
                    }}
                    onClick={() => setPreviewFile(null)}
                >
                    {previewFile.type?.startsWith('image/') && (
                        <img 
                            src={previewFile.url || previewFile.fileSource} 
                            alt={previewFile.name}
                            style={{ maxWidth: '90%', maxHeight: '90%' }}
                        />
                    )}
                    {previewFile.type?.startsWith('video/') && (
                        <video 
                            src={previewFile.url || previewFile.fileSource}
                            controls
                            style={{ maxWidth: '90%', maxHeight: '90%' }}
                        />
                    )}
                </div>
            )}
        </div>
    );
}
```

## Drag and Drop

### Enable Drag-and-Drop

Allow users to drag files directly into chat:

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        enableDragAndDrop: true  // Enable drag and drop
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

## Save Format

### Configure File Format

Choose how files are sent to the server:

```tsx
const attachmentSettings: FileAttachmentSettingsModel = {
    saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
    saveFormat: 'Base64'  // Use Base64 encoding
};
```

Options:
- `'Blob'` - Binary large object (default, for fast uploads)
- `'Base64'` - Base64 encoded string (for text-based transmission)

## Server Path Configuration

### Specify Upload Directory

Set the server path where files are stored:

```tsx
const attachmentSettings: FileAttachmentSettingsModel = {
    saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
    path: '/uploads/chat-files'
};
```

## Complete Attachment Example

### Full Configuration

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel, BeforeAttachmentUploadEventArgs, AttachmentUploadSuccessEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const handleBeforeUpload = (args: BeforeAttachmentUploadEventArgs) => {
        console.log('Uploading files:', args.files);
    };

    const handleUploadSuccess = (args: AttachmentUploadSuccessEventArgs) => {
        console.log('File uploaded:', args.fileName);
    };

    const handleUploadFailure = (args) => {
        console.error('Upload failed:', args.error);
    };

    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        allowedFileTypes: '.pdf, .docx, .xlsx, .jpg, .png, .gif',
        maxFileSize: 5242880,  // 5MB
        maximumCount: 5,
        enableDragAndDrop: true,
        beforeAttachmentUpload: handleBeforeUpload,
        attachmentUploadSuccess: handleUploadSuccess,
        attachmentUploadFailure: handleUploadFailure
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

## Best Practices

1. **Validate file types** on both client and server
2. **Implement file size limits** to prevent abuse
3. **Scan uploaded files** for malware
4. **Store files securely** with proper permissions
5. **Clean up old files** periodically
6. **Provide clear feedback** for upload progress
7. **Handle network failures** gracefully

