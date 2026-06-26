---
number: 1403
title: global $t show issue 
type: other
state: open
created: 2023-05-15
url: "https://github.com/intlify/vue-i18n/issues/1403"
reactions: 17
comments: 61
labels: "[Status: Need More Info, typescript]"
---

# global $t show issue 

### Reporting a bug?

The global variable "$t" show issue 'Property '$t' does not exist on type' in vue template

My ./i18n/index.ts files : 
```
  import { createI18n } from 'vue-i18n';
  
  import fr from "./locales/fr.json";
  type MessageSchema = typeof fr
  
  export default createI18n<[MessageSchema], 'fr'>({
    allowComposition: true,
    locale: import.meta.env.VITE_DEFAULT_LOCALE,
    fallbackLocale: import.meta.env.VITE_FALLBACK_LOCALE,
    legacy: false,
    messages: {
      'fr': fr,
    },
  })  
```

My main.ts file : 
```
import { createApp } from 'vue';
import { createPinia } from 'pinia';

import i18n from "./i18n";

import App from './App.vue';
import router from './router';

import './index.css';

const app = createApp(App)

app.use(i18n)
app.use(createPinia())
app.use(router)

app.mount('#app')
```

My template file : 
```
<nav class="flex flex-row mx-2 m-0.5">
      <RouterLink class="px-1" to="login">{{  $t("auth.login") }}</RouterLink> /
       <RouterLink class="px-1" to="register">{{  $t("auth.register") }}</RouterLink>
</nav>
```

### Expected behavior

No issue :D

### Reproduction

1. create new vue3 project
2. install "vue-i18n": "^9.3.0-beta.17",
3. create json files
4. use $t in template

### System Info

```shell
System:
    OS: Linux 5.15 Ubuntu 22.04.2 LTS 22.04.2 LTS (Jammy Jellyfish)
    CPU: (4) x64 Intel(R) Core(TM) i5-7300U CPU @ 2.60GHz
    Memory: 6.79 GB / 15.50 GB
    Container: Yes
    Shell: 5.1.16 - /bin/bash
  Binaries:
    Node: 18.16.0 - /usr/bin/node
    npm: 8.19.1 - /usr/local/bin/npm
  Browsers:
    Chrome: 113.0.5672.92
    Firefox: 113.0.1
  npmPackages:
    @intlify/unplugin-vue-i18n: ^0.10.0 => 0.10.0 
    @vitejs/plugin-vue: ^4.2.1 => 4.2.2 
    @vitejs/plugin-vue-jsx: ^3.0.1 => 3.0.1 
    @vue/eslint-config-prettier: ^7.1.0 => 7.1.0 
    @vue/eslint-config-typescript: ^11.0.3 => 11.0.3 
    @vue/tsconfig: ^0.3.2 => 0.3.2 
    vite: ^4.3.4 => 4.3.5 
    vue: ^3.2.47 => 3.3.1 
    vue-i18n: ^9.3.0-beta.17 => 9.3.0-beta.14-77e850b 
    vue-moment: ^4.1.0 => 4.1.0 
    vue-router: ^4.1.6 => 4.2.0 
    vue-tsc: ^1.6.4 => 1.6.4
```...

---

## Top Comments

**@dodo1708** (+3):

I'm having the same issue.
Adding 

`"types": "./dist/vue-i18n.d.ts",`

to 

```
"exports": {
    ".": {
      "types": "./dist/vue-i18n.d.ts",
      "import": {
        "node": "./index.mjs",
        "default": "./dist/vue-i18n.esm-bundler.js"
      },
      "require": "./index.js"
    },
    "./dist/*": "./dist/*",
    "./index.mjs": "./index.mjs",
    "./package.json": "./package.json"
  },
  ```

in the vie-i18n package.json fixed the issue for me when running it locally. 


**@kazupon** [maintainer] (+1):

Thank you for your reporting!

Issue template said:
>Please provide a link to a repo that can reproduce the problem you ran into. A minimal reproduction is required (Why?). If a report is vague (e.g. just a generic error message) and has no reproduction, it will receive a "Status: Need More Info" label. If no reproduction is provided after 5 days, it will be closed.

Could you give us your **minimal reproduction** with github repo or [stackbliz](https://stackblitz.com/) please? 🙏 

**@g1eny0ung** (+1):

I have the same problem. The situation for me is that I upgrade `vue` to `v3.3` with pnpm, the package with the old vue version seems to be confusing with the new one, and running `pnpm dedupe` solves this problem.