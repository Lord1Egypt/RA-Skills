---
number: 2968
title: Cannot view error page, hydrate of error object fails
category: Help and Questions
created: 2025-04-08
url: "https://github.com/vuejs/pinia/discussions/2968"
upvotes: 1
comments: 4
answered: true
---

# Cannot view error page, hydrate of error object fails

### Reproduction

https://stackblitz.com/edit/bobbiegoede-nuxt-i18n-starter-ycvcel1p?file=nuxt.config.ts,stores%2Fhello.js

### Steps to reproduce the bug

1. Create nuxt project
2. Install pinia
3. Go to an error page (which should be 404)
4. ????
5. obj.hasOwnProperty is not a function

### Expected behavior

Should display error template.

### Actual behavior

Goes through error, tries to hydrate payload which should not be hydrated.


### Additional information

This error started appearing after the latest nuxt update, consistently happens only after cleaning lockfile.

---

## Accepted Answer

**@posva** [maintainer]:

Fixed in fd6d969