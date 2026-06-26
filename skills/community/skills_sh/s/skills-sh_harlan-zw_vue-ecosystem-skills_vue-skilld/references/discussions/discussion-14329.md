---
number: 14329
title: About props
category: Help/Questions
created: 2026-01-17
url: "https://github.com/orgs/vuejs/discussions/14329"
upvotes: 1
comments: 2
answered: false
---

# About props

When I was learning how to use a ref object as a prop,I couldn't understand why
```js
const { foo } = defineProps(["foo"])
watch(foo,()=>{}) // Not work
watchEffect(()=>{
foo
...
}) //Work well
```
I know it will compile to
```js
const prop = defineProps(["foo"])
watch(prop.foo,()=>{}) // Not work
watchEffect(()=>{
prop.foo
...
}) //Work well
```
But I can't understand why prop.foo can't detected by watch()
AI told me it will auto unpack ref data,so prop.foo is just normal object
But I have learnt watchEffect() detect releative data by call it's getter or setter,if prop.foo is just normal object,it doesn't have getter or setter,so what causes this

Because it's difficult to read all source code about this part for me,so I came to there for help
Thanks

---

## Top Comments

**@skirtles-code** (+1):

Props destructuring is a distraction here. You're essentially correct, that it compiles `watch(foo, ...` to `watch(props.foo, ...`, so the real question is why doesn't `watch(props.foo, ...` do what you want?

To be a bit more explicit, consider this code:

```js
const props = defineProps(['foo'])

watch(props.foo, () => {
  console.log('changed')
})
```

As you noted, this won't work. Here's a Playground showing that:

- [Playground](https://play.vuejs.org/#eNqFUstu2zAQ/JUFL1IQQ0LRngzZaBvk0AJtgz5OZQ8qtZKZUCRBUo4LQf/eJRU5ThA4N+3O7HBWOyP7YG2xH5CtWeWFkzaAxzDYLdeyt8YFGMFhCxO0zvSQETU...

**@ismaildasci**:

Hey, I had the same confusion before so let me explain what I learned.

When you destructure props like this:
```js
const { foo } = defineProps(["foo"])
```

you basically extract the value at that moment. Its not reactive anymore, just a plain value. Thats why watch() cant detect changes.

But watchEffect works different - it tracks whatever you access inside it while running. So when you use `foo` inside watchEffect, Vue still catches it.

**What you can do:**

Use getter function in watch:
```js
const { foo } = defineProps(["foo"])
watch(() => foo, (newVal) => {
  console.log(newVal)
})
```...