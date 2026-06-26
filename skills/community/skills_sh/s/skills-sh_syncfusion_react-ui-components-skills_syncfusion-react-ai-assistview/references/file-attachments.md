# File Attachments

## Enabling File Attachments

### Basic Enable

Enable file attachment support with the `enableAttachments` property:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
            enableAttachments={true}
        />
    );
}

export default App;
```

## Attachment Settings Configuration

### Setting Upload and Remove Endpoints

Configure `saveUrl` and `removeUrl` for server-side file handling:

```tsx
const attachmentSettings = {
    saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove'
};

<AIAssistViewComponent 
    id="aiAssistView"
    enableAttachments={true}
    attachmentSettings={attachmentSettings}
/>
```

## File Type Restrictions

### Allow Specific File Types

Restrict uploads to specific file extensions using `allowedFileType`:

```tsx
// Allow only images
const attachmentSettings = {
    saveUrl: 'https://example.com/upload',
    removeUrl: 'https://example.com/remove',
    allowedFileType: '.png, .jpg, .jpeg, .gif'
};

<AIAssistViewComponent 
    id="aiAssistView"
    enableAttachments={true}
    attachmentSettings={attachmentSettings}
/>
```

### Common File Type Restrictions

```tsx
// Documents
allowedFileType: '.pdf, .doc, .docx, .txt'

// Images
allowedFileType: '.png, .jpg, .jpeg, .gif, .bmp'

// Spreadsheets
allowedFileType: '.xlsx, .xls, .csv'

// Mixed (documents + images)
allowedFileType: '.pdf, .doc, .docx, .png, .jpg, .jpeg'

// All types (no restriction)
// Don't specify allowedFileType property
```

## File Size Management

### Setting Maximum File Size

Configure `maxFileSize` property (default is 2000000 bytes / 2 MB):

```tsx
const attachmentSettings = {
    saveUrl: 'https://example.com/upload',
    removeUrl: 'https://example.com/remove',
    maxFileSize: 5000000  // 5 MB in bytes
};

<AIAssistViewComponent 
    id="aiAssistView"
    enableAttachments={true}
    attachmentSettings={attachmentSettings}
/>
```

### Size Limit Examples

```tsx
// 1 MB
maxFileSize: 1000000

// 5 MB
maxFileSize: 5000000

// 10 MB
maxFileSize: 10000000

// 50 MB
maxFileSize: 50000000
```

## Maximum File Count

### Restrict Number of Attachments

Use `maximumCount` to limit how many files can be attached (default is 10):

```tsx
const attachmentSettings = {
    saveUrl: 'https://example.com/upload',
    removeUrl: 'https://example.com/remove',
    maximumCount: 5  // Max 5 files per message
};

<AIAssistViewComponent 
    id="aiAssistView"
    enableAttachments={true}
    attachmentSettings={attachmentSettings}
/>
```

### Count Examples

```tsx
maximumCount: 1    // Only one file at a time
maximumCount: 3    // Up to 3 files
maximumCount: 5    // Up to 5 files (recommended)
maximumCount: 10   // Default - up to 10 files
```

## Complete Attachment Configuration

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs, AttachmentSettings } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const attachmentSettings: AttachmentSettings = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        allowedFileType: '.pdf, .doc, .docx, .png, .jpg, .jpeg',
        maxFileSize: 5000000,      // 5 MB
        maximumCount: 5             // Max 5 files
    };

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        console.log('Prompt with potential attachments:', args.prompt);
        
        // Get attachment information from component
        const prompts = assistInstance.current?.prompts;
        const lastPrompt = prompts?.[prompts.length - 1];
        
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Files received and processed');
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
            promptRequest={handlePromptRequest}
        />
    );
}

export default App;
```

## Server-Side File Handling

### ASP.NET Backend Example

