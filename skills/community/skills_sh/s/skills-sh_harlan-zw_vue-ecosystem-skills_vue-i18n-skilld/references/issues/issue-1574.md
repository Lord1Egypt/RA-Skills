---
number: 1574
title: Typescript error when using pluralization and formatting
type: bug
state: open
created: 2023-09-29
url: "https://github.com/intlify/vue-i18n/issues/1574"
reactions: 5
comments: 4
labels: "[ p3-minor-bug, typescript]"
---

# Typescript error when using pluralization and formatting

### Reporting a bug?

I'm trying to use pluralization and formatting together. This works as it should, but the TypeScript types seem to be incorrect, which makes it impossible to build the project properly.

### Expected behavior

The types match the actual call signature of the `t` function and I can successfully build my project.

### Reproduction

```ts
// messages.json
{
  "contacts": "{count} contact | {count} contacts"
}

// somewhere else
console.log(t("contacts", 1, { count: 1})) // prints "1 contact" correctly, but raises an error while building
```

The error in question:

```
  The last overload gave the following error.
    Argument of type 'number' is not assignable to parameter of type 'Record<string, unknown>'.

1   console.log(t("contacts", 1, { count: 1 }));
                              ~

  node_modules/vue-i18n/dist/vue-i18n.d.ts:1244:5
    1244     <Key extends string>(key: Key | ResourceKeys | number, named: NamedValue, defaultMsg: string): string;
             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    The last overload is declared here.
```

### System Info

```shell
System:
    OS: Linux 5.15 Linux Mint 21.1 (Vera)
    CPU: (32) x64 AMD Ryzen 9 7950X3D 16-Core Processor
    Memory: 45.44 GB / 61.96 GB
    Container: Yes
    Shell: 5.8.1 - /usr/bin/zsh
  Binaries:
    Node: 18.17.1 - /usr/bin/node
    npm: 9.6.7 - /usr/bin/npm
  Browsers:
    Chrome: 117.0.5938.92
  npmPackages:
    @vitejs/plugin-vue: ^4.0.0 => 4.1.0 
    @vue/tsconfig: ^0.1.3 => 0.1.3 
    vite: ^4.1.4 => 4.3.9 
    vue: ^3.2.47 => 3.2.47 
    vue-i18n: ^9.2.2 => 9.2.2 
    vue-router: ^4.1.6 => 4.1.6 
    vue-tsc: ^1.2.0 => 1.2.0
```...