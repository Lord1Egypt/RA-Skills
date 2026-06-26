---
number: 7312
title: v-bind style not working in some edge cases (teleport + transition, slots)
type: bug
state: open
created: 2022-12-09
url: "https://github.com/vuejs/core/issues/7312"
reactions: 7
comments: 14
labels: "[:lady_beetle:  bug, scope: teleport, has workaround]"
---

# v-bind style not working in some edge cases (teleport + transition, slots)

### Vue version

3.2.45

### Link to minimal reproduction

https://sfc.vuejs.org/#eNqdVM1uozAQfpVZX9JKAe7ZNNo97HX3sL1U4kJgkrgF2xoPSaso796xoYQ2KFV7Qcx4vp/5kDmq386l+xbVQi0ZG1cXjKvcACzXLbM18Kusdfl0lyu/s4f7nTZbuIMfQ5Gr1b3dbmsEDuUy62A9BWWr+AhV7FR6D2VdeC+EjM8s8NAHMBaYCuM1a2vmscQanSWOuEyAZ5bzZI+e4IV9ojdj24MUwMOf/+/U/v57pzbWW2YfxHKTsyTVTQNbkVjb6mVg/44VrANZ52NQm3DSqw5BfOrlIqgv+7sMq3c8SmvsciKxS+OfJ3i2O7HCN5a4vgYkcNC8AyGiAgL3gQrnkEaKow0ndrz6oUJjuFlS+pK0Y/DIrZOObqKHIxBu4AQbsg3M5ErOOnRpjWcobW1Jbp7M3MwIq9nt28n4XoZTphZvfwbVTqfX5Jc6yKchLTgG6ki5kNzW2lQ3sQq4U4TGcTVXnbmkKVz66K2R30TE5v2Bz9WiYws9MR3qXO2YnV9kmd+U4efy6FNL20zeUmoN6wZT9E2yJnvwSEKcq/mII5PmHikhNBWSfIUrnB9GL3gDrWx0UqdXm5CifQ==

### Steps to reproduce

click the toggle button off and on

### What is expected?

all text should be red

### What is actually happening?

using v-bind inside of a teleport inside of a transition fails. It does actually work if there is an extra div wrapper around the transition. However in a case where a v-if transition is being triggered because the parent component has been unmounted, this will not work.

### System Info

_No response_

### Any additional comments?

see https://github.com/vuejs/core/issues/4605 and https://github.com/vuejs/core/commit/42239cf2846f50b6ac2c060dad381113840d9ea1

-------
**For anyone encountering this bug in the meantime**

a workaround is to inject your own css var with [@vueuse/head]. In my case there was only one of the component at a time, but y...