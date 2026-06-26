/**
 * Config utilities — loads project configuration for Remotion components.
 */
import type { ProjectConfig } from "../types/types";

// In Remotion's webpack/rspack environment, JSON imports are resolved at build time.
// We use require() here because Remotion bundles this for the browser.
// eslint-disable-next-line @typescript-eslint/no-var-requires
const projectConfig = require("../../config/project.json");

/**
 * Get the project configuration object.
 */
export function getProjectConfig(): ProjectConfig {
  return projectConfig as ProjectConfig;
}

/**
 * Calculate the total duration in frames for a slide, given its audio duration.
 * @param audioDurationSeconds - Duration of the audio in seconds
 * @param fps - Frames per second
 * @param paddingFrames - Extra frames to add before and after
 */
export function calculateSlideDuration(
  audioDurationSeconds: number,
  fps: number,
  paddingFrames: number
): number {
  return Math.ceil(audioDurationSeconds * fps) + paddingFrames * 2;
}
