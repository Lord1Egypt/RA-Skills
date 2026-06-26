---
number: 2575
title: Quasar v1.0 - Feature freeze in effect for v0.17
type: other
state: closed
created: 2018-09-17
url: "https://github.com/quasarframework/quasar/issues/2575"
reactions: 47
comments: 11
labels: "[announcement :rocket:]"
---

# Quasar v1.0 - Feature freeze in effect for v0.17

Hi All Quasarians,

It's been a long, winding road up until this point, but I'm finally working with the team on a solid Quasar v1.0, after which there will be no further breaking changes.

To do this, I’ve decided to feature-freeze v0.17 in order to fully focus on v1.0. This means that v0.17 is the last pre 1.0 release - and there will only be fixes merged and no new features. The only exception to this is to honour agreements with partners or main sponsors who require the integration of critical functionality or features.

When 1.0 lands, the Quasar you know and love will have been polished to a mirror’s sheen. The UI design will be perfect - and if you think Quasar's rendering speed is fast today, you will be glad to know that all of its components will be ruthlessly curated for the best performance possible, the most logical ease of use and the smallest footprint. Furthermore, all of the pain points (no matter how trivial) are being addressed and will be resolved.

The documentation website is also being rebuilt using Quasar SSR, where you'll be able to see live examples and also the source code for them in one place, optionally playing with the example in Codepen - just by clicking on a button.

You can expect more announcements on v1.0 as we inch closer to the release. The plan is to publish it as soon as possible, but without affecting the quality -- we want you to rest easy in the knowledge that everything is perfect and you can trust Quasar 100%. That said, it seems like the stars are aligning for a release candidate late this year.

Thanks,
Razvan Stoenescu

---

## Top Comments

**@nothingismagick** (+12):




**@rstoenescu** [maintainer] (+1):

@trsiddiqui Ripples or not, every component that has a ripple integrated by default will also have the ability to turn it off (and also customize it!). Regarding performance, v1 is **a LOT faster** than 0.17. Regarding iOS theme -- you won't be needing it anymore as v1 is much more customizable and way more easy to customize too; also, almost each component has some props that you can use to mimick exactly the iOS looks.

More on each when v1.0 is released. Everything is covered, no worries!

@mesqueeb In v1.0, every boot file (renamed app plugins to avoid the constant confusion between ap...

**@mesqueeb**:

@rstoenescu

I'm curious what will happen to iOS/Material themes in v1.0. A while ago I think there was some discussion on wether or not iOS theme is used enough to keep? Will there be any changes to this or not?

Also will `boot.js` be depreciated before v1.0?