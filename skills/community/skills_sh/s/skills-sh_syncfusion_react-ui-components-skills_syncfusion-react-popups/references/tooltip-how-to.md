# How-To Patterns — Syncfusion React Tooltip

## Table of Contents
- [Tooltip on Multiple Targets with Dynamic Content](#tooltip-on-multiple-targets-with-dynamic-content)
- [Tooltip on Disabled Elements](#tooltip-on-disabled-elements)
- [Enable and Disable Tooltip at Runtime](#enable-and-disable-tooltip-at-runtime)
- [Tooltip on SVG Elements](#tooltip-on-svg-elements)
- [Tooltip on Canvas Elements](#tooltip-on-canvas-elements)
- [Tooltip with Embedded iframe](#tooltip-with-embedded-iframe)
- [Custom Open Modes (Double-Click, Right-Click)](#custom-open-modes-double-click-right-click)
- [Tooltip Open/Display Modes Demo](#tooltip-opendisplay-modes-demo)

---

## Tooltip on Multiple Targets with Dynamic Content

> ⚠️ **Security — Third-Party Content Ingestion:**  
> Only call endpoints you own or fully trust. Escape all values extracted from the response before assigning them as tooltip content, and never surface raw remote error messages as tooltip HTML.

Use a single `TooltipComponent` with a shared `target` selector and load different content per target via `beforeRender`:

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';
import { Ajax } from '@syncfusion/ej2-base';

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
            // ✅ Assign plain text directly to avoid XSS via HTML injection.
            tooltip.content = String(result[i].Name);
          }
        }
        tooltip.dataBind();
      },
      (_reason: any) => {
        // ✅ Never expose raw remote error messages as tooltip content.
        tooltip.content = 'Failed to load content.';
        tooltip.dataBind();
      }
    );
  }

  return (
    <div id="container">
      <TooltipComponent
        ref={i => (tooltip = i)}
        beforeRender={beforeRender}
        content="Loading..."
        target=".circletool"
        position="BottomCenter"
        showTipPointer={false}
      >
        <h2>Dynamic Tooltip Content</h2>
        <div id="box">
          <div id="1" className="circletool" />
          <div id="2" className="circletool" />
          <div id="3" className="circletool" />
          <div id="4" className="circletool" />
          <div id="5" className="circletool" />
          <div id="6" className="circletool" />
        </div>
      </TooltipComponent>
    </div>
  );
}
export default App;
```

**Pattern:**
- Each target element has a unique `id`.
- The `beforeRender` callback receives `args.target` — the currently hovered element.
- Fetch data matching the target's `id` and set `tooltip.content`, then `dataBind()`.

---

## Tooltip on Disabled Elements

By default, disabled elements do not fire mouse events and tooltips won't appear. Workaround:

1. Wrap the disabled element in an `inline-block` container.
2. Apply `pointer-events: none` to the disabled element via CSS.
3. Attach the tooltip to the **wrapper** div (not the disabled button).

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  return (
    <div style={{ display: 'inline-block' }}>
      <TooltipComponent content="This button is disabled" position="TopCenter">
        <div style={{ display: 'inline-block' }}>
          {/* pointer-events none lets the parent div receive hover events */}
          <button
            className="e-btn"
            disabled={true}
            style={{ pointerEvents: 'none' }}
          >
            Disabled Button
          </button>
        </div>
      </TooltipComponent>
    </div>
  );
}
export default App;
```

> The tooltip is attached to the outer `div`, which receives pointer events even though the inner `button` has `pointerEvents: none`.

---

## Enable and Disable Tooltip at Runtime

Use `destroy()` to remove the tooltip entirely and `render()` to re-initialize it:

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';
import { SwitchComponent, ChangeEventArgs } from '@syncfusion/ej2-react-buttons';

function App() {
  let tooltip: TooltipComponent;

  function handleChange(args: ChangeEventArgs) {
    if (!args.checked) {
      tooltip.destroy();   // removes tooltip behavior
    } else {
      tooltip.render();    // re-initializes tooltip
    }
  }

  return (
    <div>
      <TooltipComponent
        content="Tooltip Content"
        target="#tooltipTarget"
        ref={d => (tooltip = d)}
        style={{ display: 'inline-block' }}
      >
        <button className="e-btn" id="tooltipTarget" style={{ margin: '50px' }}>
          Show Tooltip
        </button>
      </TooltipComponent>

      <div>
        <label htmlFor="enableSwitch">Enable Tooltip</label>
        <SwitchComponent
          id="enableSwitch"
          checked={true}
          change={handleChange}
        />
      </div>
    </div>
  );
}
export default App;
```

---

## Tooltip on SVG Elements

Target SVG elements by their `id` using the `target` prop. The tooltip renders over the SVG shape:

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  return (
    <TooltipComponent content="SVG Square" cssClass="e-tooltip-css" target="#square">
      <div>
        <svg>
          <rect
            id="square"
            x="50" y="20"
            width="50" height="50"
            style={{ fill: '#FDA600' }}
          />
        </svg>
      </div>
    </TooltipComponent>
  );
}
export default App;
```

For multiple SVG shapes, nest `TooltipComponent` instances or use a single one with a shared class selector:

```tsx
<TooltipComponent content="SVG Ellipse" target="#ellipse">
  <TooltipComponent content="SVG Square" target="#square">
    <svg>
      <rect id="square" x="50" y="20" width="50" height="50" />
      <ellipse id="ellipse" cx="200" cy="50" rx="40" ry="20" />
    </svg>
  </TooltipComponent>
</TooltipComponent>
```

---

## Tooltip on Canvas Elements

Canvas elements don't have inherent HTML children to target — wrap the `<canvas>` in a div and target the canvas `id`:

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  const canvasRef = React.useRef<HTMLCanvasElement>(null);

  React.useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas?.getContext) {
      const ctx = canvas.getContext('2d')!;
      ctx.beginPath();
      ctx.arc(30, 30, 25, 0, 2 * Math.PI);
      ctx.fillStyle = '#0450C2';
      ctx.fill();
    }
  }, []);

  return (
    <TooltipComponent content="Canvas Circle" cssClass="e-tooltip-css" target="#circle">
      <div>
        <canvas id="circle" ref={canvasRef} width="60" height="60" />
      </div>
    </TooltipComponent>
  );
}
export default App;
```

---

## Tooltip with Embedded iframe

> ⚠️ **Security — Iframe Third-Party Content:**  
> Embedding an `<iframe>` that points to an external or third-party URL loads and executes that site's scripts inside your page. This can expose users to clickjacking, credential harvesting, or malicious script execution.  
> **Always:**  
> - Use only **same-origin or fully trusted internal URLs** as the `src` — never a public third-party URL.  
> - Add `sandbox` attribute restrictions to limit iframe capabilities (e.g., `sandbox="allow-scripts allow-same-origin"`).  
> - Never construct the `src` value from user-supplied or remotely fetched data without strict allow-list validation.

Embed an iframe in the tooltip content using a JSX function and `opensOn="Click"` (so the user can interact with the iframe):

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  function iFrameContent() {
    return (
      // ✅ Use a same-origin or fully trusted internal URL — never a public third-party URL.
      // ✅ Always add sandbox restrictions to limit iframe capabilities.
      <iframe
        src="/your-internal-page"  // replace with your own trusted same-origin URL
        sandbox="allow-scripts allow-same-origin"
        title="Tooltip embedded content"
        style={{ width: '400px', height: '300px' }}
      />
    );
  }

  return (
    <TooltipComponent
      target="#iframeContent"
      content={iFrameContent}
      opensOn="Click"
      position="BottomCenter"
      isSticky={true}
    >
      <div>
        <ButtonComponent id="iframeContent">Embedded Iframe</ButtonComponent>
      </div>
    </TooltipComponent>
  );
}
export default App;
```

