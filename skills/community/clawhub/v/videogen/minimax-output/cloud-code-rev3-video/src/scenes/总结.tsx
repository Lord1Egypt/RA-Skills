import React from "react";
import { AbsoluteFill } from "remotion";
import { AppleBg, SceneTag, TagGroup, EngineSpin } from "../components/AppleShared";

export const 总结: React.FC = () => {
  return (
    <AppleBg>
      <SceneTag text="总结" startFrame={0} color="#FFFFFF" />
      <div style={{
        position: "absolute",
        top: "10%",
        left: 0,
        right: 0,
        textAlign: "center",
      }}>
        <div style={{
          fontSize: 24,
          color: "#FFFFFF",
          fontWeight: 700,
          fontFamily: "Inter, -apple-system, sans-serif",
        }}>
          关键不是装不装得下，而是该不该装进去
        </div>
      </div>

      <div style={{
        position: "absolute",
        top: "22%",
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
      }}>
        <EngineSpin startFrame={8} />
      </div>

      <div style={{
        position: "absolute",
        bottom: "38%",
        left: 0,
        right: 0,
        textAlign: "center",
      }}>
        <div style={{
          fontSize: 28,
          fontWeight: 800,
          color: "#FFFFFF",
          fontFamily: "Inter, -apple-system, sans-serif",
          letterSpacing: "-0.02em",
          lineHeight: 1.2,
        }}>
          模型是引擎
        </div>
        <div style={{
          fontSize: 28,
          fontWeight: 800,
          color: "#0A84FF",
          fontFamily: "Inter, -apple-system, sans-serif",
          letterSpacing: "-0.02em",
          marginTop: 8,
        }}>
          上下文管理是油路系统
        </div>
        <div style={{
          fontSize: 20,
          color: "#48484A",
          fontFamily: "Inter, -apple-system, sans-serif",
          marginTop: 10,
        }}>
          再强的引擎，没油也跑不动
        </div>
      </div>

      <div style={{ position: "absolute", bottom: 70, left: 0, right: 0 }}>
        <TagGroup
          startFrame={55}
          tags={[
            { text: "上下文是稀缺资源", color: "#8E8E93" },
            { text: "需要主动管理", color: "#8E8E93" },
            { text: "四层压缩各有权衡", color: "#8E8E93" },
            { text: "每一层假设上一层不够用", color: "#8E8E93" },
          ]}
        />
      </div>
    </AppleBg>
  );
};
