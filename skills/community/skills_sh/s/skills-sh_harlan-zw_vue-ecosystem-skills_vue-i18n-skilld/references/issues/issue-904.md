---
number: 904
title: How to use i18n in ts file?
type: other
state: closed
created: 2022-01-25
url: "https://github.com/intlify/vue-i18n/issues/904"
reactions: 8
comments: 17
---

# How to use i18n in ts file?

### Reporting a bug?

I use i18n in .vue file usually, that is ok. But how can I use it in other typescript file? Such as follow:
```vue
<script setup lang="ts">
import { jslook } from './util'
</script>
```
```ts
// util.ts
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

export const jslook = () => {
    console.log(t('message.hello'))
}
```
I expect the terminal logs right message, but it shows me error:
```bash
SyntaxError: Must be called at the top of a `setup` function
```

### Expected behavior

no errors and show messages

### Reproduction

I describe it in the bug report

### System Info

```shell
windows,chrome
```


### Screenshot

_No response_

### Additional context

Maybe I didn't find it in documents, if you know, please show me, thanks!

### Validations

- [X] Read the Contributing Guidelines
- [X] Read the Documentation
- [X] Check that there isn't already an issue that reports the same bug to avoid creating a duplicate.
- [X] Check that this is a concrete bug. For Q&A open a GitHub Discussion
- [X] The provided reproduction is a minimal reproducible example of the bug.

---

## Top Comments

**@kazupon** [maintainer] (+68):

Thank you for your reporting!

> SyntaxError: Must be called at the top of a `setup` function

`useI18n` is composal function that is implemented by Composition API.
It means that it needs to use by `setup` fucntion.
about `setup`, see here
https://staging.vuejs.org/api/composition-api-setup.html#composition-api-setup

Thanks

**@pommedepain** (+65):

@cboseck in the config file where you setup your i18n config, get what createI18n returns in a variable and then export it that way :
```
import { createI18n } from "vue-i18n";

const i18n = createI18n({
	// Set locale
	locale: "en",

	// Set fallback locale
	fallbackLocale: "fr",

	// Must be set to 'false', to use Composition API
	legacy: false,

	// Refer a global scope Composer instance of i18n
	globalInjection: true,

	// Set locale messages
	messages,
});

export default i18n;
```

Then, in your ts file, import the variable from your setup file and use it this way...

**@kazupon** [maintainer] (+9):

From vue-i18n v9, you need to use `global` of `I18n` instance that is created `createI18n`
API docs here:
https://vue-i18n.intlify.dev/api/general.html#global

In about example, I think `lazy-loading` example will be helped for you:
https://github.com/intlify/vue-i18n-next/blob/master/examples/lazy-loading/vite/src/i18n.ts
