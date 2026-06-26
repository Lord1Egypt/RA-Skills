---
number: 14254
title: How to correctly type the native popover API when `strictTemplates` is enabled?
category: Help/Questions
created: 2025-12-26
url: "https://github.com/orgs/vuejs/discussions/14254"
upvotes: 1
comments: 1
answered: false
---

# How to correctly type the native popover API when `strictTemplates` is enabled?

The Popover API is already included in the 2024 browser baseline, so why doesn't Vue include definitions for these APIs?
<img width="1251" height="579" alt="image" src="https://github.com/user-attachments/assets/1325ea9a-cb1c-4a28-baad-29fd5751c944" />

I don't like this:
```ts
declare module "vue" {
  export interface HTMLAttributes {
    popover?: "auto" | "manual" | "" | boolean;
    popovertarget?: string;
    popovertargetaction?: "toggle" | "show" | "hide";
  }
}
```

---

## Top Comments

**@rzzf** (+1):

I’ve submitted a pull request. Let’s wait for the official review.