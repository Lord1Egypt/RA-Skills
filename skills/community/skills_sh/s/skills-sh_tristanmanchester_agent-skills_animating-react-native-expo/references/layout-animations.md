# Layout animations (enter/exit/layout transitions)

Use layout animations when components:
- mount/unmount (entering/exiting)
- change layout (position/size changes because of reflow)

## Entering / exiting

```tsx
import Animated, { FadeIn, FadeOut } from 'react-native-reanimated';

export function Item({ visible }: { visible: boolean }) {
  return visible ? <Animated.View entering={FadeIn} exiting={FadeOut} /> : null;
}
```

Docs: https://docs.swmansion.com/react-native-reanimated/docs/layout-animations/entering-exiting-animations/

Notes from the docs:
- Prefer defining builders outside components or memoising them for performance.
- On the New Architecture, `nativeID` is used internally for entering animations; don’t overwrite it. Some components overwrite `nativeID` of children—wrap with a plain `View` if animations don’t run.
- View flattening can cause a removed parent not to wait for exiting animations; mitigate with `collapsable={false}` when needed.

## Layout transitions

```tsx
import Animated, { LinearTransition } from 'react-native-reanimated';

export function ResizingBox() {
  return <Animated.View layout={LinearTransition} />;
}
```

Docs: https://docs.swmansion.com/react-native-reanimated/docs/layout-animations/layout-transitions/

## FlatList item layout animations

```tsx
import Animated, { LinearTransition } from 'react-native-reanimated';

<Animated.FlatList
  data={data}
  renderItem={renderItem}
  itemLayoutAnimation={LinearTransition}
/>
```

Docs: https://docs.swmansion.com/react-native-reanimated/docs/layout-animations/list-layout-animations/

## Skipping entering/exiting animations

Wrap a subtree with `LayoutAnimationConfig`:

```tsx
import { LayoutAnimationConfig } from 'react-native-reanimated';

<LayoutAnimationConfig skipEntering>
  {show && <Animated.View entering={PinwheelIn} exiting={PinwheelOut} />}
</LayoutAnimationConfig>
```

Docs: https://docs.swmansion.com/react-native-reanimated/docs/layout-animations/layout-animation-config/
