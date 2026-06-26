import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { 开场 } from "./scenes/开场";
import { HarnessIntro } from "./scenes/HarnessIntro";
import { 工具层 } from "./scenes/工具层";
import { AgentLoop } from "./scenes/AgentLoop";
import { 上下文管理 } from "./scenes/上下文管理";
import { 权限系统 } from "./scenes/权限系统";
import { MCP协议 } from "./scenes/MCP协议";
import { 结尾 } from "./scenes/结尾";

// 场景定义
const SCENES = [
        { name: "开场", durationInFrames: 600, fps: 30 },
        { name: "HarnessIntro", durationInFrames: 900, fps: 30 },
        { name: "工具层", durationInFrames: 1350, fps: 30 },
        { name: "AgentLoop", durationInFrames: 1500, fps: 30 },
        { name: "上下文管理", durationInFrames: 1350, fps: 30 },
        { name: "权限系统", durationInFrames: 1050, fps: 30 },
        { name: "MCP协议", durationInFrames: 1050, fps: 30 },
        { name: "结尾", durationInFrames: 1200, fps: 30 }
];

// 旁白文本
const NARRATIONS = {
  开场: `你在终端里敲了一行字，按下回车。AI开始读文件、改代码、跑测试——整个过程没有你介入。它是怎么知道该做什么、不该做什么的？答案是：不是AI自己知道，是有一套系统，在替它管理这一切。今天，我们就把这套系统，从里到外讲清楚。`,
  HarnessIntro: `大多数人对Claude Code的理解，是一个聊天机器人。但真正用下来，你会发现它跟聊天完全不一样。Claude Code的本质是一个agent harness system。它把AI模型，通过工具连接层，接入开发环境，再加上状态管理、权限控制、会话管理——四个模块串成一圈，形成完整的运转系统。`,
  工具层: `先看工具层。Claude Code内置了三大类工具。第一类：文件操作——读写、编辑、glob搜索、grep关键词，让AI能精确找到要改的代码。第二类：终端执行——跑测试、构建项目、处理脚本，注意这些不是AI直接执行，而是Harness接收请求、校验权限、执行命令、返回结果。第三类：高级工具——AgentTool，让AI调用子agent完成任务。`,
  AgentLoop: `答案是Agent Loop，代理循环，这是Claude Code最核心的引擎。它分四个步骤不断运转。第一步，计划——你给一个任务，AI先想清楚：需要改几个文件？先读还是先写？第二步，选择工具——根据计划决定调用哪个工具。第三步，执行——Harness接收工具调用请求，校验权限，执行命令，返回结果。第四步，评估——AI拿到执行结果，判断：成功了吗？报错了吗？然后循环回来。这个过程一直重复，直到任务完成，或者token用完，或者你手动中断。`,
  上下文管理: `Agent Loop有一个隐含的前提：AI每次循环都需要知道现在在哪、之前发生了什么、这个项目是什么，这就是上下文管理，分三个层次。第一层：会话历史——你关掉终端再回来，输入/resume，它能回到上次中断的地方继续工作。第二层：上下文窗口——AI有token上限，当对话越来越长，Claude Code会自动压缩历史内容，保留最重要的上下文，这个过程叫Compact。第三层：项目级记忆CLAUDE.md——你在项目根目录下创建一个文件，写明项目的技术栈、架构约定、不想被改动的规则，AI每次启动时都会自动读取这份文件。这三层加起来，就是Claude Code的完整记忆系统。`,
  权限系统: `工具再强大，如果AI可以无限制地读写和执行，那太危险了。所以Claude Code有一套权限系统，分三档。只读模式：AI只能读文件，不能写，不能执行任何修改操作。工作区写入模式：AI可以读写文件、创建目录、运行测试，但不能执行高危命令。完全信任模式：AI可以执行任何操作，默认是关闭的，除非你主动开启。除了这三档，还有一道前置守卫，叫PreToolUse Hook——在工具真正执行之前，Harness会先停下来，检查请求是否合法。你可以在这个节点上加自己的检查逻辑。`,
  MCP协议: `内置工具再多，总有不够用的时候。Claude Code通过MCP协议来扩展工具链。MCP是Anthropic推出的一个开放标准，核心思想很简单：定义一套标准接口，任何实现了这套接口的工具，都可以被Claude Code调用。以前每个工具都要单独对接API，现在只要符合MCP标准，插上就能用。现在社区里已经有很多人做了MCP适配器——数据库连接工具、GitHub操作工具、Slack通知工具，公司内部的定制系统。只要有人写过适配器，你就可以把它接进来。`,
  结尾: `好了，四个模块都讲完了。最后说一点想法。Claude Code的核心创新，不在于它的AI有多强，而在于它那套harness系统——把一个不确定的模型，变成了一个可靠的工具。这才是它真正值钱的地方。关注我，我们继续拆解AI时代的工程能力。`
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
    case "开场": return <开场 narration={narration} />;
    case "HarnessIntro": return <HarnessIntro narration={narration} />;
    case "工具层": return <工具层 narration={narration} />;
    case "AgentLoop": return <AgentLoop narration={narration} />;
    case "上下文管理": return <上下文管理 narration={narration} />;
    case "权限系统": return <权限系统 narration={narration} />;
    case "MCP协议": return <MCP协议 narration={narration} />;
    case "结尾": return <结尾 narration={narration} />;
    default: return <div style={{ color: "#fff" }}>Unknown: {name}</div>;
  }
};
