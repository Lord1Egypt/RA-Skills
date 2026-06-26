---
name: animations-spring
description: Interpolate number over time according to spring dynamics with useSpring hook
---

# useSpring

React animation hook that updates a single numeric value over time according to spring dynamics.

## Usage

```jsx
import useSpring from 'react-use/lib/useSpring';

const Demo = () => {
  const [target, setTarget] = useState(50);
  const value = useSpring(target);

  return (
    <div>
      {value}
      <br />
      <button onClick={() => setTarget(0)}>Set 0</button>
      <button onClick={() => setTarget(100)}>Set 100</button>
    </div>
  );
};
```

## Requirements

Install [`rebound`](https://github.com/facebook/rebound-js) peer dependency:

```bash
npm add rebound
# or
yarn add rebound
```

## Reference

```js
const currentValue = useSpring(targetValue);
const currentValue = useSpring(targetValue, tension, friction);
```

- **`targetValue`**: `number` - target value to animate to
- **`tension`**: `number` - optional spring tension
- **`friction`**: `number` - optional spring friction
- Returns: `number` - current animated value

## Key Points

- Requires `rebound` as peer dependency
- Must import directly: `import useSpring from 'react-use/lib/useSpring'`
- Provides smooth spring physics animation
- Configurable tension and friction

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useSpring.md
-->
