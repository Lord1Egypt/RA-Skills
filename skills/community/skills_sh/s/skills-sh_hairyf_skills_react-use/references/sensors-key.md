---
name: sensors-key
description: Execute handler when keyboard key is used with useKey hook
---

# useKey

React UI sensor hook that executes a `handler` when a keyboard key is used.

## Usage

```jsx
import {useKey} from 'react-use';

const Demo = () => {
  const [count, set] = useState(0);
  const increment = () => set(count => ++count);
  useKey('ArrowUp', increment);

  return (
    <div>
      Press arrow up: {count}
    </div>
  );
};
```

Or as render-prop:

```jsx
import UseKey from 'react-use/lib/component/UseKey';

<UseKey filter='a' fn={() => alert('"a" key pressed!')} />
```

## Reference

```js
useKey(filter, handler, options?, deps?)
```

- **`filter`**: `string | (event: KeyboardEvent) => boolean` - key to listen for or predicate function
- **`handler`**: `(event: KeyboardEvent) => void` - function to execute when key is pressed
- **`options`**: `object` - optional configuration
  - `event`: `'keydown' | 'keyup'` - event type, defaults to 'keydown'
- **`deps`**: `DependencyList` - dependency array (like useEffect)

## Examples

```js
useKey('a', () => alert('"a" pressed'));

const predicate = (event) => event.key === 'a'
useKey(predicate, handler, {event: 'keyup'});
```

## Key Points

- Can use string key names or predicate functions
- Supports both keydown and keyup events
- Accepts dependency array for conditional execution

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useKey.md
-->
