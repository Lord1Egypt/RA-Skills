> Subclip sandbox: use only pinned, validated imports and native Subclip tools. Package/skill installation, external CLI execution, provider API keys, and standalone project setup are unavailable. Verify managed resources before use; use a supported alternative when unavailable.

# Motion blur

Use `@remotion/motion-blur` for frame-driven motion blur.  
Use the dependency already provided by Subclip. If the import is unavailable, choose a supported alternative; do not install packages inside the layer.

`<HtmlInCanvasMotionBlur>` is the state of the art in Remotion for blurring animated HTML. It captures the content at fractional frames and averages its pixels in a canvas.

## `<HtmlInCanvasMotionBlur>`

Available from Remotion 4.0.529.  
Supply the canvas `width` and `height`, usually from `useVideoConfig()`.  
`shutterAngle` defaults to `180` and accepts `0` to `360`.
`0` disables blur. `samples` defaults to `8` and must be an integer from `1` to `64`. More samples can smooth the blur but increase preview and render cost.

Call `useCurrentFrame()` inside the child component so each sample receives its own frame. Start with a small sample count (for example 4) and increase only when visual review needs it. In 4.0.530, `disabled` captures a single frame while retaining the canvas. Do not nest this component inside another HTML-in-canvas surface.

```tsx
import {
  HtmlInCanvasMotionBlur,
} from '@remotion/motion-blur';
import {useCurrentFrame, useVideoConfig} from 'remotion';

const MovingBox = () => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        position: 'absolute',
        left: frame * 10,
        top: 200,
        width: 120,
        height: 120,
        backgroundColor: '#ff6b6b',
      }}
    />
  );
};

export const HtmlInCanvasBlur = () => {
  const {width, height} = useVideoConfig();

  return (
    <HtmlInCanvasMotionBlur
      width={width}
      height={height}
      samples={8}
      shutterAngle={180}
    >
      <MovingBox />
    </HtmlInCanvasMotionBlur>
  );
};
```

Subclip enables HTML-in-canvas in its desktop Chromium runtime. Verify the renderer supports `HtmlInCanvasMotionBlur` before use; if unavailable, use a supported effect alternative. Do not change browser flags or install dependencies from a layer.  
No configuration for rendering is necessary.

Do not nest `<HtmlInCanvas>` or `<HtmlInCanvasMotionBlur>` components; nested HTML-in-canvas is unsupported.

If HTML-in-canvas is unavailable, see the [motion blur guide](https://www.remotion.dev/docs/motion-blur) for other options. See the [`<HtmlInCanvasMotionBlur>` reference](https://www.remotion.dev/docs/motion-blur/html-in-canvas-motion-blur) for API details.
