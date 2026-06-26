import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

/**
 * TypewriterText - 打字机效果文字
 */
interface TypewriterTextProps {
  text: string;
  fontSize?: number;
  color?: string;
  fontFamily?: string;
  startFrame?: number;
  charsPerFrame?: number;
  x?: number; // 0-1 relative
  y?: number; // 0-1 relative
  anchor?: "left" | "center" | "right";
}

export const TypewriterText: React.FC<TypewriterTextProps> = ({
  text,
  fontSize = 96,
  color = "#ffffff",
  fontFamily = "system-ui, sans-serif",
  startFrame = 0,
  charsPerFrame = 2,
  x = 0.5,
  y = 0.5,
  anchor = "center",
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const visibleChars = Math.max(
    0,
    Math.floor((frame - startFrame) * charsPerFrame)
  );
  const displayText = text.slice(0, visibleChars);

  const anchorMap = {
    left: "0%",
    center: "50%",
    right: "100%",
  };

  return (
    <div
      style={{
        position: "absolute",
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        transform: `translateX(-${anchorMap[anchor]})`,
        color,
        fontSize,
        fontFamily,
        fontWeight: "bold",
        lineHeight: 1.4,
        textAlign: anchor,
        whiteSpace: "pre-wrap",
      }}
    >
      {displayText}
    </div>
  );
};

/**
 * FadeInText - 淡入文字
 */
interface FadeInTextProps {
  text: string;
  fontSize?: number;
  color?: string;
  fontFamily?: string;
  startFrame?: number;
  duration?: number;
  x?: number;
  y?: number;
  anchor?: "left" | "center" | "right";
}

export const FadeInText: React.FC<FadeInTextProps> = ({
  text,
  fontSize = 96,
  color = "#ffffff",
  fontFamily = "system-ui, sans-serif",
  startFrame = 0,
  duration = 20,
  x = 0.5,
  y = 0.5,
  anchor = "center",
}) => {
  const frame = useCurrentFrame();
  const progress = Math.min(
    1,
    Math.max(0, (frame - startFrame) / duration)
  );

  const anchorMap = {
    left: "0%",
    center: "50%",
    right: "100%",
  };

  return (
    <div
      style={{
        position: "absolute",
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        transform: `translateX(-${anchorMap[anchor]})`,
        color,
        fontSize,
        fontFamily,
        fontWeight: "bold",
        opacity: progress,
        whiteSpace: "pre-wrap",
        textAlign: anchor,
      }}
    >
      {text}
    </div>
  );
};

/**
 * HighlightedText - 带高亮背景的文字
 */
interface HighlightedTextProps {
  text: string;
  highlightColor?: string;
  textColor?: string;
  fontSize?: number;
  startFrame?: number;
  x?: number;
  y?: number;
}

export const HighlightedText: React.FC<HighlightedTextProps> = ({
  text,
  highlightColor = "#00d4ff",
  textColor = "#ffffff",
  fontSize = 72,
  startFrame = 0,
  x = 0.5,
  y = 0.5,
}) => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, Math.max(0, (frame - startFrame) / 20));

  return (
    <div
      style={{
        position: "absolute",
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        transform: "translate(-50%, -50%)",
        backgroundColor: highlightColor,
        color: textColor,
        fontSize,
        fontFamily: "system-ui, sans-serif",
        fontWeight: "bold",
        padding: "12px 24px",
        borderRadius: 8,
        opacity: progress,
        boxShadow: `0 0 30px ${highlightColor}40`,
      }}
    >
      {text}
    </div>
  );
};

/**
 * BulletList - 逐条出现的列表
 */
interface BulletListProps {
  items: string[];
  fontSize?: number;
  color?: string;
  startFrame?: number;
  itemDelay?: number; // 每条间隔帧数
  x?: number;
  y?: number;
}

export const BulletList: React.FC<BulletListProps> = ({
  items,
  fontSize = 56,
  color = "#c9d1d9",
  startFrame = 0,
  itemDelay = 20,
  x = 0.1,
  y = 0.2,
}) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        position: "absolute",
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        display: "flex",
        flexDirection: "column",
        gap: 16,
      }}
    >
      {items.map((item, i) => {
        const itemProgress = Math.min(
          1,
          Math.max(0, (frame - startFrame - i * itemDelay) / 15)
        );
        return (
          <div
            key={i}
            style={{
              display: "flex",
              alignItems: "flex-start",
              gap: 12,
              opacity: itemProgress,
              transform: `translateX(${(1 - itemProgress) * -20}px)`,
              transition: "none",
            }}
          >
            <span style={{ color: "#00d4ff", fontSize: 20, marginTop: 4 }}>
              ▸
            </span>
            <span
              style={{
                color,
                fontSize,
                fontFamily: "system-ui, sans-serif",
                lineHeight: 1.5,
              }}
            >
              {item}
            </span>
          </div>
        );
      })}
    </div>
  );
};
