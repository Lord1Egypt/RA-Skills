# Reanimated 4 CSS transitions & animations (quick reference)

Use these when you want “animate on style change” rather than writing worklets.

## CSS transitions

Minimal:

```tsx
<Animated.View
  style={{
    width: expanded ? 260 : 180,
    transitionProperty: 'width',
    transitionDuration: 220,
  }}
/>
```

Key properties (official docs):
- `transitionProperty`: which property (or array of properties) should transition.
- `transitionDuration`: how long the transition lasts.
- `transitionDelay`, `transitionTimingFunction`, `transitionBehavior`.

Docs:
- Category overview: https://docs.swmansion.com/react-native-reanimated/docs/category/css-transitions/
- `transitionProperty`: https://docs.swmansion.com/react-native-reanimated/docs/css-transitions/transition-property/

Important remarks from `transitionProperty` docs:
- You need `transitionDuration` alongside `transitionProperty`.
- Discrete props (e.g. `flexDirection`, `justifyContent`) can’t transition smoothly; use Layout Animations.
- Avoid `transitionProperty: 'all'` (performance risk).

## CSS animations (keyframes)

Minimal:

```tsx
<Animated.View
  style={{
    animationName: {
      from: { transform: [{ scale: 0.95 }] },
      to: { transform: [{ scale: 1.05 }] },
    },
    animationDuration: '600ms',
  }}
/>
```

Docs:
- `animationName`: https://docs.swmansion.com/react-native-reanimated/docs/css-animations/animation-name/

Rules of thumb:
- Prefer transitions for “state flips” (collapsed/expanded, selected/unselected).
- Prefer animations (keyframes) for looping, staged motion, and micro-interactions.
- Prefer shared values/worklets for gestures and scroll.
