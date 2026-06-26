---
number: 1033
title: Peer dependencies issue when using Pinia and nuxt3/latest (as of today)
type: other
state: closed
created: 2022-02-05
url: "https://github.com/vuejs/pinia/issues/1033"
reactions: 18
comments: 2
---

# Peer dependencies issue when using Pinia and nuxt3/latest (as of today)

### Reproduction

When trying to run through a Nuxt3 getting started guide for Pinia, I came across an error with `@pinia/nuxt`.

```
Conflicting peer dependency: vue@2.6.14
```

Full error output

...

---

## Top Comments

**@LinusBorg** [maintainer] (+1):

That's npm's issue, I'd say. Pinia has this peerDependency config:

https://github.com/vuejs/pinia/blob/d72b964e40e49d6b8a0238a03e1dd7e1b88e2119/packages/pinia/package.json?_pjax=%23js-repo-pjax-container%2C%20div%5Bitemtype%3D%22http%3A%2F%2Fschema.org%2FSoftwareSourceCode%22%5D%20main%2C%20%5Bdata-pjax-container%5D#L85

...which is totally fine. `@vue/composition-api` is an *optional* peerDependency of pinia, which I presume you didn't install. So npm should ignore the fact that that package would require Vue 2 *if it were installed, which it isn't*.

**@posva** [maintainer] (+1):

Duplicate of #853 