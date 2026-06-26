/**
 * Scene 03 — "Intuitive Understanding"
 * Animation: Mixed sound wave → separates into violin, piano, drum waves.
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

const instruments = [
  { name: "🎻 Violin", freq: 8, amp: 30, color: "#3b82f6", phaseSpeed: 0.06 },
  { name: "🎹 Piano", freq: 4, amp: 25, color: "#10b981", phaseSpeed: 0.04 },
  { name: "🥁 Drum", freq: 2, amp: 20, color: "#f59e0b", phaseSpeed: 0.03 },
];

/**
 * Mixed wave: sum of all instrument frequencies.
 */
const MixedWave: React.FC<{
  width: number;
  height: number;
  frame: number;
  opacity: number;
}> = ({ width, height, frame, opacity }) => {
  const cy = height / 2;
  const resolution = 300;

  const points: string[] = [];
  for (let i = 0; i <= resolution; i++) {
    const x = (i / resolution) * width;
    const t = (i / resolution) * 2 * Math.PI;
    let y = cy;
    instruments.forEach((inst) => {
      y -= inst.amp * Math.sin(inst.freq * t + frame * inst.phaseSpeed);
    });
    points.push(`${i === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
  }

  return (
    <svg width={width} height={height} style={{ opacity }}>
      <path
        d={points.join(" ")}
        fill="none"
        stroke="#e2e8f0"
        strokeWidth={3}
        strokeLinecap="round"
      />
    </svg>
  );
};

export const FourierScene03: React.FC<SceneProps> = ({ title, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEntrance = spring({ frame, fps, config: { damping: 200 } });
  const titleOpacity = interpolate(titleEntrance, [0, 1], [0, 1]);
  const titleY = interpolate(titleEntrance, [0, 1], [30, 0]);

  // Mixed wave visible at start, fades as separation happens
  const mixedOpacity = interpolate(frame, [20, 45, 80, 110], [0, 1, 1, 0.15], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Ear icon and brain icon
  const earOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const brainOpacity = interpolate(frame, [80, 100], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Separation label
  const separationOpacity = interpolate(frame, [90, 110], [0, 1], {
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

      {/* Animation area */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 6,
        }}
      >
        {/* Mixed wave + ear icon */}
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <div style={{ opacity: earOpacity, fontSize: 56 }}>👂</div>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div
              style={{
                color: "#e2e8f0",
                fontSize: 20,
                fontWeight: 600,
                marginBottom: 4,
                opacity: earOpacity,
                fontFamily: theme.fontFamily,
              }}
            >
              Mixed Sound (Time Domain)
            </div>
            <MixedWave width={900} height={110} frame={frame} opacity={mixedOpacity} />
          </div>
        </div>

        {/* Brain separation */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 16,
            opacity: brainOpacity,
          }}
        >
          <div style={{ fontSize: 48 }}>🧠</div>
          <div
            style={{
              color: "#f59e0b",
              fontSize: 22,
              fontWeight: 700,
              fontFamily: theme.fontFamily,
            }}
          >
            Your brain performs Fourier Transform!
          </div>
        </div>

        {/* Separated instrument waves */}
        {instruments.map((inst, i) => {
          const waveOpacity = interpolate(
            frame,
            [100 + i * 15, 120 + i * 15],
            [0, 1],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          );

          return (
            <div
              key={inst.name}
              style={{
                opacity: waveOpacity,
                display: "flex",
                alignItems: "center",
                gap: 16,
              }}
            >
              <div
                style={{
                  color: inst.color,
                  fontSize: 20,
                  fontWeight: 600,
                  width: 140,
                  textAlign: "right",
                  fontFamily: theme.fontFamily,
                }}
              >
                {inst.name}
              </div>
              <SineWave
                width={800}
                height={70}
                frequency={inst.freq}
                amplitude={inst.amp * 0.8}
                phaseSpeed={inst.phaseSpeed}
                color={inst.color}
                strokeWidth={2.5}
              />
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
