---
number: 2281
title: Incorrect .te() result
type: other
state: open
created: 2025-10-07
url: "https://github.com/intlify/vue-i18n/issues/2281"
reactions: 4
comments: 0
labels: "[Status: Review Needed]"
---

# Incorrect .te() result

### Reporting a bug?

The error occurs when checking for translation using the te function. When checking a string without dots - the result is correct. But if the string contains a dot - the function for some reason shows that such translation doesn't exist.

### Expected behavior

expected **true**, got **false**

### Reproduction

translations.json
```
{
  "aaa": "translation without dot",
  "aaa.": "translation with dot."
}
```

function
```
      console.log("without dot", i18().i18n.global.te("aaa"));
      console.log("translation", i18().i18n.global.t("aaa"));
      console.log("with dot", i18().i18n.global.te("aaa."));
      console.log("translation", i18().i18n.global.t("aaa."));
```

...