# Customization and Styling: Themes, Responsive Design, and Advanced Features

## Table of Contents
- [Built-in Themes](#built-in-themes)
- [CSS Customization](#css-customization)
- [CSS Variables](#css-variables)
- [Responsive Design](#responsive-design)
- [Virtual Scrolling](#virtual-scrolling)
- [Persistence (Saving State)](#persistence-saving-state)
- [Localization](#localization)
- [Accessibility](#accessibility)

## Built-in Themes

### Material Theme (Default)
```css
@import '../node_modules/@syncfusion/ej2-kanban/styles/material.css';
```
Modern, clean design inspired by Material Design.

### Bootstrap Theme
```css
@import '../node_modules/@syncfusion/ej2-kanban/styles/bootstrap.css';
```
Bootstrap-compatible styling.

### Bootstrap 4 Theme
```css
@import '../node_modules/@syncfusion/ej2-kanban/styles/bootstrap4.css';
```
Bootstrap 4 styling for modern layouts.

### Fluent Theme
```css
@import '../node_modules/@syncfusion/ej2-kanban/styles/fluent.css';
```
Microsoft Fluent Design System styling.

### Tailwind Theme
```css
@import '../node_modules/@syncfusion/ej2-kanban/styles/tailwind3.css';
```
Tailwind CSS compatible styling.

### High Contrast Theme
```css
@import '../node_modules/@syncfusion/ej2-kanban/styles/highcontrast.css';
```
High contrast for accessibility and low-vision users.

## CSS Customization

### Override Default Styles

```css
/* Customize card appearance */
.e-card {
  background-color: #f5f5f5;
  border-left: 4px solid #2196f3;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  transition: all 0.3s ease;
}

.e-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* Customize column header */
.e-column-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  padding: 16px;
}

/* Customize swimlane header */
.e-swimlane-header {
  background-color: #e8eaf6;
  border-bottom: 2px solid #667eea;
  font-weight: 600;
}

/* Card priority indicator */
.e-card.priority-critical {
  border-left-color: #f44336;
}

.e-card.priority-high {
  border-left-color: #ff9800;
}

.e-card.priority-medium {
  border-left-color: #2196f3;
}

.e-card.priority-low {
  border-left-color: #4caf50;
}
```

### Add Custom CSS Classes to Cards

```tsx
import { ReactElement } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

// Card props expected: { Priority, Summary }
const cardTemplate = (props: any): ReactElement => {
  const priorityClass = `priority-${props.Priority?.toLowerCase()}`;
  
  return (
    <div className={`custom-card ${priorityClass}`}>
      <div>{props.Summary}</div>
    </div>
  );
};

<KanbanComponent cardSettings={{ template: cardTemplate }}>
  {/* ... */}
</KanbanComponent>
```

## CSS Variables

Use CSS variables for dynamic theming:

```css
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --card-bg: #ffffff;
  --card-border: #e0e0e0;
  --header-bg: #f5f5f5;
  --text-dark: #333333;
  --text-light: #666666;
}

.e-kanban {
  --primary: var(--primary-color);
  --kanban-card-bg: var(--card-bg);
}

.e-card {
  background-color: var(--card-bg);
  border-left-color: var(--primary-color);
  color: var(--text-dark);
}
```

### Runtime Theme Switching

```tsx
const handleThemeChange = (theme: string): void => {
  const root = document.documentElement;
  
  if (theme === 'dark') {
    root.style.setProperty('--card-bg', '#2a2a2a');
    root.style.setProperty('--text-dark', '#ffffff');
    root.style.setProperty('--header-bg', '#1a1a1a');
  } else {
    root.style.setProperty('--card-bg', '#ffffff');
    root.style.setProperty('--text-dark', '#333333');
    root.style.setProperty('--header-bg', '#f5f5f5');
  }
};

<button onClick={() => handleThemeChange('dark')}>Dark Mode</button>
<button onClick={() => handleThemeChange('light')}>Light Mode</button>
```

## Responsive Design

Kanban adapts to different screen sizes automatically:

```tsx
import * as React from 'react';
import { useState, useEffect } from 'react';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';

export default function ResponsiveKanban() {
  const [isMobile, setIsMobile] = useState<boolean>(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = (): void => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Hide less-critical columns on mobile
  const getVisibleColumns = (): string[] => {
    const visibleStatuses = isMobile
      ? ['Open', 'InProgress', 'Closed']
      : ['Open', 'InProgress', 'Testing', 'Closed'];
    return visibleStatuses;
  };

  return (
    <KanbanComponent>
      <ColumnsDirective>
        {getVisibleColumns().map(status => (
          <ColumnDirective key={status} keyField={status} />
        ))}
      </ColumnsDirective>
    </KanbanComponent>
  );
}
```

### Mobile Card Adaptation

```tsx
import { ReactElement } from 'react';

// Card props expected: { Id, Summary, Priority, Assignee }
const cardTemplate = (props: any): ReactElement => {
  const isMobile = window.innerWidth < 768;
  
  if (isMobile) {
    // Compact card for mobile
    return (
      <div style={{ padding: '8px' }}>
        <div style={{ fontWeight: 'bold', fontSize: '13px' }}>{props.Id}</div>
        <div style={{ fontSize: '12px', marginTop: '4px' }}>{props.Summary}</div>
      </div>
    );
  }

  // Full card for desktop
  return (
    <div style={{ padding: '12px' }}>
      <div style={{ fontWeight: 'bold' }}>{props.Id}</div>
      <div>{props.Summary}</div>
      <div style={{ marginTop: '8px', display: 'flex', gap: '8px' }}>
        <span>{props.Priority}</span>
        <span>{props.Assignee}</span>
      </div>
    </div>
  );
};
```

## Virtual Scrolling

Enable for large datasets to improve performance:

```tsx
// Data shape: { Id, Summary }
<KanbanComponent
  enableVirtualization={true}
  cardSettings={{
    headerField: 'Id',
    contentField: 'Summary'
  }}
>
  {/* Only visible cards render, scrolling loads more */}
</KanbanComponent>
```

**Benefits:**
- Handles 1000+ cards smoothly
- Reduces DOM nodes by rendering only visible cards
- Improves scroll performance

**Trade-offs:**
- May have slight scroll jump initially
- Not ideal for animations across all cards

## Persistence (Saving State)

Save Kanban state to localStorage or database:

### Save to localStorage

```tsx
import * as React from 'react';
import { useState } from 'react';
import { KanbanComponent, DragEventArgs } from '@syncfusion/ej2-react-kanban';

// Card shape: { Id, Status, Summary }
export default function PersistentKanban() {
  const [data, setData] = useState(() => {
    const saved = localStorage.getItem('kanban-data');
    return saved ? JSON.parse(saved) : initialData;
  });

  const handleDragStop = (args: DragEventArgs): void => {
    // Update state and persist
    const updated = data.map(card =>
      card.Id === args.data.Id ? args.data : card
    );
    setData(updated);
    localStorage.setItem('kanban-data', JSON.stringify(updated));
  };

  return (
    <KanbanComponent
      dataSource={data}
      dragStop={handleDragStop}
    >
      {/* ... */}
    </KanbanComponent>
  );
}
```

### Save to Server via API

```tsx
import { DragEventArgs } from '@syncfusion/ej2-react-kanban';

const handleDragStop = (args: DragEventArgs): void => {
  // Save to server
  fetch('/api/tasks/' + args.data.Id, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(args.data)
  }).then(r => {
    if (!r.ok) {
      console.error('Save failed');
      // Revert card position
      args.cancel = true;
    }
  });
};
```

## Localization

Translate Kanban text to different languages:

```tsx
import { L10n } from '@syncfusion/ej2-base';

// Define translations
L10n.load({
  'fr': {
    'kanban': {
      'cardSaveButton': 'Enregistrer',
      'cardDeleteButton': 'Supprimer',
      'cardCancelButton': 'Annuler'
    }
  },
  'es': {
    'kanban': {
      'cardSaveButton': 'Guardar',
      'cardDeleteButton': 'Eliminar',
      'cardCancelButton': 'Cancelar'
    }
  }
});

// Apply locale
<KanbanComponent locale="fr">
  {/* Dialog buttons show French text */}
</KanbanComponent>
```

### Custom Translations

```tsx
import { L10n } from '@syncfusion/ej2-base';

L10n.load({
  'en': {
    'kanban': {
      'placeholder': 'Search tasks...',
      'addButton': '+ Add Card',
      'deleteConfirm': 'Are you sure?'
    }
  }
});
```

## Accessibility

### ARIA Labels

```tsx
import { ReactElement } from 'react';

// Card props expected: { Id, Summary, Priority }
const cardTemplate = (props: any): ReactElement => {
  return (
    <div
      role="button"
      tabIndex={0}
      aria-label={`Task ${props.Id}: ${props.Summary}, Priority: ${props.Priority}`}
    >
      {props.Summary}
    </div>
  );
};
```

### Keyboard Navigation

- **Tab**: Navigate between cards
- **Enter**: Click/activate card
- **Space**: Select card (if multi-select)
- **Arrow keys**: Move focus within column

### Screen Reader Support

```tsx
// Data shape: { Id, Status, Summary }
<KanbanComponent
  aria-label="Project task board with columns for workflow stages"
  aria-describedby="kanban-description"
>
  <div id="kanban-description" style={{ display: 'none' }}>
    Drag and drop cards between columns to change task status.
    Double-click a card to edit. Columns show task counts.
  </div>
  {/* ... */}
</KanbanComponent>
```

### Color Contrast

```css
/* Ensure text is readable */
.e-card {
  color: #212121;  /* Dark text on light background */
  background-color: #ffffff;
}

.e-card.dark-theme {
  color: #ffffff;  /* Light text on dark background */
  background-color: #1e1e1e;
}
```

### High Contrast Mode Support

```css
@media (prefers-contrast: more) {
  .e-card {
    border: 2px solid #000;
    color: #000;
    background-color: #fff;
  }
}
```
