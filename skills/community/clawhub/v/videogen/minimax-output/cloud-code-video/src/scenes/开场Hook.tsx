import React from "react";
import { AbsoluteFill } from "remotion";

export const 开场Hook: React.FC<{ narration: string }> = ({ narration }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center", alignItems: "center" }}>
      <div style={{ color: "#00d4ff", fontSize: 36, fontWeight: "bold", textAlign: "center" }}>
        开场Hook
      </div>
      <div style={{ color: "#666", fontSize: 18, marginTop: 20, textAlign: "center", maxWidth: 700 }}>
        SCENE_Cloud Code 源码泄露，目前公认最强的编码 Agent。核心竞争力不在模型，而在模型周围那套精密的控制系统。|核心骨架是一个 While 循环加一组工具
      </div>
    </AbsoluteFill>
  );
};
