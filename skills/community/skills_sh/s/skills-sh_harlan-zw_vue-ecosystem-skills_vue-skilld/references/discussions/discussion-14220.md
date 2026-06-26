---
number: 14220
title: Correct way of extending tsconfig lib in a vue project
category: Help/Questions
created: 2025-12-17
url: "https://github.com/orgs/vuejs/discussions/14220"
upvotes: 1
comments: 1
answered: true
---

# Correct way of extending tsconfig lib in a vue project

My question is kind of related to this topic: https://github.com/orgs/vuejs/discussions/13583
On a fresh vue installation with typescript, a `tsconfig.app.json` will be created, that extends https://github.com/vuejs/tsconfig/blob/main/tsconfig.dom.json. 
The `tsconfig.dom.json` says: 

```json
  // Target ES2020 to align with Vite.
  // <https://vite.dev/config/build-options.html#build-target>
  // Support for newer versions of language built-ins are
  // left for the users to include, because that would require:
  //   - either the project doesn't need to support older versions of browsers;
  //   - or the project has properly included the necessary polyfills.
 ```
 So Baseline availabe features like `Object.groupBy` are unknown to typescript.
 As far as I understand, I would...

---

## Accepted Answer

Yeah unfortunately thats how TypeScript works - the `lib` array doesnt merge, it completely overrides.

Your approach is correct but theres a cleaner way. Instead of manually listing all libs, you can check what the base config includes and just add what you need:

```json
{
  "extends": "@vue/tsconfig/tsconfig.dom.json",
  "compilerOptions": {
    "lib": ["ES2020", "DOM", "DOM.Iterable", "ESNext.Object"]
  }
}
```

For `Object.groupBy` specifically, you need `ESNext` or `ES2024` in your lib:

```json
{
  "compilerOptions": {
    "lib": ["ES2020", "DOM", "DOM.Iterable", "ESNext"]
  }
}
```

Or if you only want `Object.groupBy` without all ESNext stuff:

```json
{
  "compilerOptions": {
    "lib": ["ES2020", "DOM", "DOM.Iterable", "ES2024"]
  }
}
```

The thing is - when base tsconfig updates, you would need to update yours too. Theres no automatic merge unfortunately. 

One workaround some people use is to not extend for compilerOptions and just copy ...