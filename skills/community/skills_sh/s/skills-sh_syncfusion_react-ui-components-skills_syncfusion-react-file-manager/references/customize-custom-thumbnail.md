# Customize Custom Thumbnail in React File Manager

The React File Manager component allows you to customize thumbnails and icons displayed for files and folders using the `showThumbnail` property and custom templates. This enables you to display custom icons or images based on file types or specific requirements.

## Table of Contents

1. [Basic Thumbnail Customization](#basic-thumbnail-customization)
2. [Advanced Thumbnail Customization](#advanced-thumbnail-customization)
3. [Custom Thumbnail Properties](#custom-thumbnail-properties)
4. [Icon Sources](#icon-sources)
5. [Best Practices](#best-practices)
6. [Related Topics](#related-topics)

## Basic Thumbnail Customization

### Pattern 1: Hide Thumbnails

By default, thumbnails are shown. You can disable them using the `showThumbnail` property:

```typescript
import React from 'react';
import { FileManagerComponent, Inject, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function HideThumbnailExample() {
  return (
    <FileManagerComponent
      id="file-manager"
      height="500px"
      showThumbnail={false}  // Disable thumbnail display
      ajaxSettings={{
        url: "url",
        downloadUrl: "url",
        uploadUrl: "url",
        getImageUrl: "url"
      }}
    >
      <Inject services={[NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default HideThumbnailExample;
```

### Pattern 2: Show Thumbnails (Default)

```typescript
<FileManagerComponent
  showThumbnail={true}  // Enable thumbnail display
  // ... other properties
/>
```

## Advanced Thumbnail Customization

### Pattern 1: Custom Template for Large Icons View

```typescript
import React from 'react';
import { FileManagerComponent, Inject, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function CustomLargeIconTemplate() {
  const largeIconsTemplate = (props) => {
    const getFileIcon = (name) => {
      const ext = name.split('.').pop().toLowerCase();
      const iconMap = {
        'pdf': '📄',
        'doc': '📝',
        'docx': '📝',
        'xls': '📊',
        'xlsx': '📊',
        'ppt': '🎯',
        'pptx': '🎯',
        'txt': '📃',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'png': '🖼️',
        'gif': '🖼️',
        'mp4': '🎬',
        'mp3': '🎵',
        'zip': '📦',
        'rar': '📦',
      };
      return iconMap[ext] || '📁';
    };

    return (
      <div className="e-large-icon-item" style={{
        textAlign: 'center',
        padding: '10px',
        cursor: 'pointer'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '8px' }}>
          {props.isFile ? getFileIcon(props.name) : '📁'}
        </div>
        <div style={{
          fontSize: '12px',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          whiteSpace: 'nowrap',
          maxWidth: '100px'
        }}>
          {props.name}
        </div>
      </div>
    );
  };

  return (
    <FileManagerComponent
      id="file-manager"
      height="500px"
      view="LargeIcons"
      largeIconsTemplate={largeIconsTemplate}
      ajaxSettings={{
        url: "url",
        downloadUrl: "url",
        uploadUrl: "url",
        getImageUrl: "url"
      }}
    >
      <Inject services={[NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default CustomLargeIconTemplate;
```

### Pattern 2: File Type-Based Icons

```typescript
function getCustomIcon(fileName) {
  const fileType = fileName.split('.').pop().toLowerCase();
  
  const iconClasses = {
    // Documents
    'pdf': 'e-icon-pdf',
    'doc': 'e-icon-doc',
    'docx': 'e-icon-doc',
    'txt': 'e-icon-txt',
    
    // Spreadsheets
    'xls': 'e-icon-xls',
    'xlsx': 'e-icon-xls',
    'csv': 'e-icon-csv',
    
    // Presentations
    'ppt': 'e-icon-ppt',
    'pptx': 'e-icon-ppt',
    
    // Images
    'jpg': 'e-icon-jpg',
    'jpeg': 'e-icon-jpg',
    'png': 'e-icon-png',
    'gif': 'e-icon-gif',
    'bmp': 'e-icon-bmp',
    
    // Videos
    'mp4': 'e-icon-video',
    'avi': 'e-icon-video',
    'mov': 'e-icon-video',
    'mkv': 'e-icon-video',
    
    // Audio
    'mp3': 'e-icon-audio',
    'wav': 'e-icon-audio',
    'flac': 'e-icon-audio',
    
    // Archives
    'zip': 'e-icon-zip',
    'rar': 'e-icon-zip',
    '7z': 'e-icon-zip',
    
    // Code
    'js': 'e-icon-code',
    'ts': 'e-icon-code',
    'py': 'e-icon-code',
    'java': 'e-icon-code',
    'cpp': 'e-icon-code',
    'html': 'e-icon-html',
    'css': 'e-icon-css',
    'json': 'e-icon-json',
    'xml': 'e-icon-xml',
  };
  
  return iconClasses[fileType] || 'e-icon-default';
}
```

### Pattern 3: Size-Based Color Coding

```typescript
function getThumbnailStyle(fileSize) {
  let colorClass = 'thumbnail-small';
  
  if (fileSize > 100 * 1024 * 1024) {  // 100MB+
    colorClass = 'thumbnail-large';
  } else if (fileSize > 10 * 1024 * 1024) {  // 10MB+
    colorClass = 'thumbnail-medium';
  }
  
  return colorClass;
}

const styles = `
  .thumbnail-small {
    border: 2px solid green;
    opacity: 0.8;
  }
  
  .thumbnail-medium {
    border: 2px solid orange;
    opacity: 0.8;
  }
  
  .thumbnail-large {
    border: 2px solid red;
    opacity: 0.8;
  }
`;
```

### Pattern 4: Date-Based Icons (Recent/Archived)

```typescript
function getDateBasedIcon(fileDate) {
  const now = new Date();
  const file = new Date(fileDate);
  const diffDays = (now - file) / (1000 * 60 * 60 * 24);
  
  if (diffDays < 1) {
    return 'e-icon-new';  // New file (today)
  } else if (diffDays < 7) {
    return 'e-icon-recent';  // Recent file (this week)
  } else if (diffDays > 365) {
    return 'e-icon-archived';  // Archived file (older than 1 year)
  } else {
    return 'e-icon-default';
  }
}
```

## Complete Example with Custom Thumbnails

```typescript
import React from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function AdvancedThumbnailCustomization() {
  const hostUrl = "url";

  const getFileIcon = (name) => {
    const ext = name.split('.').pop().toLowerCase();
    
    const iconMap = {
      // Documents
      'pdf': '📄', 'doc': '📝', 'docx': '📝', 'txt': '📃',
      // Spreadsheets
      'xls': '📊', 'xlsx': '📊', 'csv': '📊',
      // Presentations
      'ppt': '🎯', 'pptx': '🎯',
      // Images
      'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️', 'bmp': '🖼️',
      // Videos
      'mp4': '🎬', 'avi': '🎬', 'mov': '🎬', 'mkv': '🎬',
      // Audio
      'mp3': '🎵', 'wav': '🎵', 'flac': '🎵',
      // Archives
      'zip': '📦', 'rar': '📦', '7z': '📦',
      // Code
      'js': '⚙️', 'ts': '⚙️', 'py': '🐍', 'java': '☕', 'html': '🌐', 'css': '🎨',
    };
    
    return iconMap[ext] || '📁';
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const largeIconsTemplate = (props) => {
    const isRecent = (date) => {
      const diff = (new Date() - new Date(date)) / (1000 * 60 * 60 * 24);
      return diff < 1;
    };

    return (
      <div className="e-large-icon-item" style={{
        textAlign: 'center',
        padding: '10px',
        cursor: 'pointer',
        borderRadius: '8px',
        transition: 'all 0.3s ease',
      }}>
        <div style={{
          fontSize: '48px',
          marginBottom: '8px',
          position: 'relative'
        }}>
          {props.isFile ? getFileIcon(props.name) : '📁'}
          {isRecent(props.dateModified) && (
            <span style={{
              position: 'absolute',
              top: '0',
              right: '0',
              backgroundColor: 'red',
              color: 'white',
              borderRadius: '50%',
              width: '24px',
              height: '24px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '12px',
              fontWeight: 'bold'
            }}>
              🆕
            </span>
          )}
        </div>
        <div style={{
          fontSize: '12px',
          fontWeight: '500',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          whiteSpace: 'nowrap',
          maxWidth: '100px',
          marginBottom: '4px'
        }}>
          {props.name}
        </div>
        {props.isFile && (
          <div style={{
            fontSize: '10px',
            color: '#666'
          }}>
            {formatFileSize(props.size)}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="control-section">
      <FileManagerComponent
        id="custom-thumbnail"
        height="500px"
        view="LargeIcons"
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
        largeIconsTemplate={largeIconsTemplate}
        showThumbnail={true}
      >
        <Inject services={[NavigationPane, DetailsView, Toolbar]} />
      </FileManagerComponent>

      <style>{`
        .e-large-icon-item:hover {
          background-color: #f5f5f5;
          transform: scale(1.05);
        }
      `}</style>
    </div>
  );
}

export default AdvancedThumbnailCustomization;
```

## Custom Thumbnail Properties

| Property | Type | Description |
|----------|------|-------------|
| `showThumbnail` | boolean | Show/hide thumbnails |
| `largeIconsTemplate` | Template | Custom template for large icons view |
| `detailsViewTemplate` | Template | Custom template for details view |

## Icon Sources

### Built-in Syncfusion Icons

Use Syncfusion Material or Fabric icon classes:

```typescript
const iconClasses = {
  'e-icons e-file',           // Generic file
  'e-icons e-folder',         // Folder
  'e-icons e-file-pdf',       // PDF
  'e-icons e-file-xls',       // Excel
  'e-icons e-file-ppt',       // PowerPoint
  'e-icons e-file-image',     // Image
  'e-icons e-file-video',     // Video
  'e-icons e-file-audio',     // Audio
  'e-icons e-file-zip',       // Archive
};
```

## Best Practices

1. **Use Emoji or Icons Consistently** - Choose either emoji or icon fonts
2. **Maintain Visual Hierarchy** - Use size and color to indicate importance
3. **Show File Information** - Display size, date, or other metadata
4. **Optimize Performance** - Cache icon mappings
5. **Test Accessibility** - Ensure icons are accompanied by text descriptions

## Related Topics

- [Customization](customization.md)
- [Views and Navigation](views-and-navigation.md)
- [File Operations](file-operations.md)
- [Getting Started](getting-started.md)
