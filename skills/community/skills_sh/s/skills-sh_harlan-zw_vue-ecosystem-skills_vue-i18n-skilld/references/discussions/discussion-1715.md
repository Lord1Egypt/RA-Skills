---
number: 1715
title: use hyphens in named interpolation in json file
category: Q&A
created: 2024-01-26
url: "https://github.com/intlify/vue-i18n/discussions/1715"
upvotes: 2
comments: 1
answered: false
---

# use hyphens in named interpolation in json file

there is some workaround to use hyphens in named interpolation, for instance the key max-consecutive-length?

example:

`{
  "CONTINUOUS_DUPLICATE_CHARACTERS": "Exceeding {max-consecutive-length} identical characters in a row is not allowed"
}`

---

## Top Comments

**@ChrisGV04**:

I don't think so, since variable names in Javascript cannot include hyphens, but I'm not sure.

Is it possible that you use camel case `maxConsecutiveLenght` instead?