import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { 开场Hook } from "./scenes/开场Hook";
import { 核心架构 } from "./scenes/核心架构";
import { 上下文管理 } from "./scenes/上下文管理";
import { 安全约束 } from "./scenes/安全约束";
import { 多Agent协作 } from "./scenes/多Agent协作";
import { 结语 } from "./scenes/结语";

// 场景定义
const SCENES = [
        { name: "开场Hook", durationInFrames: 300, fps: 30 },
        { name: "核心架构", durationInFrames: 300, fps: 30 },
        { name: "上下文管理", durationInFrames: 360, fps: 30 },
        { name: "安全约束", durationInFrames: 300, fps: 30 },
        { name: "多Agent协作", durationInFrames: 240, fps: 30 },
        { name: "结语", durationInFrames: 150, fps: 30 }
];

// 旁白文本
const NARRATIONS = {
  开场Hook: `Cloud Code 源码泄露，目前公认最强的编码 Agent。核心竞争力不在模型，而在模型周围那套精密的控制系统。|核心骨架是一个 While 循环加一组工具，叫 Query Engine，用户输入一句话，构建提示词，调用模型，执行工具，循环直到输出结果。|第一层是上下文管理，三级压缩流水线：微压缩保留最近结果，记忆压缩提取结构化事实，完整压缩总结对话。|第二层是安全约束，五步评估加双层分类器，规则是法律不是建议。|第三层是多 Agent 协作，Leader 生成 Teammate，上下文隔离但关键发现同步。|`,
  核心架构: ``,
  上下文管理: ``,
  安全约束: ``,
  多Agent协作: ``,
  结语: ``
};

export const Video: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <TransitionSeries>
        {SCENES.map((scene) => {
          const narration = NARRATIONS[scene.name] || "";
          return (
            <TransitionSeries.Sequence
              key={scene.name}
              durationInFrames={scene.durationInFrames}
            >
              <TransitionSeries.Transition
                presentation={fade()}
                timing={linearTiming({ durationInFrames: 15 })}
              />
              <SceneWrapper name={scene.name} narration={narration} />
            </TransitionSeries.Sequence>
          );
        })}
      </TransitionSeries>
    </AbsoluteFill>
  );
};

// 场景渲染分发
const SceneWrapper: React.FC<{ name: string; narration: string }> = ({ name, narration }) => {
  switch (name) {
    case "开场Hook": return <开场Hook narration={narration} />;
    case "核心架构": return <核心架构 narration={narration} />;
    case "上下文管理": return <上下文管理 narration={narration} />;
    case "安全约束": return <安全约束 narration={narration} />;
    case "多Agent协作": return <多Agent协作 narration={narration} />;
    case "结语": return <结语 narration={narration} />;
    default: return <div style={{ color: "#fff" }}>Unknown: {name}</div>;
  }
};
