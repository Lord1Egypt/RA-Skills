---
name: state-observable
description: Track latest value of Observable with useObservable hook
---

# useObservable

React state hook that tracks the latest value of an `Observable`.

## Usage

```jsx
import {useObservable} from 'react-use';

const counter$ = new BehaviorSubject(0);
const Demo = () => {
  const value = useObservable(counter$, 0);

  return (
    <button onClick={() => counter$.next(value + 1)}>
      Clicked {value} times
    </button>
  );
};
```

## Reference

```ts
const value = useObservable<T>(observable: Observable<T>, initialValue?: T): T | undefined;
```

- **`observable`**: RxJS Observable
- **`initialValue`**: optional initial value

## Key Points

- Integrates with RxJS Observables
- Tracks latest emitted value
- Useful for reactive programming

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useObservable.md
-->
