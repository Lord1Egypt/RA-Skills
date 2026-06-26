import React, { useMemo } from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/**
 * RingDiagram - 环形流程图组件
 * 用于 Agent Loop 等环形流程展示
 */
interface RingDiagramProps {
  nodes: string[];
  centerText?: string;
  color?: string;
  activeIndex?: number;
  showArrows?: boolean;
}

export const RingDiagram: React.FC<RingDiagramProps> = ({
  nodes,
  centerText = "Agent Loop",
  color = "#00d4ff",
  activeIndex,
  showArrows = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const totalNodes = nodes.length;
  const centerX = 540; // 1080/2
  const centerY = 540; // 1920/2
  const radius = 280;

  const nodePositions = useMemo(() => {
    return nodes.map((_, i) => {
      const angle = (i / totalNodes) * Math.PI * 2 - Math.PI / 2;
      return {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        angle,
      };
    });
  }, [nodes, totalNodes]);

  // 入场动画：从中心淡入
  const entryProgress = Math.min(1, frame / 30);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0e17",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* SVG 画布 */}
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        {/* 外圈 */}
        <circle
          cx={centerX}
          cy={centerY}
          r={radius + 60}
          fill="none"
          stroke="#1a2035"
          strokeWidth={2}
          strokeDasharray="8 4"
          opacity={0.5 * entryProgress}
        />

        {/* 环形路径（虚线） */}
        <circle
          cx={centerX}
          cy={centerY}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={2}
          strokeDasharray="12 6"
          opacity={0.4 * entryProgress}
        />

        {/* 箭头线 */}
        {showArrows &&
          nodePositions.map((pos, i) => {
            const nextPos = nodePositions[(i + 1) % totalNodes];
            const midX = (pos.x + nextPos.x) / 2;
            const midY = (pos.y + nextPos.y) / 2;
            return (
              <line
                key={`arrow-${i}`}
                x1={pos.x}
                y1={pos.y}
                x2={midX}
                y2={midY}
                stroke={color}
                strokeWidth={2}
                opacity={0.6 * entryProgress}
              />
            );
          })}

        {/* 节点 */}
        {nodePositions.map((pos, i) => {
          const nodeProgress = Math.min(
            1,
            Math.max(0, (frame - i * 8) / 15)
          );

          return (
            <g key={`node-${i}`} opacity={nodeProgress * entryProgress}>
              {/* 节点圆 */}
              <circle
                cx={pos.x}
                cy={pos.y}
                r={activeIndex === i ? 120 : 100}
                fill={activeIndex === i ? color : "#141922"}
                stroke={color}
                strokeWidth={activeIndex === i ? 3 : 2}
              />
              {/* 节点文字 */}
              <text
                x={pos.x}
                y={pos.y + 5}
                textAnchor="middle"
                fill={activeIndex === i ? "#000" : color}
                fontSize={36}
                fontWeight="bold"
                fontFamily="system-ui, sans-serif"
              >
                {nodes[i]}
              </text>
            </g>
          );
        })}

        {/* 中心文字 */}
        <text
          x={centerX}
          y={centerY}
          textAnchor="middle"
          fill={color}
          fontSize={22}
          fontWeight="bold"
          fontFamily="system-ui, sans-serif"
          opacity={entryProgress}
        >
          {centerText}
        </text>
      </svg>
    </AbsoluteFill>
  );
};

/**
 * FlowChart - 横向流程图
 * 用于工具调用流程等
 */
interface FlowChartProps {
  nodes: { label: string; sublabel?: string }[];
  activeIndex?: number;
  direction?: "row" | "column";
  color?: string;
}

export const FlowChart: React.FC<FlowChartProps> = ({
  nodes,
  activeIndex,
  direction = "row",
  color = "#00d4ff",
}) => {
  const frame = useCurrentFrame();
  const isRow = direction === "row";
  const totalNodes = nodes.length;
  const nodeSize = isRow ? 140 : 80;
  const gap = isRow ? 80 : 60;
  const totalLength = totalNodes * nodeSize + (totalNodes - 1) * gap;
  const startPos = isRow
    ? (1080 - totalLength) / 2
    : (1920 - totalLength) / 2;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0e17",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <svg width={1080} height={isRow ? 400 : 1920} viewBox={`0 0 ${1080} ${isRow ? 400 : 1920}`}>
        {nodes.map((node, i) => {
          const nodeProgress = Math.min(1, Math.max(0, (frame - i * 10) / 20));
          const x = isRow ? startPos + i * (nodeSize + gap) : 540;
          const y = isRow ? 200 : startPos + i * (nodeSize + gap);
          const isActive = activeIndex === i;

          return (
            <g key={i} opacity={nodeProgress}>
              {/* 连接箭头 */}
              {i < totalNodes - 1 && (
                <line
                  x1={isRow ? x + nodeSize : x}
                  y1={isRow ? y : y + nodeSize}
                  x2={isRow ? x + nodeSize + gap : x}
                  y2={isRow ? y : y + nodeSize + gap}
                  stroke={color}
                  strokeWidth={2}
                  markerEnd="url(#arrowhead)"
                  opacity={0.6}
                />
              )}

              {/* 节点框 */}
              <rect
                x={x - nodeSize / 2}
                y={y - 30}
                width={nodeSize}
                height={60}
                rx={8}
                fill={isActive ? color : "#141922"}
                stroke={color}
                strokeWidth={2}
              />

              {/* 节点文字 */}
              <text
                x={x}
                y={y + 5}
                textAnchor="middle"
                fill={isActive ? "#000" : color}
                fontSize={36}
                fontWeight="bold"
                fontFamily="system-ui, sans-serif"
              >
                {node.label}
              </text>
              {node.sublabel && (
                <text
                  x={x}
                  y={y + 22}
                  textAnchor="middle"
                  fill={isActive ? "#333" : "#888"}
                  fontSize={12}
                  fontFamily="system-ui, sans-serif"
                >
                  {node.sublabel}
                </text>
              )}
            </g>
          );
        })}

        {/* 箭头标记 */}
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill={color} />
          </marker>
        </defs>
      </svg>
    </AbsoluteFill>
  );
};
