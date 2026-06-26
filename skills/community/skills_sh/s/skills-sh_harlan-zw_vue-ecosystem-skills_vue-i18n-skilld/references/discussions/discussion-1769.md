---
number: 1769
title: Different approaches for i18n of large applications?
category: Q&A
created: 2024-03-19
url: "https://github.com/intlify/vue-i18n/discussions/1769"
upvotes: 1
comments: 3
answered: false
---

# Different approaches for i18n of large applications?

Hi!


I'm struggling to find a way how to implement my i18n properly. It's a large-scale project (Approx. 5k translation keys or so), and I need to follow these criterias:


- be able to add new language, even those I don't know (as for now, usually, just pass key-value file to a localizator on customer side)
- support different languages noun cases and genders
- i really want to reuse my locales, instead of creating new ones (if they can be composed from existing ones)


I'm considering using 4 different approaches, but none of them is great enough to be sure it's a right way:


- use a external i18n tool like Localazy, so it would be easy to add new languages for non-technical people like business analyst or even customer
- just use json or js translations, with pluralizat...

---

## Top Comments

**@felicienfrancois** (+1):

I used to work with :
- vue-i18n
- single json translation file (per language)
- i18n Ally vscode extension (inline translation editing for developers)
- external i18n tool Phrase, with automatic synchronisation and onpage editing integration (for non developers)

I would recommend to use single json translation file (per language), to be able to integrate more easily with tools.

i18n ally and Phrase are both powerful tools which are quite easy to setup.
Both i18n Ally and Phrase work best with single file json.
i18n ally is a pain with multiple file (it ask f...

**@dlohvinov**:

@felicienfrancois thank you for sharing your experience!
May I ask: have you been using vue-i18n with its advanced (more powerful and complicated :) ) features, or just most common features like `$t` and `$tc`?

**@felicienfrancois**:

To be complete, we're currently considering changing or improving our setup to solve the issues we have:
- Tree shaking / Bundle size
- Issues with scope (vue-i18n is not usable outside setup function, so not in router, stores, not in backend)
- Dates & amount formatting

We may either go with another framework (ex: i18next) or extend our usage of vue-i18n.
We're currently evaluating the opportunity to use Function translation for dates and amounts (thoose would not be synced in third party translation tool)
And also the opportunity to use i18n tags or multiple json files in other to fi...