> Use `isSticky={true}` with embedded iframes so the tooltip stays open while the user interacts with the iframe content.

---

## Custom Open Modes (Double-Click, Right-Click)

Combine `opensOn="Custom"` with React event handlers to trigger on any gesture:

**Double-click:**
```tsx
function App() {
  let tooltipRef: TooltipComponent;
  let btnRef: HTMLButtonElement;

  function onDoubleClick() {
    if (btnRef.getAttribute('data-tooltip-id')) {
      tooltipRef.close();
    } else {
      tooltipRef.open(btnRef);
    }
  }

  return (
    <TooltipComponent
      ref={t => (tooltipRef = t)}
      opensOn="Custom"
      content="Opened via double-click"
    >
      <button ref={d => (btnRef = d)} className="e-btn" onDoubleClick={onDoubleClick}>
        Double Click Me
      </button>
    </TooltipComponent>
  );
}
```

**Right-click (context menu):**
```tsx
function onContextMenu(e: React.MouseEvent) {
  e.preventDefault();
  if (btnRef.getAttribute('data-tooltip-id')) {
    tooltipRef.close();
  } else {
    tooltipRef.open(btnRef);
  }
}

<button ref={d => (btnRef = d)} className="e-btn" onContextMenu={onContextMenu}>
  Right Click Me
</button>
```

---

## Tooltip Open/Display Modes Demo

A complete multi-mode example showing all open modes side by side:

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  let customTooltip: TooltipComponent;

  function handleDoubleClick(args: React.MouseEvent<HTMLButtonElement>) {
    const target = args.currentTarget as HTMLElement;
    if (target.getAttribute('data-tooltip-id')) {
      customTooltip.close();
    } else {
      customTooltip.open(target);
    }
  }

  return (
    <div id="showTooltip">
      {/* Hover */}
      <TooltipComponent opensOn="Hover" content="Tooltip from hover" position="BottomCenter">
        <button className="e-btn">Hover Me</button>
      </TooltipComponent>

      {/* Click */}
      <TooltipComponent opensOn="Click" content="Tooltip from click" position="BottomCenter">
        <button className="e-btn">Click Me</button>
      </TooltipComponent>

      {/* Sticky */}
      <TooltipComponent content="Click × to close" position="BottomCenter" isSticky={true}>
        <button className="e-btn">Sticky Mode</button>
      </TooltipComponent>

      {/* Delay */}
      <TooltipComponent content="Delayed tooltip" position="BottomCenter" openDelay={1000} closeDelay={1000}>
        <button className="e-btn">With Delay</button>
      </TooltipComponent>

      {/* Custom (double-click) */}
      <TooltipComponent
        ref={t => (customTooltip = t)}
        opensOn="Custom"
        content="Tooltip from custom mode"
        position="BottomCenter"
      >
        <button className="e-btn" onDoubleClick={handleDoubleClick}>
          Double Click Me
        </button>
      </TooltipComponent>

      {/* Focus */}
      <TooltipComponent content="Tooltip from focus" position="BottomCenter">
        <div className="e-float-input">
          <input type="text" placeholder="Focus and blur" />
        </div>
      </TooltipComponent>
    </div>
  );
}
export default App;
```

---

## See Also
- [Content](content.md) — Dynamic/async content patterns
- [Open Mode](open-mode.md) — Full `opensOn` reference
- [Position](position.md) — SVG/Canvas positioning edge cases
- [API Reference](api.md) — `destroy()`, `render()`, `open()`, `close()`, `dataBind()`
