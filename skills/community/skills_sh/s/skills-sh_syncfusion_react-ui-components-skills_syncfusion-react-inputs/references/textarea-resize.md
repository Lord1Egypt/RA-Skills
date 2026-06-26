# Resize Behavior in React TextArea Component

Configure how users can resize the TextArea to accommodate varying content and interface preferences. The `resizeMode` property offers flexible control over resizing behavior.

## Resize Modes

The `resizeMode` property accepts four values:

| Mode | Description | Default? |
|------|-------------|----------|
| **Both** | Users can resize both height and width | ✓ Yes |
| **Vertical** | Only vertical (height) resizing allowed | |
| **Horizontal** | Only horizontal (width) resizing allowed | |
| **None** | Resizing disabled | |

## Both Mode (Default)

Users can resize the TextArea both vertically (height) and horizontally (width).

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='default'
      placeholder='Drag the corner to resize'
      resizeMode='Both'
      rows={5}
      cols={40}
    />
  );
}

export default App;
```

**User Experience:**
- Resize handle appears in the bottom-right corner
- Dragging adjusts both dimensions
- Default browser textarea behavior

**Note:** Width adjustment works when CSS allows it. By default, the width won't auto-adjust without explicit CSS configuration.

## Vertical Mode

Allow only vertical (height) resizing. Users can increase or decrease the number of visible lines.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='vertical-only'
      placeholder='Resize vertically only'
      resizeMode='Vertical'
      rows={4}
      cols={50}
    />
  );
}

export default App;
```

**Best for:**
- Form fields where width should remain consistent
- Responsive layouts with fixed container widths
- Better control of layout integrity

**User Experience:**
- Resize handle only on vertical axis
- Height can be increased/decreased
- Width remains fixed

## Horizontal Mode

Allow only horizontal (width) resizing. Users can adjust the visible width.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='horizontal-only'
      placeholder='Resize horizontally only'
      resizeMode='Horizontal'
      rows={5}
      cols={40}
    />
  );
}

export default App;
```

**Best for:**
- Scenarios requiring fixed height but variable width
- Code editors or specialized inputs
- Accommodating longer lines without vertical expansion

## None Mode

Disable resizing entirely. The TextArea maintains fixed dimensions.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='no-resize'
      placeholder='Cannot be resized'
      resizeMode='None'
      rows={5}
      cols={40}
    />
  );
}

export default App;
```

**Best for:**
- Consistent form layouts where user resizing would break design
- Fixed-size input fields in compact interfaces
- Design-critical layouts where dimension consistency is essential

**User Experience:**
- No resize handle visible
- TextArea maintains specified dimensions
- Content scrolls if it exceeds visible area

## Combining with Width Property

Control both dimensions with width and resizeMode:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='controlled'
      placeholder='Controlled dimensions'
      resizeMode='Vertical'
      width='100%'
      rows={5}
    />
  );
}

export default App;
```

This creates a full-width textarea that can only be resized vertically.

## Responsive Resize Control

Adjust resize behavior based on screen size:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState, useEffect } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [resizeMode, setResizeMode] = useState('Both');

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setResizeMode('Vertical'); // Mobile: vertical only
      } else {
        setResizeMode('Both'); // Desktop: both directions
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <TextAreaComponent 
      id='responsive-resize'
      placeholder='Responsive resize control'
      resizeMode={resizeMode}
      rows={5}
      cols={40}
    />
  );
}

export default App;
```

## Fixed Height with Scrollable Content

Use `None` mode for fixed dimensions with scroll for overflow:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='fixed-scroll'
      placeholder='Fixed size with scrollbars'
      resizeMode='None'
      rows={5}
      cols={40}
      width='400px'
    />
  );
}

export default App;
```

CSS for scrollable behavior:

```css
#fixed-scroll {
  overflow: auto;
}
```

## User-Controlled Sizing with Constraints

Allow resizing within limits:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='limited-resize'
      placeholder='Resizable with constraints'
      resizeMode='Vertical'
      rows={4}
      cols={50}
      width='500px'
    />
  );
}

export default App;
```

With CSS constraints:

```css
#limited-resize {
  min-height: 120px;      /* At least 4 rows */
  max-height: 400px;      /* Maximum 20+ rows */
  min-width: 300px;
  max-width: 800px;
}
```

## Combining with Other Features

### Resize with Max Length

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [charCount, setCharCount] = useState(0);

  return (
    <TextAreaComponent 
      id='limited-content'
      placeholder='Resizable with character limit'
      resizeMode='Vertical'
      maxLength={500}
      input={(args) => setCharCount((args.value || '').length)}
      rows={5}
      cols={40}
    />
  );
}

export default App;
```

### Resize with Floating Labels

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='float-resize'
      placeholder='Enter your message'
      floatLabelType='Auto'
      resizeMode='Vertical'
      rows={4}
      cols={45}
    />
  );
}

export default App;
```

### Resize with Adornments

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const appendContent = () => (
    <button className='send-btn'>Send</button>
  );

  return (
    <TextAreaComponent 
      id='adorned-resize'
      placeholder='Message with action'
      resizeMode='Vertical'
      appendTemplate={appendContent}
      rows={4}
      cols={40}
    />
  );
}

export default App;
```

## Layout Considerations

### Fixed Layout with No Resize

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <form className='form-layout'>
      <div className='form-row'>
        <label>Name</label>
        <input type='text' />
      </div>

      <div className='form-row'>
        <label>Email</label>
        <input type='email' />
      </div>

      <div className='form-row'>
        <label>Message</label>
        <TextAreaComponent 
          id='form-textarea'
          placeholder='Your message'
          resizeMode='None'
          rows={5}
          width='100%'
        />
      </div>

      <button type='submit'>Submit</button>
    </form>
  );
}

export default App;
```

### Flexible Vertical with Fixed Width

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='editor-pane'>
      <TextAreaComponent 
        id='editor'
        placeholder='Code editor'
        resizeMode='Vertical'
        rows={10}
        width='100%'
        cssClass='monospace'
      />
    </div>
  );
}

export default App;
```

## Browser Support

- **Both, Vertical, Horizontal**: Supported in all modern browsers
- **None**: Removes resize handle by applying CSS `resize: none`
- **Mobile**: Touch gestures for resizing may vary by browser

## Best Practices

- **Forms**: Use `Vertical` for consistent layout
- **Text Editors**: Use `Both` for flexibility
- **Compact UIs**: Use `None` to maintain design
- **Mobile**: Constrain `Vertical` on small screens
- **Accessibility**: Ensure resize handles are visible with sufficient contrast
- **Content**: Plan min/max heights to accommodate typical content
- **Responsive**: Adjust resize mode based on viewport size
- **Performance**: Complex layouts may benefit from `None` mode
