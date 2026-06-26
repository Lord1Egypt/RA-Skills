/**
 * Scene 05 — "Discrete Fourier Transform / FFT"
 * Animation: Continuous wave → discrete sample points, then O(N²) vs O(NlogN) comparison.
 */
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { CountUp } from "../animations/CountUp";

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
 * Continuous wave with discrete sample points appearing on it.
 */
const DiscreteSampling: React.FC<{
  width: number;
  height: number;
  frame: number;
}> = ({ width, height, frame }) => {
  const cy = height / 2;
  const resolution = 300;
  const numSamples = 16;
  const padding = 40;
  const plotW = width - padding * 2;

  // Continuous wave path
  const points: string[] = [];
  for (let i = 0; i <= resolution; i++) {
    const x = padding + (i / resolution) * plotW;
    const t = (i / resolution) * 4 * Math.PI;
    const y = cy - (30 * Math.sin(t) + 15 * Math.sin(3 * t));
    points.push(`${i === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
  }

  // Continuous wave opacity (fades slightly as dots appear)
  const waveOpacity = interpolate(frame, [10, 30, 60, 90], [0, 1, 1, 0.4], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Sample dots appear one by one
  const dotsVisible = interpolate(frame, [40, 100], [0, numSamples], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <svg width={width} height={height}>
      {/* Axes */}
      <line x1={padding} y1={cy} x2={width - padding} y2={cy} stroke="#333" strokeWidth={1} />
      <line x1={padding} y1={20} x2={padding} y2={height - 20} stroke="#333" strokeWidth={1} />

      {/* Continuous wave */}
      <path
        d={points.join(" ")}
        fill="none"
        stroke="#3b82f6"
        strokeWidth={2}
        opacity={waveOpacity}
      />

      {/* Discrete sample points */}
      {Array.from({ length: numSamples }).map((_, i) => {
        if (i >= dotsVisible) return null;
        const t = (i / (numSamples - 1)) * 4 * Math.PI;
        const x = padding + (i / (numSamples - 1)) * plotW;
        const y = cy - (30 * Math.sin(t) + 15 * Math.sin(3 * t));

        return (
          <React.Fragment key={i}>
            {/* Vertical line from axis to point */}
            <line
              x1={x}
              y1={cy}
              x2={x}
              y2={y}
              stroke="#f59e0b"
              strokeWidth={1}
              strokeDasharray="3 3"
              opacity={0.5}
            />
            {/* Sample dot */}
            <circle cx={x} cy={y} r={5} fill="#f59e0b" stroke="#fff" strokeWidth={1.5} />
          </React.Fragment>
        );
      })}

      {/* Labels */}
      <text x={padding + 5} y={height - 5} fill="#888" fontSize={13}>
        Continuous → Discrete (N={numSamples} samples)
      </text>
    </svg>
  );
};

export const FourierScene05: React.FC<SceneProps> = ({ title, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEntrance = spring({ frame, fps, config: { damping: 200 } });
  const titleOpacity = interpolate(titleEntrance, [0, 1], [0, 1]);
  const titleY = interpolate(titleEntrance, [0, 1], [30, 0]);

  // Sampling visualization
  const samplingOpacity = interpolate(frame, [10, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Complexity comparison appears later
  const comparisonOpacity = interpolate(frame, [110, 135], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // N = 1024 for the comparison
  const n = 1024;
  const nSquared = n * n; // 1,048,576
  const nLogN = Math.round(n * Math.log2(n)); // 10,240

  // Bar widths for visual comparison
  const dftBarWidth = interpolate(frame, [140, 180], [0, 700], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fftBarWidth = interpolate(frame, [155, 195], [0, 700 * (nLogN / nSquared)], {
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
          marginBottom: 16,
        }}
      >
        {title}
      </div>

      {/* Sampling visualization */}
      <div style={{ opacity: samplingOpacity, display: "flex", justifyContent: "center" }}>
        <DiscreteSampling width={1000} height={250} frame={frame} />
      </div>

      {/* Complexity comparison */}
      <div
        style={{
          opacity: comparisonOpacity,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 20,
          marginTop: 20,
        }}
      >
        <div
          style={{
            color: theme.textColor,
            fontSize: 24,
            fontWeight: 700,
            fontFamily: theme.fontFamily,
          }}
        >
          Computational Complexity (N = {n})
        </div>

        {/* DFT bar */}
        <div style={{ display: "flex", alignItems: "center", gap: 16, width: 900 }}>
          <div
            style={{
              color: "#ef4444",
              fontSize: 20,
              fontWeight: 600,
              width: 120,
              textAlign: "right",
              fontFamily: "monospace",
            }}
          >
            DFT O(N²)
          </div>
          <div
            style={{
              height: 36,
              width: dftBarWidth,
              backgroundColor: "#ef4444",
              borderRadius: 6,
              transition: "none",
            }}
          />
          <div style={{ color: "#ef4444", fontSize: 18, fontWeight: 600 }}>
            {frame > 150 && (
              <CountUp to={nSquared} animationDuration={40} delay={150} fontSize={18} color="#ef4444" />
            )}
          </div>
        </div>

        {/* FFT bar */}
        <div style={{ display: "flex", alignItems: "center", gap: 16, width: 900 }}>
          <div
            style={{
              color: "#10b981",
              fontSize: 20,
              fontWeight: 600,
              width: 120,
              textAlign: "right",
              fontFamily: "monospace",
            }}
          >
            FFT O(NlogN)
          </div>
          <div
            style={{
              height: 36,
              width: fftBarWidth,
              backgroundColor: "#10b981",
              borderRadius: 6,
              transition: "none",
            }}
          />
          <div style={{ color: "#10b981", fontSize: 18, fontWeight: 600 }}>
            {frame > 165 && (
              <CountUp to={nLogN} animationDuration={40} delay={165} fontSize={18} color="#10b981" />
            )}
          </div>
        </div>

        {/* Speed-up label */}
        {frame > 190 && (
          <div
            style={{
              color: "#f59e0b",
              fontSize: 28,
              fontWeight: 700,
              fontFamily: theme.fontFamily,
              opacity: interpolate(frame, [190, 210], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              }),
            }}
          >
            ⚡ {Math.round(nSquared / nLogN)}× faster!
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
