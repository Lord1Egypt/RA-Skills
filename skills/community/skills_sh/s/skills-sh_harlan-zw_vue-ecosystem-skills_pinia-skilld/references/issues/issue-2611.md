---
number: 2611
title: acceptHMRUpdate skips optional attributes without default values
type: other
state: open
created: 2024-03-13
url: "https://github.com/vuejs/pinia/issues/2611"
reactions: 0
comments: 3
labels: "[discussion, HMR ]"
---

# acceptHMRUpdate skips optional attributes without default values

### Reproduction

https://github.com/bodograumann/pinia-hmr-optional-attributes

### Steps to reproduce the bug

1. `git clone https://github.com/bodograumann/pinia-hmr-optional-attributes`
2. `cd pinia-hmr-optional-attributes`
3. `npm install`
4. `npm run dev`
5. `xdg-open http://localhost:5173`
6. Press the "Increment" button. Sign says "positive".
7. `touch src/store/counter.ts`

### Expected behavior

All the state should be preserved.

### Actual behavior

`counter.nr` is preserved as `1`, but `counter.sign` is lost. The page shows `-`, while it should show `positive`.

### Additional information

The relevant code is here: https://github.com/vuejs/pinia/blob/93b5546cf18bc54bb90de2397219dec7360fa697/packages/pinia/src/hmr.ts#L41-L43