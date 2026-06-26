import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

const ITEMS = [
  { num: "01", title: "200行硬上限", detail: "新记忆把老记忆顶掉", color: "#ff6b6b" },
  { num: "02", title: "只有grep检索", detail: "语义不匹配就搜不到", color: "#ff9f43" },
  { num: "03", title: "粒度太粗", detail: "代码片段调试上下文丢", color: "#feca57" },
  { num: "04", title: "补丁越叠越复杂", detail: "Auto Memory → Dream → KAIROS", color: "#48dbfb" },
  { num: "05", title: "记忆锁在单个工具", detail: "换 agent 从零开始", color: "#a29bfe" },
];

const ITEM_H = 68;
const GAP    = 10;
const TOTAL_H = ITEMS.length * ITEM_H + (ITEMS.length - 1) * GAP;

export const 五层天花板: React.FC<{ narration: string }> = ({ narration }) => {
  const { height } = useVideoConfig();
  const frame = useCurrentFrame();
  const dur = 30;
  const progress = Math.min(frame / dur, 1);
  const phase = (s: number, e: number) => Math.max(0, Math.min((progress - s) / (e - s), 1));

  const safeTop = 90;
  const safeBottom = 90;
  const availableH = height - safeTop - safeBottom;
  const stackTop = safeTop + Math.max(0, (availableH - TOTAL_H) / 2);

  const showAll = progress >= 0.70;
  const cardPhase = (i: number) => {
    const starts = [0.07, 0.07, 0.25, 0.25, 0.50];
    const s = starts[i];
    return Math.max(0, Math.min((progress - s) / 0.2, 1));
  };
  const isActive = (i: number) => {
    const starts = [0.07, 0.07, 0.25, 0.25, 0.50];
    return progress >= starts[i] && progress < 0.70;
  };

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d0d0d", alignItems: "center" }}>
      {/* 标题 */}
      <div style={{
        position: "absolute", top: safeTop - 54,
        width: "100%", textAlign: "center",
        fontSize: 56, fontWeight: "bold", color: "#fff",
        fontFamily: "system-ui, sans-serif",
        opacity: phase(0, 0.07),
      }}>
        五层天花板
      </div>

      {/* 单卡片 */}
      {!showAll && ITEMS.map((item, i) => {
        if (!isActive(i)) return null;
        const cp = cardPhase(i);
        return (
          <div key={i} style={{
            position: "absolute",
            top: stackTop,
            left: 0, right: 0,
            display: "flex", justifyContent: "center",
            opacity: 1,
          }}>
            <div style={{
              width: 640,
              height: ITEM_H,
              backgroundColor: "#111",
              border: `2px solid ${item.color}55`,
              borderLeft: `6px solid ${item.color}`,
              borderRadius: 12,
              padding: "0 20px",
              display: "flex", alignItems: "center", gap: 14,
              opacity: cp,
            }}>
              <span style={{ fontSize: 52, fontWeight: "bold", color: item.color, minWidth: 70 }}>{item.num}</span>
              <span style={{ fontSize: 40, fontWeight: "bold", color: "#fff" }}>{item.title}</span>
              <span style={{ fontSize: 24, color: "#666", marginLeft: "auto" }}>{item.detail}</span>
            </div>
          </div>
        );
      })}

      {/* 全家桶 */}
      {showAll && (
        <div style={{
          position: "absolute", top: stackTop,
          left: 0, right: 0,
          display: "flex", flexDirection: "column", alignItems: "center",
          gap: GAP,
          opacity: phase(0.70, 1),
        }}>
          {ITEMS.map((item, i) => (
            <div key={i} style={{
              width: 640,
              height: ITEM_H,
              backgroundColor: "#111",
              border: `1px solid ${item.color}33`,
              borderLeft: `4px solid ${item.color}`,
              borderRadius: 8,
              padding: "0 18px",
              display: "flex", alignItems: "center", gap: 12,
            }}>
              <span style={{ fontSize: 36, fontWeight: "bold", color: item.color, minWidth: 60 }}>{item.num}</span>
              <span style={{ fontSize: 32, fontWeight: "bold", color: "#ccc" }}>{item.title}</span>
              <span style={{ fontSize: 20, color: "#555", marginLeft: "auto" }}>{item.detail}</span>
            </div>
          ))}
          <div style={{ fontSize: 24, color: "#666", marginTop: 4, fontFamily: "system-ui" }}>
            单 agent 内部记忆优化，架构限制不是 bug，是路线选择
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
