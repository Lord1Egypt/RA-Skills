/**
 * AnimatedPath — progressively draws an arbitrary SVG path.
 * Useful for custom shapes, arrows, diagrams, etc.
 */
import React from "react";
import {
  useCurrentFrame,
  interpolate,
  Easing,
} from "remotion";

type AnimatedPathProps = {
  /** SVG path data string (d attribute) */
  d: string;
  /** SVG viewBox width */
  width?: number;
  /** SVG viewBox height */
  height?: number;
  /** Stroke color */
  color?: string;
  /** Stroke width */
  strokeWidth?: number;
  /** Fill color (default none) */
  fill?: string;
  /** Fill opacity (animates in after path is drawn) */
  fillOpacity?: number;
  /** Estimated path length (for dash animation) */
  pathLength?: number;
  /** Animation duration in frames */
  animationDuration?: number;
  /** Delay in frames */
  delay?: number;
  /** Custom style on the SVG */
  style?: React.CSSProperties;
};

export const AnimatedPath: React.FC<AnimatedPathProps> = ({
  d,
  width = 800,
  height = 400,
  color = "#3b82f6",
  strokeWidth = 3,
  fill = "none",
  fillOpacity = 0,
  pathLength = 1000,
  animationDuration = 60,
  delay = 0,
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

  const dashOffset = pathLength * (1 - progress);

  // Fill fades in after path is mostly drawn
  const currentFillOpacity =
    fillOpacity > 0
      ? interpolate(progress, [0.8, 1], [0, fillOpacity], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      : 0;

  return (
    <svg width={width} height={height} style={style}>
      {/* Fill layer */}
      {fillOpacity > 0 && (
        <path
          d={d}
          fill={fill}
          opacity={currentFillOpacity}
          stroke="none"
        />
      )}
      {/* Stroke layer */}
      <path
        d={d}
        fill="none"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray={pathLength}
        strokeDashoffset={dashOffset}
      />
    </svg>
  );
};
