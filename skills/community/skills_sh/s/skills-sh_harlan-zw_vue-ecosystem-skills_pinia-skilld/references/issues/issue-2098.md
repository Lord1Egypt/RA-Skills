---
number: 2098
title: `acceptHMRUpdate` type error when switching to TS 5.0
type: bug
state: closed
created: 2023-03-23
url: "https://github.com/vuejs/pinia/issues/2098"
reactions: 23
comments: 3
labels: "[bug, contribution welcome, typescript, has workaround]"
---

# `acceptHMRUpdate` type error when switching to TS 5.0

### Reproduction

https://github.com/josh-hemphill/pinia_bug-report

### Steps to reproduce the bug

1. Use Typescript >5.0
2. Use Setup-style to create a store
3. Use Hot module reload snippet if not present (`acceptHMRUpdate` function)
4. Set VSCode to use workspace tsc or run `tsc --noEmit`
5. Observe the error

### Expected behavior

For there not to be a type error

### Actual behavior

Type error is thrown:
```
Argument of type 'StoreDefinition<"counter", _UnwrapAll<Pick<{ n: Ref<number>; getN: () => Ref<number>; }, "n">>, Pick<{ n: Ref<number>; getN: () => Ref<number>; }, never>, Pick<...>>' is not assignable to parameter of type 'StoreDefinition<string, StateTree, _GettersTree<StateTree>, _ActionsTree>'.
  Property 'getN' is missing in type '_ActionsTree' but required in type 'Pick<{ n: Ref<number>; getN: () => Ref<number>; }, "getN">'.ts(2345)
```

### Additional information

_No response_

---

## Top Comments

**@posva** [maintainer] (+1):

Using as `any` for this particular case is fine. I will take a look in the future (I will remove the contribution welcome tag if I do) but feel free to take this if you want.

**@samydoesit** (+4):

Not great, but adding `as any` to the first parameter of `acceptHMRUpdate` works around it on my end.

```typescript
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useUserStore as any, import.meta.hot));
}
```

or add a shim

```typescript
# shim-pinia.d.ts

// TODO: https://github.com/vuejs/pinia/issues/2098
declare module 'pinia' {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types
  export function acceptHMRUpdate(initialUseStore: StoreDefinition | any, hot: any): (newModule: any) => any;
}

export {}
```

**@thisVioletHydra**:

```ts
Argument of type 'StoreDefinition<"asdsad", { text: string; agent: string; extension: string; factory: boolean; }, { getText: (state: { text: string; agent: string; extension: string; factory: boolean; } & PiniaCustomStateProperties<{ text: string; agent: string; extension: string; factory: boolean; }>) => string; getAccess: (state: ...' is not assignable to parameter of type 'StoreDefinition<string, StateTree, _GettersTree<StateTree>, _ActionsTree>'.
  Property 'updateAccess' is missing in type '_ActionsTree' but required in type '{ updateAccess({ agent, extension, factory }: AccessState): void; }'.
  ```...