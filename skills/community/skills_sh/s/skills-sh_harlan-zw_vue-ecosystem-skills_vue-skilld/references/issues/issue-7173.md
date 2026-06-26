---
number: 7173
title: Add option to enable Typescript by default in 
type: feature
state: open
created: 2022-11-18
url: "https://github.com/vuejs/core/issues/7173"
reactions: 38
comments: 7
labels: "[:sparkles: feature request, scope: compiler]"
---

# Add option to enable Typescript by default in 

### What problem does this feature solve?

If you have fully Typescript project it doesn't make sense to write `<script lang="ts">` all the time. It would be nice to have an option to enable Typescript by default.

### What does the proposed API look like?

```ts
compileScript(src, {
  defaultLang: 'ts'
})
```

---

## Top Comments

**@johnsoncodehk** [maintainer] (+9):

Thank you for your proposal, but I hope avoid adding this feature, I think it makes sense to add lang explicitly.

- This feature needs to be followed by all downstream tools, we should try our best to avoid this, because if some IDE can't support it, we can't control this. Volar is easy to support for IntelliSense, but Syntax Highlight is not, and VSCode doesn't actually support configurable Syntax Highlight behavior. Furthermore, the Syntax Highlight behavior needs to be implemented individually by each IDE, instead of directly taking effect in all downstream IDEs when Volar is implemented...

**@enkot** (+4):

My point in this proposal is more about cleaner component look without the repetitive lang=“ts” in each file. For sure, most of devs use snippets and this is even not a problem, it’s just “don’t repeat it” feature if you have 100% TS codebase.

**@sxzz** [maintainer]:

Yeah. Once it gets supported in Vue compiler, then ESLint, Volar, and other tools have to support this feature as well. 