---
number: 14226
title: Best practise to ensure reactivity of prop values
category: Help/Questions
created: 2025-12-19
url: "https://github.com/orgs/vuejs/discussions/14226"
upvotes: 1
comments: 1
answered: true
---

# Best practise to ensure reactivity of prop values

We have a fairly large SaaS product, and it relies on a lot of `props` being used in components.

With the arrival of being able to destructure props I thought something like this would work:

```ts
const { thingId } = defineProps<{
  thingId: string
}>()

const enabled = computed (() => !!thingId)

const { data: thing, isLoading: isLoadingThing } = getThingQuery(thingId, { enabled })
```

However, it turns out that the query example won't rerun when `thingId` changes.

The way we've done this to date is:

```ts
const props = defineProps<{
  thingId: string
}>()

const thingId = computed(() => props.thingId)
const enabled = computed(() => !!thingId.value)

const { data: thing, isLoading: isLoadingThing } = getThingQuery(thingId, { enabled })
```

I've since com...

---

## Accepted Answer

When using prop destructuring for `thingId`, the compiler will rewrite uses of `thingId` to `props.thingId`. If something wouldn't work with `props.thingId` then it won't work with props destructuring either.

For example, with code like this:

```ts
getThingQuery(thingId)
```

The compiler will rewrite it to something like this:

```ts
getThingQuery(props.thingId)
```

Importantly, that is passing the current value of `props.thingId` to `getThingQuery`. If that value changes later, `getThingQuery` won't know anything about it.

As you noted, you can use `computed` to get around this problem when using `props` explicitly:

```ts
const t = computed(() => props.thingId)
getThingQuery(t)
```

That's fine, but `computed` comes with some extra internal overhead that isn't really needed for reading a single property. Using `toRef` is slightly more lightweight:

```ts
// toRef with a function, similar to `computed`
const t = toRef(() => props.thingId)
getThingQuery(t)
```...