---
number: 829
title: Docs Roadmap
type: docs
state: open
created: 2021-11-24
url: "https://github.com/vuejs/pinia/issues/829"
reactions: 19
comments: 31
labels: "[ docs]"
---

# Docs Roadmap

These are the documentation sections I want to add or improve

- [ ] Migrate to Vue.js theme
  - [x] Use a neutral font (#873)
  - [ ] Adapt instructions for Vue 2.7
- Cookbook
  - Testing
    - [x] Initializing the store before
    - [ ] What is needed for Nuxt (maybe link to another page) (#910)
    - [ ] Document action usage within setup stores cannot be stubbed https://github.com/vuejs/pinia/issues/2291
  - [x] Advanced reactivity
  	- Show how to use composables inside option and setup stores
  - [ ] Spltting the store into multiple files (#802) 
  - [ ] Allowing making a Store implement an interface (state, actions, or/and getters)
  - [ ] Advanced SSR
    - [ ] Hydrating differing state like `useLocalStorage()`
    - [x] Differences between Setup and Option stores
    - [ ] Using stores before hydration https://github.com/vuejs/pinia/discussions/948
  - [ ] Handling Errors with API calls 
  - [ ] CDN installation for Vue 2 and Vue 3 #1051
- [ ] State must be defined as a whole #1335 
- [x] Setup Stores (https://github.com/vuejs/pinia/issues/978)
	- Currently only Option stores are documented properly. It would be nice to have a switch somewhere or to mention them early on and link to a cookbook entry about advanced reactivity as these stores allow patterns that are impossible (or not intuitive) to achieve with the options API, like `watching`
- [ ] Being able to switch between syntaxes (option / setup store) (TBD if worth) https://github.com/vuejs/pinia/issues/1265
- [x] Reorganize the What is Pinia and Getting Started sections so the latter shows complete examples (#1195)
- [ ] Add note about `patch` modifying in place objects #1921 


If you have suggestions about common use cases that are not covered or improvement / refactoring for the existing docs, please share

## How to contribute

If you want to contribute to the docs, make sure first **there is no active Pull Request** or **an existing branch on this repository**. Fo...

---

## Top Comments

**@posva** [maintainer] (+3):

@Jamiewarb I added an item to the list and updated the issue about how to contribute. Let me know if it's missing anything!
I'm really keen on having cookbook entries contributed  

**@tobiasdiez** (+3):

What I'm currently missing from the docs (also from the vuex ones) are some general guidelines and best practices to work with a store. Questions that would be nice to answer in this context:
- For what kind of 'state' do you want to use a store over say component-wise reactive variables
- How much logic do you put in the actions of the store vs in composables that use the store (e.g. should a `login` action only set `isLoggedIn` and `currentUser` or should it also call the API to fetch the new user config [which would be handled in a different store] and do some general logging for stats et...

**@BenShelton** (+2):

> I would assume that any modification of the store would result in re-rendering of all components subscribed to the store through mapStores

I don't think this is correct. If you had a "global" `reactive` object and imported it into multiple components, it would only trigger a render if part of that object is tracked and that specifically is changed. For example if in one component you access `globalObj.prop1` within the template or in a computed etc. the render will only trigger if you changed the `prop1` property on that object, whether it be within the component or elsewhere. That's the ...