import React from "react";
import { AbsoluteFill } from "remotion";
import { Terminal } from "../components/Terminal";
import { fs, useFontScale } from "../theme";

export const 开场: React.FC<{ narration: string }>= ({ narration }) => {
  const scale = useFontScale();
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Terminal text="你在终端里敲了一行字，按下回车。AI开始读文件、改代码、跑测试——整个过程没有你介入。它是怎么知道该做什么、不该做什么的？答案是：不是AI自己知道，是有一套系统" startFrame={5} />
    </AbsoluteFill>
  );
};
