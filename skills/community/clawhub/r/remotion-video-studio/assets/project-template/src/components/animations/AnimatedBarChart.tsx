/**
 * AnimatedBarChart — renders an animated bar chart with staggered spring entrances.
 * All animations driven by useCurrentFrame().
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";

export type BarDataItem = {
  label: string;
  value: number;
  color?: string;
};

type AnimatedBarChartProps = {
  /** Data items to display */
  data: BarDataItem[];
  /** Chart title (optional) */
  title?: string;
  /** Chart height in pixels */
  chartHeight?: number;
  /** Chart width in pixels */
  chartWidth?: number;
  /** Default bar color */
  barColor?: string;
  /** Background color */
  backgroundColor?: string;
  /** Text color */
  textColor?: string;
  /** Muted text color (for labels) */
  mutedColor?: string;
  /** Axis line color */
  axisColor?: string;
  /** Stagger delay between bars in frames */
  staggerDelay?: number;
  /** Initial delay before first bar animates */
  delay?: number;
  /** Spring damping */
  damping?: number;
  /** Spring stiffness */
  stiffness?: number;
  /** Show value labels on top of bars */
  showValues?: boolean;
  /** Font family */
  fontFamily?: string;
  /** Custom style */
  style?: React.CSSProperties;
};

export const AnimatedBarChart: React.FC<AnimatedBarChartProps> = ({
  data,
  title,
  chartHeight = 400,
  chartWidth = 800,
  barColor = "#3b82f6",
  backgroundColor = "transparent",
  textColor = "#ffffff",
  mutedColor = "#888888",
  axisColor = "#333333",
  staggerDelay = 5,
  delay = 10,
  damping = 18,
  stiffness = 80,
  showValues = true,
  fontFamily = "sans-serif",
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const maxValue = Math.max(...data.map((d) => d.value), 1);
  const barGap = 16;

  return (
    <div
      style={{
        backgroundColor,
        fontFamily,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        ...style,
      }}
    >
      {/* Title */}
      {title && (
        <div
          style={{
            color: textColor,
            fontSize: 32,
            fontWeight: 600,
            marginBottom: 24,
            textAlign: "center",
          }}
        >
          {title}
        </div>
      )}

      {/* Chart area */}
      <div style={{ display: "flex", alignItems: "flex-end" }}>
        {/* Bars container */}
        <div
          style={{
            display: "flex",
            alignItems: "flex-end",
            gap: barGap,
            height: chartHeight,
            width: chartWidth,
            borderLeft: `2px solid ${axisColor}`,
            borderBottom: `2px solid ${axisColor}`,
            paddingLeft: 16,
            paddingBottom: 4,
          }}
        >
          {data.map((item, i) => {
            const progress = spring({
              frame: frame - delay - i * staggerDelay,
              fps,
              config: { damping, stiffness },
            });

            const barHeight =
              (item.value / maxValue) * chartHeight * Math.max(0, progress);
            const barOpacity = interpolate(
              progress,
              [0, 0.3],
              [0, 1],
              { extrapolateRight: "clamp" }
            );

            return (
              <div
                key={item.label}
                style={{
                  flex: 1,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "flex-end",
                  height: "100%",
                }}
              >
                {/* Value label */}
                {showValues && (
                  <div
                    style={{
                      color: textColor,
                      fontSize: 16,
                      fontWeight: 600,
                      marginBottom: 4,
                      opacity: barOpacity,
                    }}
                  >
                    {item.value}
                  </div>
                )}

                {/* Bar */}
                <div
                  style={{
                    width: "100%",
                    height: barHeight,
                    backgroundColor: item.color || barColor,
                    borderRadius: "6px 6px 0 0",
                    opacity: barOpacity,
                  }}
                />
              </div>
            );
          })}
        </div>
      </div>

      {/* X-axis labels */}
      <div
        style={{
          display: "flex",
          gap: barGap,
          paddingLeft: 18,
          marginTop: 12,
          width: chartWidth,
        }}
      >
        {data.map((item) => (
          <div
            key={item.label}
            style={{
              flex: 1,
              textAlign: "center",
              color: mutedColor,
              fontSize: 16,
            }}
          >
            {item.label}
          </div>
        ))}
      </div>
    </div>
  );
};
