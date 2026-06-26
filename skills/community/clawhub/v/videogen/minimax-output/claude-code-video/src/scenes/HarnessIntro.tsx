import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { fs, useFontScale } from "../theme";

export const HarnessIntro: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame()
  const scale = useFontScale();;
  const nodes = [
    { label: "AI Model", sublabel: "大脑", x: 0.5, y: 0.05 },
    { label: "Tools", sublabel: "工具层", x: 0.92, y: 0.5 },
    { label: "Session", sublabel: "状态管理", x: 0.5, y: 0.92 },
    { label: "Permissions", sublabel: "权限控制", x: 0.08, y: 0.5 },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}>
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        {[0,1,2,3].map((i) => {
          const sources = [
            { x: 540, y: 54 },
            { x: 995, y: 540 },
            { x: 540, y: 995 },
            { x: 85, y: 540 },
          ];
          const progress = Math.min(1, Math.max(0, (frame - i * 8) / 30));
          return (
            <line
              key={i}
              x1={sources[i].x} y1={sources[i].y}
              x2={540 + (540 - sources[i].x) * progress}
              y2={540 + (540 - sources[i].y) * progress}
              stroke="#00d4ff"
              strokeWidth={3}
              opacity={0.8}
            />
          );
        })}
        {[0,1,2,3].map((i) => {
          const pos = [
            { x: 540, y: 54 },
            { x: 995, y: 540 },
            { x: 540, y: 995 },
            { x: 85, y: 540 },
          ];
          const p = Math.min(1, Math.max(0, (frame - 30 - i * 10) / 20));
          return (
            <g key={i} opacity={p}>
              <circle cx={pos[i].x} cy={pos[i].y} r={90} fill="#141922" stroke="#00d4ff" strokeWidth={2} />
              <text x={pos[i].x} y={pos[i].y - 5} textAnchor="middle" fill="#00d4ff" fontSize={Math.round(72 * scale)} fontWeight="bold" fontFamily="system-ui, sans-serif">{nodes[i].label}</text>
              <text x={pos[i].x} y={pos[i].y + 14} textAnchor="middle" fill="#666" fontSize={Math.round(22 * scale)} fontFamily="system-ui, sans-serif">{nodes[i].sublabel}</text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
