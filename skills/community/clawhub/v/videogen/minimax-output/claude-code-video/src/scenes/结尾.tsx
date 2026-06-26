import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { TypewriterText } from "../components/Typography";
import { fs, useFontScale } from "../theme";

export const 结尾: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame()
  const scale = useFontScale();;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <TypewriterText
        text="好了，四个模块都讲完了。最后说一点想法。Claude Code的核心创新，不在于它的AI有多强，而在于它那套harness系统——把一个不确定的模型，变成了一个"
        fontSize={Math.round(72 * scale)}
        color="#ffffff"
        fontFamily="system-ui, sans-serif"
        startFrame={5}
        charsPerFrame={2}
        x={0.5}
        y={0.45}
        anchor="center"
      />
      {frame > 80 && (
        <div style={{ position: "absolute", bottom: 120, left: "50%", transform: "translateX(-50%)", color: "#444", fontSize: Math.round(16 * scale), fontFamily: "system-ui, sans-serif", letterSpacing: 2 }}>
          关注我，继续拆解 AI 时代的工程能力
        </div>
      )}
    </AbsoluteFill>
  );
};
