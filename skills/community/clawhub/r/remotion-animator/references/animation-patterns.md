# Animation Patterns

Quick cookbook of common animation effects with Remotion.

## Timing

Use frame-based timing. At 30fps:
```
1 second = 30 frames
0.5 seconds = 15 frames
0.1 seconds = 3 frames
```

## Easing

```
Easing.out(Easing.cubic)        // smooth deceleration
Easing.out(Easing.back(1.2))    // slight overshoot
Easing.inOut(Easing.quad)       // symmetric ease
Easing.linear                   // constant speed
```

## Patterns

### Staggered list

Render items with incremental start delays:

```tsx
{items.map((item, i) => (
  <FadeIn start={20 + i * 15} duration={15}>
    <div>{item}</div>
  </FadeIn>
))}
```

### Looping animation

Use frame modulo for infinite motion:

```tsx
const drift = frame * 0.2;
const looped = drift % 50;
```

For ping-pong (back-and-forth):

```tsx
const angle = frame / 60;
const pingpong = Math.sin(angle); // -1 to 1
```

### Exit animation

Define both an enter and an exit window:

```tsx
const enter = interpolate(frame, [start, start + 10], [0, 1]);
const exit = interpolate(frame, [end - 10, end], [1, 0]);
const opacity = enter * exit;
```

### Text splitting

Word-by-word reveal:

```tsx
const words = text.split(" ");
{words.map((word, i) => {
  const wStart = start + i * 5;
  const opacity = interpolate(frame, [wStart, wStart + 4], [0, 1]);
  return <span style={{ opacity }}>{word} </span>;
})}
```

Character-by-character:

```tsx
const chars = Math.min(text.length, Math.floor((frame - start) / 2));
const visible = text.slice(0, chars);
```

### Reusing a component with variants

Pass timing as props:

```tsx
const AnimatedMetric = ({ label, value, start }) => (
  <FadeIn start={start}>
    <CountUp value={value} start={start + 10} duration={40} />
    <div>{label}</div>
  </FadeIn>
);
```

## Audio Sync

Load audio in your composition:

```tsx
import { Audio, staticFile } from "remotion";

// In your component:
<Audio src={staticFile("audio.mp3")} />
```

Derive duration from audio metadata:

```tsx
import { getVideoMetadata } from "@remotion/media-utils";

const metadata = await getVideoMetadata(staticFile("audio.mp3"));
const durationInFrames = Math.ceil(metadata.durationInSeconds * 30);
```

## Responsive Text

Scale font size based on video dimensions:

```tsx
const { width } = useVideoConfig();
const fontSize = width / 1920 * 72; // 72px at 1920w
```

## Custom Colors via Props

Pass a palette config for theming:

```tsx
const THEMES = {
  dark: { bg: "#0a0a0f", text: "#ffffff", accent: "#6366f1" },
  light: { bg: "#ffffff", text: "#1a1a2e", accent: "#6366f1" },
};
```
