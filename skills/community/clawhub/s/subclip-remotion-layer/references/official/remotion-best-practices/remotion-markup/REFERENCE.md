---
name: remotion-markup
description: Content, animation and effects best practices
version: 4.0.530
---

> Subclip sandbox: use only pinned, validated imports and native Subclip tools. Package/skill installation, external CLI execution, provider API keys, and standalone project setup are unavailable. Verify managed resources before use; use a supported alternative when unavailable.

This is guidance for writing Remotion React Markup.
If this is not relevant, load Remotion Best Practices instead.

## Preserve user changes

Users may make edits in the code outside of the conversation.

If you detect a surprising change made in the meanwhile, don't overwrite it, assume it was intentional or ask for confirmation.

## General rules

Drive animations using `useCurrentFrame()` and `interpolate()`.  
CSS `transition` or `animation` will not render correctly, they need to refactored.  
Tailwind animation class will not render correctly, they need to be refactored.

Use `Easing.bezier()` and `Easing.spring()` to customize timing.

Structure your markup according to Remotion Interactivity Best Practices

The Studio edits the JSX source node that created an item. Author every
composition registration, clip, scene, layer and sequence that should be
editable independently as its own JSX node, with its editable props inline.
Programmatic loops are suitable when the generated instances are intentionally
controlled as one source template, not when users need to edit the instances
separately.

```tsx
import { useCurrentFrame, Easing, interpolate, Interactive } from "remotion";

export const FadeIn = () => {
  const frame = useCurrentFrame();

  return (
    <Interactive.Div
      name="Title"
      style={{
        opacity: interpolate(frame, [0, 2 * fps], [0, 1], {
          extrapolateRight: "clamp",
          extrapolateLeft: "clamp",
          easing: Easing.bezier(0.16, 1, 0.3, 1),
        }),
      }}
    >
      Hello World!
    </Interactive.Div>
  );
};
```

Keep the `interpolate()` call inline in the `style` prop.
Use `scale`, `translate`, `rotate` CSS properties over `transform`.

```tsx
// 👍 Inline editable keyframes and transform shorthands
style={{
  scale: interpolate(frame, [0, 100], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
    output: 'perceptual-scale' // For `scale` animations, use "output: 'perceptual-scale'"
  }),
  translate: interpolate(frame, [0, 100], ["0px 0px", "100px 100px"], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
  }),
  rotate: interpolate(frame, [0, 100], ["20deg", "90deg"], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
  }),
}}

// 👎 Non-inline values and transform strings become harder to edit in Studio
const scale = interpolate(frame, [0, 100], [0, 1]);

style={{
  transform: `scale(${scale})`,
}}
```

## Assets

Place assets in the `public/` folder at your project root.
Use `staticFile()` to reference files from the `public/` folder.

## Media components

Add video and audio using `<Video>` and `<Audio>` from `@remotion/media`.  
Add images using the `<CanvasImage>` component.
For animated GIFs, APNG, WebP or AVIF images, read [gifs.md](gifs.md). Use imported project-library assets and verify preview and export compatibility.
Use `staticFile()` for files in `public/` or pass a remote URL directly:

```tsx
import { Audio, Video } from "@remotion/media";
import { staticFile, CanvasImage, AnimatedImage } from "remotion";

export const MyComposition = () => {
  return (
    <>
      <Video src={staticFile("video.mp4")} style={{ opacity: 0.5 }} />
      <Audio src={staticFile("audio.mp3")} />
      <CanvasImage
        src={staticFile("logo.png")}
        style={{ width: 100, height: 100 }}
      />
      <Video src="https://remotion.media/video.mp4" />
      <AnimatedImage src={staticFile('nyancat.gif')} />
    </>
  );
};
```

If the composition is primarily a timeline of video or audio clips, read
[video-editing.md](video-editing.md) before choosing its source structure.

## Example scene

