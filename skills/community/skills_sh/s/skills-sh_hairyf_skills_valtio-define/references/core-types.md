---
name: core-types
description: TypeScript types and interfaces for valtio-define
---

# Core Types

Type definitions for store creation and usage.

## StoreDefine

Configuration object passed to `defineStore`:

```tsx
interface StoreDefine<S extends object, A extends ActionsTree, G extends Getters<any>> {
  state: (() => S) | S
  actions?: A & ThisType<A & S & GettersReturnType<G>>
  getters?: G & ThisType<S & GettersReturnType<G>>
}
```

**Key Points:**
* `state`: Initial state object or factory function
* `actions`: Optional object with methods that have `this` bound to state
* `getters`: Optional object with computed properties
* `ThisType` ensures proper type inference for `this` in actions and getters

## Store

The store instance type:

```tsx
type Store<S, A extends Actions<S>, G extends Getters<S>> = {
  $subscribe: Subscribe<S, G>
  $subscribeKey: SubscribeKey<S, G>
  $patch: Patch<S, G>
  $state: S & GettersReturnType<G> & ActionsOmitThisParameter<A>
  $actions: ActionsOmitThisParameter<A>
  $getters: GettersReturnType<G>
  use: (plugin: Plugin) => void
  $signal: Signal<S, G>
} & S & GettersReturnType<G> & ActionsOmitThisParameter<A>
```

**Key Points:**
* Store instance extends state, getters, and actions for direct access
* Internal methods prefixed with `$`
* Actions are transformed to remove `this` parameter (ActionsOmitThisParameter)

## Actions and Getters

```tsx
type Actions<S = any> = Record<string, (this: S, ...args: any) => any>
type Getters<S = any> = Record<string, (this: S) => any>
```

**Key Points:**
* Actions receive `this` bound to the store state
* Getters receive `this` bound to the store state
* Both support full TypeScript inference

## Type Extension for Plugins

Plugins can extend `StoreDefine` via module augmentation:

```tsx
declare module 'valtio-define/types' {
  export interface StoreDefine<S extends object, A extends ActionsTree, G extends Getters<any>> {
    myPlugin?: {
      someOption?: boolean
    }
  }
}
```

This allows plugins to add typed options to the store definition.
