---
number: 14241
title: The Naming Conventions OF Vue File
category: General Discussions
created: 2025-12-24
url: "https://github.com/orgs/vuejs/discussions/14241"
upvotes: 2
comments: 1
answered: false
---

# The Naming Conventions OF Vue File

In a Vue 3 scaffolding project, I noticed that the file naming convention uses Pascal Case (e.g., HelloWorld.vue). Within the file, you can specify a name attribute to define the component name. This allows the name attribute to be different from the file name. The only reason we found for this was that third-party component checks require component names to have more than one word, which could be achieved by changing the name field. However, this makes code maintenance confusing, as the component name may not correspond to the file name. We prefer to change the file name to meet the requirements.

In other files, we use components in the same way as the file name, e.g., <HelloWorld></HelloWorld>. I thought that by adhering to this convention, my project would look consistent. However, w...

---

## Top Comments

**@ismaildasci**:

Hey, totally get the frustration here - the naming convention situation can feel messy at first, but there is actually a consistent approach that works well.

**The Vue Style Guide recommendation:**

PascalCase for both file names AND template usage is the preferred convention. So `HelloWorld.vue` as the file name and `<HelloWorld />` in your templates. This is what the Vue Style Guide recommends as "strongly recommended".

**Why this works best:**

...