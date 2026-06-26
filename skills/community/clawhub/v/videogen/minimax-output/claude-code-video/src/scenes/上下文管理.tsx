import React from "react";
import { AbsoluteFill } from "remotion";
import { LayerDiagram } from "../components/Diagrams";
import { fs, useFontScale } from "../theme";

export const 上下文管理: React.FC<{ narration: string }>= ({ narration }) => {
  const scale = useFontScale();
  const layers = [
    { label: "Session", sublabel: "会话历史 · 跨会话持久化", color: "#ff6b6b" },
    { label: "Context Window", sublabel: "Token 上限 · 自动 Compact 压缩", color: "#ffd93d" },
    { label: "CLAUDE.md", sublabel: "项目级记忆 · 项目专属规则", color: "#6bcb77" },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}>
      <LayerDiagram layers={layers} direction="top-down" />
    </AbsoluteFill>
  );
};
