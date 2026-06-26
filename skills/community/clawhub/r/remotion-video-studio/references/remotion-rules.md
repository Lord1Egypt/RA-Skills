# Remotion Core Rules Reference

Key Remotion patterns for quick reference.

## Frame-driven Animation

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

const frame = useCurrentFrame();
const { fps, durationInFrames } = useVideoConfig();

// Linear interpolation
const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });

// Spring physics
const scale = spring({ frame, fps, config: { damping: 200 } });

// With delay
const delayed = spring({ frame, fps, config: { damping: 200 }, delay: 15 });
```

## Sequencing

```tsx
import { Sequence } from "remotion";

<Sequence from={0} durationInFrames={90}><Scene1 /></Sequence>
<Sequence from={90} durationInFrames={90}><Scene2 /></Sequence>
```

## Transitions

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <Scene1 />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={90}>
    <Scene2 />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

## Audio & Static Files

```tsx
import { Audio, staticFile, Img } from "remotion";

<Audio src={staticFile("audio/narration.mp3")} />
<Audio src={staticFile("audio/bg.mp3")} volume={0.3} />
<Img src={staticFile("images/logo.png")} />
```

## Compositions

```tsx
import { Composition } from "remotion";

<Composition
  id="MyVideo"
  component={MyComponent}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{ title: "Hello" }}
  calculateMetadata={({ props }) => ({
    durationInFrames: props.slides.length * 90,
    fps: 30,
    width: 1920,
    height: 1080,
  })}
/>
```

## SVG Animation Pattern

```tsx
// Draw SVG path with stroke-dashoffset
const pathLength = 500;
const draw = interpolate(frame, [0, 60], [pathLength, 0], {
  extrapolateRight: "clamp",
});

<svg>
  <path
    d="M 0 100 Q 50 0 100 100"
    stroke="#3b82f6"
    strokeWidth={2}
    fill="none"
    strokeDasharray={pathLength}
    strokeDashoffset={draw}
  />
</svg>
```

## CLI Rendering

```bash
# Basic render
npx remotion render src/index.ts MyComposition out.mp4

# With props
npx remotion render src/index.ts MyComposition out.mp4 --props build/render-props.json

# With options
npx remotion render src/index.ts MyComposition out.mp4 --concurrency 4 --codec h264 --crf 18
```
