---
number: 1630
title: "Possible edge case in devtools integration: Cannot read properties of null (reading '__VUE_DEVTOOLS_APP_RECORD_ID__')"
type: other
state: closed
created: 2022-09-06
url: "https://github.com/vuejs/pinia/issues/1630"
reactions: 15
comments: 9
labels: "[contribution welcome, vue 2.x,  pkg:devtools]"
---

# Possible edge case in devtools integration: Cannot read properties of null (reading '__VUE_DEVTOOLS_APP_RECORD_ID__')

### Reproduction

https://github.com/basuneko/pinia-devtools-issue

### Steps to reproduce the bug

1. Checkout the reproduction repo and run `npm run serve`
2. Open a new tab and devtools
3. Open the reproduction app - you should see the default vue cli homepage
4. Wait ~60 seconds for the devtools timeout

### Expected behavior

* 'bacon' and 'yolo' stores are listed in the pinia devtools tab and can be inspected
* the console shows pinia initialisation messages
  ```
    🍍 bacon store added
    🍍 yolo store added
  ```
* No errors are raised in the console; 

### Actual behavior

 Both 'bacon' and 'yolo' stores are indeed listed in the pinia devtools tab

 However, instead of the  messages, after a timeout, devtools spits out a bunch of errors

<img width="639" alt="Screen Shot 2022-09-06 at 5 31 46 PM" src="https://user-images.githubusercontent.com/505411/188554365-2cd669d1-3a5c-4f6e-acf5-c00ea60a4ec1.png">

```
* Error: Timed out getting app record for app at backend.js:1160:14
* [Hook] Error in async event handler for devtools-plugin:setup with args:
* TypeError: Cannot read properties of null (reading '__VUE_DEVTOOLS_APP_RECORD_ID__') at getAppRecordId (backend.js:1103:11)
```

### Additional information

...

---

## Top Comments

**@posva** [maintainer] (+8):

~~I cannot reproduce but the error comes from the devtools anyway. Make sure you have the latest devtools version installed and not the beta.~~ I managed to reproduce it.

As a side note, I discourage you from doing this:

```js
const useUserStore = defineStore('user', { ... })

export const userStore = useUserStore(pinia) 
```

Instead, use the patterns shown in docs with `setup()` or with `mapStores()` (& co). It's important the `useStore(pinia)` are called after `new Vue()`. If anybody wan...

**@jorismak** (+8):

I'm a bit confused by this.

But how do we set the state on the store to some initial stuff (like from an API) before 'loading the app' (doing the very first new Vue()).

In my code I have this:

```
Vue.use(PiniaVuePlugin);
const pinia = createPinia();

const mainStore = useMainStore(pinia);

mainStore.refreshUser().finally(() => {
    new Vue({
        router,
        vuetify,
        pinia,
        render: (h) => h(App),
    }).$mount("#app");
});
```

To make an axios call to see if we are logged in or not, and store that in the store, and only then load up the very f...

**@lee1nna** (+6):

I'm having the same problem, is there a solution? 