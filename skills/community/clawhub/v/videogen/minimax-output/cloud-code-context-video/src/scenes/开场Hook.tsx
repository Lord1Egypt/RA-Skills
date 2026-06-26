import React from "react";
import { AbsoluteFill } from "remotion";

export const 开场Hook: React.FC<{ narration: string }> = ({ narration }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center", alignItems: "center" }}>
      <div style={{ color: "#00d4ff", fontSize: 36, fontWeight: "bold", textAlign: "center" }}>
        开场Hook
      </div>
      <div style={{ color: "#666", fontSize: 18, marginTop: 20, textAlign: "center", maxWidth: 700 }}>
        SCENE_Cloud Code 的上下文管理是整个 Harness 工程含量最高的部分。源码注释里有条2026年3月的生产数据：1279个会话出现50次以上连续压缩失败，
      </div>
    </AbsoluteFill>
  );
};
