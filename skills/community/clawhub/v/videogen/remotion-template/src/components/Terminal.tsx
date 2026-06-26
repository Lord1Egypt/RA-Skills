import React, { useMemo } from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  springTiming,
  Easing,
} from "remotion";

/**
 * Terminal - 终端动画组件
 * 模拟终端界面，打字机效果显示文字
 */
interface TerminalProps {
  text: string;
  fps?: number;
  startFrame?: number;
}

export const Terminal: React.FC<TerminalProps> = ({
  text,
  fps = 30,
  startFrame = 0,
}) => {
  const { durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();

  // 每帧显示的字符数（根据 fps 调整速度）
  const charsPerFrame = 3; // 3 chars per frame at 30fps = ~90chars/sec
  const visibleChars = Math.max(
    0,
    Math.floor((frame - startFrame) * charsPerFrame)
  );

  const displayText = text.slice(0, visibleChars);

  // 光标闪烁
  const showCursor = Math.floor(frame / 15) % 2 === 0;

  const fontSize = 20;
  const lineHeight = fontSize * 1.6;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0d1117",
        fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
        padding: 40,
        justifyContent: "flex-start",
      }}
    >
      {/* 终端标题栏 */}
      <div
        style={{
          display: "flex",
          gap: 8,
          marginBottom: 20,
        }}
      >
        {["#FF5F56", "#FFBD2E", "#27C93F"].map((color, i) => (
          <div
            key={i}
            style={{
              width: 12,
              height: 12,
              borderRadius: "50%",
              backgroundColor: color,
            }}
          />
        ))}
        <div
          style={{
            flex: 1,
            backgroundColor: "#161b22",
            borderRadius: 4,
            height: 20,
            marginLeft: 8,
          }}
        />
      </div>

      {/* 终端内容 */}
      <div
        style={{
          color: "#c9d1d9",
          fontSize,
          lineHeight,
          whiteSpace: "pre-wrap",
        }}
      >
        <span style={{ color: "#79c0ff" }}>$ </span>
        <span>{displayText}</span>
        {showCursor && visibleChars < text.length && (
          <span style={{ color: "#c9d1d9" }}>▋</span>
        )}
      </div>
    </AbsoluteFill>
  );
};
