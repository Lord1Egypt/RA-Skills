---
number: 3030
title: Cannot handle Promise Like type in $onAction callback
category: Help and Questions
created: 2025-09-02
url: "https://github.com/vuejs/pinia/discussions/3030"
upvotes: 1
comments: 1
answered: true
---

# Cannot handle Promise Like type in $onAction callback

when I use $onAction to add after action callback, which is using promise like, it doesn‘t work
 Example:
App.vue
<img width="433" height="188" alt="app" src="https://github.com/user-attachments/assets/fecb5ee1-f6ee-450f-b062-858000653ade" />

useTestStore.js
<img width="776" height="781" alt="useStore" src="https://github.com/user-attachments/assets/73ece5b3-f9e4-4fe4-9a52-977ea0fb971f" />



maybe we can determine whether it is a Promise Like type,like use tool function
`
function isPromiseLike (val) {
  return val && typeof val.then === 'function'
}
`
to replace the following judgement
`
     // if (isPromiseLike(ret))
      if (ret instanceof Promise) { 
        return ret
          .then((value) => {
            triggerSubscriptions(afterCallbackSet, value)
    ...

---

## Accepted Answer

**@posva** [maintainer]:

My guess is that MyPromise is not properly extending the Promise class 