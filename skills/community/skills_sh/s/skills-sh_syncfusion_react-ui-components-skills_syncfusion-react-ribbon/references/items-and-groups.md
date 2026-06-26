# Items and Groups Configuration

## Table of Contents
- [Item Types Overview](#item-types-overview)
- [Button Items](#button-items)
- [CheckBox Items](#checkbox-items)
- [DropDown Items](#dropdown-items)
- [SplitButton Items](#splitbutton-items)
- [ComboBox Items](#combobox-items)
- [ColorPicker Items](#colorpicker-items)
- [GroupButton Items](#groupbutton-items)
- [Template Items](#template-items)
- [Item Display Options](#item-display-options)
- [Item Sizing](#item-sizing)
- [Item Active Size](#item-active-size)
- [Item CSS Customization](#item-css-customization)
- [Item Tooltips](#item-tooltips)
- [Item Template for Custom Items](#item-template-for-custom-items)
- [Enable or Disable Items](#enable-or-disable-items)
- [Group Configuration](#group-configuration)
- [Group Orientation](#group-orientation)

## Item Types Overview

The Ribbon supports the following built-in item types:

| Type | Purpose | Common Use Cases |
|------|---------|------------------|
| Button | Clickable action button | Save, Print, Cut, Copy |
| CheckBox | Binary selection | Show/Hide options, Toggles |
| DropDown | Dropdown menu selector | Style selection, Theme picker |
| SplitButton | Primary action + dropdown | Paste (with options), Insert (with variants) |
| ComboBox | Text input + list selection | Font selection, Size picker |
| ColorPicker | Color selection | Font color, Highlight color |
| GroupButton | Related button group | Alignment (Left, Center, Right) |
| Gallery | Visual item grid | Style gallery, Template picker |
| Template | Custom HTML content | Custom controls, Complex UI |

## Button Items

Basic button item with icon and click handling:

```tsx
import { RibbonItemDirective, RibbonItemSize } from "@syncfusion/ej2-react-ribbon";

<RibbonItemDirective type="Button" 
  buttonSettings={{ 
    iconCss: "e-icons e-cut", 
    content: "Cut" 
  }}>
</RibbonItemDirective>
```

**Button with Toggle Behavior:**

```tsx
<RibbonItemDirective type="Button" 
  buttonSettings={{ 
    iconCss: "e-icons e-bold", 
    content: "Bold", 
    isToggle: true 
  }}>
</RibbonItemDirective>
```

**Button Properties:**
- `content` - Button text
- `iconCss` - Icon class (e.g., "e-icons e-cut")
- `isToggle` - True for toggle button behavior (boolean)
- `disabled` - Disable the button (boolean)

## CheckBox Items

Checkbox for binary selection:

```tsx
<RibbonItemDirective type="CheckBox" 
  checkBoxSettings={{ 
    label: "Ruler", 
    checked: true 
  }}>
</RibbonItemDirective>
```

**With Label Position:**

```tsx
<RibbonItemDirective type="CheckBox" 
  checkBoxSettings={{ 
    label: "Ruler", 
    labelPosition: "Before", 
    checked: false 
  }}>
</RibbonItemDirective>
```

**CheckBox Properties:**
- `label` - Text label for checkbox
- `labelPosition` - "Before" or "After" (default: "After")
- `checked` - Initial checked state (boolean)

## DropDown Items

Dropdown button with menu options:

```tsx
import { ItemModel } from "@syncfusion/ej2-splitbuttons";

const tableOptions: ItemModel[] = [
  { text: "Insert Table" },
  { text: "This device" },
  { text: "Convert Table" },
  { text: "Excel SpreadSheet" }
];

<RibbonItemDirective type="DropDown" 
  dropDownSettings={{ 
    iconCss: "e-icons e-table", 
    items: tableOptions, 
    content: "Table" 
  }}>
</RibbonItemDirective>
```

**DropDown with beforeItemRender Event:**

```tsx
import { MenuEventArgs } from "@syncfusion/ej2-splitbuttons";

<RibbonItemDirective type="DropDown" 
  dropDownSettings={{ 
    iconCss: "e-icons e-table", 
    items: tableOptions, 
    content: "Table",
    beforeItemRender: function (args: MenuEventArgs) {
      if (args.item.text === 'Insert Table') {
        args.element.classList.add("e-custom-class");
      }
    }
  }}>
</RibbonItemDirective>
```

**On-Demand Popup Creation:**

```tsx
<RibbonItemDirective type="DropDown" 
  dropDownSettings={{ 
    iconCss: "e-icons e-table", 
    items: tableOptions, 
    content: "Table",
    createPopupOnClick: true
  }}>
</RibbonItemDirective>
```

**DropDown Properties:**
- `items` - Array of menu items (ItemModel[])
- `content` - Button text
- `iconCss` - Icon class
- `target` - Selector for custom popup content (optional)
- `beforeItemRender` - Event for customizing dropdown items
- `createPopupOnClick` - Create popup only on click (boolean)

## SplitButton Items

Button with primary action and dropdown options:

```tsx
const pasteOptions: ItemModel[] = [
  { text: "Keep Source Format" },
  { text: "Merge format" },
  { text: "Keep text only" }
];

<RibbonItemDirective type="SplitButton" 
  allowedSizes={RibbonItemSize.Large}
  splitButtonSettings={{ 
    iconCss: "e-icons e-paste", 
    items: pasteOptions, 
    content: "Paste" 
  }}>
</RibbonItemDirective>
```

**SplitButton with Target:**

```tsx
<RibbonItemDirective type="SplitButton" 
  splitButtonSettings={{ 
    iconCss: "e-icons e-image", 
    content: "Pictures", 
    target: "#pictureList" 
  }}>
</RibbonItemDirective>
```

**SplitButton Properties:**
- `items` - Array of dropdown options
- `content` - Button text
- `iconCss` - Icon class
- `target` - Selector for custom popup (optional)

## ComboBox Items

Text input with dropdown list:

```tsx
const fontStyle: string[] = ["Algerian", "Arial", "Calibri", "Cambria", "Georgia"];

<RibbonItemDirective type="ComboBox" 
  comboBoxSettings={{ 
    dataSource: fontStyle, 
    index: 1, 
    width: "150px", 
    allowFiltering: true 
  }}>
</RibbonItemDirective>
```

**With Sorting:**

```tsx
<RibbonItemDirective type="ComboBox" 
  comboBoxSettings={{ 
    dataSource: fontStyle, 
    index: 1, 
    width: "150px", 
    allowFiltering: true,
    sortOrder: "Descending"
  }}>
</RibbonItemDirective>
```

**ComboBox Properties:**
- `dataSource` - Array of items
- `index` - Initially selected index
- `width` - ComboBox width (string, e.g., "150px")
- `allowFiltering` - Enable filtering (boolean)
- `sortOrder` - "None", "Ascending", or "Descending"

## ColorPicker Items

Color selection control:

```tsx
import { RibbonColorPicker, Inject } from "@syncfusion/ej2-react-ribbon";

<RibbonItemDirective type="ColorPicker" 
  colorPickerSettings={{ 
    value: "#123456" 
  }}>
</RibbonItemDirective>
```

**Note:** ColorPicker requires module injection:
```tsx
<Inject services={[RibbonColorPicker]} />
```

**ColorPicker Properties:**
- `value` - Initial color value (hex code)
- `columns` - Number of color columns
- `showButtons` - Show OK/Cancel buttons (boolean)

## GroupButton Items

Group of related buttons:

```tsx
import { RibbonGroupButtonSelection, RibbonGroupButtonSettingsModel } from "@syncfusion/ej2-react-ribbon";

const groupButtonItem: RibbonGroupButtonSettingsModel = {
  selection: RibbonGroupButtonSelection.Single,
  items: [
    { iconCss: 'e-icons e-align-left', selected: true, content: 'Align Left' },
    { iconCss: 'e-icons e-align-center', content: 'Align Center' },
    { iconCss: 'e-icons e-align-right', content: 'Align Right' },
    { iconCss: 'e-icons e-justify', content: 'Justify' }
  ]
};

<RibbonItemDirective type="GroupButton" 
  allowedSizes={RibbonItemSize.Medium}
  groupButtonSettings={groupButtonItem}>
</RibbonItemDirective>
```

**Multiple Selection:**

```tsx
const groupButtonItem: RibbonGroupButtonSettingsModel = {
  selection: RibbonGroupButtonSelection.Multiple,
  items: [
    { iconCss: 'e-icons e-bold', content: 'Bold', selected: true },
    { iconCss: 'e-icons e-italic', content: 'Italic' },
    { iconCss: 'e-icons e-underline', content: 'Underline' }
  ]
};
```

**GroupButton Properties:**
- `items` - Array of button items
- `selection` - "Single" or "Multiple"
- Individual item properties:
  - `iconCss` - Icon class (required)
  - `content` - Button text
  - `selected` - Initially selected state (boolean)

## Template Items

Custom HTML/React content:

```tsx
<RibbonItemDirective type="Template" 
  itemTemplate={(props: any) => {
    return (
      <span className="ribbonTemplate">
        <span className="e-icons e-video"></span>
        <span className="text">Video</span>
      </span>
    );
  }}>
</RibbonItemDirective>
```

**Template with Custom Controls:**

```tsx
<RibbonItemDirective type="Template" 
  itemTemplate={(props: any) => {
    return (
      <div className="custom-template">
        <label htmlFor="fname">First name:</label>
        <input type="text" id="fname" name="fname"/>
        <br/>
        <label htmlFor="lname">Last name:</label>
        <input type="text" id="lname" name="lname"/>
      </div>
    );
  }}>
</RibbonItemDirective>
```

## Item Display Options

Control where items appear in different layouts:

```tsx
import { DisplayMode } from "@syncfusion/ej2-react-ribbon";

// Display only in Classic layout
<RibbonItemDirective type="Button" 
  displayOptions={DisplayMode.Classic}
  buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
</RibbonItemDirective>

// Display only in Simplified layout
<RibbonItemDirective type="Button" 
  displayOptions={DisplayMode.Simplified}
  buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
</RibbonItemDirective>

// Display only in overflow popup
<RibbonItemDirective type="Button" 
  displayOptions={DisplayMode.Overflow}
  buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
</RibbonItemDirective>
```

**Available Options:**
- `DisplayMode.Auto` - (Default) Display in all layouts
- `DisplayMode.Classic` - Classic layout only
- `DisplayMode.Simplified` - Simplified layout only
- `DisplayMode.Overflow` - Overflow popup only

## Item Sizing

Control item size with `allowedSizes`:

```tsx
import { RibbonItemSize } from "@syncfusion/ej2-react-ribbon";

// Large size
<RibbonItemDirective type="SplitButton" 
  allowedSizes={RibbonItemSize.Large}
  splitButtonSettings={{ content: "Paste" }}>
</RibbonItemDirective>

// Medium size
<RibbonItemDirective type="Button" 
  allowedSizes={RibbonItemSize.Medium}
  buttonSettings={{ content: "Copy" }}>
</RibbonItemDirective>

// Small size
<RibbonItemDirective type="Button" 
  allowedSizes={RibbonItemSize.Small}
  buttonSettings={{ content: "Cut" }}>
</RibbonItemDirective>
```

**Size Effects:**
- **Large:** Large icon with text below
- **Medium:** Small icon with text beside
- **Small:** Small icon only

Items resize automatically during ribbon resizing: Large → Medium → Small

## Item Active Size

Control the current active size of a ribbon item programmatically:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective, RibbonItemSize } from "@syncfusion/ej2-react-ribbon";
import { useRef, useState } from 'react';

function App() {
  const [currentSize, setCurrentSize] = useState<RibbonItemSize>(RibbonItemSize.Large);

  const changeToCut = () => {
    setCurrentSize(RibbonItemSize.Medium);
  };

  return (
    <div>
      <button onClick={changeToCut}>Change to Medium Size</button>
      
      <RibbonComponent id="ribbon">
        <RibbonTabsDirective>
          <RibbonTabDirective header="Home">
            <RibbonGroupsDirective>
              <RibbonGroupDirective header="Clipboard">
                <RibbonCollectionsDirective>
                  <RibbonCollectionDirective>
                    <RibbonItemsDirective>
                      <RibbonItemDirective 
                        type="Button" 
                        activeSize={currentSize}
                        allowedSizes={RibbonItemSize.Large | RibbonItemSize.Medium | RibbonItemSize.Small}
                        buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
                      </RibbonItemDirective>
                    </RibbonItemsDirective>
                  </RibbonCollectionDirective>
                </RibbonCollectionsDirective>
              </RibbonGroupDirective>
            </RibbonGroupsDirective>
          </RibbonTabDirective>
        </RibbonTabsDirective>
      </RibbonComponent>
    </div>
  );
}

export default App;
```

**activeSize Property:**
- **Type:** `RibbonItemSize`
- **Purpose:** Sets the current display size of the item
- **Values:** `RibbonItemSize.Large`, `RibbonItemSize.Medium`, `RibbonItemSize.Small`
- **Note:** Must be one of the sizes specified in `allowedSizes`

**Dynamic Size Control:**

```tsx
import { useRef } from 'react';

function App() {
  const ribbonRef = useRef<RibbonComponent>(null);

  const setItemSize = (itemId: string, size: RibbonItemSize) => {
    if (ribbonRef.current) {
      // Access item and update its active size
      const item = ribbonRef.current.element?.querySelector(`[id="${itemId}"]`);
      if (item) {
        // Update via component API
        console.log(`Setting ${itemId} to ${size}`);
      }
    }
  };

  return (
    <RibbonComponent id="ribbon" ref={ribbonRef}>
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Clipboard">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="Button" 
                      id="cutButton"
                      activeSize={RibbonItemSize.Large}
                      allowedSizes={RibbonItemSize.Large | RibbonItemSize.Medium}
                      buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}
```

**Use Cases:**
- Force specific item size regardless of ribbon width
- Maintain consistent sizing for important items
- Override automatic size adaptation
- Control item appearance programmatically

## Item CSS Customization

Apply custom CSS classes to individual items:

```tsx
import { RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";

// Single custom class
<RibbonItemDirective 
  type="Button" 
  cssClass="custom-button"
  buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
</RibbonItemDirective>

// Multiple classes
<RibbonItemDirective 
  type="Button" 
  cssClass="custom-button highlight-item"
  buttonSettings={{ iconCss: "e-icons e-copy", content: "Copy" }}>
</RibbonItemDirective>

// Conditional styling
<RibbonItemDirective 
  type="Button" 
  cssClass={isImportant ? "important-action" : "normal-action"}
  buttonSettings={{ iconCss: "e-icons e-save", content: "Save" }}>
</RibbonItemDirective>
```

**CSS Styling Example:**

```css
/* Custom button styles */
.custom-button .e-btn {
  background-color: #007bff;
  color: white;
  border-radius: 6px;
  font-weight: bold;
}

.custom-button .e-btn:hover {
  background-color: #0056b3;
}

/* Highlight important items */
.highlight-item {
  border: 2px solid #ffc107;
  padding: 2px;
  border-radius: 4px;
}

/* Important action styling */
.important-action .e-btn {
  background-color: #dc3545;
  color: white;
}

.important-action .e-btn:hover {
  background-color: #c82333;
}

/* Normal action styling */
.normal-action .e-btn {
  background-color: #6c757d;
  color: white;
}
```

**Complete Example with Custom Styling:**

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";
import './customStyles.css';

function App() {
  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Actions">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    {/* Primary action with custom style */}
                    <RibbonItemDirective 
                      type="Button" 
                      cssClass="primary-action"
                      buttonSettings={{ 
                        iconCss: "e-icons e-save", 
                        content: "Save" 
                      }}>
                    </RibbonItemDirective>

                    {/* Secondary action */}
                    <RibbonItemDirective 
                      type="Button" 
                      cssClass="secondary-action"
                      buttonSettings={{ 
                        iconCss: "e-icons e-cut", 
                        content: "Cut" 
                      }}>
                    </RibbonItemDirective>

                    {/* Danger action */}
                    <RibbonItemDirective 
                      type="Button" 
                      cssClass="danger-action"
                      buttonSettings={{ 
                        iconCss: "e-icons e-trash", 
                        content: "Delete" 
                      }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}

export default App;
```

**cssClass Property:**
- **Type:** `string`
- **Purpose:** Apply custom CSS classes to the item container
- **Use Cases:** Custom styling, theme overrides, visual emphasis, conditional styling

## Item Tooltips

Add detailed tooltips to ribbon items using `ribbonTooltipSettings`:

```tsx
import { RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";
import { RibbonTooltipModel } from '@syncfusion/ej2-react-ribbon';

// Basic tooltip
<RibbonItemDirective 
  type="Button" 
  ribbonTooltipSettings={{ 
    title: 'Cut', 
    content: 'Remove selected content and place it on the clipboard' 
  }}
  buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
</RibbonItemDirective>

// Tooltip with keyboard shortcut
<RibbonItemDirective 
  type="Button" 
  ribbonTooltipSettings={{ 
    title: 'Copy', 
    content: 'Copy selected content to clipboard (Ctrl+C)',
    cssClass: 'custom-tooltip'
  }}
  buttonSettings={{ iconCss: "e-icons e-copy", content: "Copy" }}>
</RibbonItemDirective>

// Detailed tooltip
<RibbonItemDirective 
  type="SplitButton" 
  ribbonTooltipSettings={{ 
    title: 'Paste Options', 
    content: 'Insert content from clipboard. Click the arrow for paste options.'
  }}
  splitButtonSettings={{ 
    iconCss: "e-icons e-paste", 
    content: "Paste",
    items: [
      { text: "Keep Source Formatting" },
      { text: "Merge Formatting" },
      { text: "Keep Text Only" }
    ]
  }}>
</RibbonItemDirective>
```

**RibbonTooltipModel Properties:**
- **title:** Tooltip header text (string)
- **content:** Tooltip body/description (string)
- **cssClass:** Custom CSS class for styling (string)

**Advanced Tooltip Example:**

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective, RibbonItemSize } from "@syncfusion/ej2-react-ribbon";
import { RibbonTooltipModel } from '@syncfusion/ej2-react-ribbon';

function App() {
  const cutTooltip: RibbonTooltipModel = {
    title: 'Cut',
    content: 'Remove the selection and put it on the Clipboard so you can paste it somewhere else.',
    cssClass: 'ribbon-tooltip'
  };

  const copyTooltip: RibbonTooltipModel = {
    title: 'Copy',
    content: 'Put a copy of the selection on the Clipboard so you can paste it somewhere else.',
    cssClass: 'ribbon-tooltip'
  };

  const pasteTooltip: RibbonTooltipModel = {
    title: 'Paste',
    content: 'Insert the content from the Clipboard at the current location.',
    cssClass: 'ribbon-tooltip'
  };

  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Clipboard">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="SplitButton" 
                      allowedSizes={RibbonItemSize.Large}
                      ribbonTooltipSettings={pasteTooltip}
                      splitButtonSettings={{ 
                        iconCss: "e-icons e-paste", 
                        content: "Paste",
                        items: [
                          { text: "Keep Source Formatting" },
                          { text: "Merge Formatting" }
                        ]
                      }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="Button" 
                      ribbonTooltipSettings={cutTooltip}
                      buttonSettings={{ 
                        iconCss: "e-icons e-cut", 
                        content: "Cut" 
                      }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective 
                      type="Button" 
                      ribbonTooltipSettings={copyTooltip}
                      buttonSettings={{ 
                        iconCss: "e-icons e-copy", 
                        content: "Copy" 
                      }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}

export default App;
```

**Custom Tooltip Styling:**

```css
/* Custom tooltip styles */
.ribbon-tooltip.e-tooltip-wrap {
  background-color: #2d3748;
  color: #ffffff;
  border-radius: 6px;
  padding: 12px;
  max-width: 300px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.ribbon-tooltip .e-tip-content {
  font-size: 13px;
  line-height: 1.5;
}

.ribbon-tooltip .e-arrow-tip-outer {
  border-top-color: #2d3748;
}
```

**Tooltip with HTML Content:**

```tsx
const advancedTooltip: RibbonTooltipModel = {
  title: 'Format Painter',
  content: `
    <div style="padding: 5px;">
      <p><strong>Copy formatting from one place to another</strong></p>
      <ul style="margin: 5px 0; padding-left: 20px;">
        <li>Single-click: Apply once</li>
        <li>Double-click: Apply multiple times</li>
        <li>Press ESC to cancel</li>
      </ul>
      <p style="margin-top: 5px;"><em>Keyboard: Ctrl+Shift+C, then Ctrl+Shift+V</em></p>
    </div>
  `,
  cssClass: 'advanced-tooltip'
};

<RibbonItemDirective 
  type="Button" 
  ribbonTooltipSettings={advancedTooltip}
  buttonSettings={{ 
    iconCss: "e-icons e-format-painter", 
    content: "Format Painter" 
  }}>
</RibbonItemDirective>
```

## Item Template for Custom Items

Define custom templates for ribbon items beyond the built-in Template type:

```tsx
import { RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";

// Custom item template that receives activeSize as context
<RibbonItemDirective 
  type="Button" 
  itemTemplate={(props: any) => {
    const size = props.activeSize || 'Medium';
    return (
      <div className={`custom-item size-${size.toLowerCase()}`}>
        <span className="e-icons e-custom-icon"></span>
        {size !== 'Small' && <span className="item-text">Custom Action</span>}
      </div>
    );
  }}
  buttonSettings={{ content: "Custom" }}>
</RibbonItemDirective>
```

**itemTemplate Property:**
- **Type:** `string | function | JSX.Element | HTMLElement`
- **Context:** Receives `activeSize` property as string in template context
- **Purpose:** Complete control over item rendering

**Responsive Template Example:**

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";

function App() {
  const customItemTemplate = (props: any) => {
    const activeSize = props.activeSize || 'Medium';
    
    // Different rendering based on size
    if (activeSize === 'Large') {
      return (
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center', 
          padding: '8px',
          cursor: 'pointer'
        }}>
          <span className="e-icons e-star" style={{ fontSize: '24px', color: '#ffc107' }}></span>
          <span style={{ marginTop: '4px', fontSize: '12px' }}>Favorite</span>
        </div>
      );
    } else if (activeSize === 'Medium') {
      return (
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          padding: '6px',
          cursor: 'pointer'
        }}>
          <span className="e-icons e-star" style={{ fontSize: '16px', color: '#ffc107', marginRight: '6px' }}></span>
          <span style={{ fontSize: '12px' }}>Favorite</span>
        </div>
      );
    } else {
      return (
        <div style={{ padding: '6px', cursor: 'pointer' }}>
          <span className="e-icons e-star" style={{ fontSize: '16px', color: '#ffc107' }}></span>
        </div>
      );
    }
  };

  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Actions">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="Template" 
                      itemTemplate={customItemTemplate}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}

export default App;
```

**Template with State Management:**

```tsx
import { useState } from 'react';

function App() {
  const [isFavorite, setIsFavorite] = useState(false);

  const favoriteTemplate = (props: any) => {
    const handleClick = () => {
      setIsFavorite(!isFavorite);
    };

    return (
      <button 
        onClick={handleClick}
        style={{
          background: 'transparent',
          border: 'none',
          cursor: 'pointer',
          padding: '8px'
        }}>
        <span 
          className="e-icons e-star" 
          style={{ 
            fontSize: '20px', 
            color: isFavorite ? '#ffc107' : '#ccc' 
          }}>
        </span>
      </button>
    );
  };

  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Quick Actions">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="Template" 
                      itemTemplate={favoriteTemplate}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}
```

**Use Cases:**
- Custom controls not provided by built-in types
- Dynamic content based on application state
- Size-aware rendering
- Interactive components with complex logic

## Enable or Disable Items

```tsx
// Disable specific item
<RibbonItemDirective type="Button" 
  disabled={true}
  buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
</RibbonItemDirective>

// Disable CheckBox
<RibbonItemDirective type="CheckBox" 
  disabled={true}
  checkBoxSettings={{ label: "Ruler", checked: true }}>
</RibbonItemDirective>

// Disable DropDown
<RibbonItemDirective type="DropDown" 
  disabled={true}
  dropDownSettings={{ content: "Table", iconCss: "e-icons e-table" }}>
</RibbonItemDirective>
```

## Group Configuration

Group-level properties:

```tsx
<RibbonGroupDirective 
  header="Clipboard" 
  id="clipboardGroup"
  groupIconCss="e-icons e-paste"
  showLauncherIcon={true}
  isCollapsible={true}
  priority={2}
  enableGroupOverflow={false}>
  {/* Collections and items */}
</RibbonGroupDirective>
```

**Group Properties:**
- `header` - Group title text
- `id` - Unique identifier
- `groupIconCss` - Icon for overflow button
- `showLauncherIcon` - Show launcher icon (boolean)
- `isCollapsible` - Allow group to collapse (default: true)
- `priority` - Collapse order (higher = collapse first)
- `enableGroupOverflow` - Dedicated overflow for group (boolean)

## Group Orientation

Arrange items vertically or horizontally:

```tsx
// Column orientation (default)
<RibbonGroupDirective header="Clipboard" orientation="Column">
  {/* Items stack vertically */}
</RibbonGroupDirective>

// Row orientation
<RibbonGroupDirective header="Font" orientation="Row">
  {/* Items arrange horizontally */}
</RibbonGroupDirective>
```

**Constraints:**
- **Column:** Multiple items per collection, up to 3 small/medium-sized items
- **Row:** Maximum 3 collections per group, each with any number of items

## Common Patterns

**Pattern 1: Large Primary + Small Secondary**
Large paste button with small cut/copy buttons

**Pattern 2: ComboBox + Action Buttons**
Font selector with formatting buttons

**Pattern 3: Grouped Format Buttons**
GroupButton for alignment (Left, Center, Right, Justify)
