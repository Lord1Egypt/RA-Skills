import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { 开场Hook } from "./scenes/开场Hook";
import { 生产数据 } from "./scenes/生产数据";
import { 微压缩 } from "./scenes/微压缩";
import { 绘画记忆压缩 } from "./scenes/绘画记忆压缩";
import { 完整压缩 } from "./scenes/完整压缩";
import { 自动触发 } from "./scenes/自动触发";
import { 结语 } from "./scenes/结语";

// 场景定义
const SCENES = [
        { name: "开场Hook", durationInFrames: 240, fps: 30 },
        { name: "生产数据", durationInFrames: 240, fps: 30 },
        { name: "微压缩", durationInFrames: 240, fps: 30 },
        { name: "绘画记忆压缩", durationInFrames: 240, fps: 30 },
        { name: "完整压缩", durationInFrames: 240, fps: 30 },
        { name: "自动触发", durationInFrames: 240, fps: 30 },
        { name: "结语", durationInFrames: 270, fps: 30 }
];

// 旁白文本
const NARRATIONS = {
  开场Hook: `Cloud Code 的上下文管理是整个 Harness 工程含量最高的部分。源码注释里有条2026年3月的生产数据：1279个会话出现50次以上连续压缩失败，最多的失败3272次，全局每天浪费约25万次API调用，修复方案三行代码。|1279个会话，50次以上连续失败，最多的3272次，25万次API调用每天。三行代码修复。这个系统不是设计出来的，是踩坑踩出来的。|`,
  生产数据: ``,
  微压缩: ``,
  绘画记忆压缩: ``,
  完整压缩: ``,
  自动触发: ``,
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
    case "生产数据": return <生产数据 narration={narration} />;
    case "微压缩": return <微压缩 narration={narration} />;
    case "绘画记忆压缩": return <绘画记忆压缩 narration={narration} />;
    case "完整压缩": return <完整压缩 narration={narration} />;
    case "自动触发": return <自动触发 narration={narration} />;
    case "结语": return <结语 narration={narration} />;
    default: return <div style={{ color: "#fff" }}>Unknown: {name}</div>;
  }
};
