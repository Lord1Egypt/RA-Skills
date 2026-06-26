---
number: 2962
title: "rstore + Pinia lead to Error: obj.hasOwnProperty is not a function ⁃ at shouldHydrate"
category: Help and Questions
created: 2025-04-02
url: "https://github.com/vuejs/pinia/discussions/2962"
upvotes: 1
comments: 2
answered: true
---

# rstore + Pinia lead to Error: obj.hasOwnProperty is not a function ⁃ at shouldHydrate

### Reproduction

https://codesandbox.io/p/github/gabrielstuff/rstore-pinia-demo/main?import=true

### Steps to reproduce the bug

First, thanks for all the work on Pinia.
The issue I face is as follow : 
- i'm using rstore to call and manage api call
- i'm willing to use Pinia to manage state for other use.

I'm using the following in my rstore : 

```
const headers = useRequestHeaders(['cookie'])
const { data: todos, error, loading, refresh } = await store.todo.queryMany({
  fetchOptions: {
    headers
  }
})
```

which looks like working perfectly. In a real life example the rstore is making authenticated call with an API.

Without Pinia everything is going fine. As soon as I add Pinia the following errors rised up :

...

---

## Accepted Answer

**@posva** [maintainer]:

Fixed in fd6d969