```tsx
import {
  AbsoluteFill,
  Easing,
  Interactive,
  interpolate,
  useCurrentFrame,
  useVideoConfig
} from "remotion";

export const Empty = () => {
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      name="Scene"
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'white'
      }}
    >
      <Interactive.Div
        name="Title"
        style={{
          opacity: interpolate(frame, [1 * fps, 2 * fps], [0, 1], {
            extrapolateRight: "clamp",
            extrapolateLeft: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
          fontSize: 88
        }}
      >
        Title
      </Interactive.Div>
      <Interactive.Div
        name="Subtitle"
        style={{
          opacity: interpolate(frame, [2 * fps, 3 * fps, 8 * fps, 10 * fps], [0, 1, 1, 0], {
            extrapolateRight: "clamp",
            extrapolateLeft: "clamp",
            easing: [Easing.bezier(0.16, 1, 0.3, 1), Easing.linear, Easing.bezier(0.16, 1, 0.3, 1)],
          }),
          fontSize: 32
        }}
      >
        Subtitle
      </Interactive.Div>
    </AbsoluteFill>
  );
}
```

## Delaying, trimming

Most components (`<AbsoluteFill>`, `<Interactive.*>` `<Img>`, `<AnimatedImage>`, `<CanvasImage>`, `<HtmlInCanvas>`, `<Solid>`, `<Sequence>` from `remotion`, `<Video>` and `<Audio>` from `@remotion/media`, and more) support the following props:

### from

```tsx
<Img from={1 * fps} {/* ... */}/>
<Video from={1 * fps} {/* ... */}/>
<Interactive.Div from={1 * fps} {/* ... */}/>
```

When the element starts appearing in the timelien.

### durationInFrames

```tsx
<Img durationInFrames={20 * fps} {/* ... */}/>
<Interactive.Div durationInFrames={20 * fps} {/* ... */}/>
```

For how long the layer plays in the timeline.  
For media, pass the natural duration of the media: `<Video durationInFrames={29.322 * fps}/>`

### `trimBefore`

Useful for components whose internal clock should start later:

```tsx
// Trim away first 2 seconds of footage
<Video trimBefore={2 * fps} {/* ... */} />

// `useCurrenFrame()` for children starts at `10 * fps`
<Sequence trimBefore={10 * fps} {/* ... */} />
```

### `trimAfter`

Ends the internal clock at a frame. Measured in the same clock as `trimBefore`, so the layer lasts `(trimAfter - trimBefore) / playbackRate` frames in the timeline unless `durationInFrames` is shorter:

```tsx
// Play the footage from second 2 to second 5
<Video trimBefore={2 * fps} trimAfter={5 * fps} {/* ... */} />

// Children see frames `10 * fps` through `15 * fps - 1`
<Sequence trimBefore={10 * fps} trimAfter={15 * fps} {/* ... */} />
```

### `loop`

Repeats the range between `trimBefore` and `trimAfter`. `durationInFrames` sets the total length. `<Video>` and `<Audio>` may omit `trimAfter` and loop the whole file; other layers need `trimAfter` because they have no intrinsic end:

```tsx
<Video loop durationInFrames={20 * fps} {/* ... */} />
<Sequence trimAfter={2 * fps} durationInFrames={20 * fps} loop {/* ... */} />
```

`<Img>`, `<CanvasImage>`, `<Solid>` and shapes do not support `loop` because their output does not change over time.

### Fallback

If a component does not support these props, wrap it in`<Sequence>` from `remotion`, which has them.

- `layout="absolute-fill"` makes the Sequence behave like AbsoluteFill
- `layout="none"` is "headless" mode, no wrapper element is used.

## Maps


## Text highlights and annotations

See [text-highlights.md](text-highlights.md) for text highlights (highlight markers), circles, underlines, strike-throughs, crossed-off text, boxes.

## Multi-scene videos

See [multi-scene-video.md](multi-scene-video.md) if planning to make a video with multiple subsequent scenes.

## Connected compositions



