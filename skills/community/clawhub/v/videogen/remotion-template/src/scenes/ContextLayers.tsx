import React from "react";
import {
import { LayerDiagram } from "../components/Diagrams";
import { BulletList } from "../components/Typography";
import { scale } from "../theme";
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/**
 * Context Layers Scene (2:25 - 3:10)
 * 三层上下文结构图
 */
export const ContextLayers: React.FC<{ narration: string }> = ({
  narration,
}) => {
  const frame = useCurrentFrame();
  const lines = narration.split("\n").filter(Boolean);

  const layers = [
    { label: "Session", sublabel: "会话历史 · 跨会话持久化", color: "#ff6b6b" },
    { label: "Context Window", sublabel: "Token 上限 · 自动 Compact 压缩", color: "#ffd93d" },
    { label: "CLAUDE.md", sublabel: "项目级记忆 · 项目专属规则", color: "#6bcb77" },
  ];

  return (
    <AbsoluteFill
      style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}
    >
      <LayerDiagram layers={layers} direction="top-down" />

      {/* 右侧补充文字 */}
      {frame > 80 && (
        <div
          style={{
            position: "absolute",
            right: 80,
            top: "50%",
            transform: "translateY(-50%)",
            width: 280,
          }}
        >
          <BulletList
            items={lines.slice(0, 3).map((l) => l.trim())}
            fontSize={scale(16)}
            color="#aaa"
            startFrame={80}
            itemDelay={15}
            x={0}
            y={0}
          />
        </div>
      )}
    </AbsoluteFill>
  );
};
