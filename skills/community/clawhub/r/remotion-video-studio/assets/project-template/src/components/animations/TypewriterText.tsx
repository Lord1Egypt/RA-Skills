/**
 * TypewriterText — reveals text character by character with a blinking cursor.
 * Supports a pause after a specified substring.
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";

type TypewriterTextProps = {
  /** Full text to type out */
  text: string;
  /** Frames per character */
  charFrames?: number;
  /** Pause after this substring (optional) */
  pauseAfter?: string;
  /** Pause duration in seconds */
  pauseDurationSec?: number;
  /** Show blinking cursor */
  showCursor?: boolean;
  /** Cursor blink cycle in frames */
  cursorBlinkFrames?: number;
  /** Delay in frames before typing starts */
  delay?: number;
  /** Font size */
  fontSize?: number;
  /** Font weight */
  fontWeight?: number;
  /** Text color */
  color?: string;
  /** Font family */
  fontFamily?: string;
  /** Custom style */
  style?: React.CSSProperties;
};

const getTypedText = ({
  frame,
  fullText,
  pauseAfter,
  charFrames,
  pauseFrames,
}: {
  frame: number;
  fullText: string;
  pauseAfter: string | undefined;
  charFrames: number;
  pauseFrames: number;
}): string => {
  if (!pauseAfter) {
    const typedChars = Math.min(fullText.length, Math.floor(frame / charFrames));
    return fullText.slice(0, typedChars);
  }

  const pauseIndex = fullText.indexOf(pauseAfter);
  const preLen =
    pauseIndex >= 0 ? pauseIndex + pauseAfter.length : fullText.length;

  let typedChars = 0;
  if (frame < preLen * charFrames) {
    typedChars = Math.floor(frame / charFrames);
  } else if (frame < preLen * charFrames + pauseFrames) {
    typedChars = preLen;
  } else {
    const postPhase = frame - preLen * charFrames - pauseFrames;
    typedChars = Math.min(
      fullText.length,
      preLen + Math.floor(postPhase / charFrames)
    );
  }
  return fullText.slice(0, typedChars);
};

const Cursor: React.FC<{
  frame: number;
  blinkFrames: number;
  color: string;
}> = ({ frame, blinkFrames, color }) => {
  const opacity = interpolate(
    frame % blinkFrames,
    [0, blinkFrames / 2, blinkFrames],
    [1, 0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return <span style={{ opacity, color }}>{"\u258C"}</span>;
};

export const TypewriterText: React.FC<TypewriterTextProps> = ({
  text,
  charFrames = 2,
  pauseAfter,
  pauseDurationSec = 1,
  showCursor = true,
  cursorBlinkFrames = 16,
  delay = 0,
  fontSize = 48,
  fontWeight = 700,
  color = "#ffffff",
  fontFamily = "sans-serif",
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = Math.max(0, frame - delay);
  const pauseFrames = Math.round(fps * pauseDurationSec);

  const typedText = getTypedText({
    frame: localFrame,
    fullText: text,
    pauseAfter,
    charFrames,
    pauseFrames,
  });

  return (
    <div
      style={{
        fontSize,
        fontWeight,
        color,
        fontFamily,
        ...style,
      }}
    >
      <span>{typedText}</span>
      {showCursor && (
        <Cursor
          frame={localFrame}
          blinkFrames={cursorBlinkFrames}
          color={color}
        />
      )}
    </div>
  );
};
