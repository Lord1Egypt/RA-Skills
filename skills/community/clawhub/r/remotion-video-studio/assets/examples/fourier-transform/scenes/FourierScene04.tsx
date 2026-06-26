/**
 * Scene 04 — "Mathematical Expression"
 * Animation: Fourier formula appears with typewriter effect,
 * then shows a sine wave "matching" the original signal (similarity visualization).
 */
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { TypewriterText } from "../animations/TypewriterText";

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
 * Animated similarity visualization: a test sine wave slides across the signal,
 * and the "match area" fills in where they overlap.
 */
const SimilarityViz: React.FC<{
  width: number;
  height: number;
  frame: number;
  opacity: number;
}> = ({ width, height, frame, opacity }) => {
  const cy = height / 2;
  const resolution = 300;
  const testFreq = 3;
  const phase = frame * 0.03;

  // Original signal
  const signalPoints: string[] = [];
  for (let i = 0; i <= resolution; i++) {
    const x = (i / resolution) * width;
    const t = (i / resolution) * 4 * Math.PI;
    const y = cy - (30 * Math.sin(t) + 18 * Math.sin(3 * t) + 10 * Math.sin(5 * t));
    signalPoints.push(`${i === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
  }

  // Test sine wave (slides in frequency)
  const testPoints: string[] = [];
  for (let i = 0; i <= resolution; i++) {
    const x = (i / resolution) * width;
    const t = (i / resolution) * 4 * Math.PI;
    const y = cy - 25 * Math.sin(testFreq * t + phase);
    testPoints.push(`${i === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
  }

  // Similarity meter
  const similarity = interpolate(
    Math.sin(frame * 0.02),
    [-1, 1],
    [0.2, 0.95]
  );
  const meterWidth = 200;
  const meterHeight = 20;
  const meterX = width - meterWidth - 20;
  const meterY = 15;

  return (
    <svg width={width} height={height} style={{ opacity }}>
      {/* Original signal */}
      <path
        d={signalPoints.join(" ")}
        fill="none"
        stroke="#3b82f6"
        strokeWidth={2.5}
        strokeLinecap="round"
      />
      {/* Test sine wave */}
      <path
        d={testPoints.join(" ")}
        fill="none"
        stroke="#f59e0b"
        strokeWidth={2}
        strokeDasharray="8 4"
        strokeLinecap="round"
      />
      {/* Legend */}
      <text x={20} y={20} fill="#3b82f6" fontSize={14} fontWeight={600}>
        ── Original Signal f(t)
      </text>
      <text x={20} y={40} fill="#f59e0b" fontSize={14} fontWeight={600}>
        - - Test Sine sin(ωt)
      </text>
      {/* Similarity meter */}
      <text x={meterX} y={meterY - 2} fill="#888" fontSize={13}>
        Similarity:
      </text>
      <rect
        x={meterX}
        y={meterY + 4}
        width={meterWidth}
        height={meterHeight}
        rx={4}
        fill="#222"
      />
      <rect
        x={meterX}
        y={meterY + 4}
        width={meterWidth * similarity}
        height={meterHeight}
        rx={4}
        fill={similarity > 0.7 ? "#10b981" : "#f59e0b"}
      />
    </svg>
  );
};

export const FourierScene04: React.FC<SceneProps> = ({ title, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEntrance = spring({ frame, fps, config: { damping: 200 } });
  const titleOpacity = interpolate(titleEntrance, [0, 1], [0, 1]);
  const titleY = interpolate(titleEntrance, [0, 1], [30, 0]);

  // Formula appears after title
  const formulaOpacity = interpolate(frame, [20, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Visualization appears after formula
  const vizOpacity = interpolate(frame, [80, 110], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Explanation text
  const explainOpacity = interpolate(frame, [120, 145], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.backgroundColor,
        padding: 50,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Title */}
      <div
        style={{
          fontSize: theme.titleFontSize * 0.8,
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

      {/* Formula */}
      <div
        style={{
          opacity: formulaOpacity,
          textAlign: "center",
          marginBottom: 24,
        }}
      >
        <div
          style={{
            display: "inline-block",
            backgroundColor: "rgba(59, 130, 246, 0.1)",
            border: "1px solid rgba(59, 130, 246, 0.3)",
            borderRadius: 12,
            padding: "16px 32px",
          }}
        >
          <TypewriterText
            text="F(ω) = ∫ f(t) · e^(-iωt) dt"
            fontSize={44}
            fontWeight={700}
            color="#3b82f6"
            charFrames={3}
            delay={30}
            showCursor={true}
            fontFamily="'Courier New', monospace"
          />
        </div>
      </div>

      {/* Similarity visualization */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 16,
        }}
      >
        <SimilarityViz
          width={1000}
          height={280}
          frame={frame}
          opacity={vizOpacity}
        />

        {/* Explanation */}
        <div
          style={{
            opacity: explainOpacity,
            color: theme.textColor,
            fontSize: 22,
            textAlign: "center",
            maxWidth: 800,
            lineHeight: 1.6,
            fontFamily: theme.fontFamily,
          }}
        >
          The integral measures how similar the signal is to each frequency.
          <br />
          <span style={{ color: "#10b981", fontWeight: 600 }}>
            Higher similarity → larger coefficient in the spectrum
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
