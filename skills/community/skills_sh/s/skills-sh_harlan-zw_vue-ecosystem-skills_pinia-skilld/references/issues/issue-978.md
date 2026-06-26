---
number: 978
title: Setup store - A more comprehensive example
type: other
state: closed
created: 2022-01-21
url: "https://github.com/vuejs/pinia/issues/978"
reactions: 17
comments: 9
---

# Setup store - A more comprehensive example

I think that the setup way of building a store will be the future. I would love to shift towards that in the docs.

### Currently in the docs

https://pinia.vuejs.org/introduction.html#basic-example

```js
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  function increment() {
    count.value++
  }

  return { count, increment }
})
```

### Comprehensive example

```js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useStoreCounter = defineStore('counter', () => {
  // STATES
  const count = ref(0)

  // GETTERS
  const isEven = computed(() => {
    return count.value % 2 === 0
  })

  const messageIfEven = computed(() => {
    return (message) => {
      if (!isEven.value) return
      return message
    }
  })

  // ACTIONS
  function increment() {
    count.value++
  }

  return { count, isEven, messageIfEven, increment }
})
```

#### Notes

- I think not everyone will remember the syntax for the imports so I added them.
- I also added comments to make it really clear what is states, getters and actions.
- `isEven` is a getter without arguments which works similar to a value.
- `messageIfEven(message)` which works more like a method. It takes an argument and also uses the other getter `isEven`.
- In the future we can get rid of `.value` after values and computed properties by using `$ref()`, but now we still has to deal with `ref()`.

I hope this can help someone.

---

## Top Comments

**@jaybo** (+6):

Is there any way to avoid re-enumerating all of the states, getters, and actions in the return, (or at least automate the entries)?

```return { count, isEven, messageIfEven, increment }```

**@posva** [maintainer] (+1):

Thanks for the code sample! I added it to the docs roadmap

**@posva** [maintainer]:

not possible.