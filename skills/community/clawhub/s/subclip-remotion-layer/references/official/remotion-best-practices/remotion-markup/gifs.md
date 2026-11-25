---
name: gif
description: Displaying GIFs, APNG, AVIF and WebP in Remotion
metadata:
  tags: gif, animation, images, animated, apng, avif, webp
---

> Subclip sandbox: use only pinned, validated imports. Do not install packages or run external CLIs. Import animated assets into the project media library first and use the returned managed URL. Prefer native media layers; verify both preview and export before embedding animated images in layer code.

# Using Animated images in Remotion

## Basic usage

Use `<AnimatedImage>` to display a GIF, APNG, AVIF or WebP image synchronized with Remotion's timeline:

```tsx
import { AnimatedImage } from "remotion";

export const MyComposition = (props: { animationUrl: string }) => {
  return (
    <AnimatedImage
      src={props.animationUrl}
      width={500}
      height={500}
    />
  );
};
```

Use the exact URL returned by Subclip’s media library; do not bind an unimported remote URL:

```tsx
<AnimatedImage
  src={props.animationUrl}
  width={500}
  height={500}
/>
```

## Sizing and fit

Control how the image fills its container with the `fit` prop:

```tsx
// Stretch to fill (default)
<AnimatedImage
  src={props.animationUrl}
  width={500}
  height={300}
  fit="fill"
/>

// Maintain aspect ratio, fit inside container
<AnimatedImage
  src={props.animationUrl}
  width={500}
  height={300}
  fit="contain"
/>

// Fill container, crop if needed
<AnimatedImage
  src={props.animationUrl}
  width={500}
  height={300}
  fit="cover"
/>
```

## Playback speed

Use `playbackRate` to control the animation speed:

```tsx
// 2x speed
<AnimatedImage
  src={props.animationUrl}
  width={500}
  height={500}
  playbackRate={2}
/>
// Half speed
<AnimatedImage
  src={props.animationUrl}
  width={500}
  height={500}
  playbackRate={0.5}
/>
```

## Looping behavior

Control what happens when the animation finishes:

```tsx
// Loop indefinitely (default)
<AnimatedImage
  src={props.animationUrl}
  width={500}
  height={500}
  loopBehavior="loop"
/>

// Play once, show final frame
<AnimatedImage
  src={props.animationUrl}
  width={500}
  height={500}
  loopBehavior="pause-after-finish"
/>

// Play once, then clear canvas
<AnimatedImage
  src={props.animationUrl}
  width={500}
  height={500}
  loopBehavior="clear-after-finish"
/>
```

## Styling

Use the `style` prop for additional CSS (use `width` and `height` props for sizing):

```tsx
<AnimatedImage
  src={props.animationUrl}
  width={500}
  height={500}
  style={{
    borderRadius: 20,
    position: "absolute",
    top: 100,
    left: 50,
  }}
/>
```

## Getting GIF duration

Use `getGifDurationInSeconds()` from `@remotion/gif` to get the duration of a GIF.


```tsx
import { getGifDurationInSeconds } from "@remotion/gif";

const duration = await getGifDurationInSeconds(props.animationUrl);
console.log(duration); // e.g. 2.5
```

This is useful for setting the composition duration to match the GIF:

```tsx
import { getGifDurationInSeconds } from "@remotion/gif";
import { CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction<{ animationUrl: string }> = async ({ props }) => {
  const duration = await getGifDurationInSeconds(props.animationUrl);
  return {
    durationInFrames: Math.ceil(duration * 30),
  };
};
```

## Alternative

If `<AnimatedImage>` does not work (only supported in Chrome and Firefox), you can use `<Gif>` from `@remotion/gif` instead.


```tsx
import { Gif } from "@remotion/gif";

export const MyComposition = (props: { animationUrl: string }) => {
  return <Gif src={props.animationUrl} width={500} height={500} />;
};
```

The `<Gif>` component has the same props as `<AnimatedImage>` but only supports GIF files.
