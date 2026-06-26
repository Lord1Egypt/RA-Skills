import React from "react";
import {
import { ArchitectureDiagram } from "../components/Diagrams";
import { FadeInText } from "../components/Typography";
import { scale } from "../theme";
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  springTiming,
} from "remotion";

/**
 * Harness Intro Scene (0:20 - 0:50)
 * 四线汇聚架构图，展示 Agent Harness System 四个模块
 */
export const HarnessIntro: React.FC<{ narration: string }> = ({
  narration,
}) => {
  const frame = useCurrentFrame();
  const lines = narration.split("\n").filter(Boolean);

  // 四个模块节点
  const nodes = [
    { label: "AI Model", sublabel: "大脑", x: 0.5, y: 0.05 },
    { label: "Tools", sublabel: "工具层", x: 0.92, y: 0.5 },
    { label: "Session", sublabel: "状态管理", x: 0.5, y: 0.92 },
    { label: "Permissions", sublabel: "权限控制", x: 0.08, y: 0.5 },
  ];

  const connections: [number, number][] = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [0, 2],
    [1, 3],
  ];

  return (
    <AbsoluteFill
      style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}
    >
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        {/* 汇聚线动画 */}
        {frame < 60 &&
          [0, 1, 2, 3].map((i) => {
            const targets = [
              { x: 540, y: 540 },
              { x: 540, y: 540 },
              { x: 540, y: 540 },
              { x: 540, y: 540 },
            ];
            const sources = [
              { x: 540, y: 54 },
              { x: 995, y: 540 },
              { x: 540, y: 995 },
              { x: 85, y: 540 },
            ];
            const progress = Math.min(1, Math.max(0, (frame - i * 8) / 30));
            const sx = sources[i].x;
            const sy = sources[i].y;
            const tx = targets[i].x;
            const ty = targets[i].y;
            return (
              <line
                key={i}
                x1={sx}
                y1={sy}
                x2={sx + (tx - sx) * progress}
                y2={sy + (ty - sy) * progress}
                stroke="#00d4ff"
                strokeWidth={3}
                opacity={0.8}
              />
            );
          })}

        {/* 中心汇聚点 */}
        {frame > 40 && (
          <circle
            cx={540}
            cy={540}
            r={Math.min(60, (frame - 40) * 3)}
            fill="#00d4ff"
            opacity={0.3}
          />
        )}
        {frame > 50 && (
          <text
            x={540}
            y={545}
            textAnchor="middle"
            fill="#00d4ff"
            fontSize={scale(24)}
            fontWeight="bold"
            fontFamily="system-ui, sans-serif"
          >
            Agent Harness
          </text>
        )}

        {/* 四个模块 */}
        {[0, 1, 2, 3].map((i) => {
          const pos = [
            { x: 540, y: 54 },
            { x: 995, y: 540 },
            { x: 540, y: 995 },
            { x: 85, y: 540 },
          ];
          const p = Math.min(1, Math.max(0, (frame - 30 - i * 10) / 20));
          return (
            <g key={i} opacity={p}>
              <circle
                cx={pos[i].x}
                cy={pos[i].y}
                r={45}
                fill="#141922"
                stroke="#00d4ff"
                strokeWidth={2}
              />
              <text
                x={pos[i].x}
                y={pos[i].y - 5}
                textAnchor="middle"
                fill="#00d4ff"
                fontSize={scale(14)}
                fontWeight="bold"
                fontFamily="system-ui, sans-serif"
              >
                {nodes[i].label}
              </text>
              <text
                x={pos[i].x}
                y={pos[i].y + 14}
                textAnchor="middle"
                fill="#666"
                fontSize={scale(12)}
                fontFamily="system-ui, sans-serif"
              >
                {nodes[i].sublabel}
              </text>
            </g>
          );
        })}
      </svg>

      {/* 底部文字 */}
      {frame > 60 && (
        <div
          style={{
            position: "absolute",
            bottom: 80,
            left: "50%",
            transform: "translateX(-50%)",
            color: "#888",
            fontSize={scale(20)},
            fontFamily: "system-ui, sans-serif",
            textAlign: "center",
          }}
        >
          {lines[0] || "不是聊天机器人，是一套 Agent Harness System"}
        </div>
      )}
    </AbsoluteFill>
  );
};
