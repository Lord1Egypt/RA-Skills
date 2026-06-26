# Rows and Columns Sizing in React TextArea Component

Control the visible dimensions of your TextArea using the `rows` and `cols` properties. These attributes define the initial height (in lines) and width (in characters), allowing precise control over layout.

## Rows Property

The `rows` attribute sets the visible number of lines (vertical height) of the TextArea.

### Basic Row Configuration

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='textarea'
      placeholder='Enter comments'
      rows={5}
    />
  );
}

export default App;
```

This creates a TextArea that displays 5 lines without scrolling.

### Common Row Sizes

```typescript
// Compact (3 rows - good for single-line fallback)
<TextAreaComponent rows={3} />

// Standard (5 rows - good for typical comments)
<TextAreaComponent rows={5} />

// Medium (8 rows - good for detailed feedback)
<TextAreaComponent rows={8} />

// Large (10+ rows - for extended content)
<TextAreaComponent rows={12} />
```

## Cols Property

The `cols` attribute sets the visible width of the TextArea, measured in average character widths.

### Basic Column Configuration

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='textarea'
      placeholder='Enter comments'
      cols={50}
    />
  );
}

export default App;
```

This creates a TextArea with width equivalent to 50 characters.

### Common Column Widths

```typescript
// Narrow (30 cols - mobile friendly)
<TextAreaComponent cols={30} />

// Standard (40 cols - good balance)
<TextAreaComponent cols={40} />

// Wide (60 cols - full screen on desktop)
<TextAreaComponent cols={60} />

// Extra wide (80 cols - professional/code)
<TextAreaComponent cols={80} />
```

## Combined Rows and Columns

### Multiple TextArea Sizes

Create different sized textareas for various use cases:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='wrap'>
      <div className='textarea-group'>
        <h4>Small Comment Box</h4>
        <TextAreaComponent 
          id='small'
          placeholder='Quick comment'
          rows={3}
          cols={35}
        />
      </div>

      <div className='textarea-group'>
        <h4>Medium Feedback Form</h4>
        <TextAreaComponent 
          id='medium'
          placeholder='Your feedback'
          rows={5}
          cols={40}
        />
      </div>

      <div className='textarea-group'>
        <h4>Large Essay Area</h4>
        <TextAreaComponent 
          id='large'
          placeholder='Write your essay'
          rows={10}
          cols={60}
        />
      </div>
    </div>
  );
}

export default App;
```

## Responsive Sizing

### Mobile vs Desktop

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState, useEffect } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <TextAreaComponent 
      id='responsive'
      placeholder='Responsive textarea'
      rows={isMobile ? 4 : 8}
      cols={isMobile ? 25 : 50}
    />
  );
}

export default App;
```

## Dynamic Sizing

### Adjust Size Based on Content

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [rows, setRows] = useState(3);
  const [content, setContent] = useState('');

  const handleInput = (args) => {
    const value = args.value || '';
    setContent(value);
    
    // Increase rows as content grows
    const lineCount = (value.match(/\n/g) || []).length + 1;
    setRows(Math.max(3, lineCount + 1));
  };

  return (
    <TextAreaComponent 
      id='auto-expand'
      value={content}
      input={handleInput}
      placeholder='Type to expand'
      rows={rows}
      cols={40}
    />
  );
}

export default App;
```

### Fixed Size with Scrollbars

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='scrollable'
      placeholder='Fixed size with scrollbars'
      rows={5}
      cols={40}
      resizeMode='None'
    />
  );
}

export default App;
```

## Combining with Other Properties

### With Floating Label

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='textarea'
      placeholder='Enter your feedback'
      floatLabelType='Auto'
      rows={6}
      cols={45}
    />
  );
}

export default App;
```

### With Max Length

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='limited'
      placeholder='Enter comments (max 500 chars)'
      rows={5}
      cols={40}
      maxLength={500}
    />
  );
}

export default App;
```

### With Resize Control

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='resizable'
      placeholder='Resizable textarea'
      rows={4}
      cols={35}
      resizeMode='Both'
    />
  );
}

export default App;
```

## CSS-Based Width Override

While `cols` controls the default width, you can override it with CSS:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='custom-width'
      placeholder='Custom width via CSS'
      rows={5}
      cols={40}
      cssClass='full-width'
    />
  );
}

export default App;
```

With CSS:

```css
.full-width.e-field {
  width: 100%;
}
```

## Sizing Best Practices

### Form Field Layout

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <form className='feedback-form'>
      <div className='form-group'>
        <label>Name</label>
        <input type='text' />
      </div>

      <div className='form-group'>
        <label>Email</label>
        <input type='email' />
      </div>

      <div className='form-group'>
        <label>Feedback</label>
        <TextAreaComponent 
          id='feedback'
          placeholder='Your feedback'
          rows={6}
          cols={50}
          floatLabelType='Auto'
        />
      </div>

      <button type='submit'>Submit</button>
    </form>
  );
}

export default App;
```

### Different Purposes

```typescript
// Chat message input
<TextAreaComponent rows={3} cols={40} />

// Bug report form
<TextAreaComponent rows={8} cols={60} />

// Review submission
<TextAreaComponent rows={6} cols={50} />

// Code snippet area
<TextAreaComponent rows={10} cols={80} />

// Social media post
<TextAreaComponent rows={4} cols={45} />
```

## Width Property Alternative

For more precise width control, use the `width` property instead of `cols`:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='precise-width'
      placeholder='Width in pixels'
      rows={5}
      width='400px'
    />
  );
}

export default App;
```

Or percentage-based width:

```typescript
<TextAreaComponent 
  id='responsive-width'
  placeholder='Full container width'
  rows={5}
  width='100%'
/>
```

## Considerations

- **Browser Support**: `rows` and `cols` are standard HTML attributes, supported in all browsers
- **Character Width**: `cols` is based on monospace character width; actual visible width varies with fonts
- **Mobile**: Reduce `cols` for mobile devices (25-30) vs desktop (40-60)
- **Accessibility**: Provide appropriate sizing for keyboard users
- **Scrollbars**: Long content will scroll if it exceeds the visible area
- **Resizing**: Use `resizeMode` property to control user resizing capability
