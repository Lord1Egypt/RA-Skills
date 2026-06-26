/**
 * WordHighlight — highlights a specific word in a sentence with a spring-animated wipe.
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
} from "remotion";

type WordHighlightProps = {
  /** Full text containing the word to highlight */
  text: string;
  /** The word to highlight */
  highlightWord: string;
  /** Delay in frames before highlight starts */
  delay?: number;
  /** Duration of the wipe animation in frames */
  wipeDuration?: number;
  /** Highlight background color */
  highlightColor?: string;
  /** Text color */
  color?: string;
  /** Font size */
  fontSize?: number;
  /** Font weight */
  fontWeight?: number;
  /** Font family */
  fontFamily?: string;
  /** Custom style */
  style?: React.CSSProperties;
};

const HighlightSpan: React.FC<{
  word: string;
  color: string;
  delay: number;
  durationInFrames: number;
}> = ({ word, color, delay, durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const highlightProgress = spring({
    fps,
    frame,
    config: { damping: 200 },
    delay,
    durationInFrames,
  });
  const scaleX = Math.max(0, Math.min(1, highlightProgress));

  return (
    <span style={{ position: "relative", display: "inline-block" }}>
      <span
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: "50%",
          height: "1.05em",
          transform: `translateY(-50%) scaleX(${scaleX})`,
          transformOrigin: "left center",
          backgroundColor: color,
          borderRadius: "0.18em",
          zIndex: 0,
        }}
      />
      <span style={{ position: "relative", zIndex: 1 }}>{word}</span>
    </span>
  );
};

export const WordHighlight: React.FC<WordHighlightProps> = ({
  text,
  highlightWord,
  delay = 30,
  wipeDuration = 18,
  highlightColor = "#A7C7E7",
  color = "#ffffff",
  fontSize = 48,
  fontWeight = 700,
  fontFamily = "sans-serif",
  style,
}) => {
  const highlightIndex = text.indexOf(highlightWord);
  const hasHighlight = highlightIndex >= 0;
  const preText = hasHighlight ? text.slice(0, highlightIndex) : text;
  const postText = hasHighlight
    ? text.slice(highlightIndex + highlightWord.length)
    : "";

  return (
    <div
      style={{
        fontSize,
        fontWeight,
        fontFamily,
        color,
        ...style,
      }}
    >
      {hasHighlight ? (
        <>
          <span>{preText}</span>
          <HighlightSpan
            word={highlightWord}
            color={highlightColor}
            delay={delay}
            durationInFrames={wipeDuration}
          />
          <span>{postText}</span>
        </>
      ) : (
        <span>{text}</span>
      )}
    </div>
  );
};
