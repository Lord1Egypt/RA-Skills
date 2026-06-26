/**
 * Scene registry — maps slide IDs to their animated scene components.
 *
 * Add new mappings here when creating scenes for other topics.
 * This keeps SlideScene.tsx focused on rendering logic.
 */
import React from "react";
import {
  FourierScene01,
  FourierScene02,
  FourierScene03,
  FourierScene04,
  FourierScene05,
  FourierScene06,
  FourierScene07,
  FourierScene08,
  FourierScene09,
} from "./scenes";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const SCENE_MAP: Record<string, React.FC<any>> = {
  slide_01: FourierScene01,
  slide_02: FourierScene02,
  slide_03: FourierScene03,
  slide_04: FourierScene04,
  slide_05: FourierScene05,
  slide_06: FourierScene06,
  slide_07: FourierScene07,
  slide_08: FourierScene08,
  slide_09: FourierScene09,
};
