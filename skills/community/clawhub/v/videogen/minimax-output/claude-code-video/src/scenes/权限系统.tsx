import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { fs, useFontScale } from "../theme";

export const 权限系统: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame()
  const scale = useFontScale();;
  const modes = [
    { label: "Read-only", desc: "只读 · 禁止任何写入", color: "#ff6b6b", active: frame > 20 },
    { label: "Workspace-write", desc: "工作区写入 · 禁止高危命令", color: "#ffd93d", active: frame > 60 },
    { label: "Danger-full-access", desc: "完全信任 · 可执行任意操作", color: "#27C93F", active: frame > 100 },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}>
      <svg width={1080} height={800} viewBox="0 0 1080 800">
        <text x={540} y={60} textAnchor="middle" fill="#888" fontSize={Math.round(72 * scale)} fontFamily="system-ui, sans-serif">Permission Mode · 权限模式</text>
        {modes.map((mode, i) => {
          const delay = i * 40;
          const progress = Math.min(1, Math.max(0, (frame - delay) / 20));
          const y = 160 + i * 160;
          return (
            <g key={i} opacity={progress}>
              <rect x={250} y={y} width={580} height={100} rx={12} fill="#141922" stroke={mode.active ? mode.color : "#333"} strokeWidth={2} />
              <text x={280} y={y + 40} fill={mode.active ? mode.color : "#666"} fontSize={Math.round(48 * scale)} fontWeight="bold" fontFamily="system-ui, sans-serif">{mode.label}</text>
              <text x={280} y={y + 68} fill="#555" fontSize={Math.round(28 * scale)} fontFamily="system-ui, sans-serif">{mode.desc}</text>
              <rect x={720} y={y + 25} width={80} height={50} rx={25} fill={mode.active ? mode.color : "#333"} opacity={mode.active ? 1 : 0.5} />
              <circle cx={mode.active ? 775 : 745} cy={y + 50} r={20} fill="#fff" />
            </g>
          );
        })}
        {frame > 140 && (
          <g opacity={Math.min(1, (frame - 140) / 20)}>
            <rect x={250} y={620} width={580} height={80} rx={8} fill="#1a1a2e" stroke="#00d4ff" strokeWidth={1} strokeDasharray="4 2" />
            <text x={540} y={655} textAnchor="middle" fill="#00d4ff" fontSize={Math.round(72 * scale)} fontFamily="system-ui, sans-serif">PreToolUse Hook · 工具执行前置拦截点</text>
            <text x={540} y={680} textAnchor="middle" fill="#555" fontSize={Math.round(26 * scale)} fontFamily="system-ui, sans-serif">检查参数 · 拒绝执行 · 附加逻辑</text>
          </g>
        )}
      </svg>
    </AbsoluteFill>
  );
};
