---
number: 1754
title: Modifiers for interpolated values
type: feature
state: open
created: 2024-03-01
url: "https://github.com/intlify/vue-i18n/issues/1754"
reactions: 9
comments: 2
labels: "[Status: Proposal]"
---

# Modifiers for interpolated values

### Clear and concise description of the problem

Lets say you want to translate "Passenger" as well as "Remove passenger". And let's say passengers are not the only thing you want to remove (i.e. images, links etc.).

Currently, what you have to do (it seems), is to add a source key for every scenario:
```
{
  "passenger": "Passenger",
  "image": "Image",
  "link": "Link",
  "remove.passenger": "Remove @.lower:passenger",
  "remove.image": "Remove @.lower:image",
  "remove.link": "Remove @.lower:link"
}
```
And you would use it like so: `$t("remove.passenger")`.
But that seems awfully redundant!

### Suggested solution

What if, instead, you could `lowercase` interpolated strings.

```
{
  "remove": "Remove @.lower:{value}",
  "passenger": "Passenger",
  "image": "Image",
  "link": "Link",
}
```

And you would use it like so `$t("remove", { value: $t("passenger") } )`

### Alternative

_No response_

### Additional context

This would open up endless possibilities, especially for custom modifiers

### Validations

- [X] Read the Contributing Guidelines
- [X] Read the Documentation
- [X] Check that there isn't already an issue that request the same feature to avoid creating a duplicate.

---

## Top Comments

**@lnvglr** (+1):

Is there a perspective that this may get implemented at some point in the future?
Or did I miss something?


**@DennisMaass**:

Does somebody know a solution for that kind of problem?