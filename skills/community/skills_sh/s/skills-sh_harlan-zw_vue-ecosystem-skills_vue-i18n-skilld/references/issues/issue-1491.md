---
number: 1491
title: Type declaration file could not be found
type: other
state: closed
created: 2023-08-11
url: "https://github.com/intlify/vue-i18n/issues/1491"
reactions: 9
comments: 18
resolvedIn: 9.3.0
labels: "[Status: Review Needed]"
---

# Type declaration file could not be found

### Reporting a bug?

There are types at '.../node_modules/vue-i18n/dist/vue-i18n.d.ts', but this result could not be resolved when respecting package.json "exports". The 'vue-i18n' library may need to update its package.json or typings

### Expected behavior

```ts
import { createI18n } from "vue-i18n";

import type {
  I18n,
  I18nOptions,
  Locale,
  VueI18n,
  Composer,
  I18nMode,
} from "vue-i18n";
```

When I use the above code, my ts says I can't find the module declaration file.

It's fine when I modify an export in a dependent file: /node_modules/vue-i18n/package
```json
  "exports": {
    ".": {
      "import": {
        "node": "./index.mjs",
        "default": "./dist/vue-i18n.esm-bundler.js"
        // Here's what I added
       "types":"./dist/vue-i18n.d.ts"
      },
      "require": "./index.js"
    },
    "./dist/*": "./dist/*",
    "./index.mjs": "./index.mjs",
    "./package.json": "./package.json"
  },
```


### Reproduction

https://github.com/CodeGetters/studtwork_desk/tree/ae78b7538048c538dd2fe05153cba8d340db323a

### System Info

...

---

## Top Comments

**@0xDarker** (+4):

> upgrade "vue-i18n": "^9.3.0-beta.25"

I upgrade to "9.3.0-beta.25", then run  "pnpm dev" reports as this :

...

**@CodeGetters** (+2):

> same issue with vue-i18n@9.2.2

  I switched the version of vue-i18n to 9.2.2 and used the following ts configuration to successfully package and display
  ```ts
  {
    "extends": "@vue/tsconfig/tsconfig.dom.json",
    "compilerOptions": {
      "baseUrl": ".",
      "paths": {
        "@/*": ["./src/*"]
      },
      "noEmit": true
    },
    "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
    "exclude": ["node_modules"],
    "references": [{ "path": "./tsconfig.node.json" }]
  }
  ```

**@kazupon** [maintainer]:

This issue has been resolved in the latest version of v9.3.0-beta