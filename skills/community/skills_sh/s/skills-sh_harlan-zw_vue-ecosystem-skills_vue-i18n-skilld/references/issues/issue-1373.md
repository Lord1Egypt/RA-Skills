---
number: 1373
title: CamelCase component name for <i18n-t>, <i18n-d> and <i18n-n> not work 
type: bug
state: closed
created: 2023-04-14
url: "https://github.com/intlify/vue-i18n/issues/1373"
reactions: 5
comments: 0
labels: "[Type: Bug,  p3-minor-bug]"
---

# CamelCase component name for <i18n-t>, <i18n-d> and <i18n-n> not work 

### Reporting a bug?

`<i18n-t>`, `<i18n-d>`, `<i18n-n>`  don't work if written in CamelCase.

### Expected behavior

I expect the components to work just as well in CamelCase and kebab-case as the types indicate.

vue-i18n.d.ts
```ts
  export interface GlobalComponents {
    ['i18n-t']: typeof Translation
    ['i18n-d']: typeof DatetimeFormat
    ['i18n-n']: typeof NumberFormat
    ['I18nT']: typeof Translation
    ['I18nD']: typeof DatetimeFormat
    ['I18nN']: typeof NumberFormat
  }
```

### Reproduction

https://github.com/erwanjugand/vue-i18n-next-bug

```bash
yarn 
yarn dev
```

### System Info

```shell
System:
    OS: Linux 5.15 Ubuntu 22.04.2 LTS 22.04.2 LTS (Jammy Jellyfish)
    CPU: (20) x64 13th Gen Intel(R) Core(TM) i5-13600KF
    Memory: 22.77 GB / 31.27 GB
    Container: Yes
    Shell: 5.8.1 - /usr/bin/zsh
  Binaries:
    Node: 18.14.2 - ~/.nvm/versions/node/v18.14.2/bin/node
    Yarn: 1.22.19 - ~/.nvm/versions/node/v18.14.2/bin/yarn
    npm: 9.5.0 - ~/.nvm/versions/node/v18.14.2/bin/npm
  npmPackages:
    @vitejs/plugin-vue: ^4.0.0 => 4.1.0
    @vue/eslint-config-prettier: ^7.1.0 => 7.1.0
    @vue/eslint-config-typescript: ^11.0.2 => 11.0.2
    @vue/tsconfig: ^0.1.3 => 0.1.3
    vite: ^4.1.4 => 4.2.1
    vue: ^3.2.47 => 3.2.47
    vue-i18n: 9 => 9.2.2
    vue-tsc: ^1.2.0 => 1.2.0
```


### Screenshot




...