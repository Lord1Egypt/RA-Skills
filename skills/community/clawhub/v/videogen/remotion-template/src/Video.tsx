import React, { useState, useEffect } from "react";
import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
  useCurrentFrame,
  springTiming,
  interpolate,
  Easing,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import { Opening } from "./scenes/Opening";
import { HarnessIntro } from "./scenes/HarnessIntro";
import { ToolLayer } from "./scenes/ToolLayer";
import { AgentLoop } from "./scenes/AgentLoop";
import { ContextLayers } from "./scenes/ContextLayers";
import { PermissionSystem } from "./scenes/PermissionSystem";
import { MCPSystem } from "./scenes/MCPSystem";
import { ClosingScene } from "./scenes/ClosingScene";

// ─── 场景定义 ───
// 每个场景：名称 + 帧数（30fps）
// 总时长 = sum(durationsInFrames)
const SCENES = [
  { name: "Opening",         durationInFrames: 30 * 20,  fps: 30 },  // 0-20s
  { name: "HarnessIntro",    durationInFrames: 30 * 30,  fps: 30 },  // 20-50s
  { name: "ToolLayer",       durationInFrames: 30 * 45,  fps: 30 },  // 50-95s
  { name: "AgentLoop",       durationInFrames: 30 * 50,  fps: 30 },  // 95-145s
  { name: "ContextLayers",   durationInFrames: 30 * 45,  fps: 30 },  // 145-190s
  { name: "PermissionSystem",durationInFrames: 30 * 35,  fps: 30 },  // 190-225s
  { name: "MCPSystem",       durationInFrames: 30 * 35,  fps: 30 },  // 225-260s
  { name: "Closing",        durationInFrames: 30 * 40,  fps: 30 },  // 260-300s
] as const;

// ─── 配音文本 ───
// 与场景顺序对应的完整旁白文本
const NARRATIONS: Record<string, string> = {
  Opening: `你在终端里敲了一行字，按下回车。AI 开始读文件、改代码、跑测试——整个过程没有你介入。它是怎么知道该做什么、不该做什么的？答案是：不是 AI 自己知道，是有一套系统，在替它管理这一切。今天，我们就把这套系统，从里到外讲清楚。`,

  HarnessIntro: `大多数人对 Claude Code 的理解，是一个聊天机器人。但真正用下来，你会发现它跟聊天完全不一样。Claude Code 的本质是一个 agent harness system。它把 AI 模型，通过工具连接层，接入开发环境，再加上状态管理、权限控制、会话管理——四个模块串成一圈，形成完整的运转系统。`,

  ToolLayer: `先看工具层。Claude Code 内置了三大类工具。第一类：文件操作——读写、编辑、glob 搜索、grep 关键词，让 AI 能精确找到要改的代码。第二类：终端执行——跑测试、构建项目、处理脚本，注意这些不是 AI 直接执行，而是 Harness 接收请求、校验权限、执行命令、返回结果。第三类：高级工具——AgentTool，让 AI 调用子 agent 完成任务。工具再丰富，它也只是执行层的东西。下一个问题是：AI 是怎么决定用什么工具、怎么组织行动步骤的？`,

  AgentLoop: `答案是 Agent Loop，代理循环，这是 Claude Code 最核心的引擎。它分四个步骤不断运转。第一步，计划——你给一个任务，AI 先想清楚：需要改几个文件？先读还是先写？第二步，选择工具——根据计划决定调用哪个工具。第三步，执行——Harness 接收工具调用请求，校验权限，执行命令，返回结果。第四步，评估——AI 拿到执行结果，判断：成功了吗？报错了吗？需要换一种方式吗？然后循环回来。这个过程一直重复，直到任务完成，或者 token 用完，或者你手动中断。这里有一个关键点：AI 不是一次给出一个完整答案，它是多轮循环逐步逼近答案的。`,

  ContextLayers: `Agent Loop 有一个隐含的前提：AI 每次循环，都需要知道现在在哪、之前发生了什么、这个项目是什么。这就是上下文管理，分三个层次。第一层：会话历史——你关掉终端再回来，输入 /resume，它能回到上次中断的地方继续工作。第二层：上下文窗口——AI 有 token 上限，当对话越来越长，Claude Code 会自动压缩历史内容，保留最重要的上下文，这个过程叫 Compact。第三层：项目级记忆 CLAUDE.md——你在项目根目录下创建一个文件，写明项目的技术栈、架构约定、不想被改动的规则，AI 每次启动时都会自动读取这份文件。这三层加起来，就是 Claude Code 的完整记忆系统。`,

  PermissionSystem: `工具再强大，如果 AI 可以无限制地读写和执行，那太危险了。所以 Claude Code 有一套权限系统，分三档。只读模式：AI 只能读文件，不能写，不能执行任何修改操作。工作区写入模式：AI 可以读写文件、创建目录、运行测试，但不能执行高危命令，比如删除整个项目目录。完全信任模式：AI 可以执行任何操作，默认是关闭的，除非你主动开启。除了这三档，还有一道前置守卫，叫 PreToolUse Hook——在工具真正执行之前，Harness 会先停下来，检查请求是否合法、参数是否有问题。你可以在这个节点上加自己的检查逻辑。权限系统，加上这道 Hook，才构成了完整的 AI 行动守卫体系。`,

  MCPSystem: `内置工具再多，总有不够用的时候。Claude Code 通过 MCP 协议来扩展工具链。MCP 是 Anthropic 推出的一个开放标准，核心思想很简单：定义一套标准接口，任何实现了这套接口的工具，都可以被 Claude Code 调用。以前每个工具都要单独对接 Claude Code 的 API，现在只要符合 MCP 标准，插上就能用。现在社区里已经有很多人做了 MCP 适配器——数据库连接工具、GitHub 操作工具、Slack 通知工具、公司内部的定制系统。只要有人写过适配器，你就可以把它接进来。Claude Code 不是一个封闭的系统，而是一个工具平台。`,

  Closing: `好了，四个模块都讲完了。最后说一点想法。Claude Code 的核心创新，不在于它的 AI 有多强，而在于它那套 harness 系统——把一个不确定的模型，变成了一个可靠的工具。这才是它真正值钱的地方。关注我，我们继续拆解 AI 时代的工程能力。`,
};

