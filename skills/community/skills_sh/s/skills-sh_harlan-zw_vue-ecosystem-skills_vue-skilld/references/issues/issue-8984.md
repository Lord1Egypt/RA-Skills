---
number: 8984
title: "[TypeScript] Allow HTML attributes to Vue component with type, if an attribute has the same name with the component's prop, keep the prop type instead of intersection types"
type: other
state: open
created: 2023-08-16
url: "https://github.com/vuejs/core/issues/8984"
reactions: 10
comments: 6
labels: "[scope: types]"
---

# [TypeScript] Allow HTML attributes to Vue component with type, if an attribute has the same name with the component's prop, keep the prop type instead of intersection types

### Vue version

3.3.4

### Link to minimal reproduction

https://stackblitz.com/edit/vue3-typescript-vue-cli-starter-7pb4bu?file=src%2Fcomponents%2FHelloWorld.vue,src%2Fvue.d.ts,src%2FApp.vue

### Steps to reproduce

The Vue component cannot accept HTML attributes with type in **TypeScript**, or get `any` type.

It won't get suggestion of HTML attributes when typing in a component props. When typing a native HTML event in component, its parameters will get `any` type, so TypeScript will report an error.

The API shows that we can extends the props for all components with types.

Just create a `.d.ts` file in the project.

> types/vue.d.ts
```typescript
declare module "vue" {
    export interface AllowedComponentProps extends HTMLAttributes {}
}
```

Then all components will accept HTML attributes in TypeScript.

If I create a component:

> components/MyComponent.vue
```vue
<script setup lang="ts">
    defineProps<{
        id: number;
    }>();

    defineEmits<{
        click: [num: number];
    }>();
</script>
```

And use it with:
```vue
<MyComponent
    :id="1"
    lang="en"
    @click="num => handleNumber(num)"
    @mouseenter="e => handleMouseEvent(e)"
/>
```

### What is expected?

The `id` prop is defined in MyComponent, so it will use the prop type `number` instead of HTML attribute `id` type `string`;

The `lang` prop isn't defined in MyComponent, so it will use HTML attribute `lang` type `string` instead of `unknown` or `any`.

The `click` event is defined in MyComponent, so it will use the emit type `(num: number) => void` instead of HTML attribute `onClick` type `(payload: MouseEvent) => void`;

The `mouseenter` event isn't defined in MyComponent, so it will use HTML attribute `onMouseenter` type `(payload: MouseEvent) => void` instead of `unknown` or `any`.

### What is actually happening?

...