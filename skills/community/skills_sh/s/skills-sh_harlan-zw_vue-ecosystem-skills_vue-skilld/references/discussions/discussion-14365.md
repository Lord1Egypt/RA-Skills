---
number: 14365
title: attributes that are not defined as props are not converted from camelCase to kebap-case
category: Help/Questions
created: 2026-01-27
url: "https://github.com/orgs/vuejs/discussions/14365"
upvotes: 3
comments: 1
answered: false
---

# attributes that are not defined as props are not converted from camelCase to kebap-case

I came across this today and wonder if this is really intended.
Every attribute name that is not defined as prop is just converted to lowercase when applied to the component.
So things like `ariaControls` become `ariacontrols` instead of `aria-controls`

However this does not happen, if the attrubute falls through and hits another component that does define it as prop. I guess this happens because setAttribute ultimately just lowercases the attribute when it hits an html element but otherwise just passes it though as i.

So here are some examples: 

```html

<button dataTestid="foo" />
```

However, when we define it as prop it obviosuly is passed correctly because vue converts forth and back:

```ts
defineProps<{dataTestid: string}>()
```...

---

## Top Comments

**@sunnypatell**:

@Fuzzyma this is a real bug in how `<slot>` attributes interact with `v-bind` on HTML elements.

the root cause is in [`packages/compiler-core/src/transforms/transformSlotOutlet.ts`](https://github.com/vuejs/core/blob/main/packages/compiler-core/src/transforms/transformSlotOutlet.ts). when processing `<slot>` attributes, Vue's compiler explicitly camelizes every attribute name:

```ts
p.name = camelize(p.name)
```

so `data-testid` becomes `dataTestid` and `aria-controls` becomes `ariaControls` in the scope object.

...