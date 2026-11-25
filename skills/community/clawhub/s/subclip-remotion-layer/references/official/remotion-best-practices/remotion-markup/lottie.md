---
name: lottie
description: Embedding Lottie animations in Remotion.
metadata:
  category: Animation
---

> Subclip sandbox: use only pinned, validated imports and native Subclip tools. Package/skill installation, external CLI execution, provider API keys, and standalone project setup are unavailable. Verify managed resources before use; use a supported alternative when unavailable.

# Using Lottie Animations in Remotion

## Prerequisites

First, the @remotion/lottie package needs to be installed.  
If it is not, use the following command:

Subclip manages dependencies and execution. Use the installed runtime and native Subclip tools; package installation and standalone CLI execution are unavailable inside a layer.


## Displaying a Lottie file

To import a Lottie animation:

- Fetch the Lottie asset
- Wrap the loading process in `delayRender()` and `continueRender()`
- Save the animation data in a state
- Render the Lottie animation using the `Lottie` component from the `@remotion/lottie` package

```tsx
import { Lottie, LottieAnimationData } from "@remotion/lottie";
import { useEffect, useState } from "react";
import { cancelRender, continueRender, delayRender } from "remotion";

export const MyAnimation = () => {
  const [handle] = useState(() => delayRender("Loading Lottie animation"));

  const [animationData, setAnimationData] =
    useState<LottieAnimationData | null>(null);

  useEffect(() => {
    fetch("https://assets4.lottiefiles.com/packages/lf20_zyquagfl.json")
      .then((data) => data.json())
      .then((json) => {
        setAnimationData(json);
        continueRender(handle);
      })
      .catch((err) => {
        cancelRender(err);
      });
  }, [handle]);

  if (!animationData) {
    return null;
  }

  return <Lottie animationData={animationData} />;
};
```

## Styling and animating

Lottie supports the `style` prop to allow styles and animations:

```tsx
return (
  <Lottie
    animationData={animationData}
    style={{ width: 400, height: 400 }}
  />
);
```
