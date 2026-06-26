# Customize Navigation Pane in React File Manager

The navigation pane in the React File Manager component displays the folder hierarchy in a tree-like structure. You can customize the appearance and behavior of the navigation pane using the `navigationPaneTemplate` property and other configuration options.

## Table of Contents

1. [Basic Navigation Pane Configuration](#basic-navigation-pane-configuration)
2. [Custom Navigation Pane Templates](#custom-navigation-pane-templates)
3. [Navigation Pane Settings](#navigation-pane-settings)
4. [Complete Example with Advanced Customization](#complete-example-with-advanced-customization)
5. [Navigation Pane Settings Properties](#navigation-pane-settings-properties)
6. [Best Practices](#best-practices)
7. [Related Topics](#related-topics)

## Basic Navigation Pane Configuration

### Pattern 1: Control Visibility

```typescript
import React from 'react';
import { FileManagerComponent, Inject, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function NavigationPaneVisibilityExample() {
  return (
    <FileManagerComponent
      height="500px"
      navigationPaneSettings={{
        visible: true,  // Show navigation pane
        width: '200px'  // Set width
      }}
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

export default NavigationPaneVisibilityExample;
```

## Custom Navigation Pane Templates

### Pattern 1: Basic Template with Folder Name

```typescript
function NavigationTemplateExample() {
  const navigationPaneTemplate = (item) => {
    return (
      <div className="e-nav-pane-node" style={{ display: 'flex', alignItems: 'center' }}>
        <span className="folder-icon" style={{ marginRight: '8px', fontSize: '14px' }}>
          📁
        </span>
        <span className="folder-name" style={{ flex: 1 }}>
          {item.name}
        </span>
      </div>
    );
  };

  return (
    <FileManagerComponent
      navigationPaneTemplate={navigationPaneTemplate}
      // ... other props
    />
  );
}
```

### Pattern 2: Template with File Count

```typescript
function NavigationWithCountExample() {
  const navigationPaneTemplate = (item) => {
    const fileCount = item.fileCount || 0;
    
    return (
      <div className="e-nav-pane-node" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ display: 'flex', alignItems: 'center', flex: 1 }}>
          <span style={{ marginRight: '8px', fontSize: '16px' }}>
            {item.hasChild ? '📂' : '📁'}
          </span>
          <span>{item.name}</span>
        </span>
        <span style={{
          backgroundColor: '#4CAF50',
          color: 'white',
          borderRadius: '12px',
          padding: '2px 8px',
          fontSize: '12px',
          minWidth: '24px',
          textAlign: 'center'
        }}>
          {fileCount}
        </span>
      </div>
    );
  };

  return (
    <FileManagerComponent
      navigationPaneTemplate={navigationPaneTemplate}
      // ... other props
    />
  );
}
```

### Pattern 3: Template with Last Modified Date

```typescript
function NavigationWithDateExample() {
  const navigationPaneTemplate = (item) => {
    const formatDate = (date) => {
      if (!date) return '';
      return new Date(date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: '2-digit'
      });
    };

    return (
      <div className="e-nav-pane-node" style={{
        display: 'grid',
        gridTemplateColumns: '1fr auto',
        gap: '8px',
        alignItems: 'center',
        fontSize: '12px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <span style={{ marginRight: '8px' }}>📁</span>
          <span>{item.name}</span>
        </div>
        <div style={{ color: '#999', fontSize: '11px' }}>
          {formatDate(item.dateModified)}
        </div>
      </div>
    );
  };

  return (
    <FileManagerComponent
      navigationPaneTemplate={navigationPaneTemplate}
      // ... other props
    />
  );
}
```

### Pattern 4: Color-Coded Navigation

```typescript
function ColorCodedNavigationExample() {
  const getFolderColor = (folderName) => {
    const colorMap = {
      'Documents': '#FF6B6B',
      'Images': '#4ECDC4',
      'Videos': '#45B7D1',
      'Downloads': '#FFA07A',
      'Music': '#98D8C8',
      'Desktop': '#F7DC6F',
      'Recents': '#BB8FCE'
    };
    return colorMap[folderName] || '#95A5A6';
  };

  const navigationPaneTemplate = (item) => {
    const bgColor = getFolderColor(item.name);

    return (
      <div className="e-nav-pane-node" style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        padding: '4px 8px',
        borderRadius: '4px',
        backgroundColor: `${bgColor}20`,
        borderLeft: `3px solid ${bgColor}`
      }}>
        <span style={{
          width: '20px',
          height: '20px',
          backgroundColor: bgColor,
          borderRadius: '3px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontSize: '12px'
        }}>
          📁
        </span>
        <span style={{
          flex: 1,
          fontWeight: item.hasChild ? '600' : '400',
          color: bgColor
        }}>
          {item.name}
        </span>
      </div>
    );
  };

  return (
    <FileManagerComponent
      navigationPaneTemplate={navigationPaneTemplate}
      // ... other props
    />
  );
}
```

### Pattern 5: Icon-Based Template

```typescript
function IconBasedNavigationExample() {
  const getFolderIcon = (folderName) => {
    const iconMap = {
      'Documents': '📄',
      'Images': '🖼️',
      'Videos': '🎬',
      'Downloads': '⬇️',
      'Music': '🎵',
      'Desktop': '💻',
      'Archive': '📦',
      'Recent': '⏰'
    };
    return iconMap[folderName] || '📁';
  };

  const navigationPaneTemplate = (item) => {
    return (
      <div className="e-nav-pane-node" style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        padding: '6px 4px',
        cursor: 'pointer',
        borderRadius: '4px',
        transition: 'background-color 0.2s'
      }}>
        <span style={{ fontSize: '18px' }}>
          {getFolderIcon(item.name)}
        </span>
        <span style={{
          flex: 1,
          fontSize: '13px',
          fontWeight: '500'
        }}>
          {item.name}
        </span>
        {item.hasChild && (
          <span style={{
            fontSize: '10px',
            color: '#999'
          }}>
            ▶
          </span>
        )}
      </div>
    );
  };

  return (
    <FileManagerComponent
      navigationPaneTemplate={navigationPaneTemplate}
      // ... other props
    />
  );
}
```

## Navigation Pane Settings

### Pattern 1: Configure Pane Width and Sort

```typescript
<FileManagerComponent
  navigationPaneSettings={{
    visible: true,
    width: '250px',      // Custom width
    sortOrder: 'Ascending',
    sortBy: 'name'       // Sort by name, size, or date
  }}
  // ... other props
/>
```

### Pattern 2: Responsive Navigation Pane

```typescript
function ResponsiveNavigationExample() {
  const [paneWidth, setPaneWidth] = React.useState('200px');

  React.useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      if (width < 768) {
        setPaneWidth('150px');
      } else if (width < 1024) {
        setPaneWidth('180px');
      } else {
        setPaneWidth('220px');
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <FileManagerComponent
      navigationPaneSettings={{
        visible: true,
        width: paneWidth
      }}
      // ... other props
    />
  );
}
```

## Complete Example with Advanced Customization

```typescript
import React, { useRef } from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function AdvancedNavigationCustomization() {
  const fileManagerRef = useRef(null);
  const hostUrl = "url";

  const getFolderMetadata = (folderName) => {
    const metadata = {
      'Documents': { icon: '📄', color: '#FF6B6B', description: 'Documents Folder' },
      'Images': { icon: '🖼️', color: '#4ECDC4', description: 'Image Gallery' },
      'Videos': { icon: '🎬', color: '#45B7D1', description: 'Video Files' },
      'Downloads': { icon: '⬇️', color: '#FFA07A', description: 'Downloaded Files' },
      'Music': { icon: '🎵', color: '#98D8C8', description: 'Audio Files' },
      'Desktop': { icon: '💻', color: '#F7DC6F', description: 'Desktop Files' },
      'Archive': { icon: '📦', color: '#BB8FCE', description: 'Archived Files' }
    };
    return metadata[folderName] || { icon: '📁', color: '#95A5A6', description: 'Folder' };
  };

  const navigationPaneTemplate = (item) => {
    const metadata = getFolderMetadata(item.name);
    const isRecent = Math.random() > 0.7;  // Simulate recent items

    return (
      <div
        className="e-nav-pane-node"
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          padding: '8px 6px',
          borderRadius: '6px',
          backgroundColor: isRecent ? `${metadata.color}15` : 'transparent',
          borderLeft: isRecent ? `3px solid ${metadata.color}` : 'none',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = `${metadata.color}25`;
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = isRecent ? `${metadata.color}15` : 'transparent';
        }}
      >
        <span style={{
          fontSize: '18px',
          width: '24px',
          textAlign: 'center'
        }}>
          {metadata.icon}
        </span>

        <div style={{ flex: 1 }}>
          <div style={{
            fontSize: '13px',
            fontWeight: '500',
            color: '#333'
          }}>
            {item.name}
          </div>
          {isRecent && (
            <div style={{
              fontSize: '10px',
              color: '#999',
              marginTop: '2px'
            }}>
              Recently accessed
            </div>
          )}
        </div>

        {item.hasChild && (
          <span style={{
            fontSize: '12px',
            color: '#bbb',
            transition: 'transform 0.2s'
          }}>
            ▸
          </span>
        )}
      </div>
    );
  };

  return (
    <div className="control-section">
      <FileManagerComponent
        ref={fileManagerRef}
        id="advanced-navigation"
        height="500px"
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
        navigationPaneSettings={{
          visible: true,
          width: '220px',
          sortOrder: 'Ascending',
          sortBy: 'name'
        }}
        navigationPaneTemplate={navigationPaneTemplate}
      >
        <Inject services={[NavigationPane, DetailsView, Toolbar]} />
      </FileManagerComponent>

      <style>{`
        .e-nav-pane-node {
          user-select: none;
        }
        
        .e-nav-pane-node:hover {
          background-color: #f0f0f0 !important;
        }
      `}</style>
    </div>
  );
}

export default AdvancedNavigationCustomization;
```

## Navigation Pane Settings Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `visible` | boolean | true | Show/hide navigation pane |
| `width` | string | '200px' | Width of navigation pane |
| `sortOrder` | string | 'Ascending' | Sort order (Ascending/Descending) |
| `sortBy` | string | 'name' | Sort by: name, size, or dateModified |

## Best Practices

1. **Use Consistent Icons** - Choose a cohesive icon style
2. **Provide Visual Feedback** - Highlight hovered/selected items
3. **Show Additional Info** - Display file counts, dates, or descriptions
4. **Optimize Performance** - Avoid heavy calculations in templates
5. **Maintain Accessibility** - Use clear labels and proper contrast

## Related Topics

- [Customization](customization.md)
- [Views and Navigation](views-and-navigation.md)
- [Getting Started](getting-started.md)
