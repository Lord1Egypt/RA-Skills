---
number: 2767
title: WritableComputed type is lost
type: bug
state: closed
created: 2024-09-06
url: "https://github.com/vuejs/pinia/issues/2767"
reactions: 12
comments: 12
labels: "[bug, typescript]"
---

# WritableComputed type is lost

### Reproduction

https://play.pinia.vuejs.org/#eNqNVU1v2kAQ/SsjX2wksJumSiUKhKRN1faQVkkuVd2DsQe8wd619sNQIf57x7vYmDSJChd75828N7Mz4513VVVhbdAbexOVSlZpUKhNBUXCV9PY0yr2ZjFnZSWkhh0YhfdaSIQ9LKUowQ+jVBiuUYZa+TGPeSq4oiAWNO3wwSCmY3oIFwmnvyLb25hPIkdKFPSisayKRCO9AUwyVs9+CiOJyDCtYJGoNeox7HbgwofOcG3PYb+fRI1L6wv1iC0pgxPWsEC+0rnNCehnSb6U5RBYkziWCv4IA3lSY8PznC8RkRR3Ap8E9zUUbI2gcywvjxIo9sJoLTjM04Kl66dKKH9fSCoy+qTmDinxFNvAsGFE5MxqErlALrOTHGe3QgNyYVZ569qT8IKAftXCyqg88J2vPyAlV1nWhuoRT6Le3XhDz/XDqEyq8FEJTt2zaxjjg4Gahu7JlSH2KsZZ0pzEXmSfQ1TlaCHFRlHbPBJ42ELn1IpRhrUWolCjpGLOLde6UuMoSjNO+AwLVsuQo454VUb/+MwvwovwLCrYIiKiiPEMt6c05DHKsPyf6C10/iY8exe+t1Hr80PQsonaBN3HfE9l0Yq6f8lWT4qSirJiBcrvlWY0HSfFSYpCbL7ZMy0NdhLTHNP1M+ePautU/5BI5auxl5ZO5Aq1M9/c3+KWnjtjKTJTEPoV4x0qUZhGo4NdG56R7B7Oqv1q75jx1YO62Wrkqk2qEWqrYfG2zB9fSf0o9zw871XxuFCohN3myXDJ+JPlY7uJtk4HkrgcQlNuozHrYKTDribcWpjbUN0mm/ZDB/6B3R9CMIDpzMl1Lif7ZtqQBb/a2RmCn1RVgc3D8egw4b8HH45RjgugFRocSkLVGB9YT4a0TgpDc8sK0hUE1nQEwXRKq6Sd4MNN0Q6nSBw3nxvImBaZpPt6ITIpeYaOZvt1LriElgDGzu7o9y7bdkm2HH6O1D0+RBE83INYNxhJ3xrJ6eL6AoZdiZqGoA+Ht/8LgWlAcw==

### Steps to reproduce the bug

- check store.ts

### Expected behavior

No TS error

### Actual behavior

writable computed is coerced to a simple getter

### Additional information

This might require some Types refactor

---

## Top Comments

**@posva** [maintainer] (+3):

> This doesn't seem to work when the variable ref is extracted via storeToRefs whereas it was fine before (prior to vue 3.5 I believe), is this expected?

A fix is on the way

**@filipbekic01** (+5):

I'm having same issue.

**@posva** [maintainer]:

Note: different types for the setter and getter cannot be supported until the feature is supported in TS:

- https://github.com/microsoft/TypeScript/issues/43826