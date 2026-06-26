---
number: 18189
title: chrome dev tools breaks q-input floating label
category: General - Components / Directives / etc
created: 2025-11-29
url: "https://github.com/quasarframework/quasar/discussions/18189"
upvotes: 1
comments: 1
answered: false
---

# chrome dev tools breaks q-input floating label

My q-input floating labels are not moving when refreshing in chrome with dev tools open, otherwise they work fine.  Does not happen in any other browser except chrome.  Unable to open a issue for this since I can't reproduce this in codepen.  Does anyone have any ideas on why this is happening and what is the fix?  When moving the dev tools width, the labels snap into their proper place.  The issue is fixed by adding this css, but can anyone help me troubleshoot why this is happening?  Refreshing with chrome dev tools open also causes popup modals not to work, so I think this may be a larger issue?

```
.q-field--float .q-field__label {
  transform: scale(0.75) !important;
  top: 8px !important;
}
```

<img width="490" height="172" alt="image" src="https://github.com/user-attachme...

---

## Top Comments

**@henrychoy**:

I discovered that it was my icon imports in `main.ts` that was causing the issue, but I still dont understand why.  This is the way that the docs say to import them when using the vite plugin version of Quasar.  When putting them under nextTick, the issue is resolved, but this seems like a hack?  Please let me know if any of you have more insight, thanks!

```
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/material-symbols-outlined/material-symbols-outlined.css'
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'
```

```
nextTick(async () => {
  await import('@quasar/extras/material-icons/material-icons.css')
  await import('@quasar/extras/material-symbols-outlined/material-symbols-outlined.css')
  await import('@quasar/extras/fontawesome-v6/fontawesome-v6.css')
})
```...