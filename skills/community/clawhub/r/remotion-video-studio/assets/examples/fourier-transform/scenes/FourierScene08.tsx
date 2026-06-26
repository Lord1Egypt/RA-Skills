/**
 * Scene 08 — "Application: More Fields"
 * Animation: Animated icons/cards for various application domains.
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

const applications = [
  { icon: "📡", name: "Communications", desc: "Signal modulation", color: "#3b82f6" },
  { icon: "🏥", name: "Medical Imaging", desc: "CT & MRI reconstruction", color: "#10b981" },
  { icon: "⚛️", name: "Quantum Mechanics", desc: "Wave function analysis", color: "#8b5cf6" },
  { icon: "📈", name: "Finance", desc: "Periodic pattern analysis", color: "#f59e0b" },
  { icon: "🌊", name: "Seismology", desc: "Earthquake wave analysis", color: "#ef4444" },
  { icon: "🔭", name: "Astronomy", desc: "Signal processing", color: "#06b6d4" },
];

export const FourierScene08: React.FC<SceneProps> = ({ title, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEntrance = spring({ frame, fps, config: { damping: 200 } });
  const titleOpacity = interpolate(titleEntrance, [0, 1], [0, 1]);
  const titleY = interpolate(titleEntrance, [0, 1], [30, 0]);

  // Central wave animation
  const waveOpacity = interpolate(frame, [15, 35], [0, 1], {
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
          marginBottom: 30,
        }}
      >
        {title}
      </div>

      {/* Central sine wave */}
      <div style={{ opacity: waveOpacity, display: "flex", justifyContent: "center", marginBottom: 20 }}>
        <svg width={800} height={80}>
          {(() => {
            const points: string[] = [];
            for (let i = 0; i <= 200; i++) {
              const x = (i / 200) * 800;
              const t = (i / 200) * 6 * Math.PI;
              const y = 40 - 25 * Math.sin(t + frame * 0.05);
              points.push(`${i === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
            }
            return (
              <path
                d={points.join(" ")}
                fill="none"
                stroke="rgba(59, 130, 246, 0.3)"
                strokeWidth={2}
              />
            );
          })()}
        </svg>
      </div>

      {/* Application cards grid */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          gap: 24,
          padding: "0 60px",
        }}
      >
        {applications.map((app, i) => {
          const cardEntrance = spring({
            frame,
            fps,
            delay: 40 + i * 12,
            config: { damping: 15, stiffness: 80 },
          });

          const cardScale = interpolate(cardEntrance, [0, 1], [0.5, 1]);
          const cardOpacity = interpolate(cardEntrance, [0, 1], [0, 1]);

          return (
            <div
              key={app.name}
              style={{
                width: 260,
                padding: "24px 20px",
                backgroundColor: "rgba(255, 255, 255, 0.05)",
                border: `1px solid ${app.color}33`,
                borderRadius: 16,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 10,
                opacity: cardOpacity,
                transform: `scale(${cardScale})`,
              }}
            >
              <div style={{ fontSize: 48 }}>{app.icon}</div>
              <div
                style={{
                  color: app.color,
                  fontSize: 22,
                  fontWeight: 700,
                  fontFamily: theme.fontFamily,
                }}
              >
                {app.name}
              </div>
              <div
                style={{
                  color: "#888",
                  fontSize: 16,
                  textAlign: "center",
                  fontFamily: theme.fontFamily,
                }}
              >
                {app.desc}
              </div>
            </div>
          );
        })}
      </div>

      {/* Bottom tagline */}
      <div
        style={{
          textAlign: "center",
          opacity: interpolate(frame, [120, 145], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
          color: "#f59e0b",
          fontSize: 24,
          fontWeight: 700,
          fontFamily: theme.fontFamily,
          padding: "12px 0",
        }}
      >
        Wherever there are signals and waves, Fourier Transform is there 🌊
      </div>
    </AbsoluteFill>
  );
};
