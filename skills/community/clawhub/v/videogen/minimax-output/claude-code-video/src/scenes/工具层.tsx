import React from "react";
import { AbsoluteFill } from "remotion";
import { fs, useFontScale } from "../theme";

export const 工具层: React.FC<{ narration: string }> = ({ narration }) => {
  const scale = useFontScale();
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center", alignItems: "center" }}>
      <div style={{ color: "#00d4ff", fontSize: Math.round(36 * scale), fontWeight: "bold", textAlign: "center" }}>
        工具层
      </div>
      <div style={{ color: "#666", fontSize: Math.round(18 * scale), marginTop: 20, textAlign: "center", maxWidth: 700 }}>
        SCENE_先看工具层。Claude Code内置了三大类工具。第一类：文件操作——读写、编辑、glob搜索、grep关键词，让AI能精确找到要改的代码。第二类：终端执行—
      </div>
    </AbsoluteFill>
  );
};
