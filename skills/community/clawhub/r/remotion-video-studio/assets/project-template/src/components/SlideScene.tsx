/**
 * Slide component — dispatches to topic-specific animated scenes when available,
 * falls back to the generic text layout for unknown slide IDs.
 */
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  Img,
  staticFile,
} from "remotion";
import type { SlideRenderData, ThemeConfig, AnimationConfig } from "../types/types";
import { SCENE_MAP } from "./sceneMap";

type SlideProps = {
  slide: SlideRenderData;
  theme: ThemeConfig;
  animation: AnimationConfig;
};

export const SlideScene: React.FC<SlideProps> = ({ slide, theme, animation }) => {
  // Check if there's a dedicated animated scene for this slide
  const AnimatedScene = SCENE_MAP[slide.id];

  if (AnimatedScene) {
    // Pass full slide data + theme to custom scenes for maximum flexibility.
    // Scenes can access: slide.title, slide.text, slide.durationInFrames,
    // slide.audioDurationInSeconds, slide.id, slide.audioFile
    return <AnimatedScene slide={slide} title={slide.title} theme={theme} />;
  }

  // --- Fallback: generic text layout (for slides without custom scenes) ---
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance animation
  const entrance = spring({
    frame,
    fps,
    config: animation.entranceSpring,
  });

  const titleOpacity = interpolate(entrance, [0, 1], [0, 1]);
  const titleY = interpolate(entrance, [0, 1], [40, 0]);

  // Text fade-in (slightly delayed)
  const textEntrance = spring({
    frame,
    fps,
    config: animation.entranceSpring,
    delay: animation.textEntryDelay,
  });
  const textOpacity = interpolate(textEntrance, [0, 1], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.backgroundColor,
        justifyContent: "center",
        alignItems: "center",
        padding: theme.slidePadding,
      }}
    >
      {/* Optional background image */}
      {slide.backgroundImage && (
        <AbsoluteFill>
          <Img
            src={staticFile(slide.backgroundImage)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              opacity: theme.backgroundImageOpacity,
            }}
          />
        </AbsoluteFill>
      )}

      {/* Content container */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 40,
          zIndex: 1,
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
          }}
        >
          {slide.title}
        </div>

        {/* Decorative line */}
        <div
          style={{
            width: interpolate(entrance, [0, 1], [0, theme.decorLineWidth]),
            height: 3,
            backgroundColor: theme.secondaryColor,
            borderRadius: 2,
          }}
        />

        {/* Body text */}
        <div
          style={{
            fontSize: theme.bodyFontSize,
            color: theme.textColor,
            opacity: textOpacity,
            textAlign: "center",
            lineHeight: 1.6,
            maxWidth: theme.bodyMaxWidth,
            fontFamily: theme.fontFamily,
          }}
        >
          {slide.text}
        </div>
      </div>
    </AbsoluteFill>
  );
};
