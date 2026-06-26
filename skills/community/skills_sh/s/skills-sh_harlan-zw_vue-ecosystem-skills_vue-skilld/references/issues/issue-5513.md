---
number: 5513
title: Nested components in detached branch render while being detached
type: other
state: closed
created: 2022-03-03
url: "https://github.com/vuejs/core/issues/5513"
reactions: 37
comments: 7
labels: "[scope: suspense, :exclamation: p4-important]"
---

# Nested components in detached branch render while being detached

### Version
3.2.31

### Reproduction link
sfc.vuejs.org/:

Made this that could probably be a solution: https://github.com/vuejs/core/pull/6736

**@AwesomeDude091** (+18):

How likely is it that this will be fixed?

**@zkulbeda** (+1):

I checked reproduction in the description with vue v3.3.0-beta.1. I added prop `suspensible` to `<suspense>` in `ParentAsync.vue`. Still, there was two mounts of async child.
See [https://play.vuejs.org/](https://play.vuejs.org/#eNrFVllu2zAQvcpAP3ZQWXKRP8NJE+QCQRL0JyoCWaIjJhIpkJSdwPANCvQAvUjP0wv0Ch0uWu24SdEFhmFz+GbhzPANN955WQaringzby4TQUsFkqiqPI0YAC1KLhRsQGZxnvP1FVn6UAq+oimBLSwFL2CEyqMO+DIWhKnrZ5a4/SBsRdrTLvhc7qKNbAi/yGie9tGtaC+4F0cjGUKveKWI+EjJusG2okBJxOJHJZxJBULvwEknJ+MjbUtmfK2N61WkXJbGIwMf+VbNAPV3WbFEUc46WrDRG2CBwSrOK+3ltk2e3x7pk4ZudwyZPPzCksE4U+Z/bWse2vpj5XGhSFHmsSKmD+aLSin0cZbkNHk8ibw66s...