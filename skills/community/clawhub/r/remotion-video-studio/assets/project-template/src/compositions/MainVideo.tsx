/**
 * MainVideo composition — orchestrates all slides with transitions and audio.
 */
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  Audio,
  staticFile,
  useVideoConfig,
} from "remotion";
import {
  TransitionSeries,
  linearTiming,
} from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { SlideScene } from "../components/SlideScene";
import { SubtitleOverlay } from "../components/SubtitleOverlay";
import type { MainVideoProps, TransitionType } from "../types/types";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function getTransitionPresentation(type: TransitionType): any {
  switch (type) {
    case "fade":
      return fade();
    case "slide":
      return slide({ direction: "from-right" });
    case "wipe":
      return wipe({ direction: "from-left" });
    case "none":
    default:
      return fade();
  }
}

export const MainVideo: React.FC<MainVideoProps> = ({ slides, config }) => {
  const { fps } = useVideoConfig();
  const { animation, theme, subtitle: subtitleConfig } = config;

  // Guard: handle empty slides array
  if (!slides || slides.length === 0) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: theme.backgroundColor,
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div style={{ color: theme.textColor, fontSize: 32 }}>
          No slides to render
        </div>
      </AbsoluteFill>
    );
  }

  // Background music configuration
  const bgmConfig = config.bgm;
  const bgmEnabled = bgmConfig?.enabled && bgmConfig?.file;

  const useTransitions = animation.transition !== "none" && slides.length > 1;

  if (useTransitions) {
    return (
      <AbsoluteFill>
        {/* Background music layer */}
        {bgmEnabled && (
          <Audio
            src={staticFile(bgmConfig!.file)}
            volume={bgmConfig!.volume ?? 0.15}
            loop={bgmConfig!.loop ?? true}
          />
        )}
        <TransitionSeries>
          {slides.map((slideData, index) => {
            const isLast = index === slides.length - 1;
            return (
              <React.Fragment key={slideData.id}>
                <TransitionSeries.Sequence
                  durationInFrames={slideData.durationInFrames}
                >
                  {/* Slide visual */}
                  <SlideScene
                    slide={slideData}
                    theme={theme}
                    animation={animation}
                  />

                  {/* Audio track */}
                  {slideData.audioFile && (
                    <Audio src={staticFile(slideData.audioFile)} />
                  )}

                  {/* Subtitle overlay */}
                  <SubtitleOverlay
                    text={slideData.text}
                    config={subtitleConfig}
                  />
                </TransitionSeries.Sequence>

                {/* Transition between slides */}
                {!isLast && (
                  <TransitionSeries.Transition
                    presentation={getTransitionPresentation(
                      animation.transition
                    )}
                    timing={linearTiming({
                      durationInFrames: animation.transitionDurationFrames,
                    })}
                  />
                )}
              </React.Fragment>
            );
          })}
        </TransitionSeries>
      </AbsoluteFill>
    );
  }

  // No transitions — use simple Sequence layout
  let currentFrame = 0;
  return (
    <AbsoluteFill>
      {/* Background music layer */}
      {bgmEnabled && (
        <Audio
          src={staticFile(bgmConfig!.file)}
          volume={bgmConfig!.volume ?? 0.15}
          loop={bgmConfig!.loop ?? true}
        />
      )}
      {slides.map((slideData) => {
        const from = currentFrame;
        currentFrame += slideData.durationInFrames;

        return (
          <Sequence
            key={slideData.id}
            from={from}
            durationInFrames={slideData.durationInFrames}
          >
            <SlideScene
              slide={slideData}
              theme={theme}
              animation={animation}
            />

            {slideData.audioFile && (
              <Audio src={staticFile(slideData.audioFile)} />
            )}

            <SubtitleOverlay
              text={slideData.text}
              config={subtitleConfig}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
