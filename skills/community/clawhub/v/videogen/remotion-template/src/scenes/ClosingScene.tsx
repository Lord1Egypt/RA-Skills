import React from "react";
import {
import { TypewriterText } from "../components/Typography";
import { scale } from "../theme";
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/**
 * Closing Scene (4:50 - 5:00)
 * 黑底白字，金句收尾
 */
export const ClosingScene: React.FC<{ narration: string }> = ({
  narration,
}) => {
  const frame = useCurrentFrame();
  const lines = narration.split("\n").filter(Boolean);

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* 主金句 */}
      <TypewriterText
        text={lines[0] || "AI工具会越来越开放，但懂得把它们串成可靠系统的人，才是真正的稀缺资源。"}
        fontSize={scale(32)}
        color="#ffffff"
        fontFamily="system-ui, sans-serif"
        startFrame={5}
        charsPerFrame={2}
        x={0.5}
        y={0.45}
        anchor="center"
      />

      {/* 副标题 */}
      {frame > 80 && (
        <div
          style={{
            position: "absolute",
            bottom: 120,
            left: "50%",
            transform: "translateX(-50%)",
            color: "#444",
            fontSize={scale(16)},
            fontFamily: "system-ui, sans-serif",
            letterSpacing: 2,
          }}
        >
          关注我，继续拆解 AI 时代的工程能力
        </div>
      )}

      {/* 装饰线 */}
      {frame > 30 && (
        <div
          style={{
            position: "absolute",
            bottom: 170,
            left: "50%",
            transform: "translateX(-50%)",
            width: 100,
            height: 1,
            backgroundColor: "#333",
          }}
        />
      )}
    </AbsoluteFill>
  );
};
