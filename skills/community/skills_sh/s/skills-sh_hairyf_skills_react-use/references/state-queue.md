---
name: state-queue
description: Implement simple FIFO queue with useQueue hook
---

# useQueue

React state hook implements simple FIFO queue.

## Usage

```jsx
import { useQueue } from 'react-use';

const Demo = () => {
  const { add, remove, first, last, size } = useQueue();

  return (
    <div>
      <ul>
        <li>first: {first}</li>
        <li>last: {last}</li>
        <li>size: {size}</li>
      </ul>
      <button onClick={() => add((last || 0) + 1)}>Add</button>
      <button onClick={() => remove()}>Remove</button>
    </div>
  );
};
```

## Reference

```ts
const { add, remove, first, last, size } = useQueue();
```

- **`add(value)`**: add to end of queue
- **`remove()`**: remove from front of queue
- **`first`**: first element
- **`last`**: last element
- **`size`**: queue size

## Key Points

- FIFO (First In First Out) queue
- Simple queue operations
- Useful for task queues

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useQueue.md
-->
