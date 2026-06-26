/**
 * Subtitle overlay component — displays subtitles at the bottom of the video.
 * Supports two display modes:
 *   - "sentence": splits text into sentences and shows them one at a time
 *   - "full": shows the entire text at once (static)
 */
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import type { SubtitleConfig } from "../types/types";

type SubtitleOverlayProps = {
  text: string;
  config: SubtitleConfig;
};

/**
 * Split text into sentences by Chinese/English punctuation.
 * Keeps each segment short enough for a single subtitle line.
 */
function splitIntoSentences(text: string): string[] {
  // Split by Chinese period, comma, semicolon, question/exclamation marks,
  // and English period/comma followed by space
  const raw = text.split(/(?<=[。！？；.!?])\s*|(?<=[，,])\s*/);
  const sentences: string[] = [];
  let buffer = "";

  for (const seg of raw) {
    const trimmed = seg.trim();
    if (!trimmed) continue;

    // If buffer + current segment is short enough, merge them
    if (buffer && (buffer + trimmed).length <= 25) {
      buffer += trimmed;
    } else {
      if (buffer) sentences.push(buffer);
      buffer = trimmed;
    }
  }
  if (buffer) sentences.push(buffer);

  return sentences.length > 0 ? sentences : [text];
}

export const SubtitleOverlay: React.FC<SubtitleOverlayProps> = ({
  text,
  config,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  if (!config.enabled || !text) {
    return null;
  }

  const displayMode = config.displayMode || "sentence";

  // --- Full mode: show entire text with fade in/out ---
  if (displayMode === "full") {
    const fadeDuration = fps * config.fadeDurationSec;
    const fadeIn = interpolate(frame, [0, fadeDuration], [0, 1], {
      extrapolateRight: "clamp",
    });
    const fadeOut = interpolate(
      frame,
      [durationInFrames - fadeDuration, durationInFrames],
      [1, 0],
      { extrapolateLeft: "clamp" }
    );
    const opacity = Math.min(fadeIn, fadeOut);
    const positionStyle = getPositionStyle(config);

    return (
      <AbsoluteFill style={{ ...positionStyle, opacity }}>
        <div style={getTextStyle(config, false)}>
          {text}
        </div>
      </AbsoluteFill>
    );
  }

  // --- Sentence mode: show one sentence at a time ---
  const sentences = splitIntoSentences(text);
  const sentenceCount = sentences.length;

  // Evenly distribute time across sentences
  const framesPerSentence = durationInFrames / sentenceCount;
  // Fade transition duration (in frames) for each sentence
  const fadeDurationFrames = Math.min(
    Math.floor(framesPerSentence * 0.15),
    10
  );

  // Determine which sentence is currently active
  const currentIndex = Math.min(
    Math.floor(frame / framesPerSentence),
    sentenceCount - 1
  );
  const currentSentence = sentences[currentIndex];

  // Calculate local frame within the current sentence
  const localFrame = frame - currentIndex * framesPerSentence;

  // Fade in at the start of each sentence
  const fadeIn = interpolate(localFrame, [0, fadeDurationFrames], [0, 1], {
    extrapolateRight: "clamp",
  });
  // Fade out at the end of each sentence
  const fadeOut = interpolate(
    localFrame,
    [framesPerSentence - fadeDurationFrames, framesPerSentence],
    [1, 0],
    { extrapolateLeft: "clamp" }
  );
  const opacity = Math.min(fadeIn, fadeOut);

  const positionStyle = getPositionStyle(config);

  return (
    <AbsoluteFill style={{ ...positionStyle, opacity }}>
      <div style={getTextStyle(config, true)}>
        {currentSentence}
      </div>
    </AbsoluteFill>
  );
};

/**
 * Build the text container style.
 * @param singleLine - If true, force single line with ellipsis overflow.
 */
function getTextStyle(
  config: SubtitleConfig,
  singleLine: boolean
): React.CSSProperties {
  return {
    fontSize: config.fontSize,
    fontFamily: config.fontFamily,
    color: config.color,
    textAlign: "center",
    lineHeight: singleLine ? 1.4 : 1.5,
    padding: config.padding,
    borderRadius: config.borderRadius,
    backgroundColor: config.backgroundColor,
    maxWidth: config.maxWidth,
    ...(singleLine
      ? { whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }
      : {}),
    WebkitTextStroke: `${config.strokeWidth}px ${config.strokeColor}`,
    paintOrder: "stroke fill",
  };
}

function getPositionStyle(
  config: SubtitleConfig
): React.CSSProperties {
  switch (config.style) {
    case "tiktok":
    case "bottom":
      return {
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: config.marginBottom,
      };
    case "center":
      return {
        justifyContent: "center",
        alignItems: "center",
      };
    default:
      return {
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: config.marginBottom,
      };
  }
}
