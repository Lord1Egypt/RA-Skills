---
number: 675
title: Can't import the named export from non EcmaScript module (only default export is available)
type: bug
state: closed
created: 2021-09-14
url: "https://github.com/vuejs/pinia/issues/675"
reactions: 17
comments: 17
labels: "[bug, has workaround]"
---

# Can't import the named export from non EcmaScript module (only default export is available)

### Steps to reproduce the behavior

1. Use Vue-cli to create a Vue 3 app with Typescript.
2. Run `yarn add pinia@next`.
3. Edit the `main.ts`:

```
import { createApp } from "vue";
import App from "./App.vue";
import { createPinia } from "pinia";

const app = createApp(App);
app.use(createPinia());
app.mount("#app");
```
4. Run `yarn serve`.

### Expected behavior

The compilation goes without an error

### Actual behavior

Throws error:

...

---

## Top Comments

**@jhony-v** (+158):

I had the same problem  but I solved editing my **vue.config.js** file with the following webpack rule:

```javascript
// vue.config.js
module.exports = {
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.mjs$/,
          include: /node_modules/,
          type: "javascript/auto"
        }
      ] 
    }
  }
}
```

With this configuration it worked.

**@4Kazelot** (+74):

> I had the same problem but I solved editing my **vue.config.js** file with the following webpack rule:
> 
> ```js
> // vue.config.js
> module.exports = {
>   configureWebpack: {
>     module: {
>       rules: [
>         {
>           test: /\.mjs$/,
>           include: /node_modules/,
>           type: "javascript/auto"
>         }
>       ] 
>     }
>   }
> }
> ```
> 
> With this configuration it worked.

For NuxtJS:
```
export default {
  build: {
    extend(config) {
      config.module.rules.push({
        test: /\.mjs$/,
        include: /node_modules/,
        type: 'javascript/auto',
      })
    },
  },
}
```...

**@timpulver** (+18):

Here is the chained Webpack config if someone else needs it:

_vue.config.js:_
```
/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */
module.exports = {
  chainWebpack: (config) => {
    config.module
      .rule("mjs")
      .test(/\.mjs$/)
      .type("javascript/auto")
      .include.add(/node_modules/)
      .end();
  },
};

```