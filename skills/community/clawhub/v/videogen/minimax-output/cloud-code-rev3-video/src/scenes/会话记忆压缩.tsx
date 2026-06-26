import React from "react";
import { AbsoluteFill } from "remotion";
import { AppleBg, PipelineFlow, SceneTag, TagGroup } from "../components/AppleShared";

export const 会话记忆压缩: React.FC = () => {
  return (
    <AppleBg>
      <SceneTag text="第二层 · 会话记忆压缩" startFrame={0} color="#30D158" />
      <div style={{
        position: "absolute",
        top: "10%",
        left: 0,
        right: 0,
        textAlign: "center",
      }}>
        <div style={{
          fontSize: 22,
          color: "#FFFFFF",
          fontWeight: 700,
          fontFamily: "Inter, -apple-system, sans-serif",
        }}>
          不是删东西，是提炼东西
        </div>
      </div>

      <div style={{
        position: "absolute",
        top: "26%",
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
      }}>
        <PipelineFlow
          startFrame={10}
          steps={[
            { label: "对话历史", sub: "原始消息", color: "#8E8E93" },
            { label: "后台提取", sub: "结构化事实", color: "#30D158" },
            { label: "Memory.d", sub: "持久化存储", color: "#0A84FF" },
            { label: "注入上下文", sub: "替代摘要", color: "#BF5AF2" },
          ]}
        />
      </div>

      <div style={{ position: "absolute", bottom: 70, left: 0, right: 0 }}>
        <TagGroup
          startFrame={55}
          tags={[
            { text: "不需要调用模型", color: "#30D158" },
            { text: "成本比完整压缩低得多", color: "#30D158" },
            { text: "保留最近对话完整细节", color: "#30D158" },
            { text: "tool use / result 不能拆开", color: "#48484A" },
          ]}
        />
      </div>
    </AppleBg>
  );
};
