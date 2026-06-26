---
name: animations-tween
description: Tween number from 0 to 1 with useTween hook
---

# useTween

React animation hook that tweens a number between 0 and 1.

## Usage

```jsx
import {useTween} from 'react-use';

const Demo = () => {
  const t = useTween();

  return (
    <div>
      Tween: {t}
    </div>
  );
};
```

## Reference

```ts
useTween(easing?: string, ms?: number, delay?: number): number
```

- **`easing`**: `string` - one of the valid [easing names](https://github.com/streamich/ts-easing/blob/master/src/index.ts), defaults to `inCirc`
- **`ms`**: `number` - milliseconds for how long to keep re-rendering component, defaults to `200`
- **`delay`**: `number` - delay in milliseconds after which to start re-rendering component, defaults to `0`
- Returns: `number` - value that begins with 0 and ends with 1 when animation ends

## Key Points

- Tweens from 0 to 1
- Supports various easing functions
- Configurable duration and delay
- Useful for progress animations

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useTween.md
-->
