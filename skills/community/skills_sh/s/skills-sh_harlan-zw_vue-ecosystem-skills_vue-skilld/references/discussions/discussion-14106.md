---
number: 14106
title: VueJS is impossible to set up
category: Help/Questions
created: 2025-11-17
url: "https://github.com/orgs/vuejs/discussions/14106"
upvotes: 2
comments: 3
answered: true
---

# VueJS is impossible to set up

Hey guys,

i have been working a lot with Next.js but occasionally have projects that need to be in Vue.

Everytime i use Vue.js, i skip using Eslint and Prettier or accept that most files are marked as "red" because of error messages that are in fact no errors in Vue.

I would want to ask, if there is any guideline or tutorial on how to properly set up Vue.js with the regular tech-stack (Typescript, Eslint, Prettier) or if it is just not supported.

I have been trying to set it up every now and again for a long time now and was never successful.

So far i have tried the following:
- Using the CLI and enable typscript, eslint, prettier out of the box
- Using Vite to try and setup Vue custom without the CLI

Either way, i end up with:
- Prettier not working or formatting Vue ...

---

## Accepted Answer

i had same frustration before. the problem is extension conflicts.

**fix:**

1. disable Vetur completely - its for vue 2 and conflicts with vue 3
2. only keep "Vue - Official" extension (this is the new one, replaces volar)
3. remove "Vue language features (Volar)" - its merged into Vue Official now

so you should only have ONE extension: **Vue - Official**

**for eslint/prettier:**

use the new @vue/eslint-config-prettier:
```bash
npm create vue@latest my-app
# select yes for typescript, eslint, prettier
```

this sets up everything correctly. the cli now uses flat eslint config.

your eslint.config.js should look like:
```js
import pluginVue from "eslint-plugin-vue"
import vueTsEslintConfig from "@vue/eslint-config-typescript"
import skipFormatting from "@vue/eslint-config-prettier/skip-formatting"

export default [
  ...pluginVue.configs["flat/recommended"],
  ...vueTsEslintConfig(),
  skipFormatting,
]
```

...