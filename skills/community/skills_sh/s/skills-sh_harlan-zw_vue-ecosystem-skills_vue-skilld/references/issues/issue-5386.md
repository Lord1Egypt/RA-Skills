---
number: 5386
title: Kept alive components still update (renders, watchers) while being deactivated
type: bug
state: open
created: 2022-02-09
url: "https://github.com/vuejs/core/issues/5386"
reactions: 13
comments: 12
labels: "[:lady_beetle:  bug, need guidance, scope: keep-alive]"
---

# Kept alive components still update (renders, watchers) while being deactivated

### Version
3.2.30

### Reproduction link
sfc.vuejs.org/







### Steps to reproduce
- Click increment
- Click change page
- Click increment
- Observe the logs

### What is expected?
-...