```csharp
[HttpPost("api/FileUploader/Save")]
public void Save(IFormFile uploadFiles)
{
    if (uploadFiles != null)
    {
        string fileName = ContentDispositionHeaderValue.Parse(uploadFiles.ContentDisposition).FileName.Trim('"');
        string filePath = Path.Combine("Uploads", fileName);
        using (FileStream fs = System.IO.File.Create(filePath))
        {
            uploadFiles.CopyTo(fs);
        }
    }
}

[HttpPost("api/FileUploader/Remove")]
public void Remove(string[] files)
{
    if (files != null)
    {
        foreach (string file in files)
        {
            string filePath = Path.Combine("Uploads", file);
            if (System.IO.File.Exists(filePath))
            {
                System.IO.File.Delete(filePath);
            }
        }
    }
}
```

### Node.js Backend Example

```javascript
const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.post('/api/FileUploader/Save', upload.single('uploadFiles'), (req, res) => {
    if (req.file) {
        const oldPath = req.file.path;
        const newPath = path.join('uploads', req.file.originalname);
        
        fs.rename(oldPath, newPath, (err) => {
            if (err) {
                res.status(500).send('File upload failed');
            } else {
                res.send('File uploaded successfully');
            }
        });
    }
});

app.post('/api/FileUploader/Remove', (req, res) => {
    const files = req.body.files;
    if (files) {
        files.forEach(file => {
            const filePath = path.join('uploads', file);
            fs.unlink(filePath, (err) => {
                if (err) console.error('File deletion error:', err);
            });
        });
        res.send('Files removed');
    }
});
```

## Handling Attachments in Prompts

### Access Attached Files

The `attachedFiles` property in `PromptRequestEventArgs` provides access to files attached with the prompt:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs, FileInfo } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        // Access attached files from event args
        const attachedFiles: FileInfo[] = args.attachedFiles || [];
        
        console.log('User prompt:', args.prompt);
        console.log('Number of files attached:', attachedFiles.length);
        
        // Process each attached file
        attachedFiles.forEach((file, index) => {
            console.log(`File ${index + 1}:`, file.name);
            console.log('- Type:', file.type);
            console.log('- Size:', file.size, 'bytes');
        });
        
        // Simulate response
        setTimeout(() => {
            const response = attachedFiles.length > 0 
                ? `Received your prompt with ${attachedFiles.length} file(s): ${attachedFiles.map(f => f.name).join(', ')}`
                : 'Received your prompt (no files attached)';
            assistInstance.current?.addPromptResponse(response);
        }, 1500);
    };

    const attachmentSettings = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        maxFileSize: 5000000,
        maximumCount: 5
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
            promptRequest={handlePromptRequest}
        />
    );
}

export default App;
```

### FileInfo Interface

Each file in the `attachedFiles` array has the following structure:

```tsx
interface FileInfo {
    name: string;        // File name
    size: number;        // File size in bytes
    type: string;        // MIME type (e.g., 'image/png', 'application/pdf')
    rawFile?: File;      // Original File object
    status?: string;     // Upload status
    validationMessages?: any;  // Validation error messages if any
}
```

### Working with Attached Files

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    const files = args.attachedFiles || [];
    
    if (files.length === 0) {
        assistInstance.current?.addPromptResponse('Please attach files for analysis');
        return;
    }
    
    // Validate file types
    const supportedTypes = ['image/png', 'image/jpeg', 'application/pdf'];
    const unsupportedFiles = files.filter(f => !supportedTypes.includes(f.type));
    
    if (unsupportedFiles.length > 0) {
        assistInstance.current?.addPromptResponse(
            `Unsupported file types: ${unsupportedFiles.map(f => f.name).join(', ')}`
        );
        return;
    }
    
    // Process files
    const fileList = files.map(f => `📎 ${f.name} (${(f.size / 1024).toFixed(2)} KB)`).join('<br>');
    assistInstance.current?.addPromptResponse(
        `<div>Files received:<br>${fileList}<br><br>Processing your request...</div>`
    );
};
```

### File Upload Feedback

```tsx
const attachmentSettings = {
    saveUrl: 'https://example.com/upload',
    removeUrl: 'https://example.com/remove',
    allowedFileType: '.pdf, .doc, .docx',
    maxFileSize: 5000000,
    maximumCount: 3
};

// User gets automatic feedback from component:
// - "Maximum count reached" if trying to add more than maximumCount
// - "File size exceeds limit" if file > maxFileSize
// - "File type not allowed" if extension not in allowedFileType
```

## Advanced Usage

