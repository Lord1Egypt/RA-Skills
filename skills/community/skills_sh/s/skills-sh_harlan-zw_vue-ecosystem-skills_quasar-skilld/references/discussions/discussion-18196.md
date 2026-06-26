---
number: 18196
title: q-table sticky-header-and-last-column problem
category: General - Components / Directives / etc
created: 2025-12-08
url: "https://github.com/quasarframework/quasar/discussions/18196"
upvotes: 1
comments: 0
answered: false
---

# q-table sticky-header-and-last-column problem

Hi!

I have problem with https://quasar.dev/vue-components/table#example--sticky-header-and-last-column
I cheked docks example and did my style with simple CSS

Last column is sticky and use black and whit colors. But **headers ignore style...**

HTML
```
<q-table
          dense
          separator="cell"
          :rows="dataRows.data?.vr_user"
          :columns="dataColumns"
          row-key="id"
          :rows-per-page-options="[25, 50, 100]"
          :filter="filter"
          :loading="loading"
          :class="tableClass">
          
          
          
</q-table>
```
          
Script
```
const tableClass = computed(() => {
  return $q.dark.isActive ? "sticky-table-dark" : "sticky-table-light";
});
```...