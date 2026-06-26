---
name: sensors-breakpoint
description: Track innerWidth with breakpoints using createBreakpoint hook
---

# createBreakpoint

Factory function that creates a hook to track `innerWidth` with custom breakpoints.

## Usage

### Default breakpoint

laptopL: 1440, laptop: 1024, tablet: 768

```jsx
import React from "react";
import { createBreakpoint } from "react-use";

const useBreakpoint = createBreakpoint();

const Demo = () => {
  const breakpoint = useBreakpoint();

  if (breakpoint === "laptopL") return <div> This is very big Laptop </div>;
  else if (breakpoint == "laptop") return <div> This is Laptop</div>;
  else if (breakpoint == "tablet") return <div> This is Tablet</div>;
  else return <div> Too small!</div>;
};
```

### Custom breakpoint

XL: 1280, L: 768, S: 350

```jsx
import React from "react";
import { createBreakpoint } from "react-use";

const useBreakpoint = createBreakpoint({ XL: 1280, L: 768, S: 350 });

const Demo = () => {
  const breakpoint = useBreakpoint();

  if (breakpoint === "XL") return <div> XL </div>;
  else if (breakpoint == "L") return <div> LoL</div>;
  else if (breakpoint == "S") return <div> Sexyy</div>;
  else return <div> Wth</div>;
};
```

## Reference

```ts
const useBreakpoint = createBreakpoint(breakpoints?: Record<string, number>);
const breakpoint: string = useBreakpoint();
```

- **`breakpoints`**: `Record<string, number>` - object mapping breakpoint names to pixel widths
- Returns a hook that returns the current breakpoint name based on window width

## Key Points

- Factory function creates a custom hook
- Default breakpoints: laptopL (1440), laptop (1024), tablet (768)
- Custom breakpoints can be defined
- Returns breakpoint name as string

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/createBreakpoint.md
-->
