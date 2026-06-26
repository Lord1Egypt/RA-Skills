---
tag: quasar-v2.17.0
version: 2.17.0
published: 2024-09-17
---

# quasar-v2.17.0

### Potential upgrade issue
The "Platform" Quasar plugin now explicitly holds all Boolean props in `Platform.is` Object. Previously, only the active/"true" ones were contained. So, for example, on a non-Firefox browser, if previously `Platform.is.firefox` would not have been declared, now it will be defined and its value is going to be `false`. So, if you were doing `'firefox' in Platform.is` or `Platform.is.firefox === undefined`, change it to `Platform.is.firefox`/`!Platform.is.firefox`.

## New
* feat+refactor(ui/Platform): explicitly specify all boolean props (they were previously undefined if "false") #17482
* perf(QScrollArea): prevent content re-rendering on scroll or mousemove (fix #16579) #17041
* feat(QScrollArea): add scroll viewport to create overscrolling effect #17208
* feat(QUploader): New prop -> thumbnail-fit (#17494)
* feat(QSelect): New prop: disable-tab-select (#17362)
* feat(QMenu/QTooltip): new Quasar CSS vars -> $menu-max-height, $tooltip-max-width, $tooltip-max-height #16072
* feat+perf(QOptionsGroup): new props -> option-value, option-label & option-disable #16874
* feat+refactor(QSpinner): mount & patch faster
* chore(QSelect): small perf-related improvements

## Fixes
* fix(QTabPanels): tab-panels 'transition' emit fires before transition ends (fix #17479). (#17489)
* fix(QScrollArea): correctly compute snap position for thumb #17206 (#17207)
* fix(QTabs): Active route tab doesn't update on reactivation when it's a descendant of <keep-alive> #17495
* fix+feat(QSelect/QMenu/QTooltip): the position engine should not override max-width/height set in CSS for QMenu/QTooltip #16072
* fix(ui): Type-Error because of 'declare module "@vue/runtime-core"' #17416

## Donations
Quasar Framework is an open-source MIT-licensed project made possible due to the **generous contributions** by sponsors and backers. If you are interested in supporting this project, please consider the following:

- Becoming a sponsor on Github
- One-off donation via PayPal