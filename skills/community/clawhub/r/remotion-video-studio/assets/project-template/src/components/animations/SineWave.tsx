/**
 * SineWave — renders an animated sine wave using SVG.
 * Supports configurable frequency, amplitude, phase animation, and color.
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";

type SineWaveProps = {
  /** SVG width */
  width?: number;
  /** SVG height */
  height?: number;
  /** Wave frequency (number of full cycles visible) */
  frequency?: number;
  /** Wave amplitude in pixels */
  amplitude?: number;
  /** Phase speed (radians per frame) */
  phaseSpeed?: number;
  /** Initial phase offset */
  phaseOffset?: number;
  /** Stroke color */
  color?: string;
  /** Stroke width */
  strokeWidth?: number;
  /** Progressive draw: reveal the wave from left to right */
  progressiveDraw?: boolean;
  /** Duration of progressive draw in frames */
  drawDuration?: number;
  /** Delay in frames */
  delay?: number;
  /** Number of sample points */
  resolution?: number;
  /** Vertical center offset */
  centerY?: number;
  /** Custom style */
  style?: React.CSSProperties;
};

export const SineWave: React.FC<SineWaveProps> = ({
  width = 800,
  height = 200,
  frequency = 2,
  amplitude = 60,
  phaseSpeed = 0.05,
  phaseOffset = 0,
  color = "#3b82f6",
  strokeWidth = 3,
  progressiveDraw = false,
  drawDuration = 60,
  delay = 0,
  resolution = 200,
  centerY,
  style,
}) => {
  const frame = useCurrentFrame();

  const localFrame = Math.max(0, frame - delay);
  const cy = centerY ?? height / 2;
  const phase = phaseOffset + localFrame * phaseSpeed;

  // Build SVG path
  const points: string[] = [];
  for (let i = 0; i <= resolution; i++) {
    const x = (i / resolution) * width;
    const t = (i / resolution) * frequency * 2 * Math.PI;
    const y = cy - amplitude * Math.sin(t + phase);
    points.push(`${i === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
  }
  const pathD = points.join(" ");

  // Calculate approximate path length
  const pathLength = width * Math.sqrt(1 + (amplitude * frequency * 2 * Math.PI / width) ** 2);

  let dashOffset = 0;
  if (progressiveDraw) {
    const drawProgress = interpolate(
      localFrame,
      [0, drawDuration],
      [0, 1],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
    );
    dashOffset = pathLength * (1 - drawProgress);
  }

  return (
    <svg width={width} height={height} style={style}>
      <path
        d={pathD}
        fill="none"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        {...(progressiveDraw
          ? {
              strokeDasharray: pathLength,
              strokeDashoffset: dashOffset,
            }
          : {})}
      />
    </svg>
  );
};
