import React from "react";
import { AbsoluteFill } from "remotion";
import { AppleBg, FuseSteps, SceneTag, TagGroup } from "../components/AppleShared";

export const 自动触发: React.FC = () => {
  return (
    <AppleBg>
      <SceneTag text="第四层 · 自动触发 + 熔断器" startFrame={0} color="#FF453A" />
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
          每次模型调用后检查 Token 用量
        </div>
        <div style={{
          fontSize: 14,
          color: "#8E8E93",
          fontFamily: "Inter, -apple-system, sans-serif",
          marginTop: 4,
        }}>
          阈值：上下文窗口 − 13000 token 缓冲
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
        <FuseSteps startFrame={12} />
      </div>

      <div style={{ position: "absolute", bottom: 70, left: 0, right: 0 }}>
        <TagGroup
          startFrame={72}
          tags={[
            { text: "子 agent 不会触发自动压缩", color: "#FF453A" },
            { text: "避免死锁", color: "#FF453A" },
            { text: "session memory", color: "#48484A" },
            { text: "compact query source", color: "#48484A" },
          ]}
        />
      </div>
    </AppleBg>
  );
};
