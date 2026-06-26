import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { 开场Hook } from "./scenes/开场Hook";
import { 四层记忆塔 } from "./scenes/四层记忆塔";
import { 五层天花板 } from "./scenes/五层天花板";
import { Memsearch架构 } from "./scenes/Memsearch架构";
import { 结尾收尾 } from "./scenes/结尾收尾";

// 场景定义（总时长 142s = 4260 frames，配合 142.8s 旁白）
const SCENES = [
  { name: "开场Hook",      durationInFrames: 600,  fps: 30 },  // 20s
  { name: "四层记忆塔",   durationInFrames: 1050, fps: 30 },  // 35s
  { name: "五层天花板",   durationInFrames: 900,  fps: 30 },  // 30s
  { name: "Memsearch架构",durationInFrames: 1200, fps: 30 }, // 40s
  { name: "结尾收尾",     durationInFrames: 510,  fps: 30 },  // 17s
];

// 旁白文本
const NARRATIONS = {
  开场Hook: `Claude Code源码泄露，51万行代码公之于众。研究完之后的结论很意外——它的记忆系统，比想象中初级得多。|第一层CLAUDE。md你写的规则文件。第二层Auto Memory，agent自己记笔记。第三层Auto Dream，让agent做梦整理记忆。第四层KAIROS，后台守护进程。|五层天花板绕不过去：200行硬上限，grep检索，粒度太粗，补丁越叠越复杂，记忆锁在单个工具里。|memsearch把记忆从agent里抽出来，放到独立持久层。自动记忆不漏对话，混合搜索语义加关键词，召回分三层按需取用。|单agent内部的记忆优化，架构限制不是bug。但限制就是限制，天花板在那。记忆应该比任何一个agent都活得更长。`,
  四层记忆塔: ``,
  五层天花板: ``,
  Memsearch架构: ``,
  结尾收尾: ``
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
    case "四层记忆塔": return <四层记忆塔 narration={narration} />;
    case "五层天花板": return <五层天花板 narration={narration} />;
    case "Memsearch架构": return <Memsearch架构 narration={narration} />;
    case "结尾收尾": return <结尾收尾 narration={narration} />;
    default: return <div style={{ color: "#fff" }}>Unknown: {name}</div>;
  }
};
