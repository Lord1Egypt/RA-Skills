---
number: 14156
title: How can I speed up TypeScript checking in Vue projects?
category: Help/Questions
created: 2025-12-01
url: "https://github.com/orgs/vuejs/discussions/14156"
upvotes: 2
comments: 2
answered: false
---

# How can I speed up TypeScript checking in Vue projects?

Guys, could you give me some advice?

How can I speed up TypeScript checking in Vue projects?

tsc can run selectively for a file:
npx tsc --noEmit --skipLibCheck FILE_PATH

but vue-tsc doesn’t seem to allow this.

They promise to speed up the checks with Go in the future, but as far as I know it’s still in beta.

---

## Top Comments

**@panstromek**:

It helps to keep as much code as you can out of Vue files, big Vue files seems to be pretty costly for `vue-tsc` to process. It also helps to use explicit type annotations on Vue-related things, especially if they require complicated type inference to resolve (e.g. if it involves UnwrapRef or component types). This helps if the type annotation is simpler than the type that is assigned to it and it's used in more places.

**@Shyam-Chen**:

Ref: https://devblogs.microsoft.com/typescript/progress-on-typescript-7-december-2025/