# Popup Resizing

Enable users to dynamically adjust the ComboBox dropdown size using the `allowResize` property. Resized dimensions persist across sessions, providing a consistent user experience.

---

## Enable Popup Resizing

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const statusList = [
    'Open',
    'In Progress',
    'Closed',
    'On Hold',
    'Resolved',
    'Pending'
  ];

  return (
    <ComboBoxComponent 
      id="status-combo"
      dataSource={statusList}
      allowResize={true}        // ← Enable popup resizing
      placeholder="Select a status"
    />
  );
}
```

**User Experience:**
- Hover over popup edges to see resize handles
- Drag edges/corners to resize dropdown
- New size automatically remembered
- Applied to all future popups

---

## Resizing with Data Objects

```tsx
export default class App extends React.Component<{}, {}> {
  private statusData = [
    { Status: 'Open', State: false },
    { Status: 'Waiting for Customer', State: false },
    { Status: 'On Hold', State: true },
    { Status: 'Follow-up', State: false },
    { Status: 'Closed', State: true },
    { Status: 'Pending', State: true }
  ];

  private fields = { value: 'Status' };
  private allowResize = true;

  public render() {
    return (
      <ComboBoxComponent 
        id="status-combo"
        allowResize={this.allowResize}
        fields={this.fields}
        dataSource={this.statusData}
        placeholder="Select Status"
      />
    );
  }
}
```

---

## Use Cases

### Use Case 1: Long Content Display

When items have long text, allow resizing for better readability:

```tsx
const longItems = [
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
  'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
  'Ut enim ad minim veniam, quis nostrud exercitation'
];

<ComboBoxComponent 
  dataSource={longItems}
  allowResize={true}
  popupHeight="250px"
  popupWidth="300px"          // User can resize
/>
```

### Use Case 2: Custom Templates with Rich Content

Resizing helpful when using complex templates:

```tsx
const templateData = [
  { name: 'Product A', desc: 'High-performance component', price: '$299' },
  { name: 'Product B', desc: 'Budget-friendly option', price: '$99' }
];

const itemTemplate = (props) => {
  return (
    <div className="product-item">
      <strong>{props.name}</strong>
      <p>{props.desc}</p>
      <span className="price">{props.price}</span>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={templateData}
  itemTemplate={itemTemplate}
  allowResize={true}        // User can adjust size
  popupHeight="300px"
/>
```

---

## CSS Customization for Resizable Popup

Style the resize handles:

```css
/* Resize handle styling */
.e-combobox .e-resize-handle {
  background-color: #e0e0e0;
  cursor: se-resize;
}

.e-combobox .e-resize-handle:hover {
  background-color: #0066cc;
}

/* Popup while resizing */
.e-combobox .e-popup.e-resizing {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}
```

---

## Behavior Notes

- **Resize handles appear** on popup corners and edges when `allowResize={true}`
- **Minimum size:** 200px width × 100px height (enforced automatically)
- **Storage:** Size preferences saved in browser localStorage
- **Scope:** Each ComboBox instance remembers its own size independently
- **Responsive:** Resized size maintained across responsive breakpoints

---

## Common Patterns

### Pattern 1: Resizable with Filtering

```tsx
<ComboBoxComponent 
  dataSource={largeDataset}
  allowResize={true}
  allowFiltering={true}      // Combined features
  popupHeight="300px"
/>
```

### Pattern 2: Resizable with Virtual Scrolling

```tsx
<ComboBoxComponent 
  dataSource={50000items}
  allowResize={true}
  enableVirtualization={true}
  popupHeight="300px"
/>
```

### Pattern 3: Resizable with Grouping

```tsx
<ComboBoxComponent 
  dataSource={groupedData}
  fields={{ 
    text: 'name', 
    value: 'id', 
    groupBy: 'category' 
  }}
  allowResize={true}        // User adjusts to see full groups
  popupHeight="350px"
/>
```

---

## Next Steps

- **Custom item display?** → See [templates-and-customization.md](templates-and-customization.md)
- **Performance tuning?** → Check [advanced-features.md](advanced-features.md)
- **Styling the popup?** → Read [styling-and-theming.md](styling-and-theming.md)
