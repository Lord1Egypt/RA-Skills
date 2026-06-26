# Component Library API

Reference for the animation components in `components/index.tsx`.

## `<FadeIn>`

```tsx
<FadeIn start={0} duration={15} from={0} to={1}>
  <div>Content</div>
</FadeIn>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `start` | number | — | Frame to begin fade |
| `duration` | number | 15 | Fade duration in frames |
| `from` | number | 0 | Starting opacity |
| `to` | number | 1 | Ending opacity |

## `<SlideIn>`

```tsx
<SlideIn start={20} duration={20} direction="up" distance={60}>
  <div>Content</div>
</SlideIn>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `start` | number | — | Start frame |
| `duration` | number | 20 | Slide duration |
| `direction` | `"up" \| "down" \| "left" \| "right"` | "up" | Slide direction |
| `distance` | number | 60 | Pixel distance to travel |

## `<ScaleIn>`

```tsx
<ScaleIn start={10} duration={15} from={0.8} to={1}>
  <div>Content</div>
</ScaleIn>
```

Uses `back(1.2)` easing for a subtle overshoot.

## `<Typewriter>`

```tsx
<Typewriter text="Hello world" start={0} speed={2} />
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | string | — | Text to type |
| `start` | number | — | Start frame |
| `speed` | number | 2 | Frames per character |

## `<ProgressBar>`

```tsx
<ProgressBar start={0} end={60} color="#6366f1" height={4} />
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `start` | number | — | Frame to start filling |
| `end` | number | — | Frame to reach 100% |
| `color` | string | `#6366f1` | Bar color |
| `height` | number | 4 | Bar height in px |

## `<FloatingOrb>`

```tsx
<FloatingOrb x="20%" y="30%" size={300} color="rgba(99,102,241,0.1)" speed={90} />
```

Background ambient element. Position with CSS `left`/`top`.

## `<DriftingGrid>`

```tsx
<DriftingGrid color="rgba(99,102,241,0.04)" size={50} speed={0.2} />
```

Animated CSS grid background pattern.

## `<CountUp>`

```tsx
<CountUp value={1000} start={0} duration={60} prefix="$" suffix="K" decimals={1} />
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | number | — | Final value to count to |
| `start` | number | — | Start frame |
| `duration` | number | — | Count duration in frames |
| `prefix` | string | `""` | Prefix string |
| `suffix` | string | `""` | Suffix string |
| `decimals` | number | 0 | Decimal places |

## `<PulseRing>`

```tsx
<PulseRing start={0} color="#6366f1" size={200} />
```

Expanding ring that fades out — good for call-attention effects.

## `<StaggerChildren>`

```tsx
<StaggerChildren start={10} stagger={15} renderChild={(child, style) => (
  <div style={style}>{child}</div>
)}>
  <Item1 />
  <Item2 />
  <Item3 />
</StaggerChildren>
```