### Custom File Validation

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    const prompts = assistInstance.current?.prompts;
    const currentPrompt = prompts?.[prompts.length - 1];
    
    // Validate based on prompt content and attachments
    if (currentPrompt && !validatePromptWithAttachments(currentPrompt)) {
        assistInstance.current?.addPromptResponse('Invalid combination of prompt and files');
        return;
    }
    
    processValidPrompt(args.prompt);
};

const validatePromptWithAttachments = (prompt: any): boolean => {
    // Custom validation logic
    return true;
};
```

### File Upload with Progress

```tsx
const handleFileUploadProgress = () => {
    // Files upload automatically through attachment settings
    // Server receives files via saveUrl endpoint
    // Remove via removeUrl endpoint
    // Progress handled by component automatically
};
```

## Attachment Lifecycle Events

The AI AssistView provides four events for tracking attachment operations:

### beforeAttachmentUpload Event

Triggered before file upload begins. Use this to validate files or cancel uploads:

```tsx
import { AIAssistViewComponent, BeforeUploadEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handleBeforeUpload = (args: BeforeUploadEventArgs) => {
        console.log('Uploading file:', args.fileData.name);
        console.log('File size:', args.fileData.size);
        console.log('File type:', args.fileData.type);
        
        // Custom validation
        if (args.fileData.size > 10000000) {  // 10 MB
            args.cancel = true;
            alert('File is too large. Maximum size is 10 MB.');
            return;
        }
        
        // Check file type
        const allowedTypes = ['image/png', 'image/jpeg', 'application/pdf'];
        if (!allowedTypes.includes(args.fileData.type)) {
            args.cancel = true;
            alert('File type not allowed');
            return;
        }
        
        // Modify upload data if needed
        args.customFormData = [
            { userId: 'user123' },
            { uploadDate: new Date().toISOString() }
        ];
    };

    const attachmentSettings = {
        saveUrl: 'https://example.com/upload',
        removeUrl: 'https://example.com/remove'
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
            beforeAttachmentUpload={handleBeforeUpload}
        />
    );
}

export default App;
```

### attachmentUploadSuccess Event

Triggered when file upload completes successfully:

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);

    const handleUploadSuccess = (args: any) => {
        console.log('Upload successful:', args.file.name);
        console.log('Server response:', args.response);
        
        // Track uploaded files
        setUploadedFiles(prev => [...prev, args.file.name]);
        
        // Show notification
        const notification = document.createElement('div');
        notification.className = 'upload-notification';
        notification.textContent = `✅ ${args.file.name} uploaded successfully`;
        document.body.appendChild(notification);
        
        setTimeout(() => notification.remove(), 3000);
    };

    const attachmentSettings = {
        saveUrl: 'https://example.com/upload',
        removeUrl: 'https://example.com/remove'
    };

    return (
        <div>
            <div className="upload-status">
                Uploaded files: {uploadedFiles.length}
            </div>
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                enableAttachments={true}
                attachmentSettings={attachmentSettings}
                attachmentUploadSuccess={handleUploadSuccess}
            />
        </div>
    );
}

export default App;
```

### attachmentUploadFailure Event

Triggered when file upload fails:

```tsx
const handleUploadFailure = (args: any) => {
    console.error('Upload failed:', args.file.name);
    console.error('Error details:', args.error);
    
    // Show error message to user
    const errorMessage = args.error?.message || 'Upload failed. Please try again.';
    
    assistInstance.current?.addPromptResponse(
        `<div class="error-message">
            ⚠️ Failed to upload ${args.file.name}: ${errorMessage}
        </div>`
    );
    
    // Log for debugging
    console.log('Status code:', args.statusCode);
    console.log('Response:', args.response);
};

<AIAssistViewComponent 
    id="aiAssistView"
    ref={assistInstance}
    enableAttachments={true}
    attachmentSettings={attachmentSettings}
    attachmentUploadFailure={handleUploadFailure}
/>
```

### attachmentRemoved Event

Triggered when user removes an attached file:

