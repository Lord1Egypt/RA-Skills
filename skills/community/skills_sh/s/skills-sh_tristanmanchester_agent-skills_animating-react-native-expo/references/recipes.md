# Recipes (copy/paste)

These are “good defaults” that follow the skill’s rules:
- per-frame updates in worklets (UI runtime)
- shared values as state
- bridge to JS only with `scheduleOnRN`

## 1) Tap-to-scale (double-tap)

(Expo shows a similar pattern in its gestures tutorial.)

```tsx
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, { useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';

export function DoubleTapScale({ size = 120 }: { size?: number }) {
  const s = useSharedValue(1);

  const doubleTap = Gesture.Tap()
    .numberOfTaps(2)
    .onStart(() => {
      s.value = s.value === 1 ? 2 : 1;
    });

  const style = useAnimatedStyle(() => ({
    transform: [{ scale: withSpring(s.value) }],
  }));

  return (
    <GestureDetector gesture={doubleTap}>
      <Animated.View style={[{ width: size, height: size }, style]} />
    </GestureDetector>
  );
}
```

## 2) Swipe-to-delete row (with JS callback)

```tsx
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withTiming,
} from 'react-native-reanimated';
import {
  GestureDetector,
  usePanGesture,
} from 'react-native-gesture-handler';
import { scheduleOnRN } from 'react-native-worklets';

const THRESHOLD = 120;

export function SwipeToDeleteRow({
  width,
  onDelete,
  children,
}: {
  width: number;
  onDelete: () => void;
  children: React.ReactNode;
}) {
  const x = useSharedValue(0);

  const pan = usePanGesture({
    onUpdate: (e) => {
      // Only allow swiping left
      x.value = Math.min(0, e.translationX);
    },
    onDeactivate: (_, success) => {
      // success indicates the gesture ended in ACTIVE
      const shouldDelete = x.value < -THRESHOLD;
      x.value = withTiming(shouldDelete ? -width : 0, { duration: 180 }, (finished) => {
        if (finished && shouldDelete) {
          scheduleOnRN(onDelete);
        }
      });
    },
  });

  const style = useAnimatedStyle(() => ({
    transform: [{ translateX: x.value }],
  }));

  return (
    <GestureDetector gesture={pan}>
      <Animated.View style={style}>{children}</Animated.View>
    </GestureDetector>
  );
}
```

Notes:
- `onDelete` must be defined in JS scope.
- Don’t allocate new functions inside the worklet callback you pass to `withTiming` if you intend to `scheduleOnRN` them.

## 3) Pinch + pan (simultaneous)

If you’re using RNGH 3 hook API, compose gestures with composition hooks.

```tsx
import {
  GestureDetector,
  usePanGesture,
  usePinchGesture,
  useSimultaneousGestures,
} from 'react-native-gesture-handler';
import Animated, { useSharedValue, useAnimatedStyle } from 'react-native-reanimated';

export function PinchPan() {
  const tx = useSharedValue(0);
  const ty = useSharedValue(0);
  const scale = useSharedValue(1);

  const pan = usePanGesture({
    onUpdate: (e) => {
      tx.value = e.translationX;
      ty.value = e.translationY;
    },
  });

  const pinch = usePinchGesture({
    onUpdate: (e) => {
      scale.value = e.scale;
    },
  });

  const gesture = useSimultaneousGestures(pan, pinch);

  const style = useAnimatedStyle(() => ({
    transform: [
      { translateX: tx.value },
      { translateY: ty.value },
      { scale: scale.value },
    ],
  }));

  return (
    <GestureDetector gesture={gesture}>
      <Animated.View style={[{ width: 220, height: 220 }, style]} />
    </GestureDetector>
  );
}
```

Composition reference: https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/gesture-composition/

## 4) Layout-driven accordion (layout animations)

```tsx
import Animated, { LinearTransition, FadeIn, FadeOut } from 'react-native-reanimated';

export function Accordion({ open, children }: { open: boolean; children: React.ReactNode }) {
  return (
    <Animated.View layout={LinearTransition}>
      {open && (
        <Animated.View entering={FadeIn} exiting={FadeOut}>
          {children}
        </Animated.View>
      )}
    </Animated.View>
  );
}
```

## 5) Simple state change: CSS transitions

```tsx
import Animated from 'react-native-reanimated';

export function TogglePill({ on }: { on: boolean }) {
  return (
    <Animated.View
      style={{
        width: on ? 64 : 40,
        opacity: on ? 1 : 0.6,
        transitionProperty: ['width', 'opacity'],
        transitionDuration: 180,
      }}
    />
  );
}
```
