---
number: 58
title: Add an option to disallow direct state modification from component
type: feature
state: open
created: 2020-01-21
url: "https://github.com/vuejs/pinia/issues/58"
reactions: 70
comments: 28
labels: "[discussion, feature request, plugins]"
---

# Add an option to disallow direct state modification from component

In the example, I kind of dislike the fact that the component can directly call `cart.state.rawItems = [];`. Just because I think that can encourage people to modify state in a disorganized manner. Can we get a plugin setting that disallows state being modified from the component (rather than an explicit action)?

---

## Top Comments

**@posva** [maintainer] (+77):

I think disallowing direct state modification is a rule that should be enforced at a linter level instead because runtime-wise this would only be a dev-only warning, so it would be slower during dev and require more code in the library

Being able to directly modify the state (or using `patch`) is intentional **to lower the entry barrier and _scale down_**. After many years using Vuex, **most mutations were completely unnecessary** as they were merely doing a single operation via an assignment (`=`) or collection methods like `push`. They were **always perceived as verbose**, no matter the s...

**@sisou** (+13):

Vue 3 includes a `readonly()` method that makes anything passed into it read-only. This could be used for the exported state, which would show an error with Typescript and log an error/stop mutations during runtime.

Futhermore, Typescript has a `Readonly<>` type modifier that can be used for Typescript errors already in Vue 2.

Would you consider using either of those?

**@Aaron-Pool** (+25):

@posva just to clarify, I wasn't requesting to disallow direct state mutation in _actions_. I was only requesting to disallow direct state mutation from _component methods_. I agree that mutations feel like overkill, and I'm happy to see the concept of mutations is absent from pinia. I do, however, think that only being allowed to modify state through actions encourages a concise, and thought-through API for state management and modification. It also creates an incentive to only put state in vuex that really _needs_ to be there, and use component local state for everything else, rather than th...