/**
 * Scene 01 — "What is Fourier Transform"
 * Animation: A complex wave decomposes into 3 simple sine waves.
 */
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
} from "remotion";
import { SineWave } from "../animations/SineWave";
import { FadeIn } from "../animations/FadeIn";

type SceneProps = {
  title: string;
  theme: {
    backgroundColor: string;
    primaryColor: string;
    secondaryColor: string;
    textColor: string;
    titleFontSize: number;
    fontFamily: string;
  };
};

/**
 * Composite wave: sum of 3 sine waves drawn via SVG path.
 */
const CompositeWave: React.FC<{
  width: number;
  height: number;
  frame: number;
  opacity: number;
}> = ({ width, height, frame, opacity }) => {
  const cy = height / 2;
  const phase = frame * 0.04;
  const resolution = 300;

  const points: string[] = [];
  for (let i = 0; i <= resolution; i++) {
    const x = (i / resolution) * width;
    const t = (i / resolution) * 2 * Math.PI;
    // Sum of 3 frequencies
    const y =
      cy -
      (40 * Math.sin(1 * t * 2 + phase) +
        25 * Math.sin(3 * t * 2 + phase * 1.5) +
        15 * Math.sin(5 * t * 2 + phase * 2.2));
    points.push(`${i === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
  }

  return (
    <svg width={width} height={height} style={{ opacity }}>
      <path
        d={points.join(" ")}
        fill="none"
        stroke="#f59e0b"
        strokeWidth={4}
        strokeLinecap="round"
      />
      {/* Label */}
      <text x={width - 120} y={30} fill="#f59e0b" fontSize={18} fontWeight={600}>
        Complex Signal
      </text>
    </svg>
  );
};

export const FourierScene01: React.FC<SceneProps> = ({ title, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Phase 1 (0–60): Title entrance
  // Phase 2 (30–90): Show composite wave
  // Phase 3 (90+): Decompose into 3 sine waves

  const titleEntrance = spring({ frame, fps, config: { damping: 200 } });
  const titleOpacity = interpolate(titleEntrance, [0, 1], [0, 1]);
  const titleY = interpolate(titleEntrance, [0, 1], [30, 0]);

  // Composite wave fades in then fades out as decomposition starts
  const compositeOpacity = interpolate(
    frame,
    [30, 50, 90, 120],
    [0, 1, 1, 0.15],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Individual waves fade in staggered
  const wave1Opacity = interpolate(frame, [90, 110], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const wave2Opacity = interpolate(frame, [105, 125], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const wave3Opacity = interpolate(frame, [120, 140], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Arrow / "=" sign between composite and components
  const arrowOpacity = interpolate(frame, [110, 130], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.backgroundColor,
        padding: 60,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Title */}
      <div
        style={{
          fontSize: theme.titleFontSize * 0.85,
          fontWeight: 700,
          color: theme.primaryColor,
          opacity: titleOpacity,
          transform: `translateY(${titleY}px)`,
          textAlign: "center",
          fontFamily: theme.fontFamily,
          marginBottom: 20,
        }}
      >
        {title}
      </div>

      {/* Animation area */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 8,
        }}
      >
        {/* Composite wave */}
        <CompositeWave
          width={1000}
          height={120}
          frame={frame}
          opacity={compositeOpacity}
        />

        {/* Decomposition arrow */}
        <div
          style={{
            opacity: arrowOpacity,
            color: theme.textColor,
            fontSize: 28,
            fontWeight: 700,
            textAlign: "center",
            margin: "4px 0",
            fontFamily: theme.fontFamily,
          }}
        >
          ↓ Decompose ↓
        </div>

        {/* 3 individual sine waves */}
        <div style={{ opacity: wave1Opacity, position: "relative" }}>
          <SineWave
            width={1000}
            height={80}
            frequency={2}
            amplitude={35}
            phaseSpeed={0.04}
            color="#3b82f6"
            strokeWidth={3}
          />
          <div
            style={{
              position: "absolute",
              right: 20,
              top: 8,
              color: "#3b82f6",
              fontSize: 16,
              fontWeight: 600,
            }}
          >
            f₁ = 1× (Fundamental)
          </div>
        </div>

        <div style={{ opacity: wave2Opacity, position: "relative" }}>
          <SineWave
            width={1000}
            height={80}
            frequency={6}
            amplitude={22}
            phaseSpeed={0.06}
            color="#8b5cf6"
            strokeWidth={3}
          />
          <div
            style={{
              position: "absolute",
              right: 20,
              top: 8,
              color: "#8b5cf6",
              fontSize: 16,
              fontWeight: 600,
            }}
          >
            f₂ = 3× (3rd Harmonic)
          </div>
        </div>

        <div style={{ opacity: wave3Opacity, position: "relative" }}>
          <SineWave
            width={1000}
            height={80}
            frequency={10}
            amplitude={13}
            phaseSpeed={0.088}
            color="#ec4899"
            strokeWidth={3}
          />
          <div
            style={{
              position: "absolute",
              right: 20,
              top: 8,
              color: "#ec4899",
              fontSize: 16,
              fontWeight: 600,
            }}
          >
            f₃ = 5× (5th Harmonic)
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
