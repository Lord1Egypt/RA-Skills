---
name: sensors-pinch-zoom
description: Track pinch zoom gestures with usePinchZoom hook
---

# usePinchZoom

React sensor hook that tracks the changes in pointer touch events and detects value of pinch difference and tell if user is zooming in or out.

## Usage

```jsx
import { usePinchZoom } from "react-use";

const Demo = () => {
  const [scale, setState] = useState(1);
  const scaleRef = useRef();
  const { zoomingState, pinchState } = usePinchZoom(scaleRef);

  useEffect(() => {
    if (zoomingState === "ZOOM_IN") {
      // perform zoom in scaling
      setState(scale + 0.1)
    } else if (zoomingState === "ZOOM_OUT") {
      // perform zoom out in scaling
      setState(scale - 0.1)
    }
  }, [zoomingState]);

  return (
    <div ref={scaleRef}>
      <img
        src="https://www.olympus-imaging.co.in/content/000107506.jpg"
        style={{
          zoom: scale,
        }}
      />
    </div>
  );
};
```

## Reference

```ts
const { zoomingState, pinchState } = usePinchZoom(ref);
```

Returns:
- `zoomingState`: `"ZOOM_IN" | "ZOOM_OUT" | null` - current zoom direction
- `pinchState`: object with pinch gesture details

## Key Points

- Tracks pinch zoom gestures on touch devices
- Provides zoom direction state
- Useful for image zoom or scale interactions

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/usePinchZoom.md
-->
