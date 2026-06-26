/**
 * AnimatedLineChart — draws an animated line chart using SVG.
 * The line progressively reveals from left to right.
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";

export type LineDataPoint = {
  x: number;
  y: number;
};

type AnimatedLineChartProps = {
  /** Data points (x, y) */
  data: LineDataPoint[];
  /** Chart width */
  width?: number;
  /** Chart height */
  height?: number;
  /** Line stroke color */
  strokeColor?: string;
  /** Line stroke width */
  strokeWidth?: number;
  /** Show data points as dots */
  showDots?: boolean;
  /** Dot radius */
  dotRadius?: number;
  /** Dot color */
  dotColor?: string;
  /** Fill area under the line */
  fillArea?: boolean;
  /** Fill color (with alpha) */
  fillColor?: string;
  /** Axis color */
  axisColor?: string;
  /** Animation duration in frames */
  animationDuration?: number;
  /** Delay in frames */
  delay?: number;
  /** Padding inside the SVG */
  padding?: number;
  /** Custom style */
  style?: React.CSSProperties;
};

export const AnimatedLineChart: React.FC<AnimatedLineChartProps> = ({
  data,
  width = 800,
  height = 400,
  strokeColor = "#3b82f6",
  strokeWidth = 3,
  showDots = true,
  dotRadius = 5,
  dotColor = "#ffffff",
  fillArea = false,
  fillColor = "rgba(59, 130, 246, 0.2)",
  axisColor = "#333333",
  animationDuration = 60,
  delay = 0,
  padding = 40,
  style,
}) => {
  const frame = useCurrentFrame();

  const localFrame = Math.max(0, frame - delay);

  // Progress from 0 to 1 over animationDuration frames
  const progress = interpolate(
    localFrame,
    [0, animationDuration],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.inOut(Easing.quad),
    }
  );

  if (data.length < 2) return null;

  // Normalize data to SVG coordinates
  const xMin = Math.min(...data.map((d) => d.x));
  const xMax = Math.max(...data.map((d) => d.x));
  const yMin = Math.min(...data.map((d) => d.y));
  const yMax = Math.max(...data.map((d) => d.y));

  const xRange = xMax - xMin || 1;
  const yRange = yMax - yMin || 1;

  const plotW = width - padding * 2;
  const plotH = height - padding * 2;

  const toSvgX = (x: number) => padding + ((x - xMin) / xRange) * plotW;
  const toSvgY = (y: number) => padding + plotH - ((y - yMin) / yRange) * plotH;

  // Build the path
  const points = data.map((d) => ({ sx: toSvgX(d.x), sy: toSvgY(d.y) }));
  const pathD = points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${p.sx} ${p.sy}`)
    .join(" ");

  // Calculate total path length for dash animation
  let totalLength = 0;
  for (let i = 1; i < points.length; i++) {
    const dx = points[i].sx - points[i - 1].sx;
    const dy = points[i].sy - points[i - 1].sy;
    totalLength += Math.sqrt(dx * dx + dy * dy);
  }

  const visibleLength = totalLength * progress;

  // Area fill path
  const areaD = fillArea
    ? `${pathD} L ${points[points.length - 1].sx} ${padding + plotH} L ${points[0].sx} ${padding + plotH} Z`
    : "";

  return (
    <svg width={width} height={height} style={style}>
      {/* Axes */}
      <line
        x1={padding}
        y1={padding}
        x2={padding}
        y2={padding + plotH}
        stroke={axisColor}
        strokeWidth={2}
      />
      <line
        x1={padding}
        y1={padding + plotH}
        x2={padding + plotW}
        y2={padding + plotH}
        stroke={axisColor}
        strokeWidth={2}
      />

      {/* Area fill */}
      {fillArea && (
        <path
          d={areaD}
          fill={fillColor}
          opacity={progress}
        />
      )}

      {/* Line */}
      <path
        d={pathD}
        fill="none"
        stroke={strokeColor}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray={totalLength}
        strokeDashoffset={totalLength - visibleLength}
      />

      {/* Dots */}
      {showDots &&
        points.map((p, i) => {
          // Show dot only when the line has reached it
          const dotProgress =
            i === 0
              ? progress > 0 ? 1 : 0
              : progress >= (i / (points.length - 1)) ? 1 : 0;

          return (
            <circle
              key={i}
              cx={p.sx}
              cy={p.sy}
              r={dotRadius * dotProgress}
              fill={dotColor}
              stroke={strokeColor}
              strokeWidth={2}
            />
          );
        })}
    </svg>
  );
};
