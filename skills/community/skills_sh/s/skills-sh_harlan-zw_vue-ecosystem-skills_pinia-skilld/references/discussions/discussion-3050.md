---
number: 3050
title: How to type-safely handle specific action returns in $onAction?
category: Help and Questions
created: 2025-09-29
url: "https://github.com/vuejs/pinia/discussions/3050"
upvotes: 1
comments: 1
answered: true
---

# How to type-safely handle specific action returns in $onAction?

Hey Pinia team! 

I'm wondering about a TypeScript type inference challenge with `$onAction`. 

When using something like:

```typescript  
assetStore.$onAction(({ name, after }) => {  
  after((ret) => {  
    if (name === "importAssetsFromPath") {  
      // How can I make TypeScript understand 'ret' is AssetImportResult here?  
      handleAssetsImported(ret as AssetImportResult);  
    }  
  });  
});  
```

Right now, I'm using a type assertion, but it feels a bit hacky.

Any elegant TypeScript solutions or patterns you'd recommend for this scenario?

Curious to hear your thoughts! 

---

## Accepted Answer

**@posva** [maintainer]:

Putting the `if` outside of the `after` should constrain the type as expected