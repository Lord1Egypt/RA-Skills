import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { fs, useFontScale } from "../theme";

export const MCP协议: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame()
  const scale = useFontScale();;
  const nodes = [
    { label: "Claude Code", sublabel: "核心系统", x: 0.2, y: 0.5, color: "#6bcb77" },
    { label: "MCP Hub", sublabel: "协议接口", x: 0.5, y: 0.5, color: "#00d4ff" },
    { label: "Database", sublabel: "数据库", x: 0.8, y: 0.25, color: "#ffd93d" },
    { label: "GitHub", sublabel: "代码托管", x: 0.8, y: 0.5, color: "#ffd93d" },
    { label: "Custom", sublabel: "定制工具", x: 0.8, y: 0.75, color: "#ffd93d" },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}>
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        {nodes.map((node, i) => {
          const progress = Math.min(1, Math.max(0, (frame - i * 10) / 20));
          const x = node.x * 1080;
          const y = node.y * 1080;
          const isHub = i === 1;
          return (
            <g key={i} opacity={progress}>
              <circle cx={x} cy={y} r={isHub ? 70 : 50} fill={isHub ? "#00d4ff20" : "#141922"} stroke={node.color} strokeWidth={isHub ? 3 : 2} />
              <text x={x} y={y} textAnchor="middle" dominantBaseline="middle" fill={node.color} fontSize={isHub ? 16 : 14} fontWeight="bold" fontFamily="system-ui, sans-serif">{node.label}</text>
              <text x={x} y={y + 25} textAnchor="middle" fill="#555" fontSize={Math.round(24 * scale)} fontFamily="system-ui, sans-serif">{node.sublabel}</text>
            </g>
          );
        })}
        <line x1={216} y1={540} x2={540} y2={540} stroke="#00d4ff" strokeWidth={3} opacity={0.7} />
        <line x1={540} y1={540} x2={864} y2={270} stroke="#00d4ff" strokeWidth={2} opacity={0.6} strokeDasharray="6 3" />
        <line x1={540} y1={540} x2={864} y2={540} stroke="#00d4ff" strokeWidth={2} opacity={0.6} strokeDasharray="6 3" />
        <line x1={540} y1={540} x2={864} y2={810} stroke="#00d4ff" strokeWidth={2} opacity={0.6} strokeDasharray="6 3" />
      </svg>
      <div style={{ position: "absolute", bottom: 60, left: "50%", transform: "translateX(-50%)", color: "#555", fontSize: Math.round(14 * scale), fontFamily: "system-ui, sans-serif" }}>
        MCP = Model Context Protocol · 开放标准接口
      </div>
    </AbsoluteFill>
  );
};
