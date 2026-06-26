import React from "react";
import { AbsoluteFill } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { 开场Hook } from "./scenes/开场Hook";
import { 四层框架 } from "./scenes/四层框架";
import { 微压缩 } from "./scenes/微压缩";
import { 会话记忆压缩 } from "./scenes/会话记忆压缩";
import { 完整压缩 } from "./scenes/完整压缩";
import { 自动触发 } from "./scenes/自动触发";
import { 工具系统 } from "./scenes/工具系统";
import { 总结 } from "./scenes/总结";

// 8个场景，时长对应95秒总长
const SCENES = [
  { name: "开场Hook",      durationInFrames: 300  },  // 10s
  { name: "四层框架",       durationInFrames: 360  },  // 12s
  { name: "微压缩",         durationInFrames: 480  },  // 16s
  { name: "会话记忆压缩",   durationInFrames: 420  },  // 14s
  { name: "完整压缩",       durationInFrames: 480  },  // 16s
  { name: "自动触发",       durationInFrames: 420  },  // 14s
  { name: "工具系统",       durationInFrames: 360  },  // 12s
  { name: "总结",           durationInFrames: 300  },  // 10s
];

export const Video: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0f" }}>
      <TransitionSeries>
        {SCENES.map((scene) => (
          <TransitionSeries.Sequence
            key={scene.name}
            durationInFrames={scene.durationInFrames}
          >
            <TransitionSeries.Transition
              presentation={fade()}
              timing={linearTiming({ durationInFrames: 12 })}
            />
            <SceneWrapper name={scene.name} />
          </TransitionSeries.Sequence>
        ))}
      </TransitionSeries>
    </AbsoluteFill>
  );
};

const SceneWrapper: React.FC<{ name: string }> = ({ name }) => {
  switch (name) {
    case "开场Hook":      return <开场Hook />;
    case "四层框架":       return <四层框架 />;
    case "微压缩":         return <微压缩 />;
    case "会话记忆压缩":   return <会话记忆压缩 />;
    case "完整压缩":       return <完整压缩 />;
    case "自动触发":       return <自动触发 />;
    case "工具系统":       return <工具系统 />;
    case "总结":           return <总结 />;
    default:              return <div style={{ color: "#fff" }}>Unknown: {name}</div>;
  }
};
