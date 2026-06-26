import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

const EVENTS = [
  { date: "2026.04.01", title: "Claude Code 源码泄露", sub: "512,000 行 TypeScript 公之于众", color: "#ff4444" },
  { date: "研究结论", title: "记忆系统比想象中初级得多", sub: "扒开来看，记忆出不去，也活不长", color: "#ffd700" },
  { date: "但 Claude Code 做对了一件事", title: "开始认真对待 agent 记忆问题", sub: "KAIROS · Auto Dream · Auto Memory", color: "#00ff88" },
];

const CARD_H = 96;
const GAP = 14;
const TOTAL_H = EVENTS.length * CARD_H + (EVENTS.length - 1) * GAP;

export const 开场Hook: React.FC<{ narration: string }> = ({ narration }) => {
  const { height } = useVideoConfig();
  const frame = useCurrentFrame();
  const dur = 20;
  const progress = Math.min(frame / dur, 1);
  const ev = (i: number) => 0.05 + i * 0.28;
  const p = (i: number) => Math.max(0, Math.min((progress - ev(i)) / 0.15, 1));

  const safeTop = 80;
  const safeBottom = 100;
  const availableH = height - safeTop - safeBottom;
  const stackTop = safeTop + Math.max(0, (availableH - TOTAL_H) / 2);

  return (
    <AbsoluteFill style={{ backgroundColor: "#000", alignItems: "center" }}>
      {/* 顶部红线 */}
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 4, backgroundColor: "#ff4444", opacity: Math.min(progress / 0.1, 1) }} />

      {/* 事件卡片（垂直居中） */}
      <div style={{
        position: "absolute", top: stackTop,
        left: 0, right: 0,
        display: "flex", flexDirection: "column", alignItems: "center",
        gap: GAP,
      }}>
        {EVENTS.map((ev_, i) => {
          const active = progress >= ev(i);
          return (
            <div key={i} style={{
              width: 640,
              height: CARD_H,
              backgroundColor: "#111",
              border: `2px solid ${ev_.color}44`,
              borderLeft: `6px solid ${ev_.color}`,
              borderRadius: 12,
              padding: "0 18px",
              display: "flex", flexDirection: "column", justifyContent: "center",
              opacity: active ? p(i) : 0,
              transform: active ? `translateX(${(1 - p(i)) * -20}px)` : "none",
            }}>
              <div style={{ fontSize: 22, color: ev_.color, marginBottom: 2 }}>{ev_.date}</div>
              <div style={{ fontSize: 36, fontWeight: "bold", color: "#fff" }}>{ev_.title}</div>
              <div style={{ fontSize: 22, color: "#666" }}>{ev_.sub}</div>
            </div>
          );
        })}
      </div>

      {/* Terminal 预览 */}
      {progress > 0.70 && (
        <div style={{
          position: "absolute",
          bottom: safeBottom - 50,
          left: 0, right: 0,
          display: "flex", justifyContent: "center",
          opacity: Math.min((progress - 0.70) / 0.15, 1),
        }}>
          <div style={{
            width: 640,
            backgroundColor: "#0a0a0a",
            border: "1px solid #333",
            borderRadius: 10,
            padding: "12px 18px",
            fontFamily: "monospace",
            fontSize: 22,
            color: "#6bcb77",
          }}>
            <span style={{ color: "#555" }}>$ </span>
            Claude Code源码泄露，51万行代码。研究完结论——记忆系统比想象中初级得多。
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
