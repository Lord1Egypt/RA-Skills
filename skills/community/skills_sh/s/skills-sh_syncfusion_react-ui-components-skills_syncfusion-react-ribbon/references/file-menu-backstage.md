# File Menu and Backstage View

## Table of Contents
- [File Menu Basics](#file-menu-basics)
- [Adding File Menu](#adding-file-menu)
- [Menu Items Configuration](#menu-items-configuration)
- [File Menu Item Template](#file-menu-item-template)
- [File Menu Popup Template](#file-menu-popup-template)
- [File Menu Animation Settings](#file-menu-animation-settings)
- [File Menu Tooltip Settings](#file-menu-tooltip-settings)
- [File Menu Events](#file-menu-events)
- [Backstage View](#backstage-view)
- [Backstage Items](#backstage-items)
- [Footer Items](#footer-items)
- [Backstage Advanced Configuration](#backstage-advanced-configuration)

## File Menu Basics

The Ribbon file menu provides quick access to file-related operations (New, Open, Save, etc.).

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective, RibbonFileMenu, Inject } from "@syncfusion/ej2-react-ribbon";
import { MenuItemModel } from '@syncfusion/ej2-navigations';

function App() {
  const fileOptions: MenuItemModel[] = [
    { text: "New", iconCss: "e-icons e-file-new", id: "new" },
    { text: "Open", iconCss: "e-icons e-folder-open", id: "open" },
    { text: "Save", iconCss: "e-icons e-save", id: "save" },
    { text: "Save as", iconCss: "e-icons e-save", id: "saveas" }
  ];

  return (
    <RibbonComponent id="ribbon" fileMenu={{ visible: true, menuItems: fileOptions }}>
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          {/* Tabs and groups */}
        </RibbonTabDirective>
      </RibbonTabsDirective>
      <Inject services={[RibbonFileMenu]} />
    </RibbonComponent>
  );
}

export default App;
```

## Adding File Menu

Set file menu visibility and configure items:

```tsx
const fileOptions: MenuItemModel[] = [
  { text: "New", iconCss: "e-icons e-file-new", id: "new" },
  { text: "Open", iconCss: "e-icons e-folder-open", id: "Open" },
  { text: "Rename", iconCss: "e-icons e-rename", id: "rename" },
  { text: "Save as", iconCss: "e-icons e-save", id: "save" }
];

<RibbonComponent id="ribbon" fileMenu={{ visible: true, menuItems: fileOptions }}>
  {/* Ribbon content */}
</RibbonComponent>
```

**File Menu Properties:**
- `visible` (boolean) - Show/hide file menu (default: false)
- `menuItems` (MenuItemModel[]) - Array of menu items

## Menu Items Configuration

Define file menu items with text, icons, and submenus:

```tsx
const fileOptions: MenuItemModel[] = [
  { text: "New", iconCss: "e-icons e-file-new", id: "new" },
  { text: "Open", iconCss: "e-icons e-folder-open", id: "open" },
  { text: "Rename", iconCss: "e-icons e-rename", id: "rename" },
  {
    text: "Save as",
    iconCss: "e-icons e-save",
    id: "saveas",
    items: [
      { text: "Microsoft Word (.docx)", iconCss: "sf-icon-word", id: "newword" },
      { text: "Microsoft Word 97-2003 (.doc)", iconCss: "sf-icon-word", id: "oldword" },
      { text: "Download as PDF", iconCss: "e-icons e-export-pdf", id: "pdf" }
    ]
  }
];

<RibbonComponent id="ribbon" fileMenu={{ visible: true, showItemOnClick: true, menuItems: fileOptions }}>
  {/* Ribbon content */}
</RibbonComponent>
```

**Menu Item Properties:**
- `text` (string) - Menu item text
- `iconCss` (string) - Icon class
- `id` (string) - Unique identifier
- `items` (MenuItemModel[]) - Submenu items
- `url` (string) - Navigation URL (optional)

**Open Submenu on Click:**

```tsx
fileMenu={{ 
  visible: true, 
  showItemOnClick: true,  // Opens on click instead of hover
  menuItems: fileOptions 
}}
```

## File Menu Item Template

Customize the appearance of file menu items using templates:

```tsx
import { RibbonComponent, RibbonFileMenu, Inject } from "@syncfusion/ej2-react-ribbon";
import { MenuItemModel } from '@syncfusion/ej2-navigations';

function App() {
  const fileOptions: MenuItemModel[] = [
    { text: "New", iconCss: "e-icons e-file-new", id: "new" },
    { text: "Open", iconCss: "e-icons e-folder-open", id: "open" },
    { text: "Save", iconCss: "e-icons e-save", id: "save" }
  ];

  const itemTemplate = (props: any) => {
    return (
      <div style={{ display: 'flex', alignItems: 'center', padding: '8px' }}>
        <span className={props.iconCss} style={{ marginRight: '10px', fontSize: '16px' }}></span>
        <div>
          <div style={{ fontWeight: 'bold' }}>{props.text}</div>
          <div style={{ fontSize: '11px', color: '#666' }}>
            {props.id === 'new' && 'Create a new document'}
            {props.id === 'open' && 'Open an existing document'}
            {props.id === 'save' && 'Save current document'}
          </div>
        </div>
      </div>
    );
  };

  return (
    <RibbonComponent 
      id="ribbon" 
      fileMenu={{ 
        visible: true, 
        menuItems: fileOptions,
        itemTemplate: itemTemplate
      }}>
      <RibbonTabsDirective>
        {/* Tabs */}
      </RibbonTabsDirective>
      <Inject services={[RibbonFileMenu]} />
    </RibbonComponent>
  );
}

export default App;
```

**itemTemplate Property:**
- **Type:** `string | function | JSX.Element`
- **Purpose:** Customize rendering of each menu item
- **Context:** Receives menu item data as props

## File Menu Popup Template

Define custom content for the file menu popup area:

```tsx
import { RibbonComponent, RibbonFileMenu, Inject } from "@syncfusion/ej2-react-ribbon";
import { MenuItemModel } from '@syncfusion/ej2-navigations';

function App() {
  const fileOptions: MenuItemModel[] = [
    { text: "New", iconCss: "e-icons e-file-new", id: "new" },
    { text: "Open", iconCss: "e-icons e-folder-open", id: "open" }
  ];

  const popupTemplate = () => {
    return (
      <div style={{ padding: '20px', width: '300px', backgroundColor: '#f9f9f9' }}>
        <h3 style={{ marginTop: 0 }}>Recent Documents</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ padding: '8px', borderBottom: '1px solid #ddd', cursor: 'pointer' }}>
            <span className="e-icons e-file-new" style={{ marginRight: '8px' }}></span>
            Document1.docx
          </li>
          <li style={{ padding: '8px', borderBottom: '1px solid #ddd', cursor: 'pointer' }}>
            <span className="e-icons e-file-new" style={{ marginRight: '8px' }}></span>
            Document2.docx
          </li>
          <li style={{ padding: '8px', cursor: 'pointer' }}>
            <span className="e-icons e-file-new" style={{ marginRight: '8px' }}></span>
            Document3.docx
          </li>
        </ul>
      </div>
    );
  };

  return (
    <RibbonComponent 
      id="ribbon" 
      fileMenu={{ 
        visible: true, 
        menuItems: fileOptions,
        popupTemplate: popupTemplate
      }}>
      <RibbonTabsDirective>
        {/* Tabs */}
      </RibbonTabsDirective>
      <Inject services={[RibbonFileMenu]} />
    </RibbonComponent>
  );
}

export default App;
```

**popupTemplate Property:**
- **Type:** `string | HTMLElement | JSX.Element`
- **Purpose:** Display custom content alongside menu items
- **Use Case:** Recent files, account info, quick actions

## File Menu Animation Settings

Configure animation effects for submenu open/close:

```tsx
import { RibbonComponent, RibbonFileMenu, Inject } from "@syncfusion/ej2-react-ribbon";
import { MenuItemModel, MenuAnimationSettingsModel } from '@syncfusion/ej2-navigations';

function App() {
  const fileOptions: MenuItemModel[] = [
    { 
      text: "Save as",
      iconCss: "e-icons e-save",
      id: "saveas",
      items: [
        { text: "Microsoft Word (.docx)", id: "docx" },
        { text: "PDF Document (.pdf)", id: "pdf" },
        { text: "Plain Text (.txt)", id: "txt" }
      ]
    },
    { text: "Print", iconCss: "e-icons e-print", id: "print" }
  ];

  const animationSettings: MenuAnimationSettingsModel = {
    effect: 'SlideDown',
    duration: 400,
    easing: 'ease'
  };

  return (
    <RibbonComponent 
      id="ribbon" 
      fileMenu={{ 
        visible: true, 
        menuItems: fileOptions,
        animationSettings: animationSettings
      }}>
      <RibbonTabsDirective>
        {/* Tabs */}
      </RibbonTabsDirective>
      <Inject services={[RibbonFileMenu]} />
    </RibbonComponent>
  );
}

export default App;
```

**Animation Settings Properties:**
- **effect:** Animation type - 'None', 'SlideDown', 'ZoomIn', 'FadeIn'
- **duration:** Animation duration in milliseconds (default: 400)
- **easing:** Easing function - 'ease', 'linear', 'ease-in', 'ease-out', 'ease-in-out'

## File Menu Tooltip Settings

Add tooltips to the file menu button:

```tsx
import { RibbonComponent, RibbonFileMenu, Inject } from "@syncfusion/ej2-react-ribbon";
import { MenuItemModel } from '@syncfusion/ej2-navigations';
import { RibbonTooltipModel } from '@syncfusion/ej2-react-ribbon';

function App() {
  const fileOptions: MenuItemModel[] = [
    { text: "New", iconCss: "e-icons e-file-new", id: "new" },
    { text: "Open", iconCss: "e-icons e-folder-open", id: "open" },
    { text: "Save", iconCss: "e-icons e-save", id: "save" }
  ];

  const tooltipSettings: RibbonTooltipModel = {
    title: 'File Menu',
    content: 'Access file operations like New, Open, Save, and Print',
    cssClass: 'custom-tooltip'
  };

  return (
    <RibbonComponent 
      id="ribbon" 
      fileMenu={{ 
        visible: true, 
        menuItems: fileOptions,
        ribbonTooltipSettings: tooltipSettings
      }}>
      <RibbonTabsDirective>
        {/* Tabs */}
      </RibbonTabsDirective>
      <Inject services={[RibbonFileMenu]} />
    </RibbonComponent>
  );
}

export default App;
```

**Tooltip Settings Properties:**
- **title:** Tooltip header text
- **content:** Tooltip body content
- **cssClass:** Custom CSS class for styling

## File Menu Events

Handle file menu interactions with events:

```tsx
import { RibbonComponent, RibbonFileMenu, Inject } from "@syncfusion/ej2-react-ribbon";
import { MenuItemModel, FileMenuEventArgs, FileMenuBeforeOpenCloseEventArgs, FileMenuOpenCloseEventArgs } from '@syncfusion/ej2-navigations';

function App() {
  const fileOptions: MenuItemModel[] = [
    { text: "New", iconCss: "e-icons e-file-new", id: "new" },
    { text: "Open", iconCss: "e-icons e-folder-open", id: "open" },
    { text: "Save", iconCss: "e-icons e-save", id: "save" },
    { text: "Print", iconCss: "e-icons e-print", id: "print" }
  ];

  // Event: Before opening file menu
  const handleBeforeOpen = (args: FileMenuBeforeOpenCloseEventArgs) => {
    console.log('File menu is about to open');
    // args.cancel = true; // Uncomment to prevent opening
  };

  // Event: After file menu opens
  const handleOpen = (args: FileMenuOpenCloseEventArgs) => {
    console.log('File menu opened');
  };

  // Event: Before closing file menu
  const handleBeforeClose = (args: FileMenuBeforeOpenCloseEventArgs) => {
    console.log('File menu is about to close');
    // args.cancel = true; // Uncomment to prevent closing
  };

  // Event: After file menu closes
  const handleClose = (args: FileMenuOpenCloseEventArgs) => {
    console.log('File menu closed');
  };

  // Event: Before rendering each menu item
  const handleBeforeItemRender = (args: FileMenuEventArgs) => {
    console.log(`Rendering menu item: ${args.item.text}`);
    // Customize item rendering
    if (args.item.id === 'new') {
      args.element.style.backgroundColor = '#e3f2fd';
    }
  };

  // Event: When menu item is selected
  const handleSelect = (args: FileMenuEventArgs) => {
    console.log(`Menu item selected: ${args.item.text}`);
    
    switch (args.item.id) {
      case 'new':
        console.log('Creating new document...');
        break;
      case 'open':
        console.log('Opening document...');
        break;
      case 'save':
        console.log('Saving document...');
        break;
      case 'print':
        console.log('Printing document...');
        break;
    }
  };

  return (
    <RibbonComponent 
      id="ribbon" 
      fileMenu={{ 
        visible: true, 
        menuItems: fileOptions,
        beforeOpen: handleBeforeOpen,
        open: handleOpen,
        beforeClose: handleBeforeClose,
        close: handleClose,
        beforeItemRender: handleBeforeItemRender,
        select: handleSelect
      }}>
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          {/* Groups and items */}
        </RibbonTabDirective>
      </RibbonTabsDirective>
      <Inject services={[RibbonFileMenu]} />
    </RibbonComponent>
  );
}

export default App;
```

**Available File Menu Events:**

| Event | Type | Description |
|-------|------|-------------|
| **beforeOpen** | `FileMenuBeforeOpenCloseEventArgs` | Triggers before opening file menu popup. Set `args.cancel = true` to prevent opening. |
| **open** | `FileMenuOpenCloseEventArgs` | Triggers after file menu popup opens. |
| **beforeClose** | `FileMenuBeforeOpenCloseEventArgs` | Triggers before closing file menu popup. Set `args.cancel = true` to prevent closing. |
| **close** | `FileMenuOpenCloseEventArgs` | Triggers after file menu popup closes. |
| **beforeItemRender** | `FileMenuEventArgs` | Triggers while rendering each menu item. Use to customize item appearance. |
| **select** | `FileMenuEventArgs` | Triggers when a menu item is selected/clicked. |

**Event Arguments Properties:**

**FileMenuEventArgs:**
- `element` (HTMLElement) - Menu item element
- `item` (MenuItemModel) - Menu item data

**FileMenuBeforeOpenCloseEventArgs:**
- `cancel` (boolean) - Set to true to cancel the action
- `element` (HTMLElement) - File menu element
- `event` (Event) - Original browser event

**FileMenuOpenCloseEventArgs:**
- `element` (HTMLElement) - File menu element

### Complete Event Example

```tsx
function App() {
  const [isModified, setIsModified] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);

  const fileOptions: MenuItemModel[] = [
    { text: "New", iconCss: "e-icons e-file-new", id: "new" },
    { text: "Save", iconCss: "e-icons e-save", id: "save" },
    { text: "Exit", iconCss: "e-icons e-close", id: "exit" }
  ];

  const handleBeforeClose = (args: FileMenuBeforeOpenCloseEventArgs) => {
    if (isModified) {
      const confirm = window.confirm('You have unsaved changes. Close anyway?');
      if (!confirm) {
        args.cancel = true; // Prevent closing
      }
    }
  };

  const handleSelect = (args: FileMenuEventArgs) => {
    const log = `Selected: ${args.item.text} at ${new Date().toLocaleTimeString()}`;
    setLogs(prev => [...prev, log]);

    if (args.item.id === 'save') {
      setIsModified(false);
    } else if (args.item.id === 'new') {
      setIsModified(true);
    }
  };

  return (
    <div>
      <RibbonComponent 
        id="ribbon" 
        fileMenu={{ 
          visible: true, 
          menuItems: fileOptions,
          beforeClose: handleBeforeClose,
          select: handleSelect
        }}>
        <RibbonTabsDirective>
          {/* Tabs */}
        </RibbonTabsDirective>
        <Inject services={[RibbonFileMenu]} />
      </RibbonComponent>

      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f5f5f5' }}>
        <h4>Event Log:</h4>
        <ul>
          {logs.map((log, index) => (
            <li key={index}>{log}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

## Backstage View

Backstage is a comprehensive replacement for file menu, displaying application settings and information.

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective, RibbonBackstage, Inject, BackStageMenuModel } from "@syncfusion/ej2-react-ribbon";

function App() {
  const backstageSettings: BackStageMenuModel = {
    visible: true,
    items: [
      { 
        id: 'home', 
        text: 'Home', 
        iconCss: 'e-icons e-home', 
        content: "<div style='padding: 20px;'><h2>Welcome to Backstage</h2></div>" 
      },
      { 
        id: 'new', 
        text: 'New', 
        iconCss: 'e-icons e-file-new', 
        content: "<div style='padding: 20px;'><h2>Create New Document</h2></div>" 
      },
      { 
        id: 'open', 
        text: 'Open', 
        iconCss: 'e-icons e-folder-open', 
        content: "<div style='padding: 20px;'><h2>Open Document</h2></div>" 
      }
    ],
    backButton: { text: 'Close' }
  };

  return (
    <RibbonComponent id="ribbon" backStageMenu={backstageSettings}>
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          {/* Tabs and groups */}
        </RibbonTabDirective>
      </RibbonTabsDirective>
      <Inject services={[RibbonBackstage]} />
    </RibbonComponent>
  );
}

export default App;
```

## Backstage Items

Configure backstage items with custom content:

```tsx
const backstageSettings: BackStageMenuModel = {
  visible: true,
  items: [
    {
      id: 'home',
      text: 'Home',
      iconCss: 'e-icons e-home',
      content: homeContentTemplate()
    },
    {
      id: 'new',
      text: 'New',
      iconCss: 'e-icons e-file-new',
      content: newContentTemplate()
    }
  ],
  backButton: {
    text: 'Close'
  }
};

function homeContentTemplate() {
  return `
    <div id='home-wrapper' style='padding: 20px;'>
      <div id='new-section' class='new-wrapper'>
        <div class='section-title'> New </div>
        <div class='category_container'>
          <div class='doc_category_image'></div>
          <span class='doc_category_text'> New document </span>
        </div>
      </div>
      <div id='block-wrapper'>
        <div class='section-title'> Recent </div>
        <div class='section-content' style='padding: 12px 0px; cursor: pointer'>
          <table>
            <tbody>
              <tr>
                <td> <span class='doc_icon e-icons e-open-link'></span> </td>
                <td>
                  <span style='display: block; font-size: 14px'> Document.docx </span>
                  <span style='font-size: 12px'> Path >> To >> Document </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}
```

**Backstage Item Properties:**
- `id` (string) - Unique identifier
- `text` (string) - Display text
- `iconCss` (string) - Icon class
- `content` (string) - HTML content for backstage pane
- `isFooter` (boolean) - Display as footer item

## Footer Items

Add footer items to backstage for account or settings info:

```tsx
const backstageSettings: BackStageMenuModel = {
  visible: true,
  items: [
    // Regular items
    { id: 'home', text: 'Home', iconCss: 'e-icons e-home', content: homeContent() },
    { id: 'new', text: 'New', iconCss: 'e-icons e-file-new', content: newContent() },
    
    // Separator
    { separator: true, isFooter: true },
    
    // Footer item
    {
      id: 'account',
      text: 'Account',
      isFooter: true,
      content: `
        <div style='padding: 20px;'>
          <div class='section-content' style='padding: 12px 0px;'>
            <table>
              <tbody>
                <tr>
                  <td> <span class='doc_icon e-icons e-people'></span> </td>
                  <td>
                    <span style='display: block; font-size: 14px'>Account type</span>
                    <span style='font-size: 12px'>Administrator</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      `
    }
  ],
  backButton: { text: 'Close' }
};
```

**Separator Item:**
- Use `{ separator: true, isFooter: true }` to add visual separator above footer items

## Complete Backstage Example

```tsx
function App() {
  const backstageSettings: BackStageMenuModel = {
    visible: true,
    items: [
      {
        id: 'home',
        text: 'Home',
        iconCss: 'e-icons e-home',
        content: "<div style='padding: 20px;'><p>Welcome to Home</p></div>"
      },
      {
        id: 'new',
        text: 'New',
        iconCss: 'e-icons e-file-new',
        content: "<div style='padding: 20px;'><p>Create New Document</p></div>"
      },
      {
        id: 'open',
        text: 'Open',
        iconCss: 'e-icons e-folder-open',
        content: "<div style='padding: 20px;'><p>Open Existing Document</p></div>"
      },
      { separator: true, isFooter: true },
      {
        id: 'options',
        text: 'Options',
        isFooter: true,
        content: "<div style='padding: 20px;'><p>Application Options</p></div>"
      }
    ],
    backButton: {
      text: 'Close'
    }
  };

  return (
    <RibbonComponent id="ribbon" backStageMenu={backstageSettings}>
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Clipboard">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
      <Inject services={[RibbonBackstage]} />
    </RibbonComponent>
  );
}

export default App;
```

## Backstage Advanced Configuration

### Backstage Width and Height

Control the dimensions of the backstage view:

```tsx
import { RibbonComponent, RibbonBackstage, Inject, BackStageMenuModel } from "@syncfusion/ej2-react-ribbon";

function App() {
  const backstageSettings: BackStageMenuModel = {
    visible: true,
    width: '600px',    // Custom width
    height: '500px',   // Custom height
    items: [
      { 
        id: 'home', 
        text: 'Home', 
        iconCss: 'e-icons e-home', 
        content: "<div style='padding: 20px;'><h2>Home</h2></div>" 
      },
      { 
        id: 'settings', 
        text: 'Settings', 
        iconCss: 'e-icons e-settings', 
        content: "<div style='padding: 20px;'><h2>Settings</h2></div>" 
      }
    ],
    backButton: { text: 'Close' }
  };

  return (
    <RibbonComponent id="ribbon" backStageMenu={backstageSettings}>
      <RibbonTabsDirective>
        {/* Tabs */}
      </RibbonTabsDirective>
      <Inject services={[RibbonBackstage]} />
    </RibbonComponent>
  );
}

export default App;
```

**Dimension Properties:**
- **width:** Width of backstage menu (string, e.g., '600px', '50%')
- **height:** Height of backstage menu (string, e.g., '500px', '80vh')

### Backstage Target Element

Position backstage within a specific element:

```tsx
import { RibbonComponent, RibbonBackstage, Inject, BackStageMenuModel } from "@syncfusion/ej2-react-ribbon";

function App() {
  const backstageSettings: BackStageMenuModel = {
    visible: true,
    target: '#backstage-container',  // CSS selector for target element
    items: [
      { 
        id: 'home', 
        text: 'Home', 
        iconCss: 'e-icons e-home', 
        content: "<div style='padding: 20px;'><h2>Welcome</h2></div>" 
      }
    ],
    backButton: { text: 'Close' }
  };

  return (
    <div>
      <RibbonComponent id="ribbon" backStageMenu={backstageSettings}>
        <RibbonTabsDirective>
          {/* Tabs */}
        </RibbonTabsDirective>
        <Inject services={[RibbonBackstage]} />
      </RibbonComponent>

      {/* Target container for backstage */}
      <div id="backstage-container" style={{ 
        position: 'relative', 
        width: '100%', 
        height: '600px',
        border: '1px solid #ddd'
      }}>
        {/* Backstage will be positioned here */}
      </div>
    </div>
  );
}

export default App;
```

**target Property:**
- **Type:** `string | HTMLElement`
- **Purpose:** Defines element for backstage positioning
- **Default:** Document body

### Backstage KeyTip

Add keyboard shortcut access to backstage:

```tsx
import { RibbonComponent, RibbonBackstage, RibbonKeyTip, Inject, BackStageMenuModel } from "@syncfusion/ej2-react-ribbon";

function App() {
  const backstageSettings: BackStageMenuModel = {
    visible: true,
    text: 'File',
    keyTip: 'F',  // Press Alt+F to open backstage
    items: [
      { 
        id: 'new', 
        text: 'New', 
        iconCss: 'e-icons e-file-new',
        keyTip: 'N',  // Press N after opening backstage
        content: "<div style='padding: 20px;'><h2>Create New</h2></div>" 
      },
      { 
        id: 'open', 
        text: 'Open', 
        iconCss: 'e-icons e-folder-open',
        keyTip: 'O',
        content: "<div style='padding: 20px;'><h2>Open File</h2></div>" 
      }
    ],
    backButton: { text: 'Close' }
  };

  return (
    <RibbonComponent id="ribbon" enableKeyTips={true} backStageMenu={backstageSettings}>
      <RibbonTabsDirective>
        {/* Tabs */}
      </RibbonTabsDirective>
      <Inject services={[RibbonBackstage, RibbonKeyTip]} />
    </RibbonComponent>
  );
}

export default App;
```

**KeyTip Properties:**
- **keyTip** (backstage button): Keyboard shortcut for opening backstage
- **keyTip** (backstage items): Keyboard shortcuts for navigation within backstage
- **Requires:** `enableKeyTips={true}` on RibbonComponent and `RibbonKeyTip` service injection

### Backstage Tooltip Settings

Add tooltips to the backstage button:

```tsx
import { RibbonComponent, RibbonBackstage, Inject, BackStageMenuModel } from "@syncfusion/ej2-react-ribbon";
import { RibbonTooltipModel } from '@syncfusion/ej2-react-ribbon';

function App() {
  const tooltipSettings: RibbonTooltipModel = {
    title: 'Backstage',
    content: 'Access file operations, settings, and account information',
    cssClass: 'backstage-tooltip'
  };

  const backstageSettings: BackStageMenuModel = {
    visible: true,
    text: 'File',
    ribbonTooltipSettings: tooltipSettings,
    items: [
      { 
        id: 'home', 
        text: 'Home', 
        iconCss: 'e-icons e-home', 
        content: "<div style='padding: 20px;'><h2>Home</h2></div>" 
      }
    ],
    backButton: { text: 'Close' }
  };

  return (
    <RibbonComponent id="ribbon" backStageMenu={backstageSettings}>
      <RibbonTabsDirective>
        {/* Tabs */}
      </RibbonTabsDirective>
      <Inject services={[RibbonBackstage]} />
    </RibbonComponent>
  );
}

export default App;
```

**ribbonTooltipSettings Properties:**
- **title:** Tooltip header
- **content:** Tooltip description
- **cssClass:** Custom CSS class for styling

### Backstage Template

Use a custom template for backstage content:

```tsx
import { RibbonComponent, RibbonBackstage, Inject, BackStageMenuModel } from "@syncfusion/ej2-react-ribbon";

function App() {
  const backstageTemplate = () => {
    return (
      <div style={{ display: 'flex', height: '100%' }}>
        <div style={{ width: '200px', backgroundColor: '#f0f0f0', padding: '20px' }}>
          <h3>Navigation</h3>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li style={{ padding: '10px', cursor: 'pointer' }}>New</li>
            <li style={{ padding: '10px', cursor: 'pointer' }}>Open</li>
            <li style={{ padding: '10px', cursor: 'pointer' }}>Save</li>
          </ul>
        </div>
        <div style={{ flex: 1, padding: '20px' }}>
          <h2>Welcome to Backstage</h2>
          <p>Select an option from the navigation menu.</p>
        </div>
      </div>
    );
  };

  const backstageSettings: BackStageMenuModel = {
    visible: true,
    text: 'File',
    template: backstageTemplate,  // Custom template overrides items
    backButton: { text: 'Close' }
  };

  return (
    <RibbonComponent id="ribbon" backStageMenu={backstageSettings}>
      <RibbonTabsDirective>
        {/* Tabs */}
      </RibbonTabsDirective>
      <Inject services={[RibbonBackstage]} />
    </RibbonComponent>
  );
}

export default App;
```

**template Property:**
- **Type:** `string | function | JSX.Element`
- **Purpose:** Completely custom backstage content
- **Note:** When template is used, `items` property is ignored

### Complete Backstage Configuration Example

```tsx
import { RibbonComponent, RibbonBackstage, RibbonKeyTip, Inject, BackStageMenuModel } from "@syncfusion/ej2-react-ribbon";
import { RibbonTooltipModel } from '@syncfusion/ej2-react-ribbon';

function App() {
  const tooltipSettings: RibbonTooltipModel = {
    title: 'File Menu',
    content: 'Manage your documents and settings'
  };

  const backstageSettings: BackStageMenuModel = {
    visible: true,
    text: 'File',
    width: '700px',
    height: '600px',
    keyTip: 'F',
    ribbonTooltipSettings: tooltipSettings,
    items: [
      { 
        id: 'home', 
        text: 'Home', 
        iconCss: 'e-icons e-home',
        keyTip: 'H',
        content: `
          <div style='padding: 20px;'>
            <h2>Welcome</h2>
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px;'>
              <div style='padding: 15px; border: 1px solid #ddd; border-radius: 4px; cursor: pointer;'>
                <h3>New Document</h3>
                <p>Create a blank document</p>
              </div>
              <div style='padding: 15px; border: 1px solid #ddd; border-radius: 4px; cursor: pointer;'>
                <h3>From Template</h3>
                <p>Start with a template</p>
              </div>
              <div style='padding: 15px; border: 1px solid #ddd; border-radius: 4px; cursor: pointer;'>
                <h3>Recent</h3>
                <p>Open recent documents</p>
              </div>
            </div>
          </div>
        `
      },
      { 
        id: 'open', 
        text: 'Open', 
        iconCss: 'e-icons e-folder-open',
        keyTip: 'O',
        content: "<div style='padding: 20px;'><h2>Open Document</h2><p>Browse and open files.</p></div>" 
      },
      { 
        id: 'save', 
        text: 'Save As', 
        iconCss: 'e-icons e-save',
        keyTip: 'A',
        content: "<div style='padding: 20px;'><h2>Save As</h2><p>Save your document to a location.</p></div>" 
      },
      { separator: true, isFooter: true },
      {
        id: 'settings',
        text: 'Settings',
        iconCss: 'e-icons e-settings',
        keyTip: 'S',
        isFooter: true,
        content: "<div style='padding: 20px;'><h2>Application Settings</h2></div>"
      }
    ],
    backButton: { text: 'Close' }
  };

  return (
    <RibbonComponent id="ribbon" enableKeyTips={true} backStageMenu={backstageSettings}>
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          {/* Groups and items */}
        </RibbonTabDirective>
      </RibbonTabsDirective>
      <Inject services={[RibbonBackstage, RibbonKeyTip]} />
    </RibbonComponent>
  );
}

export default App;
```

## Best Practices

1. **Logical Organization:** Group related file operations
2. **Clear Icons:** Use consistent, recognizable icons
3. **Navigation:** Use `url` property for navigation items
4. **Content:** Keep backstage content organized and scannable
5. **Footer:** Use for account and settings items
6. **Dimensions:** Set appropriate width/height for your content
7. **KeyTips:** Provide keyboard shortcuts for accessibility
8. **Tooltips:** Add helpful tooltips to the backstage button
9. **Templates:** Use custom templates for complex layouts
10. **Performance:** Keep backstage content lightweight for fast loading
