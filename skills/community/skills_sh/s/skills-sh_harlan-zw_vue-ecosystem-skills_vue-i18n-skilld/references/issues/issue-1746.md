---
number: 1746
title: Usage of `n()` and `$n()` with `undefined` should not throw errors
type: feature
state: open
created: 2024-02-23
url: "https://github.com/intlify/vue-i18n/issues/1746"
reactions: 10
comments: 6
labels: "[Status: Proposal]"
---

# Usage of `n()` and `$n()` with `undefined` should not throw errors

### Clear and concise description of the problem

Sometimes values are undefined within an application, unfortunately this will throw a 500 error (at least in Nuxt) so the whole page is unavailable just because one variable is undefined:

```
<script setup lang="ts">
const props = defineProps<{price: number}>();
</script>

<template>
{{ $n(props.price, 'currency') }}
</template>
```

Another example are inputs:
```
<script setup lang="ts">
const price = ref(10);
</script>

<template>
<input v-model="price" type="number">
{{ $n(price, 'currency') }}
</template>
```

 These can get undefined while the user is editing the input value which will also throw errors:

> Incaught (in promise) SyntaxError: Invalid arguments (at message-compiler.mjs:77:19)

### Suggested solution

It would be great if the function `n()` and `$n()` would instead just return an empty string `''` without the whole page crashing or throwing any errors.

### Alternative

_No response_

### Additional context

_No response_

### Validations

- [X] Read the Contributing Guidelines
- [X] Read the Documentation
- [X] Check that there isn't already an issue that request the same feature to avoid creating a duplicate.

---

## Top Comments

**@KaelWD** (+8):

Also #1155

These strict runtime checks are incredibly inconvenient, I don't understand why you need to throw an error (often breaking the entire page) when just passing through null values and casting numbers to strings automatically would at worst display some mildly confusing strings to users and at best cause no problems because we have null checks *after* $t().

**@kazupon** [maintainer]:

Thank you for your feedback!

The first argument of `n` and `$n` must be `number`.
Don't pass `undefined`.
It is the responsibility of the application to verify the value passed.

However, vue-i18n API documentation does not mention that an error is raised if an unexpected value is specified.
https://vue-i18n.intlify.dev/api/composition.html#composernumberformatting

I think it would help to mention it in the documentation.


**@MickL** (+2):

Can we please allow `n()` and `$n()` to have undefined values? Consider the second example from above:

- The first example above will break the full page
- The second example above will throw errors because price is becoming an empty string when the input is empty