---
number: 18206
title: Badge type indicator size
category: Ideas / Proposals
created: 2025-12-27
url: "https://github.com/quasarframework/quasar/discussions/18206"
upvotes: 1
comments: 0
answered: false
---

# Badge type indicator size

The size of the badge used as rounded indicator is limited from below by css `padding `and `min-height` attributes of `q-badge` base class.

The default values of `min-height: 12px` and `padding: 2px 6px` cause the badge to have down-size limitation especially in mobile application where I would like to have a neat smaller badge with diameter of 6px for example.

I tweaked these values to achieve the desired size but with respect to other quasar components it would be nice to have an size attribute.