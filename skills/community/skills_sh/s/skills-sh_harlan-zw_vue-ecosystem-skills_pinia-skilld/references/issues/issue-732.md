---
number: 732
title: Pinia Devtools Wishlist
type: other
state: open
created: 2021-10-20
url: "https://github.com/vuejs/pinia/issues/732"
reactions: 19
comments: 23
labels: "[contribution welcome, discussion]"
---

# Pinia Devtools Wishlist

I think it would be nice to gather feedback about how to improve the existing devtools or reporting bugs.

If you find something that you think can be improved, a screenshot is usually enough to help describe the improvement. I want to use this issue to track those improvements.

- [x] Display all getters in the Inspector View ( Pinia (root))
- [x] Allow calling `$reset()` directly from the devtools (Using actions + adding this in `formatStoreForInspectorState()`. This should only appear in the inspector view, next to the _state_ property.
- [x] Add a settings panel (https://devtools.vuejs.org/plugin/plugins-guide.html#plugin-settings)
	- [ ] Use emojis in messages (defaults to true)
	- [x] Disable "x store installed" message https://github.com/vuejs/pinia/discussions/1070
	- [x] ~~Show stores in components (defaults to true)~~ This can be set already in plugin settings
- [ ] Time travelling
	- [ ] Changing the current state from the timeline (should not add new events)
	- [ ] Use a patch-driven approach like in Vue Devtools for perf reasons
- [ ] Clear ans concise information about single mutations
- [x] Allow prod devtools (with less information because events might not be there)
- [ ] Clicking on a store in pinia devtools should make it available as a global variable
- [ ] Add component originator of an action

**Please do not use the issue to report bugs**, use the Discussions for help or open an issue with a boiled down reproduction for bugs.

---

## Top Comments

**@j4k0xb** (+1):

Editing some state (e.g. the percent) using `Pinia (root)` leads to an error:


And it would also be nice if the root overview shows getters etc instead of only the store's state

**@izerozlu** (+1):

I'm having a somewhat weird bug. If I do initiate a store from my Vue3 application's `main.ts` file, `Pinia` instance does not get bound to devtools. Therefore cannot inspect the store whatsoever.

```
const app = createApp(App);
app.use(createPinia());
app.mount("#app");

if (user) {
  const rootStore = useRootStore();
  rootStore.setUser(user);
}
```

This is what I'm doing basically.

**PS:** Store gets initialized without a problem. Can observe the state of `rootStore`.

Devtools version: `6.0.0.20`
Vue version: `3.2.16`
Pinia version: `2.0.4`

**@posva** [maintainer]:

I fixed the error when changing from the root store. Having all the getters would be nice!

@DannyFeliz That should be doable with https://devtools.vuejs.org/plugin/api-reference.html#on-inspectcomponent