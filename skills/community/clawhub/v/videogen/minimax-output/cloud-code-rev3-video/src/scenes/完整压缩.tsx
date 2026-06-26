import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { AppleBg, NineGrid, SceneTag, TagGroup } from "../components/AppleShared";

export const 完整压缩: React.FC = () => {
  return (
    <AppleBg>
      <SceneTag text="第三层 · 完整压缩" startFrame={0} color="#BF5AF2" />
      <div style={{
        position: "absolute",
        top: "10%",
        left: 0,
        right: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 16,
      }}>
        <div style={{
          fontSize: 22,
          color: "#FFFFFF",
          fontWeight: 700,
          fontFamily: "Inter, -apple-system, sans-serif",
        }}>
          九个维度总结对话
        </div>
        <NineGrid startFrame={8} items={[
          "用户请求/意图",
          "关键技术概念",
          "文件/代码片段",
          "错误/修复",
          "解决过程",
          "所有用户消息",
          "待办任务",
          "当前工作",
          "可选的下一步",
        ]} />
        <div style={{ display: "flex", gap: 16, alignItems: "center", marginTop: 4 }}>
          <div style={{
            backgroundColor: "#BF5AF218",
            border: "1px solid #BF5AF244",
            borderRadius: 12,
            padding: "12px 22px",
            fontSize: 14,
            color: "#BF5AF2",
            fontFamily: "Menlo, monospace",
          }}>
            &lt;analysis&gt; 思考分析 &lt;/analysis&gt;
          </div>
          <div style={{ color: "#48484A", fontSize: 20 }}>→</div>
          <div style={{
            backgroundColor: "#0A84FF18",
            border: "1px solid #0A84FF44",
            borderRadius: 12,
            padding: "12px 22px",
            fontSize: 14,
            color: "#0A84FF",
            fontFamily: "Menlo, monospace",
          }}>
            &lt;summary&gt; 输出摘要 &lt;/summary&gt;
          </div>
        </div>
        <div style={{
          fontSize: 13,
          color: "#48484A",
          fontFamily: "Inter, -apple-system, sans-serif",
        }}>
          analysis 标签格式化时被剥离，本质是内嵌 Chain of Thought
        </div>
      </div>
      <div style={{ position: "absolute", bottom: 70, left: 0, right: 0 }}>
        <TagGroup
          startFrame={62}
          tags={[
            { text: "压缩请求本身可能超长", color: "#48484A" },
            { text: "按 API 轮次分组丢弃", color: "#48484A" },
            { text: "重试三次后停止", color: "#48484A" },
            { text: "善后：恢复文件/plan/skill", color: "#48484A" },
          ]}
        />
      </div>
    </AppleBg>
  );
};
