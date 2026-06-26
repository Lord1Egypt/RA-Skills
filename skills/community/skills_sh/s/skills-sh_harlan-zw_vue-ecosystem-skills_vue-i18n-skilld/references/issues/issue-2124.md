---
number: 2124
title: Cannot find module '@intlify/devtools-types' or its corresponding type declarations.
type: other
state: open
created: 2025-02-27
url: "https://github.com/intlify/vue-i18n/issues/2124"
reactions: 5
comments: 0
labels: "[Status: Review Needed]"
---

# Cannot find module '@intlify/devtools-types' or its corresponding type declarations.

### Reporting a bug?

I have switched an existing project to typescript (first time using typescript) and to debug something else I used vue-tsc on the project. I did not know about skipLibCheck so so I checked everything for type errors and I actually got errors in your files that I thought I would report. Actually installing `@intlify/devtools-types` (or just using skipLibCheck..., I found out about that while I war writing this issue) fixes the errors so I think you did not put it as a dependency (most likely because it just contains types). This is obviously not a huge issue, but I think it might be something you have not been aware of, so here is the report. 

...