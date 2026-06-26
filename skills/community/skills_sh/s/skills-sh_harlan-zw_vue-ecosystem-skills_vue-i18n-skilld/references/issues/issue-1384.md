---
number: 1384
title: Type check with typescript v5 throws error in template $t
type: other
state: open
created: 2023-04-27
url: "https://github.com/intlify/vue-i18n/issues/1384"
reactions: 11
comments: 10
labels: "[typescript]"
---

# Type check with typescript v5 throws error in template $t

### Reporting a bug?

After upgrade to typescript v5. The type check with `vue-tsc` throws errors with the usage of `$t` in vue template syntax. I think this might come from the `exports` definition in `package.json`, where you can set `types` per entry level. https://www.typescriptlang.org/docs/handbook/esm-node.html#packagejson-exports-imports-and-self-referencing

### Expected behavior

Don't throw a type error on check

### Reproduction

https://stackblitz.com/edit/vitest-dev-vitest-ztvbls?file=package.json

Run `npm run type-check-v5` to check types with `typescript@v5`

This should print the following errors:
```
src/Hello.vue:7:8 - error TS2339: Property '$t' does not exist on type '{ $: ComponentInternalInstance; $data: {}; $props: Partial<{}> & Omit<Readonly<ExtractPropTypes<{}>> & VNodeProps & AllowedComponentProps & ComponentCustomProps, never>; ... 10 more ...; $watch<T extends string | ((...args: any) => any)>(source: T, cb: T extends (...args: any) => infer R ? (args_0: R, args_1: R) => ...'.

7     {{ $t('test') }}
         ~~

src/Hello.vue:8:8 - error TS2339: Property '$t' does not exist on type '{ $: ComponentInternalInstance; $data: {}; $props: Partial<{}> & Omit<Readonly<ExtractPropTypes<{}>> & VNodeProps & AllowedComponentProps & ComponentCustomProps, never>; ... 10 more ...; $watch<T extends string | ((...args: any) => any)>(source: T, cb: T extends (...args: any) => infer R ? (args_0: R, args_1: R) => ...'.

8     {{ $t('test_with_label', { label }) }}
         ~~


Found 2 errors in the same file, starting at: src/Hello.vue:7
```

Run `npm run type-check-v4` to check types with `typescript@v4`

### System Info

...

---

## Top Comments

**@dkern** (+6):

I was able to suppress this warning with a custom typescript definition. Therefore it's not needed to change the package.json in node_modules. Of course, this is not a real fix, but at least I can build the project again.

**i18n.d.ts:**
```typescript
export {};

declare module 'vue' {
  interface ComponentCustomProperties {
    $t: (key: string) => string;
    $tm: (key: string) => []|{[p: string]: any};
  }
}
```

If you use more/other function of i18n you may need to add the to the interface.

**@kazupon** [maintainer] (+1):

If you will avoid this issue, I would recommend installing the next tag version, (i.e. vue-i18n v9.3).
Currently in beta, this version has not changed much in terms of functionality from v9.2. Actually, It's used in nuxt i18n v8 beta.

**@lupas** (+1):

Related to https://github.com/intlify/vue-i18n-next/issues/1327, should be fixed with https://github.com/intlify/vue-i18n-next/pull/1388