---
number: 789
title: You are running the esm-bundler build of vue-i18n. It is recommended to configure your bundler to explicitly replace feature flag globals with boolean literals to get proper tree-shaking in the final bundle.
type: other
state: closed
created: 2021-11-15
url: "https://github.com/intlify/vue-i18n/issues/789"
reactions: 20
comments: 30
labels: "[Status: Review Needed]"
---

# You are running the esm-bundler build of vue-i18n. It is recommended to configure your bundler to explicitly replace feature flag globals with boolean literals to get proper tree-shaking in the final bundle.

### Reporting a bug?


I have created an app with vue 3.2 and added vue-i18n. 
and i  get the following warning in the browser console:


````
You are running the esm-bundler build of vue-i18n. It is recommended to configure your bundler to explicitly replace feature flag globals with boolean literals to get proper tree-shaking in the final bundle.
`````

### Expected behavior

no warning on the console

### Reproduction

````bash
vue create vue-app
````
````bash
yarn add vue-i18n@next
````

in my main.ts

````js
import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import store from '@/store'
import i18n from "@/locales/i18n-config";

createApp(App)
    .use(i18n)
    .use(store)
    .use(router)
    .mount('#app')
````

in the @/locales/i18n-config file 

````js
import { createI18n } from 'vue-i18n'
import en from "@/locales/dictionary/en";
import fr from "@/locales/dictionary/fr";

const i18n = createI18n({
    locale: 'en', // set locale
    fallbackLocale: 'en', // set fallback locale
    messages: { en, fr }, // set locale messages
})

export default i18n


`````

### System Info

```shell
System:
    OS: macOS 12.0.1
    CPU: (8) x64 Apple M1
    Memory: 142.69 MB / 16.00 GB
    Shell: 5.8 - /bin/zsh
  Binaries:
    Node: 14.17.1 - /usr/local/bin/node
    Yarn: 1.22.10 - /usr/local/bin/yarn
    npm: 8.1.3 - /usr/local/bin/npm
  Browsers:
    Brave Browser: 95.1.31.91
    Chrome: 95.0.4638.69
    Firefox Developer Edition: 92.0
    Safari: 15.1
  npmPackages:
    @vue/cli-plugin-babel: ~4.5.0 => 4.5.15
    @vue/cli-plugin-eslint: ~4.5.0 => 4.5.15
    @vue/cli-plugin-router: ~4.5.0 => 4.5.15
    @vue/cli-plugin-typescript: ~4.5.0 => 4.5.15
    @vue/cli-plugin-vuex: ~4.5.0 => 4.5.15
    @vue/cli-service: ~4.5.0 => 4.5.15
    @vue/compiler-sfc: ^3.0.0 => 3.2.21
    @vue/eslint-config-typescript: ^7.0.0 => 7.0.0
    vue: ~3.2 => 3.2.21
    vue-apollo: ^3.0.8 => 3.0.8
    vue-class-component: ^8.0.0-0 => 8.0.0-rc.1
    vue-i18n: ^9.2.0-beta.17 => 9.2.0-beta.18
    vue-router: ~4.0 => 4.0.12
    vuex: ~4.0 => 4.0.2
```...

---

## Top Comments

**@kazupon** [maintainer] (+63):

Thank you for your reporting!

>You are running the esm-bundler build of vue-i18n. It is recommended to configure your bundler to explicitly replace feature flag globals with boolean literals to get proper tree-shaking in the final bundle.

The meaning of this warning message is that you need to specify the flag explicitly in the bundler when you do a production build.

Please refer to the following link for packages provided by vue-i18n for bundlers.
https://vue-i18n.intlify.dev/installation.html#with-a-bundler

...

**@hemengke1997** (+91):

in vite.config.ts, you can resolve the problem like:
```
resolve: {
  alias: [
    {
      find: 'vue-i18n',
      replacement: 'vue-i18n/dist/vue-i18n.cjs.js',
    }
  ]
}
```

**@leotaozeng** (+22):

With Vite

1. Install [@intlify/vite-plugin-vue-i18n](https://github.com/intlify/bundle-tools/tree/main/packages/vite-plugin-vue-i18n#intlifyvite-plugin-vue-i18n)
2. Configure it in `vite.config.js` or `vite.config.ts`

```js
import path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueI18n from '@intlify/vite-plugin-vue-i18n'

export default defineConfig({
  // ...
  alias: {
    'vue-i18n': 'vue-i18n/dist/vue-i18n.runtime.esm-bundler.js'
  },
  plugins: [
    vue(),
    vueI18n({
      include: path.resolve(__dirname, './path/to/src/locales/**')
    })
  ],
  // ...
})
```...