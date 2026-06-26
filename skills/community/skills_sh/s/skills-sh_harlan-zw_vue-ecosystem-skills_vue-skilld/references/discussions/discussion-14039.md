---
number: 14039
title: vue reactivity isn't working when i use it with services.
category: Help/Questions
created: 2025-10-30
url: "https://github.com/orgs/vuejs/discussions/14039"
upvotes: 1
comments: 1
answered: true
---

# vue reactivity isn't working when i use it with services.

I  wanted to use Angular style services.


My service decorators implementation.

```ts
type Constructor<T = any> = new (...args: any[]) => T;
const serviceRegistry = new Map<Constructor, InstanceType<Constructor> | null>();

export function Provide<T extends Constructor>(target: T) {
  serviceRegistry.set(target, null);
  return target;
}

export function Inject<T extends Constructor>(ServiceClass: T): InstanceType<T> {
  let instance = serviceRegistry.get(ServiceClass);
  if (!instance) {
    instance = new ServiceClass();
    serviceRegistry.set(ServiceClass, instance);
  }
  return instance as InstanceType<T>;
}
```


And when I'm using a ref inside these services

```ts
import { Provide } from '@/utils/DI';
import { ref } from 'vue';

@Provide
export class DrawerService {
  isDrawerOpen = ref(false);
  toggleDrawer() {
    this.isDrawerOpen.value = !this.isDrawerOpen.value;
  }
}

```...

---

## Accepted Answer

**@LinusBorg** [maintainer]:

In your specific instance, I think your problem is not one of reactivity, but plain Javascript -the problem is not the ref, but the callback (3rd argument in this code:)

```ts
useClickOutside([drawerRef, triggerRef], drawerService.toggleDrawer, drawerService.isDrawerOpen);
```

`toggleDrawer` is a method on the drawerServerice object. If you decouple the method from the object (by passing just the method to the function as the 3rd argument), then the function looses the `this` context. 

I would assume it will work when you do:

```ts
useClickOutside([drawerRef, triggerRef], () => drawerService.toggleDrawer(), drawerService.isDrawerOpen);
```

or make the `toggleDrawer` function  not loose its `this` scope:

old-school-way:
```ts
@Provide
export class DrawerService {
  isDrawerOpen = ref(false);
  constructor() {
    this.toggleDrawer = this.toggleDrawer.bind(this)
  },
  toggleDrawer() {
    this.isDrawerOpen.value = !this.isDrawerOpen.value;
  }
}
```...