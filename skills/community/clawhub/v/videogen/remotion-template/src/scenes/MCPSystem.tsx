import React from "react";
import {
import { ArchitectureDiagram } from "../components/Diagrams";
import { FadeInText } from "../components/Typography";
import { scale } from "../theme";
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/**
 * MCP System Scene (3:45 - 4:20)
 * MCP Hub 连接示意图
 */
export const MCPSystem: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame();
  const lines = narration.split("\n").filter(Boolean);

  // 中心 Claude Code，右侧三个 MCP 适配器
  const nodes = [
    { label: "Claude\nCode", sublabel: "核心系统", x: 0.2, y: 0.5 },
    { label: "MCP Hub", sublabel: "协议接口", x: 0.5, y: 0.5 },
    { label: "Database", sublabel: "数据库", x: 0.8, y: 0.25 },
    { label: "GitHub", sublabel: "代码托管", x: 0.8, y: 0.5 },
    { label: "Custom", sublabel: "定制工具", x: 0.8, y: 0.75 },
  ];

  const connections: [number, number][] = [
    [0, 1],
    [1, 2],
    [1, 3],
    [1, 4],
  ];

  return (
    <AbsoluteFill
      style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}
    >
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        {/* 连接线 */}
        {connections.map(([from, to], i) => {
          const n1 = nodes[from];
          const n2 = nodes[to];
          const x1 = n1.x * 1080;
          const y1 = n1.y * 1080;
          const x2 = n2.x * 1080;
          const y2 = n2.y * 1080;
          const delay = 20 + i * 15;
          const progress = Math.min(1, Math.max(0, (frame - delay) / 25));
          return (
            <line
              key={i}
              x1={x1}
              y1={y1}
              x2={x1 + (x2 - x1) * progress}
              y2={y1 + (y2 - y1) * progress}
              stroke="#00d4ff"
              strokeWidth={3}
              opacity={0.7}
            />
          );
        })}

        {/* 节点 */}
        {nodes.map((node, i) => {
          const progress = Math.min(1, Math.max(0, (frame - i * 10) / 20));
          const x = node.x * 1080;
          const y = node.y * 1080;
          const isHub = i === 1;
          const isLeft = i === 0;
          const isRight = i > 1;

          return (
            <g key={i} opacity={progress}>
              <circle
                cx={x}
                cy={y}
                r={isHub ? 70 : isLeft ? 60 : 50}
                fill={isHub ? "#00d4ff20" : isLeft ? "#141922" : "#141922"}
                stroke={isHub ? "#00d4ff" : isLeft ? "#6bcb77" : "#ffd93d"}
                strokeWidth={isHub ? 3 : 2}
              />
              <text
                x={x}
                y={y - 5}
                textAnchor="middle"
                fill={isHub ? "#00d4ff" : isLeft ? "#6bcb77" : "#ffd93d"}
                fontSize={isHub ? 16 : 14}
                fontWeight="bold"
                fontFamily="system-ui, sans-serif"
              >
                {node.label.split("\n")[0]}
              </text>
              {node.label.includes("\n") && (
                <text
                  x={x}
                  y={y + 10}
                  textAnchor="middle"
                  fill={isHub ? "#00d4ff" : isLeft ? "#6bcb77" : "#ffd93d"}
                  fontSize={isHub ? 14 : 12}
                  fontFamily="system-ui, sans-serif"
                >
                  {node.label.split("\n")[1]}
                </text>
              )}
              <text
                x={x}
                y={y + 30}
                textAnchor="middle"
                fill="#555"
                fontSize={scale(12)}
                fontFamily="system-ui, sans-serif"
              >
                {node.sublabel}
              </text>
            </g>
          );
        })}

        {/* 协议标注 */}
        {frame > 80 && (
          <text
            x={540}
            y={920}
            textAnchor="middle"
            fill="#555"
            fontSize={scale(14)}
            fontFamily="system-ui, sans-serif"
          >
            MCP = Model Context Protocol · 开放标准接口
          </text>
        )}
      </svg>

      {/* 右侧说明文字 */}
      {frame > 90 && (
        <div
          style={{
            position: "absolute",
            right: 60,
            top: "50%",
            transform: "translateY(-50%)",
            color: "#888",
            fontSize={scale(16)},
            fontFamily: "system-ui, sans-serif",
            lineHeight: 2,
          }}
        >
          {lines.slice(0, 2).map((l, i) => (
            <div key={i} style={{ marginBottom: 8 }}>
              {l.trim()}
            </div>
          ))}
        </div>
      )}
    </AbsoluteFill>
  );
};