// ─── 字幕组件（复用 TikTok 风格）───
interface CaptionWord {
  text: string;
  startMs: number;
  endMs: number;
}

const CaptionDisplay: React.FC<{ captions: CaptionWord[]; startFrame: number }> = ({
  captions,
  startFrame,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentMs = ((startFrame + frame) / fps) * 1000;

  // 找出当前时间对应的词
  const activeCaption = captions.find(
    (c) => c.startMs <= currentMs && c.endMs > currentMs
  );

  if (!activeCaption) return null;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 80,
        left: "50%",
        transform: "translateX(-50%)",
        backgroundColor: "rgba(0,0,0,0.8)",
        color: "#fff",
        fontSize: 28,
        fontFamily: "system-ui, sans-serif",
        fontWeight: "bold",
        padding: "10px 24px",
        borderRadius: 8,
        letterSpacing: 1,
      }}
    >
      {activeCaption.text}
    </div>
  );
};

// ─── 主视频组件 ───
export const Video: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* 场景序列 */}
      <TransitionSeries>
        {SCENES.map((scene) => {
          const narration = NARRATIONS[scene.name] || "";
          const key = scene.name;

          return (
            <TransitionSeries.Sequence
              key={key}
              durationInFrames={scene.durationInFrames}
            >
              <TransitionSeries.Transition
                presentation={fade()}
                timing={linearTiming({ durationInFrames: 15 })}
              />

              {/* 根据场景名称选择对应组件 */}
              {scene.name === "Opening" && <Opening narration={narration} />}
              {scene.name === "HarnessIntro" && <HarnessIntro narration={narration} />}
              {scene.name === "ToolLayer" && <ToolLayer narration={narration} />}
              {scene.name === "AgentLoop" && <AgentLoop narration={narration} />}
              {scene.name === "ContextLayers" && <ContextLayers narration={narration} />}
              {scene.name === "PermissionSystem" && <PermissionSystem narration={narration} />}
              {scene.name === "MCPSystem" && <MCPSystem narration={narration} />}
              {scene.name === "Closing" && <ClosingScene narration={narration} />}
            </TransitionSeries.Sequence>
          );
        })}
      </TransitionSeries>
    </AbsoluteFill>
  );
};
