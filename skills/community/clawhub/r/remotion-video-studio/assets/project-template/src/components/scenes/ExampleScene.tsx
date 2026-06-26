/**
 * Example scene — a minimal reference for creating custom animated scenes.
 *
 * Copy this file and rename it to create your own scenes.
 * Register your scene in sceneMap.ts to link it to a slide ID.
 *
 * Available props:
 *   - slide: Full SlideRenderData (id, title, text, durationInFrames, audioDurationInSeconds, audioFile)
 *   - theme: ThemeConfig (colors, fonts, sizes)
 *
 * Available animation components (import from "../animations"):
 *   FadeIn, ScaleIn, SlideIn, TypewriterText, WordHighlight,
 *   AnimatedBarChart, AnimatedLineChart, AnimatedPieChart,
 *   SineWave, CoordinateSystem, AnimatedPath, StaggeredList, CountUp
 */
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import type { SlideRenderData } from "../../types/types";
import type { ThemeConfig } from "../../types/types";
import { FadeIn } from "../animations/FadeIn";

type SceneProps = {
  slide: SlideRenderData;
  theme: ThemeConfig;
};

export const ExampleScene: React.FC<SceneProps> = ({ slide, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Title entrance with spring physics
  const titleEntrance = spring({ frame, fps, config: { damping: 200 } });
  const titleOpacity = interpolate(titleEntrance, [0, 1], [0, 1]);
  const titleY = interpolate(titleEntrance, [0, 1], [30, 0]);

  // You can use slide.durationInFrames to adapt animation timing
  // e.g., const midPoint = Math.floor(slide.durationInFrames / 2);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.backgroundColor,
        padding: 60,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Title */}
      <div
        style={{
          fontSize: theme.titleFontSize,
          fontWeight: 700,
          color: theme.primaryColor,
          opacity: titleOpacity,
          transform: `translateY(${titleY}px)`,
          textAlign: "center",
          fontFamily: theme.fontFamily,
          marginBottom: 40,
        }}
      >
        {slide.title}
      </div>

      {/* Your animated content goes here */}
      <FadeIn delay={15} duration={30}>
        <div
          style={{
            fontSize: theme.bodyFontSize,
            color: theme.textColor,
            textAlign: "center",
            maxWidth: theme.bodyMaxWidth,
            lineHeight: 1.6,
            fontFamily: theme.fontFamily,
          }}
        >
          {/* Replace this with your custom animation */}
          Replace this with your animated content
        </div>
      </FadeIn>
    </AbsoluteFill>
  );
};
