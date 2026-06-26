/**
 * CountUp — animates a number counting up from a start value to an end value.
 * Useful for statistics, metrics, and data highlights.
 */
import React from "react";
import {
  useCurrentFrame,
  interpolate,
  Easing,
} from "remotion";

type CountUpProps = {
  /** Starting value */
  from?: number;
  /** Target value */
  to: number;
  /** Animation duration in frames */
  animationDuration?: number;
  /** Delay in frames */
  delay?: number;
  /** Number of decimal places */
  decimals?: number;
  /** Prefix (e.g. "$", "¥") */
  prefix?: string;
  /** Suffix (e.g. "%", "ms") */
  suffix?: string;
  /** Font size */
  fontSize?: number;
  /** Font weight */
  fontWeight?: number;
  /** Color */
  color?: string;
  /** Font family */
  fontFamily?: string;
  /** Custom style */
  style?: React.CSSProperties;
};

export const CountUp: React.FC<CountUpProps> = ({
  from = 0,
  to,
  animationDuration = 60,
  delay = 0,
  decimals = 0,
  prefix = "",
  suffix = "",
  fontSize = 64,
  fontWeight = 700,
  color = "#ffffff",
  fontFamily = "sans-serif",
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
      easing: Easing.out(Easing.quad),
    }
  );

  const currentValue = from + (to - from) * progress;
  const displayValue = currentValue.toFixed(decimals);

  // Fade in
  const opacity = interpolate(localFrame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        fontSize,
        fontWeight,
        color,
        fontFamily,
        opacity,
        fontVariantNumeric: "tabular-nums",
        ...style,
      }}
    >
      {prefix}
      {displayValue}
      {suffix}
    </div>
  );
};
