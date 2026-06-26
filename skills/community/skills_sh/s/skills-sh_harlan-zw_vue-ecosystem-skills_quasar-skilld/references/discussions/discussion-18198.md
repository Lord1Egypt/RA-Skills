---
number: 18198
title: I'm struggling with upgrading Vue + Quasar with webpack. Does someone have Advice, am I on the 'right track' with upgrading?
category: General - Components / Directives / etc
created: 2025-12-14
url: "https://github.com/quasarframework/quasar/discussions/18198"
upvotes: 1
comments: 2
answered: false
---

# I'm struggling with upgrading Vue + Quasar with webpack. Does someone have Advice, am I on the 'right track' with upgrading?

I've 'earned' the application last year. The project has been started I believe in 2019. I have on this forum already started two other discussions, without succes unfortunately. I have been struggling further and try it again. 

### Current situation:
Node.Js: V16.20.2
npm: 8.17.0
Vue: 3.2.0
Quasar: 2.11.10
Webpack: 4.46.0
vue-cli-service

I suppose that the project at that time was build with '@vue/cli'.  The program is started with "npm run vue-cli-service serve"

### What I try todo upgrading Node.js + dependencies (LCM work):
I've the dependencies upgraded (-I think these are the most imortant ones):
Node.Js: V22.21.0
npm: 10.9.4
Vue: 3.5.25
Quasar: 2.18.6
Webpack: 5.103.0

I read on the quasar site, that 'vue\cli' will not be maintained anymore. So as suggested on...

---

## Top Comments

**@yusufkandemir** [maintainer]:

I'd say you are on the right track. Since Vue CLI is not maintained, it would be harder to try migrating all the files into something else, compared to only moving your source files to another new project.

Answers to your questions:
1. Yes, I'd say you are on the right track. Quasar CLI is a good choice. Migrate to Quasar CLI with Webpack instead of Vite to make it manageable. Otherwise, you will also have to deal with Webpack and Vite differences. You can still migrate to Vite after you finish the current migration.
2. Most parts of `main.ts` is managed for you by Quasar CLI under the ho...

**@nkamp**:

Hi Yusufkandemir,

Thanks for you're answer. But today I have fixed it!!
I was not aware of the dependency "vue-cli-plugin-quasar". I have this dependency. Than I had problem with import 'QuasarTable'( sorry I don't exactly the name now, I'm not behind my working laptop). Everywhere this type is used, i have changed into import type { QuasarTable } from "quasar";. This is an interface and type which is used at compile-time. The function useQuasar() is an 'regular' import: import { useQuasar }  from "quasar";

Now are the quasar components imported and rendered.
I have 'discovered' that I...