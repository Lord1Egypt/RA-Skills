# JavaScript / Web SDK

## Table of Contents
- [Installation](#installation)
- [Initialization](#initialization)
- [Framework-Specific Notes](#framework-specific-notes)
- [Common API Usage](#common-api-usage)

## Installation

### Option A: npm / yarn (Angular, React, Vue, Next.js, Nuxt)

```
npm install gleap --save
```

### Option B: CDN Script Tag (plain HTML or any web page)

Add to `<head>`:

```html
<script>
!function(){if(!(window.Gleap=window.Gleap||[]).invoked){window.GleapActions=[];const e=new Proxy({invoked:!0},{get:function(e,n){return"invoked"===n?e.invoked:function(){const e=Array.prototype.slice.call(arguments);window.GleapActions.push({e:n,a:e})}},set:function(e,n,t){return e[n]=t,!0}});window.Gleap=e;const n=document.getElementsByTagName("head")[0],t=document.createElement("script");t.type="text/javascript",t.async=!0,t.src="https://sdk.gleap.io/latest/index.js",n.appendChild(t),
    window.Gleap.initialize("API_KEY")
}}();
</script>
```

Replace `API_KEY` with the actual key. This loads Gleap asynchronously and initializes it. No further init call needed.

## Initialization

For npm installs, import and initialize once:

```javascript
import Gleap from "gleap";

Gleap.initialize("API_KEY");
```

Call `initialize` only once. For CDN installs, initialization is included in the snippet above.

## Framework-Specific Notes

### Angular
Add initialization to `app.component.ts` or `main.ts`.

### React
Add initialization to `index.js` or `App.js` before rendering.

### Vue.js
Add initialization to `main.js` or `main.ts`.

### Next.js
Add initialization inside a `useEffect` in `_app.js` or `_app.tsx`, or in a client component.

### Nuxt
Add initialization in a client-side plugin.

### Ruby on Rails / Turbo (soft-reload)
Some stacks clear HTML on soft reload, removing the widget. Re-initialize after:

```javascript
Gleap.getInstance().softReInitialize();

// With Turbo:
document.addEventListener("turbo:load", function () {
  Gleap.getInstance().softReInitialize();
});
```

## Common API Usage

### Identify Users

```javascript
Gleap.identify("USER_ID", {
  name: "Franz",
  email: "franz@example.com",
  phone: "+1 (902) 123123",
  value: 199.95,
  plan: "Pro plan",
  companyId: "12398958484",
  companyName: "ACME inc.",
  customData: {
    role: "admin",
    logins: 42,
  },
});
```

Update contact data (partial updates supported):
```javascript
Gleap.updateContact({ plan: "Enterprise" });
```

Clear identity on logout:
```javascript
Gleap.clearIdentity();
```

### Track Events

```javascript
Gleap.trackEvent("User signed in");

// With data:
Gleap.trackEvent("Purchase completed", {
  amount: 49.99,
  currency: "USD",
});
```

### Custom Data

```javascript
Gleap.attachCustomData({ environment: "staging", buildId: "abc123" });

// Incremental:
Gleap.setCustomData("key", "value");

// Remove:
Gleap.removeCustomData("key");

// Clear all:
Gleap.clearCustomData();
```

### Widget Control

```javascript
Gleap.open();
Gleap.close();
Gleap.isOpened(); // returns boolean
```
