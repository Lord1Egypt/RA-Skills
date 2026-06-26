---
number: 18158
title: in app theme switcher ?!
category: General - Components / Directives / etc
created: 2025-10-21
url: "https://github.com/quasarframework/quasar/discussions/18158"
upvotes: 1
comments: 1
answered: true
---

# in app theme switcher ?!

hello community,
what is the best way to add an in-app theme switcher drop-down?
light/dark is already implemented.

should i go similar way as suggested in 
https://quasar.dev/style/color-palette#dynamic-change-of-brand-colors-dynamic-theme-colors-
or does it make more sens to *dynamically* add css files?
or body classes with the theme-prefix and a theme-specific css that uses the prefix?!

currently i have no idea.. ;-)
the default should be the out-of-the-box quasar defaults.

and then there needs to be one or two custom ones..

(at least that is my current idea)

---

## Accepted Answer

I built a solution to manage dynamic themes per client that relies on a combination of **Pinia** for centralization and **Quasar's CSS Variables** utilities for application.

This approach ensures that business rules and theme state are maintained in a single, accessible location.

### 1\. Centralization with Pinia (Store)

I used a dedicated Pinia Store to concentrate:

  * **Business Rules:** The logic to identify the client (usually via URL) and determine which theme to load.
  * **Theme State:** Stores the active color scheme and the client's visual identity (`currentBrand`).

### 2\. Client Schemas and Application

I keep all **color schemes** and visual identities defined per client. The moment a user accesses the system through the client's specific URL, the Pinia Store identifies the client.

The application of colors is done instantly using Quasar's **`setCssVar`** function. This overwrites the global CSS variables, adapting the visual interface.

The code sni...