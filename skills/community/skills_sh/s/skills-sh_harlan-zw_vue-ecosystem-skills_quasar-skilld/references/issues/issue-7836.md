---
number: 7836
title: Quasar v2 (Vue 3) - released!
type: other
state: closed
created: 2020-09-29
url: "https://github.com/quasarframework/quasar/issues/7836"
reactions: 272
comments: 178
labels: "[announcement :rocket:]"
---

# Quasar v2 (Vue 3) - released!

**Quasar v2 is out!** Read our announcement.

## Is v2 stable?

**YES**

## The plan

Our main focus at the moment is shipping Quasar v2 with Vue v3.
The plan is to **not introduce any breaking changes**, unless forced by the vue 3 / vue-router 4 architectures.

Affected Quasar packages: "quasar", "@quasar/app".

## Rough schedule

* First beta: "quasar" v2.0.0-beta.1 & "@quasar/app" v3.0.0-beta.1 - **Jan 2021**
* Stable releases: "quasar" v2.0.0 & "@quasar/app" v3.0.0 - **Q2 2021**

## The code

The branch currently holding Quasar v2 is called dev (was previously `vue3-work`).

## Donations

If you want to speed up the development of Quasar please consider donating to the project. With proper funding, it allows more of the team to work on the project in a much more dedicated manner.

Donations - https://donate.quasar.dev

If you're in a company and using Quasar for commercial projects, explain to your management the importance of monthly donations (eg. $200+) for open source projects: you're the one using it every day and this makes you the best suited person to convince them. Be creative! :slight_smile:

Quasar is saving your company tens of thousands of development hours (quite literally), which in turn is a pretty high money savings. Consider giving back a part of those savings to refuel the project itself :wink:

## Update: June 21st 2021

Quasar v2 stable (with Vue.js 3) has been released! Time to party!
https://github.com/quasarframework/quasar/discussions/9734

## Update: June 19th 2021

Next release is v2.0.0 stable.
Branch `vue3-work` has been merged into `dev`. The Qv1 work will now be done exclusively on the new `v1` branch.

## Update: April 27th 2021
We have passed the final major milestone: Quasar CLI now ships with Webpack 5, which was badly needed to support Node 1...

---

## Top Comments

**@rstoenescu** [maintainer] (+70):

Hi everyone,

Sorry but we'll have to delay the beta version due to vue-loader which has some SSR features not implemented yet. We cannot release a beta version until SSR is fully solved or else we might introduce breaking changes during this beta stage -- and we want to avoid this at all costs.

The new schedule is:

* First beta: "quasar" v2.0.0-beta.1 & "@quasar/app" v3.0.0-beta.1 - **2020/12/15**
* Stable releases: "quasar" v2.0.0 & "@quasar/app" v3.0.0 - **2021/01/30**

**@IlCallo** [maintainer] (+58):

Quasar v2 will lay the fundations needed for a Composition API + TS + tests incremental migration, which will take place during Quasar v2 lifecycle.

Quasar v3 will probably be released when this incremental migration is completed.

**@rstoenescu** [maintainer] (+28):

Maybe an additional important information. For app developers it won't matter whether Quasar is written in TS or not. Sure, the autocomplete will work a bit better, but you as a developer are NOT required to also use TS in your app.