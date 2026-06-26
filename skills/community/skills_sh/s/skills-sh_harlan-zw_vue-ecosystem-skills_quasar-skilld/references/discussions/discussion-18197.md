---
number: 18197
title: "QSelect: Option to clear input text on select"
category: Ideas / Proposals
created: 2025-12-10
url: "https://github.com/quasarframework/quasar/discussions/18197"
upvotes: 3
comments: 0
answered: false
---

# QSelect: Option to clear input text on select

This is a feature that has been suggested before (#4732, #4600, #5038, #5041) but it's been several years and I would like this to be reconsidered.

When a QSelect uses `multiple` and `use-input` (and possibly in other cases), when the user selects an option the existing input text remains in the widget.

Codepen example: https://codepen.io/adam-earthscope/pen/ogxmqLW

I understand the reason for this behavior, but there are also cases where this isn't wanted. I'd like to propose a new QSelect attribute that would clear the input text on selection. The Vuetify equivalent is `clear-on-select` which seems intuitive to me.