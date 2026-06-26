import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

const ARCH = [
  { label: "Agent Plugins", sub: "Claude Code · OpenClaw · OpenCode · Codex", color: "#48dbfb", items: ["自动拦截对话", "零配置接入", "跨平台统一格式"] },
  { label: "memsearch CLI / Python API", sub: "开发者集成层", color: "#feca57", items: ["混合搜索", "子 agent 召回", "索引管理"] },
  { label: "Core: Chunker → Embedder → Milvus", sub: "引擎层", color: "#ff9f43", items: ["Haiku 自动总结", "向量语义搜索", "BM25 精确匹配"] },
  { label: "Markdown Files", sub: "持久存储层 · Source of Truth", color: "#6bcb77", items: [".memsearch/memory/", "每天一个 .md", "随时可迁移"] },
];

const LEFT_W = 200;
const ITEM_H = 72;
const GAP = 10;
const LABEL_H = 72;
const TOTAL_H = ARCH.length * ITEM_H + (ARCH.length - 1) * GAP;

export const Memsearch架构: React.FC<{ narration: string }> = ({ narration }) => {
  const { height } = useVideoConfig();
  const frame = useCurrentFrame();
  const dur = 40;
  const progress = Math.min(frame / dur, 1);
  const phase = (s: number, e: number) => Math.max(0, Math.min((progress - s) / (e - s), 1));

  const safeTop = 100;
  const safeBottom = 100;
  const availableH = height - safeTop - safeBottom;
  const stackTop = safeTop + Math.max(0, (availableH - TOTAL_H) / 2);

  const showAll = progress >= 0.88;
  const singleLayer = [0, 1, 2, 3].find((i) => {
    const [s, e] = [0.08 + i * 0.2, 0.08 + (i + 1) * 0.2];
    return progress >= s && progress < 0.88;
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#080d08", alignItems: "center" }}>
      {/* 标题 */}
      <div style={{
        position: "absolute", top: safeTop - 58,
        width: "100%", textAlign: "center",
        fontSize: 48, fontWeight: "bold", color: "#6bcb77",
        fontFamily: "system-ui, sans-serif",
        opacity: phase(0, 0.08),
      }}>
        memsearch 架构
      </div>
      <div style={{
        position: "absolute", top: safeTop - 16,
        width: "100%", textAlign: "center",
        fontSize: 22, color: "#444",
        opacity: phase(0, 0.08),
      }}>
        记忆应该比任何一个 agent 都活得更长
      </div>

      {/* 单层大卡片 */}
      {singleLayer !== undefined && !showAll && (
        <div style={{
          position: "absolute",
          top: stackTop,
          left: 0, right: 0,
          display: "flex", justifyContent: "center",
          opacity: phase(0.08 + singleLayer * 0.2, 0.08 + singleLayer * 0.2 + 0.05),
        }}>
          <div style={{
            width: 700,
            backgroundColor: ARCH[singleLayer].color + "12",
            border: `2px solid ${ARCH[singleLayer].color}`,
            borderRadius: 16,
            padding: "16px 24px",
          }}>
            <div style={{ fontSize: 48, fontWeight: "bold", color: ARCH[singleLayer].color, textAlign: "center", marginBottom: 4 }}>
              {ARCH[singleLayer].label}
            </div>
            <div style={{ fontSize: 24, color: "#666", textAlign: "center", marginBottom: 16 }}>
              {ARCH[singleLayer].sub}
            </div>
            <div style={{ display: "flex", gap: 12 }}>
              {ARCH[singleLayer].items.map((item, j) => (
                <div key={j} style={{
                  flex: 1, backgroundColor: "#111", borderRadius: 10,
                  padding: "10px 12px", textAlign: "center",
                }}>
                  <div style={{ fontSize: 26, color: ARCH[singleLayer].color }}>▸ {item}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 全家桶 */}
      {showAll && (
        <div style={{
          position: "absolute", top: stackTop,
          left: 0, right: 0,
          display: "flex", flexDirection: "column", alignItems: "center",
          gap: GAP,
          opacity: phase(0.88, 1),
        }}>
          {ARCH.map((layer, i) => (
            <div key={i} style={{
              width: 700,
              display: "flex", alignItems: "stretch", gap: 12,
            }}>
              <div style={{
                width: LEFT_W, flexShrink: 0,
                backgroundColor: layer.color + "18",
                border: `2px solid ${layer.color}`,
                borderRadius: 10,
                padding: "0 12px",
                display: "flex", flexDirection: "column", justifyContent: "center",
              }}>
                <div style={{ fontSize: 24, fontWeight: "bold", color: layer.color }}>{layer.label}</div>
              </div>
              <div style={{
                flex: 1, backgroundColor: "#111", borderRadius: 10,
                padding: "0 14px",
                display: "flex", flexDirection: "column", justifyContent: "center", gap: 2,
              }}>
                {layer.items.map((item, j) => (
                  <div key={j} style={{ fontSize: 22, color: "#aaa", display: "flex", alignItems: "center", gap: 6 }}>
                    <span style={{ color: layer.color, fontSize: 16 }}>▸</span> {item}
                  </div>
                ))}
              </div>
            </div>
          ))}
          {/* 核心差异高亮 */}
          <div style={{
            width: 700,
            backgroundColor: "#6bcb7720",
            border: `2px solid #6bcb77`,
            borderRadius: 10,
            padding: "12px 20px",
            display: "flex", alignItems: "center", gap: 12,
          }}>
            <span style={{ fontSize: 28, color: "#6bcb77" }}>★</span>
            <span style={{ fontSize: 26, color: "#6bcb77", fontWeight: "bold" }}>
              四个 agent 共享同一套记忆，换工具不断，记忆一直在
            </span>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
