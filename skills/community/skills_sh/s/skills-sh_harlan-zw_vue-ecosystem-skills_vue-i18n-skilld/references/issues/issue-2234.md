---
number: 2234
title: Incompatibility with Vue Vapor
type: other
state: open
created: 2025-07-18
url: "https://github.com/intlify/vue-i18n/issues/2234"
reactions: 4
comments: 5
labels: "[ p4-important]"
---

# Incompatibility with Vue Vapor

### Reporting a bug?

Attempting to do 

```vue
<script setup vapor lang="ts">
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>
```

Results in 

```
Uncaught (in promise) SyntaxError: Must be called at the top of a `setup` function
    createCompileError message-compiler.mjs:77
    createI18nError vue-i18n.runtime.mjs:63
    useI18n vue-i18n.runtime.mjs:2138
    setup ThisFile.vue:3
```

### Expected behavior

Works in Vue Vapor as it does with non-Vapor Vue

### Reproduction

None

### System Info

```
"@intlify/unplugin-vue-i18n": "^6.0.8",
"vue": "^3.6.0-alpha.1",
"vue-i18n": "^11.1.10",
"vite": "^7.0.5",
```

### Screenshot

_No response_

### Additional context

https://github.com/vuejs/core/releases/tag/v3.6.0-alpha.1#about-vapor-mode

### Validations

...

---

## Top Comments

**@BobbieGoede** [maintainer] (+4):

Some Vue features are not supported in Vapor Mode as described in the "About Vapor Mode" section in https://github.com/vuejs/core/releases/tag/v3.6.0-alpha.1#about-vapor-mode.

Unfortunately one of the unsupported Vue methods in Vapor mode is `getCurrentInstance()`, which will always return `null` in Vapor mode. This happens to be how vue-i18n retrieves its instance or sets it up if none is found, so this will need to be reworked if we want to support Vapor mode (not sure what the best approach would be /cc @kazupon).

...

**@kazupon** [maintainer] (+5):

I will discuss with the team whether vapor mode can continue to support getCurrentInstance as before, while also exploring other possible solutions.

I am currently working on the release of gunshi v0.27, a side project, and once that is complete, I plan to restart on vue-i18n v12.

**@wsxiaolin**:

I encountered the same issue using 3.6.0-alpha.2