---
number: 2914
title: 3.0.1,3.0.2,3.0.3 - devtoolsApi is not defined
type: docs
state: open
created: 2025-02-15
url: "https://github.com/vuejs/pinia/issues/2914"
reactions: 3
comments: 12
labels: "[contribution welcome,  docs,  pkg:devtools]"
---

# 3.0.1,3.0.2,3.0.3 - devtoolsApi is not defined

### Reproduction

https://jsfiddle.net/0sj7apb6/

### Steps to reproduce the bug

Using the pinia.iife.js 3.0.1 now gives the error: "Uncaught ReferenceError: devtoolsApi is not defined"
no error with 3.0.0, probably related to #2910 fix

### Expected behavior

no error, and working devtools with the no prod version

### Actual behavior

error using the iife.js, and no devtools using the iife.prod.js

### Additional information

_No response_