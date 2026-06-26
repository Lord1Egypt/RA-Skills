---
number: 1080
title: Implement nuxtServerInit Action to load data from server-side on the initial load
type: feature
state: open
created: 2022-02-18
url: "https://github.com/vuejs/pinia/issues/1080"
reactions: 27
comments: 10
labels: "[contribution welcome, feature request,   pkg:nuxt]"
---

# Implement nuxtServerInit Action to load data from server-side on the initial load

### What problem is this solving

Implement something like NuxtServerInit Action, so we can load data from the server-side and give it directly to the client-side on the initial load/render.

### Proposed solution

Include an `index.js` file inside `/stores` with a `nuxtServerInit` action which will be called from the server-side on the initial load.

### Describe alternatives you've considered

The only way I found to do this is using Pinia with Vuex, using the `nuxtServerInit` from Vuex:

```
// store/index.js
import { useSessionStore } from '~/stores/session'

export const actions = {
  async nuxtServerInit ({ dispatch }, { req, redirect, $pinia }) {
    if (!req.url.includes('/auth/')) {
      const store = useSessionStore($pinia)

      try {
        await store.me() // load user information from the server-side before rendering on client-side
      } catch (e) {
        redirect('/auth/login') // redirects to login if user is not logged in
      }
    }
  }
}
```


---

## Top Comments

**@nestle49** (+3):

This solution is workaround for me:

**nuxt.config.ts**


```
plugins: [
   { src: '~/plugins/init.server.ts' }, // must be the first server plugin
 ]
```


**plugins/init.server.ts**

```
import { useGlobalStateStore } from '~/store/globalState';

const initServer: () => void = async () => {
    // example code
    const host = req.hostname;
    const globalStateStore = useGlobalStateStore();
    globalStateStore.SET_HOST({ host });
};

export default initServer;
```



**@posva** [maintainer] (+1):

There should be a way to add this for both setup and option stores. Maybe a specific name for an action is enough.

One important thing to note is that given the nature of stores in pinia, **you need explicitly say somewhere in your server code** which stores must run this action as they need to be instantiated on the server. By default, if no store is ever user, no store is ever instantiated and therefore no server init function can run.

**@AustinMusiku** (+2):

> ### What problem is this solving
> Implement something like NuxtServerInit Action, so we can load data from the server-side and give it directly to the client-side on the initial load/render.
> 
> ### Proposed solution
> Include an `index.js` file inside `/stores` with a `nuxtServerInit` action which will be called from the server-side on the initial load.
> 
> ### Describe alternatives you've considered
> The only way I found to do this is using Pinia with Vuex, using the `nuxtServerInit` from Vuex:
> 
...