import React from "react";
import { AbsoluteFill } from "remotion";
import { AppleBg, LayerStack, SceneTag } from "../components/AppleShared";

export const 四层框架: React.FC = () => {
  return (
    <AppleBg>
      <SceneTag text="四层压缩框架" startFrame={0} color="#0A84FF" />
      <div style={{
        position: "absolute",
        top: "15%",
        left: 0,
        right: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}>
        <LayerStack
          startFrame={8}
          layers={[
            { label: "第四层 · 自动触发", sub: "阈值检测 + 熔断器", color: "#FF453A" },
            { label: "第三层 · 完整压缩", sub: "模型调用 + 摘要生成", color: "#BF5AF2" },
            { label: "第二层 · 会话记忆压缩", sub: "结构化事实提取", color: "#30D158" },
            { label: "第一层 · 微压缩", sub: "零成本规则驱动", color: "#0A84FF" },
          ]}
        />
      </div>
    </AppleBg>
  );
};
