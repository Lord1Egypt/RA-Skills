---
number: 1364
title: Invalid number of arguments, expected 1 
type: other
state: open
created: 2023-04-04
url: "https://github.com/intlify/vue-i18n/issues/1364"
reactions: 11
comments: 12
labels: "[Status: Need More Info]"
---

# Invalid number of arguments, expected 1 

### Reporting a bug?

When I use `$d` and `$t`, the ts error occur.
<img width="737" alt="image" src="https://user-images.githubusercontent.com/13377178/229667109-ac4acd64-1987-4028-bc88-73649808d6b9.png">
<img width="833" alt="image" src="https://user-images.githubusercontent.com/13377178/229667152-a03e8b31-8b71-4ef9-a530-f5e74587679d.png">


### Expected behavior

Should no error

### Reproduction

Just use it with params

### System Info

```shell
System:
    OS: macOS 13.4
    CPU: (16) x64 Intel(R) Core(TM) i9-9900KF CPU @ 3.60GHz
    Memory: 14.41 GB / 48.00 GB
    Shell: 3.6.0 - /usr/local/bin/fish
  Binaries:
    Node: 19.8.1 - ~/Library/Caches/fnm_multishells/11823_1680573671866/bin/node
    Yarn: 1.22.19 - /usr/local/bin/yarn
    npm: 9.5.1 - ~/Library/Caches/fnm_multishells/11823_1680573671866/bin/npm
  Browsers:
    Chrome: 111.0.5563.146
    Safari: 16.5
  npmPackages:
    @vitejs/plugin-vue: ^4.0.0 => 4.1.0 
    @vitejs/plugin-vue-jsx: ^3.0.0 => 3.0.1 
    @vue/eslint-config-prettier: ^7.1.0 => 7.1.0 
    @vue/eslint-config-typescript: ^11.0.2 => 11.0.2 
    @vue/test-utils: ^2.3.0 => 2.3.2 
    @vue/tsconfig: ^0.1.3 => 0.1.3 
    vite: ^4.1.4 => 4.2.1 
    vitest: ^0.29.1 => 0.29.8 
    vue: ^3.2.47 => 3.2.47 
    vue-i18n: ^9.2.2 => 9.2.2 
    vue-router: ^4.1.6 => 4.1.6 
    vue-tsc: ^1.2.0 => 1.2.0 
    vue3-toastify: ^0.1.6 => 0.1.6 
```
```


### Screenshot

_No response_

### Additional context

_No response_

### Validations

- [X] Read the [Contributing Guidelines](https://github.com/intlify/vue-i18n-next/blob/master/.github/CONTRIBUTING.md)
- [X] Read the [Documentation](https://vue-i18n.intlify.dev/)
- [X] Check that there isn't [already an issue](https://github.com/intlify/vue-i18n-next/issues) that reports the same bug to avoid creating a duplicate.
- [X] Check that this is a concrete bug. For Q&A open a [GitHub Discussions](https://github.com/intlify/vue-i18n-next/discussions)

---

## Top Comments

**@lovue** (+3):

Can add below before the first `$t` type definition in `vue-i18n.d.ts`.
```ts
$t<
  Key extends string,
  DefinedLocaleMessage extends RemovedIndexResources<DefineLocaleMessage> = RemovedIndexResources<DefineLocaleMessage>,
  Keys = IsEmptyObject<DefinedLocaleMessage> extends false
    ? PickupPaths<{
      [K in keyof DefinedLocaleMessage]: DefinedLocaleMessage[K]
    }>
    : never,
  ResourceKeys extends Keys = IsNever<Keys> extends false ? Keys : never
>(
  key: Key | ResourceKeys | Path,
  named?: Record<string, unknown>
): TranslateResult
```

**@anotherroot** (+5):

Same problem in Intelij

**@kazupon** [maintainer]:

Thank you for your reporting!
Sorry for my late reply. 
Unfortunately, I could not reproduce this issue.
We need minimal reproduction, so Could you give us your it please? 