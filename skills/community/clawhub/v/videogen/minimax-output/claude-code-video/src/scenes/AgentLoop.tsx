import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { RingDiagram } from "../components/FlowChart";
import { fs, useFontScale } from "../theme";

export const AgentLoop: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame()
  const scale = useFontScale();;
  const { fps } = useVideoConfig();
  const DURATION = 50;
  const nodes = ["计划", "选工具", "执行", "评估"];
  const nodeDetails = [
    ["接收任务", "用户给出目标，如：把API改成支持流式输出"],
    ["规划步骤", "AI分析需要改哪些文件，按什么顺序执行"],
    ["调用工具", "Harness接收请求，校验权限，执行命令"],
    ["评估结果", "AI判断：成功？报错？需要修复？"],
  ];
  const nodeDuration = (DURATION * fps) / nodes.length;
  const currentNode = Math.min(nodes.length - 1, Math.floor(frame / nodeDuration));

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}>
      <RingDiagram nodes={nodes} centerText="Agent Loop" color="#00d4ff" activeIndex={currentNode} />
      <div style={{ position: "absolute", bottom: 120, left: "50%", transform: "translateX(-50%)", textAlign: "center" }}>
        <div style={{ color: "#00d4ff", fontSize: Math.round(32 * scale), fontWeight: "bold", marginBottom: 12 }}>{nodeDetails[currentNode][0]}</div>
        <div style={{ color: "#888", fontSize: Math.round(18 * scale) }}>{nodeDetails[currentNode][1]}</div>
      </div>
    </AbsoluteFill>
  );
};
