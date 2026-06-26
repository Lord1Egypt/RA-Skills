# Animation Components Reference

All components are in `src/components/animations/` and exported from `index.ts`.

## Primitives

### FadeIn

Opacity fade entrance animation.

```tsx
import { FadeIn } from "./components/animations";

<FadeIn delay={0} duration={20}>
  <div>Content fades in</div>
</FadeIn>
```

Props:
- `delay?: number` — Frame delay before animation starts (default: 0)
- `duration?: number` — Animation duration in frames (default: 20)
- `children: React.ReactNode`

### ScaleIn

Scale-up entrance animation.

```tsx
<ScaleIn delay={5} from={0.5}>
  <div>Content scales up</div>
</ScaleIn>
```

Props:
- `delay?: number` — Frame delay (default: 0)
- `from?: number` — Starting scale (default: 0)
- `children: React.ReactNode`

### SlideIn

Directional slide entrance.

```tsx
<SlideIn direction="left" delay={10}>
  <div>Slides in from left</div>
</SlideIn>
```

Props:
- `direction?: "left" | "right" | "top" | "bottom"` — Slide direction (default: "left")
- `delay?: number` — Frame delay (default: 0)
- `distance?: number` — Slide distance in pixels (default: 100)
- `children: React.ReactNode`

### TypewriterText

Character-by-character text reveal.

```tsx
<TypewriterText text="Hello World" startFrame={0} charsPerFrame={0.5} />
```

Props:
- `text: string` — Text to reveal
- `startFrame?: number` — Frame to start typing (default: 0)
- `charsPerFrame?: number` — Characters revealed per frame (default: 0.5)
- `fontSize?: number` — Font size
- `color?: string` — Text color
- `fontFamily?: string` — Font family

### WordHighlight

Word-by-word highlight effect.

```tsx
<WordHighlight
  text="Each word highlights in sequence"
  highlightColor="#39E508"
  wordsPerFrame={0.1}
/>
```

Props:
- `text: string` — Text content
- `highlightColor?: string` — Highlight color (default: "#39E508")
- `wordsPerFrame?: number` — Words highlighted per frame
- `fontSize?: number`
- `color?: string`

## Data Visualization

### AnimatedBarChart

Animated bar chart with spring physics.

```tsx
<AnimatedBarChart
  data={[
    { label: "A", value: 80, color: "#3b82f6" },
    { label: "B", value: 60, color: "#8b5cf6" },
  ]}
  width={800}
  height={400}
/>
```

Props:
- `data: Array<{ label: string; value: number; color?: string }>` — Chart data
- `width?: number` — Chart width (default: 800)
- `height?: number` — Chart height (default: 400)
- `barWidth?: number` — Individual bar width
- `delay?: number` — Animation delay in frames

### AnimatedLineChart

Animated line chart with path drawing.

```tsx
<AnimatedLineChart
  data={[10, 25, 40, 35, 60, 80]}
  width={800}
  height={400}
  color="#3b82f6"
/>
```

Props:
- `data: number[]` — Data points
- `width?: number` — Chart width
- `height?: number` — Chart height
- `color?: string` — Line color
- `strokeWidth?: number` — Line width

### AnimatedPieChart

Animated pie chart with segment reveals.

```tsx
<AnimatedPieChart
  data={[
    { label: "A", value: 40, color: "#3b82f6" },
    { label: "B", value: 30, color: "#8b5cf6" },
    { label: "C", value: 30, color: "#ec4899" },
  ]}
  radius={150}
/>
```

Props:
- `data: Array<{ label: string; value: number; color: string }>` — Segments
- `radius?: number` — Pie radius (default: 150)

## SVG Drawing

### SineWave

Animated sine wave SVG.

```tsx
<SineWave
  width={800}
  height={200}
  amplitude={80}
  frequency={2}
  color="#3b82f6"
/>
```

Props:
- `width?: number` — SVG width
- `height?: number` — SVG height
- `amplitude?: number` — Wave amplitude
- `frequency?: number` — Wave frequency (number of full cycles visible)
- `color?: string` — Stroke color
- `strokeWidth?: number` — Line width
- `phaseSpeed?: number` — Phase animation speed (radians per frame, default: 0.05)
- `phaseOffset?: number` — Initial phase offset
- `progressiveDraw?: boolean` — Reveal wave from left to right
- `drawDuration?: number` — Duration of progressive draw in frames
- `delay?: number` — Delay in frames before animation starts
- `resolution?: number` — Number of sample points (default: 200)
- `centerY?: number` — Vertical center offset
- `style?: React.CSSProperties` — Custom style

### CoordinateSystem

Animated coordinate axes with labels.

```tsx
<CoordinateSystem
  width={600}
  height={400}
  xLabel="Time"
  yLabel="Amplitude"
/>
```

Props:
- `width?: number` — SVG width
- `height?: number` — SVG height
- `xLabel?: string` — X-axis label
- `yLabel?: string` — Y-axis label
- `color?: string` — Axis color
- `showGrid?: boolean` — Show grid lines

### AnimatedPath

SVG path drawing animation (stroke-dashoffset technique).

```tsx
<AnimatedPath
  d="M 0 100 Q 50 0 100 100 Q 150 200 200 100"
  color="#3b82f6"
  duration={30}
/>
```

Props:
- `d: string` — SVG path data
- `color?: string` — Stroke color
- `strokeWidth?: number` — Line width
- `duration?: number` — Drawing duration in frames

## Layout

### StaggeredList

Staggered list item entrance animation.

```tsx
<StaggeredList
  items={["Item 1", "Item 2", "Item 3"]}
  staggerDelay={5}
/>
```

Props:
- `items: string[]` — List items
- `staggerDelay?: number` — Delay between items in frames (default: 5)
- `fontSize?: number`
- `color?: string`

### CountUp

Number counting animation.

```tsx
<CountUp from={0} to={1000} duration={60} fontSize={72} />
```

Props:
- `from?: number` — Start value (default: 0)
- `to: number` — End value
- `duration?: number` — Animation duration in frames
- `fontSize?: number`
- `color?: string`
- `prefix?: string` — Text before number (e.g. "$")
- `suffix?: string` — Text after number (e.g. "%")
