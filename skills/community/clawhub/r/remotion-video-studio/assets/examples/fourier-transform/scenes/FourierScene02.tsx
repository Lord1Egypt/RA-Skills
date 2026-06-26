/**
 * Scene 02 — "Time Domain vs Frequency Domain"
 * Animation: Left side shows time-domain waveform, right side shows frequency spectrum bars.
 */
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { SineWave } from "../animations/SineWave";
import { AnimatedBarChart, BarDataItem } from "../animations/AnimatedBarChart";

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
 * Time-domain composite waveform (animated).
 */
const TimeDomainWave: React.FC<{
  width: number;
  height: number;
  frame: number;
}> = ({ width, height, frame }) => {
  const cy = height / 2;
  const phase = frame * 0.05;
  const resolution = 250;

  const points: string[] = [];
  for (let i = 0; i <= resolution; i++) {
    const x = (i / resolution) * width;
    const t = (i / resolution) * 4 * Math.PI;
    const y =
      cy -
      (35 * Math.sin(t + phase) +
        20 * Math.sin(3 * t + phase * 1.3) +
        12 * Math.sin(5 * t + phase * 1.8) +
        8 * Math.sin(7 * t + phase * 2.1));
    points.push(`${i === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
  }

  return (
    <svg width={width} height={height}>
      {/* Axes */}
      <line x1={30} y1={cy} x2={width - 10} y2={cy} stroke="#444" strokeWidth={1} />
      <line x1={30} y1={20} x2={30} y2={height - 20} stroke="#444" strokeWidth={1} />
      {/* Labels */}
      <text x={width / 2} y={height - 5} fill="#888" fontSize={14} textAnchor="middle">
        Time →
      </text>
      <text x={10} y={cy - 10} fill="#888" fontSize={14} transform={`rotate(-90, 12, ${cy})`}>
        Amplitude
      </text>
      {/* Wave */}
      <path
        d={points.join(" ")}
        fill="none"
        stroke="#3b82f6"
        strokeWidth={3}
        strokeLinecap="round"
      />
    </svg>
  );
};

export const FourierScene02: React.FC<SceneProps> = ({ title, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEntrance = spring({ frame, fps, config: { damping: 200 } });
  const titleOpacity = interpolate(titleEntrance, [0, 1], [0, 1]);
  const titleY = interpolate(titleEntrance, [0, 1], [30, 0]);

  // Left panel (time domain) fades in
  const leftOpacity = interpolate(frame, [15, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Arrow between panels
  const arrowOpacity = interpolate(frame, [50, 70], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Right panel (frequency domain) fades in
  const rightOpacity = interpolate(frame, [60, 85], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const spectrumData: BarDataItem[] = [
    { label: "f₁", value: 35, color: "#3b82f6" },
    { label: "3f₁", value: 20, color: "#8b5cf6" },
    { label: "5f₁", value: 12, color: "#ec4899" },
    { label: "7f₁", value: 8, color: "#f59e0b" },
  ];

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

      {/* Two-panel layout */}
      <div
        style={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 20,
        }}
      >
        {/* Left: Time Domain */}
        <div
          style={{
            opacity: leftOpacity,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <div
            style={{
              color: "#3b82f6",
              fontSize: 28,
              fontWeight: 700,
              marginBottom: 12,
              fontFamily: theme.fontFamily,
            }}
          >
            Time Domain
          </div>
          <div
            style={{
              border: "1px solid #333",
              borderRadius: 12,
              padding: 16,
              backgroundColor: "rgba(59, 130, 246, 0.05)",
            }}
          >
            <TimeDomainWave width={600} height={300} frame={frame} />
          </div>
        </div>

        {/* Arrow */}
        <div
          style={{
            opacity: arrowOpacity,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 8,
          }}
        >
          <div style={{ color: "#f59e0b", fontSize: 48, fontWeight: 700 }}>
            →
          </div>
          <div
            style={{
              color: "#f59e0b",
              fontSize: 16,
              fontWeight: 600,
              textAlign: "center",
              fontFamily: theme.fontFamily,
            }}
          >
            Fourier
            <br />
            Transform
          </div>
        </div>

        {/* Right: Frequency Domain */}
        <div
          style={{
            opacity: rightOpacity,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <div
            style={{
              color: "#8b5cf6",
              fontSize: 28,
              fontWeight: 700,
              marginBottom: 12,
              fontFamily: theme.fontFamily,
            }}
          >
            Frequency Domain
          </div>
          <div
            style={{
              border: "1px solid #333",
              borderRadius: 12,
              padding: 16,
              backgroundColor: "rgba(139, 92, 246, 0.05)",
            }}
          >
            <AnimatedBarChart
              data={spectrumData}
              chartHeight={260}
              chartWidth={500}
              delay={Math.max(0, frame > 60 ? 0 : 999)}
              staggerDelay={8}
              showValues={true}
              textColor={theme.textColor}
              mutedColor="#888"
              axisColor="#444"
              fontFamily={theme.fontFamily}
            />
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
