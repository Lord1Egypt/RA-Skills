# Contextual Tabs and Gallery Items

## Table of Contents
- [Contextual Tabs Overview](#contextual-tabs-overview)
- [Adding Contextual Tabs](#adding-contextual-tabs)
- [Visibility Control](#visibility-control)
- [Multiple Contextual Tabs](#multiple-contextual-tabs)
- [Gallery Items](#gallery-items)
- [Gallery Configuration](#gallery-configuration)
- [Gallery Groups](#gallery-groups)

## Contextual Tabs Overview

Contextual tabs appear conditionally when users select specific objects (table, image, shape). They provide context-specific commands.

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective, RibbonItemSize, RibbonContextualTab, RibbonContextualTabsDirective, RibbonContextualTabDirective, Inject } from "@syncfusion/ej2-react-ribbon";

function App() {
  return (
    <RibbonComponent id='ribbon'>
      <RibbonTabsDirective>
        <RibbonTabDirective header='Home'>
          {/* Home tab content */}
        </RibbonTabDirective>
      </RibbonTabsDirective>
      <RibbonContextualTabsDirective>
        <RibbonContextualTabDirective visible={true}>
          <RibbonTabsDirective>
            <RibbonTabDirective header='Shape Format' id="ShapeFormat">
              <RibbonGroupsDirective>
                <RibbonGroupDirective header="Text decoration">
                  <RibbonCollectionsDirective>
                    <RibbonCollectionDirective>
                      <RibbonItemsDirective>
                        <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-text-header", content: "Text Header" }}>
                        </RibbonItemDirective>
                      </RibbonItemsDirective>
                    </RibbonCollectionDirective>
                  </RibbonCollectionsDirective>
                </RibbonGroupDirective>
              </RibbonGroupsDirective>
            </RibbonTabDirective>
          </RibbonTabsDirective>
        </RibbonContextualTabDirective>
      </RibbonContextualTabsDirective>
      <Inject services={[RibbonContextualTab]} />
    </RibbonComponent>
  );
}

export default App;
```

## Adding Contextual Tabs

Use `RibbonContextualTabsDirective` to define contextual tab groups:

```tsx
<RibbonContextualTabsDirective>
  <RibbonContextualTabDirective visible={true}>
    <RibbonTabsDirective>
      <RibbonTabDirective header='Shape Format' id="ShapeFormat">
        <RibbonGroupsDirective>
          <RibbonGroupDirective header="Shape Styles">
            <RibbonCollectionsDirective>
              <RibbonCollectionDirective>
                <RibbonItemsDirective>
                  <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-format-painter", content: "Format Painter" }}>
                  </RibbonItemDirective>
                </RibbonItemsDirective>
              </RibbonCollectionDirective>
            </RibbonCollectionsDirective>
          </RibbonGroupDirective>
        </RibbonGroupsDirective>
      </RibbonTabDirective>
    </RibbonTabsDirective>
  </RibbonContextualTabDirective>
</RibbonContextualTabsDirective>
```

## Visibility Control

Control when contextual tabs appear:

```tsx
// Always visible
<RibbonContextualTabDirective visible={true}>
  {/* Tabs */}
</RibbonContextualTabDirective>

// Initially hidden
<RibbonContextualTabDirective visible={false}>
  {/* Tabs */}
</RibbonContextualTabDirective>

// Select tab by default
<RibbonContextualTabDirective visible={true} isSelected={true}>
  {/* Tabs */}
</RibbonContextualTabDirective>
```

**Properties:**
- `visible` - Show/hide contextual tabs (boolean)
- `isSelected` - Make tab active on initialization (boolean)

## Multiple Contextual Tabs

Create multiple contextual tab groups for different object types:

```tsx
<RibbonContextualTabsDirective>
  {/* Shape contextual tabs */}
  <RibbonContextualTabDirective visible={false} id="shapeContextual">
    <RibbonTabsDirective>
      <RibbonTabDirective header='Shape Format'>
        <RibbonGroupsDirective>
          <RibbonGroupDirective header="Shape Styles">
            {/* Shape-related items */}
          </RibbonGroupDirective>
        </RibbonGroupsDirective>
      </RibbonTabDirective>
    </RibbonTabsDirective>
  </RibbonContextualTabDirective>

  {/* Table contextual tabs */}
  <RibbonContextualTabDirective visible={false} id="tableContextual">
    <RibbonTabsDirective>
      <RibbonTabDirective header='Table Design'>
        <RibbonGroupsDirective>
          <RibbonGroupDirective header="Table Styles">
            {/* Table-related items */}
          </RibbonGroupDirective>
        </RibbonGroupsDirective>
      </RibbonTabDirective>
    </RibbonTabsDirective>
  </RibbonContextualTabDirective>

  {/* Image contextual tabs */}
  <RibbonContextualTabDirective visible={false} id="imageContextual">
    <RibbonTabsDirective>
      <RibbonTabDirective header='Picture Format'>
        <RibbonGroupsDirective>
          <RibbonGroupDirective header="Adjust">
            {/* Image-related items */}
          </RibbonGroupDirective>
        </RibbonGroupsDirective>
      </RibbonTabDirective>
    </RibbonTabsDirective>
  </RibbonContextualTabDirective>
</RibbonContextualTabsDirective>
```

## Gallery Items

Gallery displays visual collections of options (styles, templates, effects).

```tsx
import { Inject, RibbonGallery, RibbonGallerySettingsModel } from '@syncfusion/ej2-react-ribbon';

const gallerySettings: RibbonGallerySettingsModel = {
  groups: [{
    header: 'Styles',
    items: [
      { content: 'Normal' },
      { content: 'No Spacing' },
      { content: 'Heading 1' },
      { content: 'Heading 2' }
    ]
  }]
};

<RibbonItemDirective type="Gallery" gallerySettings={gallerySettings}>
</RibbonItemDirective>
```

## Gallery Configuration

Configure gallery appearance and behavior:

```tsx
const gallerySettings: RibbonGallerySettingsModel = {
  groups: [{
    header: 'Styles',
    items: [
      { content: 'Normal' },
      { content: 'No Spacing' },
      { content: 'Heading 1' },
      { content: 'Heading 2' },
      { content: 'Heading 3' }
    ]
  }],
  itemCount: 4,           // Items per row
  popupWidth: '400px',    // Popup width
  popupHeight: '300px'    // Popup height
};

<RibbonItemDirective type="Gallery" gallerySettings={gallerySettings}>
</RibbonItemDirective>
```

**Gallery Settings Properties:**
- `groups` - Array of gallery groups
- `itemCount` - Items per row in popup (default: 4)
- `popupWidth` - Width of gallery popup
- `popupHeight` - Height of gallery popup

## Gallery Groups

Organize gallery items into logical groups:

```tsx
const gallerySettings: RibbonGallerySettingsModel = {
  groups: [
    {
      header: 'Built-in Styles',
      items: [
        { content: 'Normal', iconCss: 'e-icons e-style' },
        { content: 'Heading 1', iconCss: 'e-icons e-header' },
        { content: 'Heading 2', iconCss: 'e-icons e-header' }
      ]
    },
    {
      header: 'Custom Styles',
      items: [
        { content: 'My Style 1' },
        { content: 'My Style 2' },
        { content: 'My Style 3' }
      ]
    }
  ]
};

<RibbonItemDirective type="Gallery" gallerySettings={gallerySettings}>
</RibbonItemDirective>
```

**Gallery Item Properties:**
- `content` - Display text
- `iconCss` - Icon class (optional)
- `disabled` - Disable item (boolean)

## Complete Contextual Example

```tsx
import { useRef } from 'react';

function App() {
  let ribbonObj = useRef<RibbonComponent>(null);

  const onImageSelect = () => {
    if (ribbonObj.current) {
      // Show image contextual tabs
      const imageTab = ribbonObj.current.element?.querySelector('[id="imageContextual"]');
      if (imageTab) {
        imageTab.parentElement?.classList.add('show');
      }
    }
  };

  const gallerySettings: RibbonGallerySettingsModel = {
    groups: [{
      header: 'Table Styles',
      items: [
        { content: 'Grid Table 1' },
        { content: 'Grid Table 2' },
        { content: 'Grid Table 3' },
        { content: 'Grid Table 4' }
      ]
    }]
  };

  return (
    <RibbonComponent id='ribbon' ref={ribbonObj}>
      <RibbonTabsDirective>
        <RibbonTabDirective header='Home'>
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Insert">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-image", content: "Image" }} onClick={onImageSelect}>
                    </RibbonItemDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-table", content: "Table" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>

      <RibbonContextualTabsDirective>
        <RibbonContextualTabDirective visible={false} id="imageContextual">
          <RibbonTabsDirective>
            <RibbonTabDirective header='Picture Format'>
              <RibbonGroupsDirective>
                <RibbonGroupDirective header="Adjust">
                  <RibbonCollectionsDirective>
                    <RibbonCollectionDirective>
                      <RibbonItemsDirective>
                        <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-brightness", content: "Brightness" }}>
                        </RibbonItemDirective>
                      </RibbonItemsDirective>
                    </RibbonCollectionDirective>
                  </RibbonCollectionsDirective>
                </RibbonGroupDirective>
              </RibbonGroupsDirective>
            </RibbonTabDirective>
          </RibbonTabsDirective>
        </RibbonContextualTabDirective>

        <RibbonContextualTabDirective visible={false} id="tableContextual">
          <RibbonTabsDirective>
            <RibbonTabDirective header='Table Design'>
              <RibbonGroupsDirective>
                <RibbonGroupDirective header="Table Styles">
                  <RibbonCollectionsDirective>
                    <RibbonCollectionDirective>
                      <RibbonItemsDirective>
                        <RibbonItemDirective type="Gallery" gallerySettings={gallerySettings}>
                        </RibbonItemDirective>
                      </RibbonItemsDirective>
                    </RibbonCollectionDirective>
                  </RibbonCollectionsDirective>
                </RibbonGroupDirective>
              </RibbonGroupsDirective>
            </RibbonTabDirective>
          </RibbonTabsDirective>
        </RibbonContextualTabDirective>
      </RibbonContextualTabsDirective>

      <Inject services={[RibbonContextualTab, RibbonGallery]} />
    </RibbonComponent>
  );
}

export default App;
```

## Best Practices

1. **Logical Grouping:** Use for object-specific commands
2. **Clear Labels:** Gallery headers should be descriptive
3. **Item Organization:** Group gallery items by similarity
4. **Performance:** Lazy-load contextual tabs if complex
5. **Visibility:** Control visibility with application state
