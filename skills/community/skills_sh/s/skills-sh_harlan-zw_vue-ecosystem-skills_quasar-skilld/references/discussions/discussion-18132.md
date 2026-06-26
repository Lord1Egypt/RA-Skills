---
number: 18132
title: Q-Select with autocomplete and use-input adds a weird spacing when selected text is too long
category: General - Components / Directives / etc
created: 2025-09-23
url: "https://github.com/quasarframework/quasar/discussions/18132"
upvotes: 2
comments: 0
answered: false
---

# Q-Select with autocomplete and use-input adds a weird spacing when selected text is too long

I have a beefy q-select that I use with autocomplete to query the backend. Works well. 

However, once the select item is placed inside the input, there is some weird spacing that appears at the bottom that I believe is due to the input. This breaks my design since the element then grows downwards for more space. 

I would rather the text gets truncated with an ellipsis. I have tried a custom slot for the selected-item but the result was the same no matter how small I made my width.

How do I get rid of that little space at the bottom

<img width="621" height="103" alt="Screenshot 2025-09-23 at 10 40 23" src="https://github.com/user-attachments/assets/0f7495d9-baca-4225-965b-4d3a7ed8028d" />

This is my q-select

...