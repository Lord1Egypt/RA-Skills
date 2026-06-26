/**
 * Scene registry — maps slide IDs to their animated scene components.
 *
 * Register your custom scenes here:
 *   import { YourScene01 } from "./scenes";
 *   slide_01: YourScene01,
 *
 * Slides without a registered scene will use the generic fallback layout.
 * See ExampleScene.tsx for a minimal scene template.
 */
import React from "react";

// Import your scene components:
// import { YourScene01, YourScene02 } from "./scenes";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const SCENE_MAP: Record<string, React.FC<any>> = {
  // Map slide IDs to scene components:
  // slide_01: YourScene01,
  // slide_02: YourScene02,
};
