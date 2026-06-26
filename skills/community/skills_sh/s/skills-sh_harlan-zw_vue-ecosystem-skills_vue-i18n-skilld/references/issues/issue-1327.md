---
number: 1327
title: Typescript Import issue with NodeNext
type: other
state: open
created: 2023-02-04
url: "https://github.com/intlify/vue-i18n/issues/1327"
reactions: 11
comments: 8
labels: "[Type: Improvement, typescript]"
---

# Typescript Import issue with NodeNext

### Reporting a bug?

When setting `"moduleResolution": "NodeNext",`  in `tsconfig.json` and trying to use this package will result in a error in VSCode `Could not find a declaration file for module 'vue-i18n'`. However everything runs fine, I think this has to do with how exports are being interpreted 

Changing the `package.json` exports to look like this seems to resolve the issue. Just adding types here as well. Is this a change that would be acceptable?
```json
"exports": {
    ".": {
      "import": {
        "node": "./index.mjs",
        "default": "./dist/vue-i18n.esm-bundler.js"
      },
      "require": "./index.js",
      "types": "./dist/vue-i18n.d.ts"
    },
    "./dist/*": "./dist/*",
    "./index.mjs": "./index.mjs",
    "./package.json": "./package.json"
  },
```

### Expected behavior

Package should not show dev time TS errors when using `NodeNext` moduleResolution

### Reproduction

Quickest reproduction is to just create a TS vue app using Vite, and add `vue-i8n` to the project and update the `tsconfig.json` with `"moduleResolution": "NodeNext",`

### System Info

```shell
System:
    OS: Linux 5.15 Ubuntu 20.04.4 LTS (Focal Fossa)
    CPU: (16) x64 Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz
    Memory: 25.84 GB / 31.31 GB
    Container: Yes
    Shell: 3.2.2 - /usr/bin/fish
  Binaries:
    Node: 16.17.0 - ~/.nvm/versions/node/v16.17.0/bin/node
    Yarn: 1.22.19 - /usr/bin/yarn
    npm: 9.1.3 - ~/.nvm/versions/node/v16.17.0/bin/npm
  Browsers:
    Chrome: 102.0.5005.61
  npmPackages:
    @intlify/unplugin-vue-i18n: ^0.8.1 => 0.8.1
    @vitejs/plugin-vue: ^4.0.0 => 4.0.0
    vite: ^4.1.1 => 4.1.1
    vue: ^3.2.47 => 3.2.47
    vue-i18n: ^9.2.2 => 9.2.2
    vue-router: ^4.1.6 => 4.1.6
    vue-tsc: ^1.0.24 => 1.0.24
```


### Screenshot

_No response_

### Additional context

_No response_

### Validations

- [X] Read the Contributing Guidelines:

If you will avoid this issue, I would recommend installing the next tag version, (i.e. vue-i18n v9.3).
Currently in beta, this version has not changed much in terms of functionality from v9.2. Actually, It's used in nuxt i18n v8 beta.

**@aphex** (+8):

Another update on this, updating to TS 5 and changing `moduleResolution` to `bundler` will result in a slightly different error. 

```bash
Could not find a declaration file for module 'vue-i18n'. 'C:/path/to/node_modules/.pnpm/vue-i18n@9.2.2_vue@3.2.47/node_modules/vue-i18n/dist/vue-i18n.esm-bundler.js' implicitly has an 'any' type.
  There are types at 'c:/path/to/node_modules/vue-i18n/dist/vue-i18n.d.ts', but this result could not be resolved when respecting package.json "exports". The 'vue-i18n' library may need to update its package.json or typings.ts(7016)
  ```
  
Patching as I me...

**@Basaingeal** (+3):

`"moduleResolution": "bundler"` is now the default settings in the latest `vuejs/tsconfig`, compatible with TS 5.0.
https://github.com/vuejs/tsconfig#migrating-from-typescript--50