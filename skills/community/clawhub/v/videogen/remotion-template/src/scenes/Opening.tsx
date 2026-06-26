import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { Terminal } from "../components/Terminal";

/**
 * Opening Scene (0:00 - 0:20)
 * 纯黑背景，终端动画 + 打字机效果
 */
export const Opening: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Terminal
        text={narration.split("\n")[0] || "Claude Code is working..."}
        startFrame={5}
      />
    </AbsoluteFill>
  );
};
