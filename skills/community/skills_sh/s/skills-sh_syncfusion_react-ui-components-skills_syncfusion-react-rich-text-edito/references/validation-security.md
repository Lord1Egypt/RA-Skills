# Validation & Security in Syncfusion React Rich Text Editor

## Table of Contents
- [Form Support](#form-support)
- [XHTML Validation](#xhtml-validation)
- [Read-Only Mode](#read-only-mode)
- [XSS Prevention](#xss-prevention)

## Form Support

The RTE integrates with HTML forms. Render the editor inside a `<form>` element and retrieve its value via `FormData` on submit.

```tsx
import { FormValidator, FormValidatorModel } from '@syncfusion/ej2-inputs';
import {
  Count, HtmlEditor, Image, Inject, Link,
  QuickToolbar, RichTextEditorComponent, Toolbar
} from '@syncfusion/ej2-react-richtexteditor';
import { useEffect, useRef } from 'react';

function App() {
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    const options: FormValidatorModel = {
      rules: {
        defaultRTE: {
          required: [true, 'Content is required'],
          minLength: [20, 'Minimum 20 characters required'],
          maxLength: [500, 'Maximum 500 characters allowed'],
        }
      }
    };
    const formValidator = new FormValidator('#myForm', options);

    const submitBtn = document.getElementById('submitBtn');
    submitBtn?.addEventListener('click', (e) => {
      e.preventDefault();
      const form = document.forms['myForm' as any];
      const formData = new FormData(form);
      const rteValue = formData.get('defaultRTE');
      console.log('Submitted value:', rteValue);
    });
  }, []);

  return (
    <form id="myForm">
      <RichTextEditorComponent id="defaultRTE" name="defaultRTE">
        <Inject services={[Toolbar, HtmlEditor, Image, Link, QuickToolbar, Count]} />
      </RichTextEditorComponent>
      <div id="dateError"></div>
      <button id="submitBtn" type="submit">Submit</button>
      <button type="reset">Reset</button>
    </form>
  );
}
```

**Key points:**
- Give the RTE an `id` and `name` attribute matching the form field
- Use `FormValidator` from `@syncfusion/ej2-inputs` for validation rules
- The form `reset` button clears the editor content automatically

## XHTML Validation

Enable `enableXhtml={true}` to make the editor enforce XHTML-compliant output. The editor will ensure proper tag closing, attribute quoting, and valid nesting.

```tsx
<RichTextEditorComponent enableXhtml={true}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

**What XHTML validation enforces:**
- Self-closing tags (`<br />`, `<img />`)
- Lowercase element and attribute names
- Quoted attribute values
- No deprecated elements

## Read-Only Mode

Set `readonly={true}` to render the editor in a non-editable state. The content is displayed but users cannot type or change it. The toolbar is hidden in read-only mode.

```tsx
<RichTextEditorComponent readonly={true} value="<p>This content is read-only.</p>">
  <Inject services={[HtmlEditor]} />
</RichTextEditorComponent>
```

**Toggle read-only dynamically:**

```tsx
function App() {
  const rteRef = useRef<RichTextEditorComponent>(null);
  const [isReadOnly, setIsReadOnly] = useState(false);

  const toggleReadOnly = () => {
    if (rteRef.current) {
      rteRef.current.readonly = !isReadOnly;
      setIsReadOnly(!isReadOnly);
    }
  };

  return (
    <>
      <button onClick={toggleReadOnly}>{isReadOnly ? 'Enable Editing' : 'Make Read-Only'}</button>
      <RichTextEditorComponent ref={rteRef} value="<p>Some content</p>">
        <Inject services={[Toolbar, HtmlEditor]} />
      </RichTextEditorComponent>
    </>
  );
}
```

**Enabled vs Read-Only:**
- `readonly={true}` — displays content, hides toolbar
- `enabled={false}` — disables the component entirely (greyed out state)

## XSS Prevention

The RTE sanitizes HTML input by default to prevent cross-site scripting (XSS) attacks. Dangerous tags like `<script>` and event attributes like `onclick` are stripped.

**The sanitization is enabled by default.** To control it:

```tsx
// Disable sanitization (not recommended for user-generated content)
<RichTextEditorComponent enableHtmlSanitizer={false}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

**Best practices for XSS prevention:**
- Keep `enableHtmlSanitizer={true}` (default) for user-generated content
- Use `enableHtmlEncode={true}` when storing to a database — stores encoded values
- Always sanitize on the server side as a secondary defense
- Avoid using `innerHTML` directly with RTE values; use the `value` property instead
