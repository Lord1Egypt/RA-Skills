---
number: 8952
title: Conditional properties through discriminated unions and intersections in TypeScript
type: other
state: open
created: 2023-08-10
url: "https://github.com/vuejs/core/issues/8952"
reactions: 88
comments: 13
labels: "[scope: types, :cake: p2-nice-to-have, scope: script-setup]"
---

# Conditional properties through discriminated unions and intersections in TypeScript

### What problem does this feature solve?

https://github.com/vuejs/core/issues/7553
Reopening this because I believe the problem is not solved. It is still impossible to use coditional props. 

Just try this after `npm create vue@latest` inside HelloWorld component

```vue
<script setup lang="ts">
interface CommonProps {
  size?: 'xl' | 'l' | 'm' | 's' | 'xs'
}

type ConditionalProps =
  | {
      color?: 'normal' | 'primary' | 'secondary'
      appearance?: 'normal' | 'outline' | 'text'
    }
  | {
      color: 'white'
      appearance: 'outline'
    }

type Props = CommonProps & ConditionalProps
defineProps<Props>()
</script>
``` 

and then try to use it 

<img width="437" alt="image" src="https://github.com/vuejs/core/assets/8502021/54ecbb48-c617-4c0c-8283-f4f4fc7fb8f9">

Theoretically it should not allow us to use both. That is, there can't be color="white" appearance="text" only color="white" appearance="outline"

### What does the proposed API look like?

```typescript
{
      color?: 'normal' | 'primary' | 'secondary'
      appearance?: 'normal' | 'outline' | 'text'
    }
  | {
      color: 'white'
      appearance: 'outline'
    }
``` 

---

## Top Comments

**@johnsoncodehk** [maintainer] (+5):

This is a type restriction of defineComponent, as a current solution you can use generic. This will bypass defineComponent and define the component as a functional component.

```html
<script setup lang="ts" generic="T">
interface CommonProps {
  size?: 'xl' | 'l' | 'm' | 's' | 'xs'
}
// ...
</script>
```

**@Sengulair** (+6):

> @johnsoncodehk while props with a discriminator work now in the playground (e.g. `color` in the example above), two different props as in my comment are still not possible as far as I see.↳

It's mostly because of how Typescript is designed due to its structural type system and how Typescript does checks with unions. So in your example, if we simplify it for Typescript, it would be smth like this:
```ts
type Props = { one: string } | { other: number };

const Component = (props: Props) => {};

Component({ one: '123', other: 1 }) // no errors
```...

**@TheAlexLichter** (+9):

Added another simple example wit...