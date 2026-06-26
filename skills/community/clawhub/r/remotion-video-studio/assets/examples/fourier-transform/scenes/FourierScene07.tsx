/**
 * Scene 07 — "Application: Image Processing"
 * Animation: Image → 2D frequency domain → filter → result.
 * Uses a grid of colored cells to simulate image pixels and frequency components.
 */
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

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
 * Simulated image grid (8x8 pixels with edge pattern).
 */
const ImageGrid: React.FC<{
  size: number;
  label: string;
  mode: "original" | "frequency" | "filtered" | "result";
  frame: number;
  opacity: number;
}> = ({ size, label, mode, frame, opacity }) => {
  const gridSize = 8;
  const cellSize = size / gridSize;

  const getColor = (row: number, col: number): string => {
    switch (mode) {
      case "original": {
        // Simulate an image with edges
        const hasEdge = col === 3 || col === 4;
        const brightness = hasEdge ? 220 : 60 + row * 8;
        return `rgb(${brightness}, ${brightness}, ${brightness})`;
      }
      case "frequency": {
        // Simulate 2D frequency domain (center = low freq, edges = high freq)
        const cx = gridSize / 2;
        const cy = gridSize / 2;
        const dist = Math.sqrt((col - cx) ** 2 + (row - cy) ** 2);
        const intensity = Math.max(0, 255 - dist * 50);
        const r = dist < 2 ? intensity : intensity * 0.3;
        const g = dist < 2 ? intensity * 0.5 : intensity;
        const b = intensity;
        return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
      }
      case "filtered": {
        // Low-pass filter: keep center, remove edges
        const cx = gridSize / 2;
        const cy = gridSize / 2;
        const dist = Math.sqrt((col - cx) ** 2 + (row - cy) ** 2);
        if (dist > 3) return "rgb(10, 10, 10)";
        const intensity = Math.max(0, 255 - dist * 50);
        return `rgb(${Math.round(intensity * 0.3)}, ${Math.round(intensity * 0.5)}, ${Math.round(intensity)})`;
      }
      case "result": {
        // Blurred result (no sharp edges)
        const brightness = 80 + row * 8 + Math.sin(col * 0.8) * 20;
        return `rgb(${Math.round(brightness)}, ${Math.round(brightness)}, ${Math.round(brightness)})`;
      }
    }
  };

  return (
    <div style={{ opacity, display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
      <svg width={size} height={size}>
        {Array.from({ length: gridSize }).map((_, row) =>
          Array.from({ length: gridSize }).map((_, col) => (
            <rect
              key={`${row}-${col}`}
              x={col * cellSize}
              y={row * cellSize}
              width={cellSize - 1}
              height={cellSize - 1}
              fill={getColor(row, col)}
              rx={2}
            />
          ))
        )}
      </svg>
      <div
        style={{
          color: "#888",
          fontSize: 16,
          fontWeight: 600,
          textAlign: "center",
        }}
      >
        {label}
      </div>
    </div>
  );
};

export const FourierScene07: React.FC<SceneProps> = ({ title, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEntrance = spring({ frame, fps, config: { damping: 200 } });
  const titleOpacity = interpolate(titleEntrance, [0, 1], [0, 1]);
  const titleY = interpolate(titleEntrance, [0, 1], [30, 0]);

  // Staggered appearance of each stage
  const stage1 = interpolate(frame, [20, 45], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const arrow1 = interpolate(frame, [50, 70], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const stage2 = interpolate(frame, [55, 80], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const arrow2 = interpolate(frame, [90, 110], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const stage3 = interpolate(frame, [95, 120], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const arrow3 = interpolate(frame, [130, 150], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const stage4 = interpolate(frame, [135, 160], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  // Explanation text
  const explainOpacity = interpolate(frame, [160, 185], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const arrowStyle: React.CSSProperties = {
    color: "#f59e0b",
    fontSize: 36,
    fontWeight: 700,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 4,
  };

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
          marginBottom: 24,
        }}
      >
        {title}
      </div>

      {/* Pipeline visualization */}
      <div
        style={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 20,
        }}
      >
        <ImageGrid size={180} label="Original Image" mode="original" frame={frame} opacity={stage1} />

        <div style={{ ...arrowStyle, opacity: arrow1 }}>
          →
          <span style={{ fontSize: 12, color: "#888" }}>FFT 2D</span>
        </div>

        <ImageGrid size={180} label="Frequency Domain" mode="frequency" frame={frame} opacity={stage2} />

        <div style={{ ...arrowStyle, opacity: arrow2 }}>
          →
          <span style={{ fontSize: 12, color: "#888" }}>Low-pass Filter</span>
        </div>

        <ImageGrid size={180} label="Filtered Spectrum" mode="filtered" frame={frame} opacity={stage3} />

        <div style={{ ...arrowStyle, opacity: arrow3 }}>
          →
          <span style={{ fontSize: 12, color: "#888" }}>Inverse FFT</span>
        </div>

        <ImageGrid size={180} label="Blurred Result" mode="result" frame={frame} opacity={stage4} />
      </div>

      {/* Explanation */}
      <div
        style={{
          opacity: explainOpacity,
          textAlign: "center",
          padding: "16px 0",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: 40,
            color: theme.textColor,
            fontSize: 20,
            fontFamily: theme.fontFamily,
          }}
        >
          <span>
            🔍 <strong style={{ color: "#3b82f6" }}>Edges</strong> = High frequency
          </span>
          <span>
            🌫️ <strong style={{ color: "#8b5cf6" }}>Smooth areas</strong> = Low frequency
          </span>
          <span>
            📦 <strong style={{ color: "#10b981" }}>JPEG</strong> uses this principle
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
