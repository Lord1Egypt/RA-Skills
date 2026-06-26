import React, { useMemo } from "react";
import {
import { RingDiagram } from "../components/FlowChart";
import { FadeInText, BulletList } from "../components/Typography";
import { scale } from "../theme";
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  springTiming,
  interpolate,
  Easing,
} from "remotion";

/**
 * Agent Loop Scene (1:35 - 2:25)
 * 环形流程图，展示 Agent Loop 四步骤
 */
export const AgentLoop: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame();
  const lines = narration.split("\n").filter(Boolean);
  const { fps } = useVideoConfig();

  // 每8秒切换一个活跃节点（总时长50秒，6个节点）
  const loopDuration = 50 * fps; // 50秒
  const nodeCount = 4;
  const nodeDuration = loopDuration / nodeCount;
  const currentNode = Math.min(nodeCount - 1, Math.floor(frame / nodeDuration));
  const rotationSpeed = 0.5; // 环形旋转速度

  // 计算当前帧在节点周期中的位置
  const frameInNode = frame % nodeDuration;
  // 每个节点阶段的详细说明
  const nodeDetails = [
    ["接收任务", "用户给出目标，如：把API改成支持流式输出"],
    ["规划步骤", "AI分析需要改哪些文件，按什么顺序执行"],
    ["调用工具", "Harness接收请求，校验权限，执行命令"],
    ["评估结果", "AI判断：成功？报错？需要修复？"],
  ];

  const nodes = ["计划", "选工具", "执行", "评估"];

  return (
    <AbsoluteFill
      style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}
    >
      {/* 环形图 */}
      <RingDiagram
        nodes={nodes}
        centerText="Agent Loop"
        color="#00d4ff"
        activeIndex={currentNode}
      />

      {/* 底部详情文字 */}
      {frame > 20 && (
        <div
          style={{
            position: "absolute",
            bottom: 120,
            left: "50%",
            transform: "translateX(-50%)",
            width: 800,
            textAlign: "center",
          }}
        >
          <div
            style={{
              color: "#00d4ff",
              fontSize={scale(32)},
              fontWeight: "bold",
              fontFamily: "system-ui, sans-serif",
              marginBottom: 12,
            }}
          >
            {nodeDetails[currentNode][0]}
          </div>
          <div
            style={{
              color: "#888",
              fontSize={scale(18)},
              fontFamily: "system-ui, sans-serif",
            }}
          >
            {nodeDetails[currentNode][1]}
          </div>
        </div>
      )}

      {/* 循环标签 */}
      {frame > 30 && (
        <div
          style={{
            position: "absolute",
            top: 60,
            left: "50%",
            transform: "translateX(-50%)",
            color: "#444",
            fontSize={scale(14)},
            fontFamily: "system-ui, sans-serif",
          }}
        >
          多轮循环，直到任务完成
        </div>
      )}
    </AbsoluteFill>
  );
};
