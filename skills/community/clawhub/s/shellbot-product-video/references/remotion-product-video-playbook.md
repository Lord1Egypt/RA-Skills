# Remotion Product Video Playbook

Use this guide when implementing a product marketing video in Remotion.

## 1) Project Shape

Use a composition-driven structure:

- `src/Root.tsx`: Register composition(s)
- `src/ProductVideo.tsx`: Top-level timeline orchestrator
- `src/scenes/*`: One component per scene
- `src/lib/*`: Shared animation helpers and style tokens

Pass a typed plan object to the main composition as props.
Use one bundled starter as the baseline:

- `assets/remotion-product-template` (AIDA classic)
- `assets/templates/cinematic-product-16x9`
- `assets/templates/saas-metrics-16x9`
- `assets/templates/mobile-ugc-9x16`

## 2) Timeline Model

Represent each scene with start/end frames and objective:

```ts
type Scene = {
  id: string;
  stage: "attention" | "interest" | "desire" | "action";
  from: number;
  durationInFrames: number;
  objective: string;
  voiceover: string;
};
```

Render scenes through `Sequence`:

```tsx
{plan.scenes.map((scene) => (
  <Sequence key={scene.id} from={scene.from} durationInFrames={scene.durationInFrames}>
    <SceneRenderer scene={scene} />
  </Sequence>
))}
```

## 3) Animation Principles

- Use `spring()` for entrance/exits that need natural ease.
- Use `interpolate()` for deterministic linear/value mapping.
- Limit simultaneous animated properties to maintain readability.
- Use scale + opacity + position as defaults before complex effects.

## 4) Stage Goals

### Attention

- Introduce pain quickly (first 3-5 seconds).
- Use one strong visual conflict.
- Keep on-screen text short.

### Interest

- Introduce the product as the answer.
- Show mechanism, not exhaustive detail.
- Keep pacing brisk.

### Desire

- Demonstrate real use cases.
- Show before/after outcomes or contextual wins.
- Include proof signals (metric, testimonial snippet, trust indicator).

### Action

- Present one CTA.
- Include clear incentive.
- Keep closing frame readable for at least 2 seconds.

## 5) Audio Layering

- Keep voiceover as primary channel.
- Duck music under narration.
- Add short transitional SFX only when they reinforce movement.
- Avoid dense music during problem framing.

## 6) Transition Strategy

- Use direct cuts when narrative turns are sharp.
- Use quick wipes/slides for momentum shifts.
- Use dissolve/fade only for emotional softening.
- Keep transitions mostly between 8 and 18 frames.

## 7) Rendering Checklist

- Confirm total duration aligns with platform target.
- Verify no scene overlaps unintentionally.
- Confirm text is legible at mobile-safe sizes.
- Check VO/music balance on laptop speakers and phone speakers.
- Render with deterministic props for reproducibility.
