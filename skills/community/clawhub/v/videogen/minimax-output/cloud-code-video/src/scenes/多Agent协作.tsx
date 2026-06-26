import React from "react";
import { AbsoluteFill } from "remotion";

export const 多Agent协作: React.FC<{ narration: string }> = ({ narration }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center", alignItems: "center" }}>
      <div style={{ color: "#00d4ff", fontSize: 36, fontWeight: "bold", textAlign: "center" }}>
        多Agent协作
      </div>
      <div style={{ color: "#666", fontSize: 18, marginTop: 20, textAlign: "center", maxWidth: 700 }}>
        SCENE_
      </div>
    </AbsoluteFill>
  );
};
