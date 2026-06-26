/**
 * CoordinateSystem — renders an animated 2D coordinate system with axes, labels, and grid.
 * Useful as a backdrop for math/science visualizations.
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";

type CoordinateSystemProps = {
  /** SVG width */
  width?: number;
  /** SVG height */
  height?: number;
  /** X-axis label */
  xLabel?: string;
  /** Y-axis label */
  yLabel?: string;
  /** Show grid lines */
  showGrid?: boolean;
  /** Number of grid divisions per axis */
  gridDivisions?: number;
  /** Axis color */
  axisColor?: string;
  /** Grid color */
  gridColor?: string;
  /** Label color */
  labelColor?: string;
  /** Label font size */
  labelFontSize?: number;
  /** Padding inside SVG */
  padding?: number;
  /** Delay in frames */
  delay?: number;
  /** Spring damping */
  damping?: number;
  /** Children (rendered inside the coordinate space) */
  children?: React.ReactNode;
  /** Custom style */
  style?: React.CSSProperties;
};

export const CoordinateSystem: React.FC<CoordinateSystemProps> = ({
  width = 800,
  height = 400,
  xLabel = "x",
  yLabel = "y",
  showGrid = true,
  gridDivisions = 8,
  axisColor = "#ffffff",
  gridColor = "rgba(255, 255, 255, 0.1)",
  labelColor = "#888888",
  labelFontSize = 16,
  padding = 50,
  delay = 0,
  damping = 200,
  children,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    delay,
    config: { damping },
  });

  const plotW = width - padding * 2;
  const plotH = height - padding * 2;

  // Axis draw progress
  const xAxisLength = interpolate(entrance, [0, 1], [0, plotW]);
  const yAxisLength = interpolate(entrance, [0, 1], [0, plotH]);
  const labelOpacity = interpolate(entrance, [0.5, 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Origin point
  const ox = padding;
  const oy = padding + plotH;

  return (
    <svg width={width} height={height} style={style}>
      {/* Grid */}
      {showGrid &&
        Array.from({ length: gridDivisions + 1 }).map((_, i) => {
          const gridOpacity = interpolate(entrance, [0.3, 0.8], [0, 0.5], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          // Vertical grid lines
          const gx = padding + (i / gridDivisions) * plotW;
          // Horizontal grid lines
          const gy = padding + (i / gridDivisions) * plotH;

          return (
            <React.Fragment key={i}>
              <line
                x1={gx}
                y1={padding}
                x2={gx}
                y2={padding + plotH}
                stroke={gridColor}
                strokeWidth={1}
                opacity={gridOpacity}
              />
              <line
                x1={padding}
                y1={gy}
                x2={padding + plotW}
                y2={gy}
                stroke={gridColor}
                strokeWidth={1}
                opacity={gridOpacity}
              />
            </React.Fragment>
          );
        })}

      {/* X-axis */}
      <line
        x1={ox}
        y1={oy}
        x2={ox + xAxisLength}
        y2={oy}
        stroke={axisColor}
        strokeWidth={2}
      />
      {/* X-axis arrow */}
      {entrance > 0.9 && (
        <polygon
          points={`${ox + plotW},${oy} ${ox + plotW - 8},${oy - 5} ${ox + plotW - 8},${oy + 5}`}
          fill={axisColor}
          opacity={labelOpacity}
        />
      )}

      {/* Y-axis */}
      <line
        x1={ox}
        y1={oy}
        x2={ox}
        y2={oy - yAxisLength}
        stroke={axisColor}
        strokeWidth={2}
      />
      {/* Y-axis arrow */}
      {entrance > 0.9 && (
        <polygon
          points={`${ox},${padding} ${ox - 5},${padding + 8} ${ox + 5},${padding + 8}`}
          fill={axisColor}
          opacity={labelOpacity}
        />
      )}

      {/* Labels */}
      <text
        x={ox + plotW + 10}
        y={oy + 5}
        fill={labelColor}
        fontSize={labelFontSize}
        opacity={labelOpacity}
      >
        {xLabel}
      </text>
      <text
        x={ox - 10}
        y={padding - 10}
        fill={labelColor}
        fontSize={labelFontSize}
        textAnchor="middle"
        opacity={labelOpacity}
      >
        {yLabel}
      </text>

      {/* Children (custom content inside coordinate space) */}
      {children}
    </svg>
  );
};
