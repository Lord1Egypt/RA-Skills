/**
 * AnimatedPieChart — renders an animated pie chart using SVG.
 * Segments animate in sequentially using stroke-dashoffset.
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";

export type PieDataItem = {
  label: string;
  value: number;
  color: string;
};

type AnimatedPieChartProps = {
  /** Data items */
  data: PieDataItem[];
  /** Chart size (width = height) */
  size?: number;
  /** Donut hole radius (0 for full pie) */
  innerRadius?: number;
  /** Stroke width for donut style */
  strokeWidth?: number;
  /** Animation duration in frames */
  animationDuration?: number;
  /** Delay in frames */
  delay?: number;
  /** Show labels */
  showLabels?: boolean;
  /** Label color */
  labelColor?: string;
  /** Label font size */
  labelFontSize?: number;
  /** Custom style */
  style?: React.CSSProperties;
};

export const AnimatedPieChart: React.FC<AnimatedPieChartProps> = ({
  data,
  size = 300,
  innerRadius = 0,
  strokeWidth = 40,
  animationDuration = 60,
  delay = 0,
  showLabels = true,
  labelColor = "#ffffff",
  labelFontSize = 14,
  style,
}) => {
  const frame = useCurrentFrame();

  const localFrame = Math.max(0, frame - delay);
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

  const total = data.reduce((sum, d) => sum + d.value, 0);
  if (total === 0) return null;

  const center = size / 2;
  const radius = innerRadius > 0
    ? (size / 2 - strokeWidth / 2)
    : (size / 2) * 0.8;
  const circumference = 2 * Math.PI * radius;

  // Calculate segment positions
  let cumulativeAngle = -90; // Start from 12 o'clock

  return (
    <div style={{ position: "relative", width: size, height: size, ...style }}>
      <svg width={size} height={size}>
        {data.map((item, i) => {
          const segmentAngle = (item.value / total) * 360;
          const segmentLength = (item.value / total) * circumference;

          // Animate this segment
          const segmentProgress = interpolate(
            progress,
            [i / data.length, Math.min(1, (i + 1) / data.length)],
            [0, 1],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          );

          const visibleLength = segmentLength * segmentProgress;
          const offset = segmentLength - visibleLength;

          const startAngle = cumulativeAngle;
          cumulativeAngle += segmentAngle;

          // Label position (midpoint of segment)
          const midAngle = startAngle + segmentAngle / 2;
          const labelRadius = radius * 1.3;
          const labelX =
            center + labelRadius * Math.cos((midAngle * Math.PI) / 180);
          const labelY =
            center + labelRadius * Math.sin((midAngle * Math.PI) / 180);

          return (
            <React.Fragment key={item.label}>
              <circle
                cx={center}
                cy={center}
                r={radius}
                fill="none"
                stroke={item.color}
                strokeWidth={innerRadius > 0 ? strokeWidth : radius}
                strokeDasharray={`${segmentLength} ${circumference}`}
                strokeDashoffset={offset}
                transform={`rotate(${startAngle} ${center} ${center})`}
                strokeLinecap="butt"
              />
              {showLabels && segmentProgress > 0.5 && (
                <text
                  x={labelX}
                  y={labelY}
                  fill={labelColor}
                  fontSize={labelFontSize}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fontWeight={600}
                >
                  {item.label}
                </text>
              )}
            </React.Fragment>
          );
        })}
      </svg>
    </div>
  );
};
