---
number: 2917
title: Asynchronous initialization and data recovery
category: Help and Questions
created: 2025-02-21
url: "https://github.com/vuejs/pinia/discussions/2917"
upvotes: 1
comments: 1
answered: true
---

# Asynchronous initialization and data recovery

What do I do to make sure that the data is properly recovered before it's served out, that is, to make sure that the init function is executed and the init function might be an asynchronous function like reading data from indexDB.

```ts
export const useUserStore = defineStore('user', {
  state: () => {
    return {
      token: null as DataWithExpires<string> | null,
     
    }
  },
  actions：{
  async init(){
                // read from indexdb 
     }
  }
}
```



It would be too inelegant to check initialization every place where you read it

---

## Accepted Answer

**@posva** [maintainer]:

Mount the app after the init is done:

```ts
const app = createApp()
app.use(pinia)
await useUserStore(pinia).init()
app.mount()
```

This can also be done within `App.vue` or with a boolean that toggles the Root `<RouterViev>`