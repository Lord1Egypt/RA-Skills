# Ribbon Structure: Tabs, Groups, Collections, and Items

## Table of Contents
- [Hierarchy Overview](#hierarchy-overview)
- [Adding Tabs](#adding-tabs)
- [Adding Groups](#adding-groups)
- [Adding Collections](#adding-collections)
- [Adding Items](#adding-items)
- [Organizing Multi-Level Structure](#organizing-multi-level-structure)

## Hierarchy Overview

The Ribbon follows a hierarchical structure:

```
RibbonComponent
├── RibbonTabsDirective
│   └── RibbonTabDirective (e.g., "Home" tab)
│       └── RibbonGroupsDirective
│           └── RibbonGroupDirective (e.g., "Clipboard" group)
│               └── RibbonCollectionsDirective
│                   └── RibbonCollectionDirective (item container)
│                       └── RibbonItemsDirective
│                           └── RibbonItemDirective (e.g., Button, DropDown)
```

Each level serves a specific purpose:
- **Tabs:** Organize commands into major categories
- **Groups:** Further subdivide tabs into related command groups
- **Collections:** Logically group items within a group
- **Items:** Individual controls (buttons, dropdowns, etc.)

## Adding Tabs

Use `RibbonTabsDirective` and `RibbonTabDirective` to define ribbon tabs:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective } from "@syncfusion/ej2-react-ribbon";

function App() {
  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home"></RibbonTabDirective>
        <RibbonTabDirective header="Insert"></RibbonTabDirective>
        <RibbonTabDirective header="View"></RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}

export default App;
```

**Key Properties:**
- `header` (string, required) - The tab title displayed to users
- `id` (string, optional) - Unique identifier for the tab

## Adding Groups

Add groups to organize items within tabs:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective } from "@syncfusion/ej2-react-ribbon";

function App() {
  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Clipboard"></RibbonGroupDirective>
            <RibbonGroupDirective header="Font"></RibbonGroupDirective>
            <RibbonGroupDirective header="Paragraph"></RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}

export default App;
```

**Key Properties:**
- `header` (string, required) - Group title
- `id` (string, optional) - Unique identifier
- Other properties documented in items-and-groups.md

## Adding Collections

Collections organize items within groups. Each collection is a container that can hold related items:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";

function App() {
  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Clipboard">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective id="paste-collection">
                  {/* Paste item goes here */}
                </RibbonCollectionDirective>
                <RibbonCollectionDirective id="cutcopy-collection">
                  {/* Cut and Copy items go here */}
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

**Key Properties:**
- `id` (string, optional) - Unique identifier

**Why Use Collections?**
- Better visual organization within groups
- Allows control over item layout and spacing
- Different groups can have different layout rules for collections

## Adding Items

Items are the actual controls (buttons, dropdowns, etc.) within collections:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";
import { ItemModel } from "@syncfusion/ej2-splitbuttons";

function App() {
  const pasteOptions: ItemModel[] = [
    { text: "Keep Source Format" },
    { text: "Merge format" },
    { text: "Keep text only" }
  ];

  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Clipboard">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="SplitButton" 
                      splitButtonSettings={{ 
                        iconCss: "e-icons e-paste", 
                        items: pasteOptions, 
                        content: "Paste" 
                      }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="Button" 
                      buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective type="Button" 
                      buttonSettings={{ iconCss: "e-icons e-copy", content: "Copy" }}>
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

**Key Properties:**
- `type` (string, required) - Item type: Button, CheckBox, DropDown, SplitButton, ComboBox, ColorPicker, GroupButton, Gallery, or Template
- `allowedSizes` - Item size constraints (see items-and-groups.md)
- Type-specific settings: `buttonSettings`, `dropDownSettings`, `splitButtonSettings`, etc.

## Organizing Multi-Level Structure

A complete multi-tab, multi-group example:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective, RibbonItemSize } from "@syncfusion/ej2-react-ribbon";
import { ItemModel } from "@syncfusion/ej2-splitbuttons";

function App() {
  const pasteOptions: ItemModel[] = [
    { text: "Keep Source Format" },
    { text: "Merge format" },
    { text: "Keep text only" }
  ];

  const fontSize: string[] = ["8", "9", "10", "11", "12", "14", "16", "18", "20"];
  const fontStyle: string[] = ["Arial", "Calibri", "Cambria", "Georgia", "Verdana"];

  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        {/* HOME TAB */}
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            {/* Clipboard Group */}
            <RibbonGroupDirective header="Clipboard" groupIconCss="e-icons e-paste">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="SplitButton" allowedSizes={RibbonItemSize.Large}
                      splitButtonSettings={{ iconCss: "e-icons e-paste", items: pasteOptions, content: "Paste" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-copy", content: "Copy" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>

            {/* Font Group */}
            <RibbonGroupDirective header="Font" groupIconCss="e-icons e-bold">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="ComboBox" comboBoxSettings={{ dataSource: fontStyle, index: 0, width: "150px", allowFiltering: true }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective type="ComboBox" comboBoxSettings={{ dataSource: fontSize, index: 4, width: "65px", allowFiltering: true }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="Button" allowedSizes={RibbonItemSize.Small} buttonSettings={{ iconCss: "e-icons e-bold", content: "Bold" }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective type="Button" allowedSizes={RibbonItemSize.Small} buttonSettings={{ iconCss: "e-icons e-italic", content: "Italic" }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective type="Button" allowedSizes={RibbonItemSize.Small} buttonSettings={{ iconCss: "e-icons e-underline", content: "Underline" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>

        {/* INSERT TAB */}
        <RibbonTabDirective header="Insert">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Tables">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="Button" allowedSizes={RibbonItemSize.Large} buttonSettings={{ iconCss: "e-icons e-table", content: "Table" }}>
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

## Best Practices

1. **Logical Organization:** Group related commands together (Clipboard, Font, Paragraph)
2. **Collection Usage:** Use multiple collections to visually separate related items
3. **Item Sizing:** Set `allowedSizes` consistently for better visual alignment
4. **Icon Consistency:** Use icons from the Syncfusion icon library (e-icons class)
5. **Naming:** Use unique, meaningful IDs for tabs and groups for programmatic access

## Common Patterns

**Pattern 1: Vertical Stacking (Column Orientation)**
Multiple small items stacked vertically within a collection

**Pattern 2: Horizontal Layout (Row Orientation)**
Multiple items in a single row, useful for formatting toolbars

**Pattern 3: Large + Small Items**
Large primary action (e.g., Paste) with smaller secondary actions (Cut, Copy)
