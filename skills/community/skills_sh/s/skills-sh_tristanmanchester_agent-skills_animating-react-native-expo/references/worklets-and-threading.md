# Worklets & threading (Reanimated 4)

## Mental model

- **RN Runtime**: “normal JS thread” (React state, navigation, network, etc.).
- **UI Runtime**: a separate JS runtime used to run *worklets* on the UI thread.

Reanimated uses worklets to calculate styles and react to events on the UI thread.

Reference: https://docs.swmansion.com/react-native-reanimated/docs/guides/worklets/

## Defining worklets

Mark a function with a `'worklet'` directive.

```ts
function clamp01(x: number) {
  'worklet';
  return Math.max(0, Math.min(1, x));
}
```

Most Reanimated hooks (e.g. `useAnimatedStyle`) and Gesture Handler callbacks are workletised automatically.

## Scheduling across threads

### Run a worklet on the UI runtime
Use `scheduleOnUI` when you need to manually hop to UI.

### Run JS from a worklet (UI → RN)
Use `scheduleOnRN`.

```ts
import { scheduleOnRN } from 'react-native-worklets';

function Example({ onDone }: { onDone: () => void }) {
  // onDone is JS (RN runtime)
  const tap = Gesture.Tap().onEnd(() => {
    // worklet (UI runtime)
    scheduleOnRN(onDone);
  });
}
```

Important constraint (from the docs): functions passed to `scheduleOnRN` must be defined in RN-runtime scope (module scope or the component body). Don’t create them inside a worklet/animation callback.

Docs: https://docs.swmansion.com/react-native-reanimated/docs/guides/worklets/

## Migration notes (Reanimated 3 → 4)

Reanimated 4 moves worklet/threading helpers into `react-native-worklets`:
- `runOnJS` → `scheduleOnRN`
- `runOnUI` → `scheduleOnUI`
- `executeOnUIRuntimeSync` → `runOnUISync`

Also update Babel plugin:
- `react-native-reanimated/plugin` → `react-native-worklets/plugin`

Migration guide: https://docs.swmansion.com/react-native-reanimated/docs/guides/migration-from-3.x/

## Closure capture: avoid accidental “big object” capture

Worklets capture only referenced variables, but referencing a property of a big object can still capture the whole object. The docs recommend extracting primitives first.

```ts
// BAD: theme is huge; referencing theme.color can capture the whole object
const theme = getTheme();
const style = useAnimatedStyle(() => ({ backgroundColor: theme.color }));

// GOOD: capture only the primitive
const theme = getTheme();
const bg = theme.color;
const style = useAnimatedStyle(() => ({ backgroundColor: bg }));
```

Docs: https://docs.swmansion.com/react-native-reanimated/docs/guides/worklets/
