import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

const LAYERS = [
  { label: "CLAUDE.md",     sublabel: "用户书写的规则文件",              desc: "项目级 · 个人级 · 组织级",          color: "#48dbfb", icon: "▣" },
  { label: "Auto Memory",   sublabel: "agent 主动记录 · 按需加载",         desc: "user · feedback · project · reference", color: "#feca57", icon: "◇" },
  { label: "Auto Dream",   sublabel: "记忆整合 · 让 agent 做梦",          desc: "每24h + 5次会话触发",               color: "#ff9f43", icon: "◈" },
  { label: "KAIROS",       sublabel: "后台守护进程 · 主动行动",           desc: "15秒阻塞预算 · append-only日志",      color: "#ff6b6b", icon: "◉" },
];

// 从下到上排列：CLAUDE.md 在最底部，KAIROS 在最顶部（层级越高越在上）
const ITEM_H  = 76;
const GAP     = 10;
const CARD_W  = 560;
const TOTAL_H = LAYERS.length * ITEM_H + (LAYERS.length - 1) * GAP;

export const 四层记忆塔: React.FC<{ narration: string }> = ({ narration }) => {
  const { height } = useVideoConfig();
  const frame = useCurrentFrame();
  const dur = 35;
  const progress = Math.min(frame / dur, 1);
  const phase = (s: number) => Math.max(0, Math.min((progress - s) / 0.06, 1));

  // Phase: 0=title, 0.08-0.92=4层叠显(逐层亮), 0.92-1=all
  const showAll     = progress >= 0.92;
  const layerPhase  = (i: number) => {
    // i=3(CLAUDE)先亮，i=0(KAIROS)最后亮
    const starts = [0.08, 0.20, 0.40, 0.60]; // KAIROS,i=0 第一个亮
    return Math.max(0, Math.min((progress - starts[i]) / 0.12, 1));
  };

  const safeTop    = 80;
  const safeBottom = 100;
  const availableH = height - safeTop - safeBottom;
  const stackTop    = safeTop + Math.max(0, (availableH - TOTAL_H) / 2);

  // 当前高亮的层 index（0=KAIROS, 3=CLAUDE.md）
  const activeIdx = showAll
    ? -1
    : [0, 1, 2, 3].findLast((i) => progress >= 0.08 + i * 0.20);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", alignItems: "center" }}>
      {/* 标题 */}
      <div style={{
        position: "absolute", top: safeTop - 52,
        width: "100%", textAlign: "center",
        fontSize: 48, fontWeight: "bold", color: "#fff",
        fontFamily: "system-ui, sans-serif",
        opacity: phase(0),
      }}>
        Claude Code 记忆四层塔
      </div>

      {/* 四层卡片（全部同时可见，当前层高亮，其余淡化） */}
      <div style={{
        position: "absolute",
        top: stackTop,
        left: 0, right: 0,
        display: "flex", flexDirection: "column", alignItems: "center",
        gap: GAP,
      }}>
        {LAYERS.map((l, i) => {
          const lp = layerPhase(i);
          const isActive  = activeIdx === i;
          const isDormant = activeIdx !== undefined && !isActive && !showAll;
          const alpha     = isDormant ? 0.25 : 1;

          return (
            <div key={i} style={{
              width: CARD_W,
              height: ITEM_H,
              backgroundColor: isActive ? l.color + "28" : l.color + "0e",
              border: `2px solid ${l.color}${isActive ? "" : "44"}`,
              borderRadius: 12,
              padding: "0 18px",
              display: "flex", alignItems: "center", gap: 14,
              opacity: lp,
              transition: "backgroundColor 0.4s, border-color 0.4s",
            }}>
              <span style={{ fontSize: 28, color: l.color, opacity: alpha }}>{l.icon}</span>
              <span style={{ fontSize: 32, fontWeight: "bold", color: l.color, opacity: alpha }}>
                {l.label}
              </span>
              <span style={{ fontSize: 22, color: "#888", opacity: alpha }}>
                {l.sublabel}
              </span>
              {/* 当前层进度条 */}
              {isActive && (
                <div style={{
                  position: "absolute", bottom: 0, left: 0,
                  height: 3, borderRadius: "0 0 12px 12px",
                  backgroundColor: l.color,
                  width: `${Math.min((progress - (0.08 + i * 0.20)) / 0.20 * 100, 100)}%`,
                  transition: "width 0.1s linear",
                }} />
              )}
            </div>
          );
        })}
      </div>

      {/* 底部进度指示 */}
      {activeIdx !== undefined && !showAll && (
        <div style={{
          position: "absolute", bottom: safeBottom - 36,
          width: "100%", textAlign: "center",
          fontSize: 24, color: "#555",
        }}>
          {activeIdx + 1} / 4
        </div>
      )}

      {/* 收尾注释 */}
      {showAll && (
        <div style={{
          position: "absolute", bottom: safeBottom - 36,
          width: "100%", textAlign: "center",
          fontSize: 24, color: "#555",
          opacity: phase(0.92),
          fontFamily: "system-ui, sans-serif",
        }}>
          每一层都在补上一层的锅
        </div>
      )}
    </AbsoluteFill>
  );
};