```tsx
const handleAttachmentRemoved = (args: any) => {
    console.log('File removed:', args.file.name);
    
    // Update UI or state
    setUploadedFiles(prev => prev.filter(name => name !== args.file.name));
    
    // Notify user
    console.log('File successfully removed from attachments');
};

<AIAssistViewComponent 
    id="aiAssistView"
    ref={assistInstance}
    enableAttachments={true}
    attachmentSettings={attachmentSettings}
    attachmentRemoved={handleAttachmentRemoved}
/>
```

### Complete Event Handling Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs, BeforeUploadEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [uploadStatus, setUploadStatus] = useState<string>('Ready');
    const [fileList, setFileList] = useState<string[]>([]);

    const attachmentSettings = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        allowedFileType: '.pdf, .doc, .docx, .png, .jpg, .jpeg',
        maxFileSize: 5000000,
        maximumCount: 5
    };

    const handleBeforeUpload = (args: BeforeUploadEventArgs) => {
        setUploadStatus(`Uploading ${args.fileData.name}...`);
        
        // Validate file
        if (args.fileData.size > attachmentSettings.maxFileSize) {
            args.cancel = true;
            setUploadStatus('Upload cancelled: File too large');
            return;
        }
    };

    const handleUploadSuccess = (args: any) => {
        setUploadStatus(`✅ ${args.file.name} uploaded`);
        setFileList(prev => [...prev, args.file.name]);
        
        setTimeout(() => setUploadStatus('Ready'), 2000);
    };

    const handleUploadFailure = (args: any) => {
        setUploadStatus(`❌ Failed: ${args.file.name}`);
        console.error('Upload error:', args.error);
    };

    const handleAttachmentRemoved = (args: any) => {
        setFileList(prev => prev.filter(name => name !== args.file.name));
        setUploadStatus(`Removed: ${args.file.name}`);
    };

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        const files = args.attachedFiles || [];
        setTimeout(() => {
            const response = files.length > 0
                ? `Processing your request with ${files.length} file(s)...`
                : 'Processing your request...';
            assistInstance.current?.addPromptResponse(response);
        }, 1000);
    };

    return (
        <div>
            <div className="status-bar">
                <strong>Status:</strong> {uploadStatus}
            </div>
            <div className="file-list">
                <strong>Attached:</strong> {fileList.join(', ') || 'None'}
            </div>
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                enableAttachments={true}
                attachmentSettings={attachmentSettings}
                beforeAttachmentUpload={handleBeforeUpload}
                attachmentUploadSuccess={handleUploadSuccess}
                attachmentUploadFailure={handleUploadFailure}
                attachmentRemoved={handleAttachmentRemoved}
                promptRequest={handlePromptRequest}
            />
        </div>
    );
}

export default App;
```

### Event Use Cases

**beforeAttachmentUpload:**
- Validate file size and type
- Add custom metadata to upload
- Cancel upload based on business rules
- Show upload confirmation dialog

**attachmentUploadSuccess:**
- Track successfully uploaded files
- Show success notifications
- Update application state
- Log upload analytics

**attachmentUploadFailure:**
- Display error messages to users
- Retry failed uploads
- Log errors for debugging
- Provide fallback options

**attachmentRemoved:**
- Update file list UI
- Clean up related data
- Track file removal
- Update form validation state

## Initializing Prompts with Attached Files

You can pre-populate the component with conversations that include attachments:

```tsx
import { AIAssistViewComponent, PromptModel, FileInfo } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const initialPrompts: PromptModel[] = [
        {
            prompt: "Can you analyze this document?",
            response: "I've reviewed the document. Here are my findings...",
            attachedFiles: [
                {
                    name: "report.pdf",
                    size: 245678,
                    type: "application/pdf"
                },
                {
                    name: "data.xlsx",
                    size: 123456,
                    type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                }
            ]
        }
    ];

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            prompts={initialPrompts}
            enableAttachments={true}
        />
    );
}

export default App;
```

## Best Practices

**Set realistic file size limits**: Balance usability with server capacity  
**Restrict file types**: Only allow necessary file formats  
**Limit file count**: Prevent excessive uploads  
**Validate on server**: Never trust client-side validation alone  
**Provide feedback**: Show users upload status and errors  
**Handle errors gracefully**: Display user-friendly error messages  
**Secure uploads**: Validate file content, not just extension  
**Clean up old files**: Regular maintenance of upload directory
