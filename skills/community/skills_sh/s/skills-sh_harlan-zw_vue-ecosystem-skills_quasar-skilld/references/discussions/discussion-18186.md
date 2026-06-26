---
number: 18186
title: I want to be able to disbale the sort temporily
category: Ideas / Proposals
created: 2025-11-25
url: "https://github.com/quasarframework/quasar/discussions/18186"
upvotes: 1
comments: 0
answered: false
---

# I want to be able to disbale the sort temporily

In QTable, I want to be able to suspend **sorting** during data mutations so the visible row order stays stable during edit.

**Problem**
Rows keep jumping around whilst editing.

**What I tried**
Clearing or toggling pagination.sortBy / pagination.descending per the docs.

Result: the table still reorders during mutations. Sort function gets called multiple times. Apparently, too many reactive propperties.

**Workaround I used**
Custom column sort function + a “suspend” flag to neutralize comparisons.

 ...