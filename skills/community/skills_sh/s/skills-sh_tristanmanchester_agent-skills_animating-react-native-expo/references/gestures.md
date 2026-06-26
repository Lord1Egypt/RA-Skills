# Gestures (RNGH 3 + Reanimated 4)

## Root setup (required)

Wrap your app with `GestureHandlerRootView` near the root.

```tsx
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <ActualApp />
    </GestureHandlerRootView>
  );
}
```

Official installation notes:
- Root view defaults to `flex: 1`; keep it if you override styles.
- Gestures won’t be recognised outside the root view.
- Nested roots are OK: only the top-most is used.
- For Modals on Android, wrap the Modal’s content with a root view.

Docs: https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/installation/

## GestureDetector basics

- `GestureDetector` attaches a gesture (or composed gesture) to a subtree.
- RNGH 3 supports both the **hook API** and **builder pattern**.
- Avoid nesting detectors that use different API styles.
- Avoid reusing the same gesture instance across multiple detectors.

Docs: https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/gesture-detectors/

## Default: hook API (RNGH 3)

```tsx
import { GestureDetector, usePanGesture } from 'react-native-gesture-handler';
import Animated, { useSharedValue, useAnimatedStyle } from 'react-native-reanimated';

export function DragBox() {
  const x = useSharedValue(0);
  const y = useSharedValue(0);

  const pan = usePanGesture({
    onUpdate: (e) => {
      x.value = e.translationX;
      y.value = e.translationY;
    },
  });

  const style = useAnimatedStyle(() => ({
    transform: [{ translateX: x.value }, { translateY: y.value }],
  }));

  return (
    <GestureDetector gesture={pan}>
      <Animated.View style={[{ width: 80, height: 80 }, style]} />
    </GestureDetector>
  );
}
```

RNGH 3 migration notes:
- The hook API replaces builder-style chaining; config is passed as an object.
- Some callback names changed (e.g. `onStart` → `onActivate`, `onEnd` → `onDeactivate`).
- `onChange` is removed; use `change*` values from `onUpdate`.

Docs: https://docs.swmansion.com/react-native-gesture-handler/docs/guides/upgrading-to-3/

## Gesture composition & interactions

RNGH 3 recommends answering: “Are all gestures attached to the same component?”
- If yes: use **composition hooks** to bundle gestures into one object for a `GestureDetector`.
- If no: use relation properties (e.g. `simultaneousWith`, `requireToFail`, etc.).

Docs: https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/gesture-composition/

Example (competing gestures so pan doesn’t move after long-press activates):

```ts
const pan = usePanGesture({ /* ... */ });
const longPress = useLongPressGesture({ /* ... */ });
const gesture = useCompetingGestures(pan, longPress);
```

(See the composition page for full examples and other hooks.)

## “UI thread first” rule

Keep gesture callbacks workletised and update **shared values**. Bridge to JS only for side-effects (navigation, analytics, React state), using `scheduleOnRN` (see `worklets-and-threading.md`).
