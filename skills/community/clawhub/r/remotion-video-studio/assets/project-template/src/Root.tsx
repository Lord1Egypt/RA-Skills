/**
 * Remotion Root — registers all compositions.
 */
import React from "react";
import { Composition } from "remotion";
import { MainVideo } from "./compositions/MainVideo";
import { getProjectConfig, calculateSlideDuration } from "./lib/config";
import type { MainVideoProps, SlideRenderData } from "./types/types";

const config = getProjectConfig();

// Default demo slides (used in Studio preview)
const demoSlides: SlideRenderData[] = [
  {
    id: "demo_01",
    title: "Welcome",
    text: "This is a demo slide. Replace with your content.",
    audioFile: "",
    audioDurationInSeconds: 3,
    durationInFrames: calculateSlideDuration(3, config.video.fps, config.animation.paddingFrames),
  },
  {
    id: "demo_02",
    title: "Features",
    text: "Multi-TTS support, configurable animations, and more.",
    audioFile: "",
    audioDurationInSeconds: 3,
    durationInFrames: calculateSlideDuration(3, config.video.fps, config.animation.paddingFrames),
  },
  {
    id: "demo_03",
    title: "Thank You",
    text: "Thanks for watching! Check out the project on GitHub.",
    audioFile: "",
    audioDurationInSeconds: 3,
    durationInFrames: calculateSlideDuration(3, config.video.fps, config.animation.paddingFrames),
  },
];

const totalDuration = demoSlides.reduce((sum, s) => sum + s.durationInFrames, 0);

/**
 * Dynamically calculate video metadata based on props.
 * This ensures --props from CLI correctly sets the total duration.
 */
const calculateMetadata: Parameters<
  typeof Composition<MainVideoProps>
>[0]["calculateMetadata"] = ({ props }) => {
  const { slides, config: cfg } = props;
  const transitionFrames =
    cfg.animation.transition !== "none"
      ? cfg.animation.transitionDurationFrames
      : 0;
  const total =
    slides.reduce((sum, s) => sum + s.durationInFrames, 0) -
    transitionFrames * Math.max(0, slides.length - 1);

  return {
    durationInFrames: Math.max(total, 1),
    fps: cfg.video.fps,
    width: cfg.video.width,
    height: cfg.video.height,
  };
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MainVideo"
        component={MainVideo}
        durationInFrames={totalDuration}
        fps={config.video.fps}
        width={config.video.width}
        height={config.video.height}
        defaultProps={{
          slides: demoSlides,
          config,
        } satisfies MainVideoProps}
        calculateMetadata={calculateMetadata}
      />
    </>
  );
};
