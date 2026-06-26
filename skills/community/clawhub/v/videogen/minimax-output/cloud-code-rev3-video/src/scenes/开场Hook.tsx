import React from "react";
import { AbsoluteFill } from "remotion";
import { AppleBg, HeroTitle, SceneTag } from "../components/AppleShared";

export const 开场Hook: React.FC = () => {
  return (
    <AppleBg>
      <SceneTag text="Cloud Code 源码解读 · 上下文管理" startFrame={0} color="#0A84FF" />
      <div style={{
        position: "absolute",
        top: "18%",
        left: 0,
        right: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 0,
      }}>
        <HeroTitle text="上下文管理" startFrame={5} size={88} />
        <div style={{ display: "flex", gap: 16, marginTop: 24 }}>
          {[
            { label: "四层压缩", color: "#0A84FF" },
            { label: "子系统", color: "#BF5AF2" },
          ].map((badge, i) => (
            <div key={i} style={{
              backgroundColor: badge.color + "18",
              border: `1px solid ${badge.color}44`,
              borderRadius: 24,
              padding: "12px 32px",
              fontSize: 24,
              fontWeight: 700,
              color: badge.color,
              fontFamily: "Inter, -apple-system, sans-serif",
            }}>
              {badge.label}
            </div>
          ))}
        </div>
      </div>
      <div style={{
        position: "absolute",
        bottom: 80,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
      }}>
        <div style={{
          fontSize: 22,
          color: "#48484A",
          fontFamily: "Inter, -apple-system, sans-serif",
        }}>
          Harness Engineering · 源码系列
        </div>
      </div>
    </AppleBg>
  );
};
