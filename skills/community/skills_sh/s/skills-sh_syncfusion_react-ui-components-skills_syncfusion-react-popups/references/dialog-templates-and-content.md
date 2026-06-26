# Templates and Content

## Table of Contents
- [Header Template](#header-template)
- [Content Management](#content-management)
- [Footer Templates](#footer-templates)
- [Custom HTML Content](#custom-html-content)
- [Dynamic Updates](#dynamic-updates)
- [Close Icon Customization](#close-icon-customization)
- [Edge Cases](#edge-cases)

## Header Template

The header is the top section of the dialog. It can be text or custom JSX.

### Simple Text Header

```jsx
<DialogComponent
  header="Dialog Title"
  showCloseIcon={true}
>
  Content
</DialogComponent>
```

### Custom Header JSX

```jsx
import React, { useRef } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import './App.css';

export default function App() {
  const dialogRef = useRef(null);

  // Custom header component
  const customHeader = (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span>📝 Edit Profile</span>
      <span style={{ fontSize: '12px', color: '#999' }}>Step 1 of 3</span>
    </div>
  );

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Edit</button>

      <DialogComponent
        ref={dialogRef}
        header={customHeader}
        showCloseIcon={true}
        target="#dialog-target"
      >
        Content
      </DialogComponent>
    </div>
  );
}
```

### Header with Icon

```jsx
const headerWithIcon = (
  <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
    <span>⚠️</span>
    <span>Warning Message</span>
  </div>
);

<DialogComponent header={headerWithIcon}>
  Important warning here
</DialogComponent>
```

### Styled Header

```jsx
const styledHeader = (
  <div style={{
    background: 'linear-gradient(to right, #667eea, #764ba2)',
    color: 'white',
    padding: '10px',
    borderRadius: '4px 4px 0 0'
  }}>
    Premium Dialog
  </div>
);

<DialogComponent header={styledHeader}>
  Content
</DialogComponent>
```

## Content Management

The `content` prop accepts text or JSX:

### Text Content

```jsx
<DialogComponent header="Simple">
  This is plain text content
</DialogComponent>
```

### HTML String Content

```jsx
<DialogComponent
  header="HTML Content"
  content="<h2>Hello</h2><p>This is HTML</p>"
>
</DialogComponent>
```

### JSX Content

```jsx
const dialogContent = (
  <div style={{ padding: '20px' }}>
    <h3>User Profile</h3>
    <p>Name: John Doe</p>
    <p>Email: john@example.com</p>
    <button className="e-btn">Edit</button>
  </div>
);

<DialogComponent header="Profile">
  {dialogContent}
</DialogComponent>
```

### Content as Children

```jsx
<DialogComponent header="Dialog">
  <h3>Title</h3>
  <p>Paragraph content</p>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
</DialogComponent>
```

## Footer Templates

Two options for footer: built-in buttons or custom footer template.

### Built-in Buttons (Recommended for Simple Cases)

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'OK',
      cssClass: 'e-flat',
      isPrimary: true,
    },
    click: () => console.log('OK clicked'),
  },
  {
    buttonModel: {
      content: 'Cancel',
      cssClass: 'e-flat',
    },
    click: () => dialogRef.current?.hide(),
  },
];

<DialogComponent buttons={buttons}>
  Content
</DialogComponent>
```

### Custom Footer Template

Use `footerTemplate` for complete control:

```jsx
const footerTemplate = () => {
    return (
      <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', padding: '15px' }}>
        <button className="e-control e-btn">Save</button>
        <button className="e-control e-btn">Reset</button>
        <button className="e-control e-btn">Cancel</button>
      </div>
    );
}

<DialogComponent
  header="Form"
  footerTemplate={footerTemplate}
>
  Form content
</DialogComponent>
```

### Custom Footer with Forms

```jsx
export function FormDialog() {
  const dialogRef = useRef(null);
  const [formData, setFormData] = React.useState({ name: '', email: '' });

  const handleSave = () => {
    console.log('Saving:', formData);
    dialogRef.current?.hide();
  };

  const footerTemplate = () => {
    return (
      <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', padding: '15px' }}>
        <button 
          className="e-control e-btn e-primary"
          onClick={handleSave}
        >
          Save
        </button>
        <button 
          className="e-control e-btn"
          onClick={() => dialogRef.current?.hide()}
        >
          Cancel
        </button>
      </div>
    );
  }

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Open</button>

      <DialogComponent
        ref={dialogRef}
        header="User Form"
        footerTemplate={footerTemplate}
        target="#dialog-target"
      >
        <div style={{ padding: '20px' }}>
          <div style={{ marginBottom: '15px' }}>
            <label>Name:</label>
            <input
              type="text"
              className="e-input"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>
          <div>
            <label>Email:</label>
            <input
              type="email"
              className="e-input"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            />
          </div>
        </div>
      </DialogComponent>
    </div>
  );
}
```

### Buttons vs Footer Template

| Aspect | Buttons | Footer Template |
|--------|---------|-----------------|
| **Simplicity** | Simple, one-line | Requires JSX |
| **Styling** | Limited | Full control |
| **Multiple Buttons** | Good | Better |
| **Custom Layout** | Limited | Excellent |
| **Use Case** | OK/Cancel dialogs | Complex footers |

**Important:** Cannot use both `buttons` and `footerTemplate` at the same time.

## Custom HTML Content

### Rendering Rich Content

```jsx
const richContent = (
  <div style={{ padding: '20px' }}>
    <h3>🎉 Congratulations!</h3>
    <p>You've completed the task.</p>
    <div style={{ 
      background: '#f0f9ff', 
      padding: '10px', 
      borderLeft: '4px solid #0ea5e9',
      marginTop: '10px'
    }}>
      <strong>Reward:</strong> +100 points
    </div>
  </div>
);

<DialogComponent header="Success" isModal={true}>
  {richContent}
</DialogComponent>
```

### Embedding Images

```jsx
const contentWithImage = (
  <div style={{ textAlign: 'center', padding: '20px' }}>
    <img 
      src="https://example.com/image.png" 
      alt="Illustration"
      style={{ maxWidth: '100%', height: 'auto', marginBottom: '15px' }}
    />
    <h3>Feature Highlight</h3>
    <p>Check out this new capability</p>
  </div>
);

<DialogComponent header="What's New">
  {contentWithImage}
</DialogComponent>
```

### Forms in Content

```jsx
const formContent = (
  <form style={{ padding: '20px' }}>
    <div style={{ marginBottom: '15px' }}>
      <label>Username</label>
      <input 
        type="text" 
        className="e-input" 
        placeholder="Enter username"
        style={{ width: '100%', marginTop: '5px' }}
      />
    </div>
    <div style={{ marginBottom: '15px' }}>
      <label>Password</label>
      <input 
        type="password" 
        className="e-input" 
        placeholder="Enter password"
        style={{ width: '100%', marginTop: '5px' }}
      />
    </div>
  </form>
);

<DialogComponent header="Login">
  {formContent}
</DialogComponent>
```

## Dynamic Updates

### Update Content on State Change

```jsx
export function DynamicDialog() {
  const dialogRef = useRef(null);
  const [message, setMessage] = React.useState('Loading...');
  const [status, setStatus] = React.useState('loading');

  React.useEffect(() => {
    const timer = setTimeout(() => {
      setMessage('✅ Operation completed successfully!');
      setStatus('success');
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const statusColor = status === 'success' ? '#10b981' : '#f59e0b';

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Start</button>

      <DialogComponent
        ref={dialogRef}
        header="Processing"
        isModal={true}
        target="#dialog-target"
      >
        <div style={{ padding: '20px', textAlign: 'center', color: statusColor }}>
          {message}
        </div>
      </DialogComponent>
    </div>
  );
}
```

### Update Header Dynamically

```jsx
export function DynamicHeader() {
  const dialogRef = useRef(null);
  const [step, setStep] = React.useState(1);

  const headerText = `Wizard - Step ${step} of 3`;

  const goNext = () => {
    if (step < 3) setStep(step + 1);
    else dialogRef.current?.hide();
  };

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Start Wizard</button>

      <DialogComponent
        ref={dialogRef}
        header={headerText}
        buttons={[
          {
            buttonModel: { content: 'Next', isPrimary: true, cssClass: 'e-flat' },
            click: goNext,
          },
          {
            buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
            click: () => dialogRef.current?.hide(),
          },
        ]}
        target="#dialog-target"
      >
        <div style={{ padding: '20px' }}>
          <h3>Step {step}</h3>
          {step === 1 && <p>Select your preferences</p>}
          {step === 2 && <p>Confirm your selection</p>}
          {step === 3 && <p>Almost done!</p>}
        </div>
      </DialogComponent>
    </div>
  );
}
```

## Close Icon Customization

### Show/Hide Close Icon

```jsx
// Show close icon
<DialogComponent showCloseIcon={true}>
  Click X to close
</DialogComponent>

// Hide close icon (default)
<DialogComponent showCloseIcon={false}>
  No close button available
</DialogComponent>
```

### Customize Close Icon Title

```jsx
<DialogComponent
  showCloseIcon={true}
  locale="en-US"  // Close icon title is auto-localized based on locale
>
  Content
</DialogComponent>
```

**Note:** The close icon title is automatically localized. For example, with `locale="de"` it displays "Schließen", with `locale="fr"` it displays "Fermer", etc. Set the locale property to control both content and UI text localization.

### Styled Close Icon

```css
/* CSS to style close icon */
.e-dialog .e-btn-icon.e-icon-dlg-close {
  font-size: 18px;
  color: #dc2626;
}

.e-dialog .e-btn-icon.e-icon-dlg-close:hover {
  color: #991b1b;
}
```

### Custom Close Button in Header

```jsx
const headerWithCustomClose = (
  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px' }}>
    <span>Custom Header</span>
    <button 
      onClick={() => dialogRef.current?.hide()}
      style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '20px' }}
    >
      ✕
    </button>
  </div>
);

<DialogComponent header={headerWithCustomClose} showCloseIcon={false}>
  Content with custom close
</DialogComponent>
```

## Edge Cases

### Empty Header

```jsx
<DialogComponent header="">
  Content with no header area
</DialogComponent>
```

### Very Long Header

```jsx
<DialogComponent header="This is a very long header that might wrap to multiple lines if the dialog is not wide enough">
  Content
</DialogComponent>
```

**Solution:** Set width explicitly
```jsx
<DialogComponent
  header="Very long header..."
  width="600px"
>
  Content
</DialogComponent>
```

### Content Overflow

```jsx
// Content that exceeds dialog height
<DialogComponent
  header="Scrollable Content"
  height="300px"
>
  <div>
    {/* Many items causing overflow */}
    {Array.from({ length: 50 }).map((_, i) => (
      <p key={i}>Item {i + 1}</p>
    ))}
  </div>
</DialogComponent>
```

**CSS to handle overflow:**
```css
.e-dialog .e-dlg-content {
  overflow-y: auto;
  max-height: 300px;
}
```

### HTML Injection Safety

When using string content, ensure it's safe:

```jsx
// ❌ UNSAFE - Never do this with user input
const userInput = "<img src=x onerror='alert(\"XSS\")'>";
<DialogComponent content={userInput} />

// ✅ SAFE - Use JSX instead
<DialogComponent>
  {userInput}  {/* Automatically escaped */}
</DialogComponent>

// ✅ SAFE - If HTML needed, sanitize first
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);
<DialogComponent content={clean} />
```

### Dynamic Content Loading

```jsx
export function AsyncContent() {
  const dialogRef = useRef(null);
  const [content, setContent] = React.useState('Loading...');

  const loadContent = async () => {
    dialogRef.current?.show();
    try {
      const response = await fetch('/api/data');
      const data = await response.json();
      setContent(data.message);
    } catch (error) {
      setContent('Error loading content');
    }
  };

  return (
    <div>
      <button onClick={loadContent}>Load</button>
      <DialogComponent
        ref={dialogRef}
        header="Content"
      >
        {content}
      </DialogComponent>
    </div>
  );
}
```

**Next:** Choose another reference topic based on your needs.
