---
number: 5844
title: `<Suspense>` + `<Transition>` means mounted() runs too early
type: bug
state: closed
created: 2022-05-01
url: "https://github.com/vuejs/core/issues/5844"
reactions: 50
comments: 8
labels: "[:lady_beetle:  bug, scope: transition, scope: suspense, :exclamation: p4-important]"
---

# `<Suspense>` + `<Transition>` means mounted() runs too early

### Version
3.2.33

### Reproduction link
- stackblitz.com
- SFC Playground






### Steps to reproduce
Click the Toggle component button in the reproduction, and observe that a template ref is null rather than defined.

### What is expected?
I expect the behaviour with suspense to be the same as the behaviour without suspense.

### What is actually happening?
`<Suspense>` means that the mounted() hook runs before the elements are present in the DOM.



---

## Top Comments

**@pikax** [maintainer] (+16):

Just to give an update on this, I've created a PR https://github.com/vuejs/core/pull/9388 aimed to fix this

https://github.com/vuejs/core/assets/4620458/6f81918c-f4ab-407e-be33-ec818fd96aad

It's working, but since this is touching Suspense, I would expect more scrutiny while reviewing, because it can be very easy for this PR break things downstream.

**@richgcook** (+21):

It's causing a lot of issues and having to rely on a timeout, which is irregular, is too costly.

**@Triloworld** (+16):

Confirm as comment: https://github.com/vuejs/core/pull/5952#issuecomment-1523358427
Is deal breaker . We entirely disable animation and this stop people from migration to new version of framework - it is disabled by this issue on main repo from 3.0.0-rc.13 onwards by default (https://github.com/nuxt/nuxt/releases/tag/v3.0.0-rc.13 and https://github.com/nuxt/framework/pull/8436). Waiting now whole year for pr to be merge.
Right now there is 43 other issues related to page transition feature: https://github.com/nuxt/nuxt/issues?q=is%3Aissue+is%3Aopen+transition
Whole transition feature on nux...