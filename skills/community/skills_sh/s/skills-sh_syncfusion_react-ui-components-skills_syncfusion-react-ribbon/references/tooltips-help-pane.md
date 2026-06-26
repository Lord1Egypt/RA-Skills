# Tooltips and Help Pane

## Table of Contents
- [Item Tooltips](#item-tooltips)
- [Custom Tooltips](#custom-tooltips)
- [Help Pane](#help-pane)
- [Help Pane Templates](#help-pane-templates)
- [Contextual Help](#contextual-help)

## Item Tooltips

Add tooltips to ribbon items for contextual help:

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
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="Button"
                      title="Cut (Ctrl+X)"
                      buttonSettings={{ 
                        iconCss: "e-icons e-cut", 
                        content: "Cut" 
                      }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective 
                      type="Button"
                      title="Copy selected text (Ctrl+C)"
                      buttonSettings={{ 
                        iconCss: "e-icons e-copy", 
                        content: "Copy" 
                      }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective 
                      type="Button"
                      title="Paste from clipboard (Ctrl+V)"
                      buttonSettings={{ 
                        iconCss: "e-icons e-paste", 
                        content: "Paste" 
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

**Tooltip Properties:**
- `title` - Tooltip text displayed on hover

## Custom Tooltips

Create rich tooltips with HTML content:

```tsx
<RibbonItemDirective 
  type="Button"
  tooltipText="<div><strong>Copy</strong><br/><small>Ctrl+C</small></div>"
  buttonSettings={{ 
    iconCss: "e-icons e-copy", 
    content: "Copy" 
  }}>
</RibbonItemDirective>
```

**Custom Tooltip Styling:**

```css
/* Tooltip Styles */
.e-tooltip {
  background-color: #333333;
  color: #ffffff;
  border-radius: 4px;
  padding: 8px 12px;
  max-width: 250px;
}

.e-tooltip strong {
  display: block;
  margin-bottom: 4px;
  font-weight: bold;
}

.e-tooltip small {
  color: #cccccc;
  font-size: 12px;
}
```

## Help Pane

Display contextual help in a dedicated pane:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";

function App() {
  const helpPaneTemplate = () => {
    return (
      <div id='helpPane' style={{ padding: '15px' }}>
        <h3>Ribbon Help</h3>
        <div className='help-section'>
          <h4>Getting Started</h4>
          <p>The ribbon toolbar organizes commands into tabs and groups for easy access.</p>
        </div>
        <div className='help-section'>
          <h4>Common Tasks</h4>
          <ul>
            <li><strong>Cut:</strong> Remove selected content (Ctrl+X)</li>
            <li><strong>Copy:</strong> Duplicate selected content (Ctrl+C)</li>
            <li><strong>Paste:</strong> Insert clipboard content (Ctrl+V)</li>
          </ul>
        </div>
      </div>
    );
  };

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div style={{ flex: 1 }}>
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
                          title="Cut"
                          buttonSettings={{ 
                            iconCss: "e-icons e-cut", 
                            content: "Cut" 
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
      </div>
      
      <div style={{ width: '300px', borderLeft: '1px solid #ddd' }}>
        {helpPaneTemplate()}
      </div>
    </div>
  );
}

export default App;
```

## Help Pane Templates

Create reusable help content templates:

```tsx
// Help content component
function HelpPane({ selectedTab }) {
  const renderHelp = () => {
    switch(selectedTab) {
      case 'home':
        return (
          <div>
            <h3>Home Tab</h3>
            <p>Contains basic editing and formatting commands.</p>
            <h4>Groups:</h4>
            <ul>
              <li><strong>Clipboard:</strong> Cut, Copy, Paste</li>
              <li><strong>Font:</strong> Font selection, size, formatting</li>
              <li><strong>Styles:</strong> Text and paragraph styles</li>
            </ul>
          </div>
        );
      case 'insert':
        return (
          <div>
            <h3>Insert Tab</h3>
            <p>Insert tables, images, shapes, and other content.</p>
          </div>
        );
      default:
        return <div><h3>Help</h3><p>Select a ribbon tab to see help</p></div>;
    }
  };

  return (
    <div id='helpPane' style={{ padding: '15px', overflowY: 'auto', height: '100%' }}>
      {renderHelp()}
    </div>
  );
}

// Usage in App
function App() {
  const [selectedTab, setSelectedTab] = useState('home');

  return (
    <div style={{ display: 'flex', gap: '20px', height: '100vh' }}>
      <div style={{ flex: 1 }}>
        <RibbonComponent 
          id="ribbon"
          tabSelected={(args) => setSelectedTab(args.tabIndex === 0 ? 'home' : 'insert')}>
          {/* Ribbon tabs */}
        </RibbonComponent>
      </div>
      
      <div style={{ width: '300px', borderLeft: '1px solid #ddd', backgroundColor: '#f9f9f9' }}>
        <HelpPane selectedTab={selectedTab} />
      </div>
    </div>
  );
}
```

## Contextual Help

Show help specific to user actions:

```tsx
import { useRef, useState } from 'react';

function App() {
  const [helpContent, setHelpContent] = useState('');
  const ribbonRef = useRef<RibbonComponent>(null);

  const handleItemHover = (itemName: string) => {
    const helpTexts = {
      'cut': 'Cut removes the selected content and places it on the clipboard. Use Ctrl+X to cut.',
      'copy': 'Copy duplicates selected content to the clipboard. Use Ctrl+C to copy.',
      'paste': 'Paste inserts clipboard content. Use Ctrl+V to paste.',
      'bold': 'Make selected text bold. Use Ctrl+B as a shortcut.',
      'italic': 'Make selected text italic. Use Ctrl+I as a shortcut.',
      'underline': 'Underline selected text. Use Ctrl+U as a shortcut.'
    };
    setHelpContent(helpTexts[itemName] || 'No help available');
  };

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div style={{ flex: 1 }}>
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
                          title="Cut"
                          buttonSettings={{ 
                            iconCss: "e-icons e-cut", 
                            content: "Cut" 
                          }}
                          onMouseEnter={() => handleItemHover('cut')}>
                        </RibbonItemDirective>
                        <RibbonItemDirective 
                          type="Button"
                          title="Copy"
                          buttonSettings={{ 
                            iconCss: "e-icons e-copy", 
                            content: "Copy" 
                          }}
                          onMouseEnter={() => handleItemHover('copy')}>
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
      
      <div style={{ 
        width: '250px', 
        padding: '15px',
        backgroundColor: '#f0f8ff',
        borderLeft: '1px solid #ddd',
        borderRadius: '4px'
      }}>
        <h4>Help</h4>
        <p>{helpContent}</p>
      </div>
    </div>
  );
}

export default App;
```

## Tooltip CSS

Customize tooltip appearance:

```css
/* Default Tooltip */
.e-tooltip {
  background-color: #2d3748;
  color: #ffffff;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 12px;
  max-width: 200px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

/* Tooltip Arrow */
.e-tooltip::before {
  content: '';
  position: absolute;
  top: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid #2d3748;
}

/* Tooltip Position */
.e-tooltip.top {
  top: -10px;
}

.e-tooltip.bottom {
  top: auto;
  bottom: -10px;
}

.e-tooltip.left {
  left: -10px;
}

.e-tooltip.right {
  left: auto;
  right: -10px;
}
```

## Best Practices

1. **Clarity:** Keep tooltips concise and helpful
2. **Shortcuts:** Include keyboard shortcuts in tooltips
3. **Help Pane:** Use for comprehensive help content
4. **Context:** Show contextual help when relevant
5. **Accessibility:** Ensure tooltips are accessible to screen readers
6. **Positioning:** Position tooltips to avoid covering important content
7. **Timing:** Show tooltips after brief hover delay

