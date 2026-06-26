import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  springTiming,
} from "remotion";

/**
 * LayerDiagram - 三层结构图
 * 用于上下文管理、会话层次等
 */
interface LayerDiagramProps {
  layers: { label: string; sublabel?: string; color?: string }[];
  direction?: "top-down" | "bottom-up";
}

export const LayerDiagram: React.FC<LayerDiagramProps> = ({
  layers,
  direction = "top-down",
}) => {
  const frame = useCurrentFrame();

  const colors = ["#ff6b6b", "#ffd93d", "#6bcb77"];
  const heights = [180, 140, 100];
  const width = 700;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0e17",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <svg width={1080} height={600} viewBox="0 0 1080 600">
        {/* 中央标签 */}
        <text
          x={540}
          y={30}
          textAnchor="middle"
          fill="#888"
          fontSize={32}
          fontFamily="system-ui, sans-serif"
        >
          上下文层次
        </text>

        {layers.map((layer, i) => {
          const delay = i * 12;
          const progress = Math.min(1, Math.max(0, (frame - delay) / 25));
          const y = direction === "top-down" ? 60 + i * 170 : 460 - i * 170;
          const h = heights[i] * progress;
          const color = layer.color || colors[i % colors.length];
          const x = (1080 - width) / 2;

          return (
            <g key={i} opacity={progress}>
              {/* 层叠矩形 */}
              <rect
                x={x}
                y={y}
                width={width}
                height={h}
                rx={12}
                fill={color}
                opacity={0.15}
                stroke={color}
                strokeWidth={2}
              />
              {/* 左侧标签 */}
              <rect x={x} y={y} width={6} height={h} fill={color} rx={3} />
              {/* 层级名称 */}
              <text
                x={x + 20}
                y={y + h / 2 - 8}
                fill={color}
                fontSize={40}
                fontWeight="bold"
                fontFamily="system-ui, sans-serif"
              >
                {layer.label}
              </text>
              {/* 子标签 */}
              {layer.sublabel && (
                <text
                  x={x + 20}
                  y={y + h / 2 + 16}
                  fill="#aaa"
                  fontSize={28}
                  fontFamily="system-ui, sans-serif"
                >
                  {layer.sublabel}
                </text>
              )}
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

/**
 * ArchitectureDiagram - 通用架构图
 * 多个节点 + 连接线
 */
interface ArchNode {
  label: string;
  sublabel?: string;
  x: number; // 0-1 relative
  y: number; // 0-1 relative
}

interface ArchitectureDiagramProps {
  nodes: ArchNode[];
  title?: string;
  color?: string;
  connections?: [number, number][]; // [from_idx, to_idx]
}

export const ArchitectureDiagram: React.FC<ArchitectureDiagramProps> = ({
  nodes,
  title,
  color = "#00d4ff",
  connections = [],
}) => {
  const frame = useCurrentFrame();
  const W = 1080;
  const H = 1080;
  const cx = W / 2;
  const cy = H / 2;

  return (
    <AbsoluteFill
      style={{ backgroundColor: "#0a0e17", justifyContent: "center", alignItems: "center" }}
    >
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        {title && (
          <text
            x={cx}
            y={40}
            textAnchor="middle"
            fill="#888"
            fontSize={32}
            fontFamily="system-ui, sans-serif"
          >
            {title}
          </text>
        )}

        {/* 连接线 */}
        {connections.map(([from, to], i) => {
          const n1 = nodes[from];
          const n2 = nodes[to];
          const x1 = n1.x * W;
          const y1 = n1.y * H;
          const x2 = n2.x * W;
          const y2 = n2.y * H;
          const progress = Math.min(1, (frame - i * 5) / 20);
          return (
            <line
              key={i}
              x1={x1}
              y1={y1}
              x2={x1 + (x2 - x1) * progress}
              y2={y1 + (y2 - y1) * progress}
              stroke={color}
              strokeWidth={2}
              strokeDasharray="8 4"
              opacity={0.6}
            />
          );
        })}

        {/* 节点 */}
        {nodes.map((node, i) => {
          const progress = Math.min(1, Math.max(0, (frame - i * 8) / 20));
          const x = node.x * W;
          const y = node.y * H;
          return (
            <g key={i} opacity={progress}>
              <circle
                cx={x}
                cy={y}
                r={80}
                fill="#141922"
                stroke={color}
                strokeWidth={2}
              />
              <text
                x={x}
                y={y + 4}
                textAnchor="middle"
                fill={color}
                fontSize={26}
                fontWeight="bold"
                fontFamily="system-ui, sans-serif"
              >
                {node.label}
              </text>
              {node.sublabel && (
                <text
                  x={x}
                  y={y + 20}
                  textAnchor="middle"
                  fill="#666"
                  fontSize={11}
                  fontFamily="system-ui, sans-serif"
                >
                  {node.sublabel}
                </text>
              )}
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
