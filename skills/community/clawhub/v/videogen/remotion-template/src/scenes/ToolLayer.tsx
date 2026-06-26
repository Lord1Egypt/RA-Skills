import React from "react";
import {
import { FlowChart } from "../components/FlowChart";
import { FadeInText, BulletList } from "../components/Typography";
import { scale } from "../theme";
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/**
 * Tool Layer Scene (0:50 - 1:35)
 * 三大工具类 + 调用流程
 */
export const ToolLayer: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame();
  const lines = narration.split("\n").filter(Boolean);

  const tools = [
    { label: "FileEdit", sublabel: "读写 · 编辑 · 搜索" },
    { label: "BashTool", sublabel: "终端 · 测试 · 构建" },
    { label: "AgentTool", sublabel: "子Agent · 任务分解" },
  ];

  return (
    <AbsoluteFill
      style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}
    >
      <svg width={1080} height={800} viewBox="0 0 1080 800">
        {/* 标题 */}
        <text
          x={540}
          y={50}
          textAnchor="middle"
          fill="#888"
          fontSize={scale(15)}
          fontFamily="system-ui, sans-serif"
        >
          工具层 · Tool Layer
        </text>

        {/* 三个工具图标 */}
        {tools.map((tool, i) => {
          const delay = i * 20;
          const progress = Math.min(1, Math.max(0, (frame - delay) / 20));
          const x = 180 + i * 360;
          const y = 200;

          return (
            <g key={i} opacity={progress}>
              {/* 工具图标圆形 */}
              <circle
                cx={x}
                cy={y}
                r={70}
                fill="#141922"
                stroke="#00d4ff"
                strokeWidth={2}
              />
              {/* 工具名称 */}
              <text
                x={x}
                y={y - 10}
                textAnchor="middle"
                fill="#00d4ff"
                fontSize={scale(18)}
                fontWeight="bold"
                fontFamily="ui-monospace, monospace"
              >
                {tool.label}
              </text>
              <text
                x={x}
                y={y + 14}
                textAnchor="middle"
                fill="#666"
                fontSize={scale(13)}
                fontFamily="system-ui, sans-serif"
              >
                {tool.sublabel}
              </text>
            </g>
          );
        })}

        {/* 调用箭头线 */}
        {frame > 80 && (
          <g opacity={Math.min(1, (frame - 80) / 20)}>
            <line
              x1={180}
              y1={320}
              x2={900}
              y2={320}
              stroke="#00d4ff"
              strokeWidth={2}
              strokeDasharray="8 4"
              opacity={0.5}
            />
            <text
              x={540}
              y={350}
              textAnchor="middle"
              fill="#444"
              fontSize={scale(14)}
              fontFamily="system-ui, sans-serif"
            >
              Harness 管理工具调用流程
            </text>
          </g>
        )}

        {/* Harness 层 */}
        {frame > 100 && (
          <g opacity={Math.min(1, (frame - 100) / 20)}>
            <rect
              x={100}
              y={400}
              width={880}
              height={200}
              rx={12}
              fill="#00d4ff10"
              stroke="#00d4ff"
              strokeWidth={2}
              strokeDasharray="6 3"
            />
            <text
              x={540}
              y={440}
              textAnchor="middle"
              fill="#00d4ff"
              fontSize={scale(20)}
              fontWeight="bold"
              fontFamily="system-ui, sans-serif"
            >
              Harness · 接收请求 · 校验权限 · 执行 · 返回结果
            </text>

            {/* 步骤 */}
            {[
              "接收 AI 工具调用请求",
              "权限校验（Read-only / Workspace-write / Danger-full）",
              "执行命令，返回结果",
            ].map((step, i) => (
              <text
                key={i}
                x={540}
                y={480 + i * 40}
                textAnchor="middle"
                fill="#666"
                fontSize={scale(15)}
                fontFamily="system-ui, sans-serif"
              >
                {step}
              </text>
            ))}
          </g>
        )}
      </svg>

      {/* 底部说明 */}
      {frame > 130 &&
        lines.slice(0, 2).map((l, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              bottom: 60 + i * 30,
              left: "50%",
              transform: "translateX(-50%)",
              color: "#555",
              fontSize={scale(14)},
              fontFamily: "system-ui, sans-serif",
              textAlign: "center",
            }}
          >
            {l.trim()}
          </div>
        ))}
    </AbsoluteFill>
  );
};
