# Content — Syncfusion React Tooltip

## Table of Contents
- [String Content](#string-content)
- [Template Content (JSX)](#template-content-jsx)
- [Dynamic Content via Fetch](#dynamic-content-via-fetch)
- [Dynamic Content via Ajax (Legacy)](#dynamic-content-via-ajax-legacy)
- [HTML Elements in Content (iframe, video, map)](#html-elements-in-content-iframe-video-map)
- [Updating Content Programmatically](#updating-content-programmatically)
- [HTML Sanitizer](#html-sanitizer)

---

## String Content

The simplest form — pass any string (including basic HTML tags) to `content`:

```tsx
<TooltipComponent content="Simple tooltip text">
  <button className="e-btn">Hover Me</button>
</TooltipComponent>
```

To include HTML markup (bold, italic, etc.):

```tsx
<TooltipComponent content="<b>Bold</b> and <i>italic</i> text">
  <button className="e-btn">Hover Me</button>
</TooltipComponent>
```

> HTML strings are parsed by default (`enableHtmlParse: true`). Set `enableHtmlParse={false}` to display the raw HTML string instead of rendering it.

---

## Template Content (JSX)

Pass a function that returns JSX as the `content` prop to create rich, formatted tooltips:

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  function tooltipContent() {
    return (
      <span>
        <p>
          <strong>Environmentally friendly</strong> or{' '}
          <strong>environment-friendly</strong>,{' '}
          <i>(also referred to as eco-friendly, nature-friendly, and green)</i>{' '}
          are marketing and sustainability terms referring to goods and services
          that inflict reduced, minimal, or no harm upon ecosystems.
        </p>
      </span>
    );
  }

  return (
    <div>
      A green home is a type of house designed to be
      <TooltipComponent isSticky={true} content={tooltipContent} style={{ display: 'inline-block', padding: '5px' }}>
        <a><u>environmentally friendly</u></a>
      </TooltipComponent>
      and sustainable.
    </div>
  );
}
export default App;
```

- `isSticky={true}` keeps the tooltip open until the user clicks the close icon — useful for rich template content.

---

## Dynamic Content via Fetch

> ⚠️ **Security — Third-Party Content Ingestion:**  
> Fetching content from external or third-party URLs and injecting it directly into tooltip `content` can expose users to XSS and data-injection attacks if the remote response is not validated.  
> **Always:**  
> - Fetch only from **same-origin or fully trusted internal endpoints** you control.  
> - **Sanitize every field** extracted from the response before assigning it to `tooltipInstance.content` — never interpolate raw API values into an HTML template string without escaping.  
> - Keep `enableHtmlSanitizer={true}` (the default) so the component's built-in sanitizer provides a last line of defence.  
> - Never use error/rejection `reason.message` from a remote call as raw tooltip HTML content.

Load tooltip content asynchronously in the `beforeRender` event. The pattern:
1. Set a "Loading…" placeholder immediately.
2. Call `dataBind()` to reflect the placeholder.
3. Fetch real data, **validate and sanitize each value**, then assign to `tooltipInstance.content`.
4. Call `dataBind()` again to render the fetched content.

```tsx
import * as React from 'react';
import { TooltipComponent, TooltipEventArgs } from '@syncfusion/ej2-react-popups';
import { Fetch } from '@syncfusion/ej2-base';

function App() {
  let tooltipInstance: TooltipComponent;

  function onBeforeRender(args: TooltipEventArgs): void {
    tooltipInstance.content = 'Loading...';
    tooltipInstance.dataBind();

    // ✅ Use a same-origin or fully trusted internal endpoint — never a public third-party URL.
    const fetchApi = new Fetch(
      '/api/tooltip-data',   // replace with your own trusted endpoint
      'GET'
    );
    fetchApi.send().then(
      (result: any) => {
        for (let i = 0; i < result.length; i++) {
          if (result[i].Id === args.target.getAttribute('data-content')) {
            // ✅ Encode the value before embedding in HTML to prevent XSS.
            const safeText = String(result[i].Sports)
              .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            tooltipInstance.content = `<div class='contentWrap'>${safeText}</div>`;
          }
        }
        tooltipInstance.dataBind();
      },
      (_reason: any) => {
        // ✅ Never expose raw remote error messages as HTML content.
        tooltipInstance.content = 'Failed to load content.';
        tooltipInstance.dataBind();
      }
    );
  }

  return (
    <div id="container">
      <TooltipComponent
        ref={t => (tooltipInstance = t)}
        content="Loading..."
        target=".target"
        position="RightCenter"
        beforeRender={onBeforeRender}
      >
        <ul>
          <li className="target" data-content="1"><span>Australia</span></li>
          <li className="target" data-content="2"><span>Bhutan</span></li>
          <li className="target" data-content="3"><span>China</span></li>
          <li className="target" data-content="4"><span>India</span></li>
        </ul>
      </TooltipComponent>
    </div>
  );
}
export default App;
```

> **GUID targets:** When using a GUID as the `target` value, the GUID must begin with a letter prefix, e.g., `target="#tooltip96ad88bd-294c-47c3-999b-a9daa3285a05"`.

---

## Dynamic Content via Ajax (Legacy)

> ⚠️ **Security — Third-Party Content Ingestion:**  
> The same rules that apply to `Fetch` apply here. Only call endpoints you own or fully trust, escape all response values before injecting them into HTML, and never surface raw error messages as tooltip content.

For projects using the older `Ajax` utility from `@syncfusion/ej2-base`:

```tsx
import { Ajax } from '@syncfusion/ej2-base';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  let tooltip: TooltipComponent;

  function beforeRender(args: any) {
    tooltip.content = 'Loading...';
    tooltip.dataBind();

    // ✅ Use a same-origin endpoint you control; avoid third-party URLs.
    const ajax = new Ajax('./tooltip.json', 'GET', true);
    ajax.send().then(
      (result: any) => {
        result = JSON.parse(result);
        for (let i = 0; i < result.length; i++) {
          if (result[i].Id === args.target.id) {
            // ✅ Assign plain text values directly; use text-node rendering to avoid XSS.
            tooltip.content = String(result[i].Name);
          }
        }
        tooltip.dataBind();
      },
      (_reason: any) => {
        // ✅ Never expose raw remote error messages as HTML content.
        tooltip.content = 'Failed to load content.';
        tooltip.dataBind();
      }
    );
  }

  return (
    <TooltipComponent
      ref={i => (tooltip = i)}
      beforeRender={beforeRender}
      content="Loading..."
      target=".item"
      position="BottomCenter"
      showTipPointer={false}
    >
      <div className="item" id="1">Item 1</div>
      <div className="item" id="2">Item 2</div>
    </TooltipComponent>
  );
}
```

> Prefer `Fetch` from `@syncfusion/ej2-base` for new projects; `Ajax` is available for backward compatibility.

---

## HTML Elements in Content (iframe, video, map)

> ⚠️ **Security — Iframe Third-Party Content:**  
> Embedding an `<iframe>` pointing to an external URL loads and executes that site's scripts inside your page. This can expose users to clickjacking, credential harvesting, or malicious script execution.  
> **Guidance:**  
> - Only embed `<iframe>` sources from **origins you own or fully trust** (same-origin preferred).  
> - Always add `sandbox` attribute restrictions (`sandbox="allow-scripts allow-same-origin"`) to limit iframe capabilities.  
> - Never construct the `src` from user-supplied or remote data without strict allow-list validation.

The `content` property accepts a JSX function that can embed any HTML element, including `<iframe>`:

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  function iFrame() {
    // ✅ Only embed origins you own or fully trust.
    // ✅ Always add sandbox restrictions to limit iframe capabilities.
    return (
      <iframe
        src="/your-internal-page"  // replace with a same-origin or trusted URL
        sandbox="allow-scripts allow-same-origin"
        title="Tooltip embedded content"
      />
    );
  }

  return (
    <div id="container">
      <TooltipComponent
        target="#iframeContent"
        content={iFrame}
        opensOn="Click"
        position="BottomCenter"
      >
        <div id="tooltipContent">
          <ButtonComponent id="iframeContent">Embedded Iframe</ButtonComponent>
        </div>
      </TooltipComponent>
    </div>
  );
}
export default App;
```

For SVG maps or other visualization elements, render the element into a container div and pass that element reference as the content.

---

## Updating Content Programmatically

Change tooltip content at any time by setting the `content` property and calling `dataBind()`:

```tsx
let tooltipRef: TooltipComponent;

function updateContent() {
  tooltipRef.content = 'Updated tooltip content';
  tooltipRef.dataBind(); // applies pending property changes immediately
}

return (
  <TooltipComponent ref={t => (tooltipRef = t)} content="Original content">
    <button className="e-btn">Hover</button>
  </TooltipComponent>
);
```

---

## HTML Sanitizer

> 🔒 **Security — Keep `enableHtmlSanitizer` enabled:**  
> `enableHtmlSanitizer={true}` is the default and acts as a critical last line of defence against XSS. **Do not disable it** unless the content is generated entirely by your own application code with no user or remote input involved. Setting it to `false` when content originates from any external source (fetched API, user input, remote iframe src) is a **high-severity security risk**.

By default `enableHtmlSanitizer={true}` — the component strips untrusted scripts and HTML before rendering.

```tsx
{/* ✅ Recommended: keep the default sanitizer enabled */}
<TooltipComponent content="<b>Safe text</b>">
  <button className="e-btn">Hover</button>
</TooltipComponent>
```

**Only** disable when the content is fully app-generated with no external data involved:

```tsx
{/* ⛔ High risk — only acceptable when content is 100% app-controlled with no remote/user input */}
<TooltipComponent
  content="<b>App-generated static text only</b>"
  enableHtmlSanitizer={false}
>
  <button className="e-btn">Hover</button>
</TooltipComponent>
```

---

## See Also
- [Open Mode](open-mode.md) — `isSticky`, `beforeRender` event details
- [API Reference](api.md) — `content`, `enableHtmlParse`, `enableHtmlSanitizer`, `beforeRender`
