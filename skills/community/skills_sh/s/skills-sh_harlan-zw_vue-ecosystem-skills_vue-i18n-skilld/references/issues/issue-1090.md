---
number: 1090
title: Plural counter interpolation does not respect locale's numeral system
type: other
state: open
created: 2022-07-29
url: "https://github.com/intlify/vue-i18n/issues/1090"
reactions: 4
comments: 0
labels: "[Status: Review Needed]"
---

# Plural counter interpolation does not respect locale's numeral system

### Reporting a bug?

When formatting a plural message with `$tc()` the interpolated `{n}` or `{count}` value is always displayed in the Western Arabic numeral system (1, 2, 3). Different locales use different numeral systems. For example, Arabic uses the Eastern Arabic numeral system (١، ٢، ٣).  

In contrast, `$n()` and `$d()` correctly display numbers in the active locale's numeral system. 

### Expected behavior

Consistent use of the same numeral system across a locale, including plurals, numbers, and dates. Ideally this would use the locale's official numeral system.

### Reproduction

https://codesandbox.io/s/vue-i18n-9-numeral-systems-3lbt0r?file=/index.html

### System Info

```shell
Using Vue 3.x and Vue I18n 9.x
Please see Code Sandbox linked above for more details.
```...