The extracted component may return a fragment; do not add a DOM wrapper. Preserve sibling order, props, keys, conditional rendering, dimensions, appearance, and timing. Trace values used by the selected markup: move their derivations only when the same scope and lifecycle are preserved, otherwise pass them as props. In particular, moving `useCurrentFrame()` or `useVideoConfig()` across a sequence boundary can change its result; pass the parent value when needed. If the selection or a behavior-preserving connected composition is unclear, ask for clarification instead of guessing.

## Voiceover

See [voiceover.md](voiceover.md) for adding an AI-generated voiceover to Remotion compositions using ElevenLabs TTS.

## Embedding Videos

See [embedding-videos.md](embedding-videos.md) for advanced knowledge about embedding videos - trimming, volume, speed, looping, pitch.

## Embedding Audio

See [audio.md](audio.md) for advanced audio features like trimming, volume, speed, pitch.

## Cropping

See [cropping.md](cropping.md) if needing to crop the visible rectangle of a component.

## Transitions

See [transitions.md](transitions.md) for scene transition patterns.

## Motion blur

When adding motion blur or a movement trail, read [motion-blur.md](motion-blur.md) for the preferred HTML-in-canvas approach, preview requirements, and alternatives.

## Visual and pixel effects

When creating a visual effect, consider whether it is feasible using CSS and HTML, or whether a shader is needed.  
Order or preference:

1. Regular HTML + CSS or other web techniques
2. An effect applied to the element directly (`<Video>`, `<Img>`), or by wrapping the content in [`<HtmlInCanvas>`](html-in-canvas.md), which also accepts `effects`:

- A listed effect via [effects.md](effects.md)
- A custom `createEffect()` via [effects.md](effects.md) when no preset is available.

## 3D content

See [./3d.md](./3d.md) for 3D content in Remotion using Three.js and React Three Fiber.

## Sound effects

When needing to use sound effects, load the [./sfx.md](./sfx.md) file for more information.

## Audio visualization

When needing to visualize audio (spectrum bars, waveforms, bass-reactive effects), load the [./audio-visualization.md](./audio-visualization.md) file for more information.

## Maps


## Captions

When dealing with captions or subtitles, load the Remotion Captions skill for more information.

## Google Fonts

Is the recommended way to load fonts in Remotion. See [google-fonts.md](google-fonts.md) for how to load Google Fonts.

## Local fonts

See [local-fonts.md](local-fonts.md) for how to load local fonts.


## GIFs

See [gifs.md](gifs.md) for timeline-synchronized animated images using the bundled runtime.

## Advanced Images

See [images.md](images.md) for sizing and positioning images, dynamic image paths, and getting image dimensions.

## Lottie animations

See [lottie.md](lottie.md) for embedding Lottie animations in Remotion.

## Timing

See [timing.md](timing.md) for more timing techniques for `interpolate()`.

## Parameterized videos

See [parameters.md](parameters.md) for making a composition parametrizable by adding a Zod schema.

## Measuring DOM nodes

See [measuring-dom-nodes.md](measuring-dom-nodes.md) for measuring DOM element dimensions in Remotion.

## Measuring text

See [measuring-text.md](measuring-text.md) for measuring text dimensions, fitting text to containers, and checking overflow.

## Using FFmpeg

For some video operations, such as trimming videos or detecting silence, FFmpeg should be used. Load the [./ffmpeg.md](./ffmpeg.md) file for more information.

## Silence detection

When needing to detect and trim silent segments from video or audio files, load the [./silence-detection.md](./silence-detection.md) file.

## Dynamic duration, dimensions and data

See [calculate-metadata.md](calculate-metadata.md) for dynamically set composition duration, dimensions, and props.

## Compositions and stills


## Advanced sequencing

See [sequencing.md](sequencing.md) for more sequencing patterns - delay, trim, limit duration of items.

## Available modules

Use only pinned imports accepted by `validate_runtime_layer_source`. Subclip supplies dependencies; package installation and arbitrary imports are unavailable. If a requested capability is absent, use a supported alternative.

## Visual checks

Validate with Subclip's native source validator and inspect captured project frames. Use the editor's native preview and export tools; do not start Remotion Studio, render CLIs, or external servers.
