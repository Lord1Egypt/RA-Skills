/**
 * Scene 09 — "Summary"
 * Animation: Recap — time domain wave transforms into frequency domain spectrum,
 * with a "Thank you" closing.
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

export const FourierScene09: React.FC<SceneProps> = ({ title, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEntrance = spring({ frame, fps, config: { damping: 200 } });
  const titleOpacity = interpolate(titleEntrance, [0, 1], [0, 1]);
  const titleY = interpolate(titleEntrance, [0, 1], [30, 0]);

  // Phase 1: Show the 3 sine waves stacking up
  const wave1Opacity = interpolate(frame, [20, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const wave2Opacity = interpolate(frame, [35, 55], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const wave3Opacity = interpolate(frame, [50, 70], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Phase 2: Merge into composite
  const mergeProgress = interpolate(frame, [80, 120], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Phase 3: Transform arrow and spectrum
  const transformOpacity = interpolate(frame, [120, 145], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Phase 4: Closing message
  const closingOpacity = interpolate(frame, [160, 190], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Composite wave
  const compositeWavePoints = (() => {
    const width = 500;
    const height = 120;
    const cy = height / 2;
    const resolution = 200;
    const points: string[] = [];
    for (let i = 0; i <= resolution; i++) {
      const x = (i / resolution) * width;
      const t = (i / resolution) * 2 * Math.PI;
      const y =
        cy -
        (30 * Math.sin(2 * t + frame * 0.04) +
          18 * Math.sin(6 * t + frame * 0.06) +
          10 * Math.sin(10 * t + frame * 0.088));
      points.push(`${i === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
    }
    return { points: points.join(" "), width, height };
  })();

  // Spectrum bars
  const spectrumBars = [
    { label: "f₁", value: 30, color: "#3b82f6" },
    { label: "f₂", value: 18, color: "#8b5cf6" },
    { label: "f₃", value: 10, color: "#ec4899" },
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
          gap: 16,
        }}
      >
        {/* Individual waves (fade out as merge happens) */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 4,
            opacity: interpolate(mergeProgress, [0, 1], [1, 0]),
          }}
        >
          <div style={{ opacity: wave1Opacity }}>
            <SineWave width={500} height={60} frequency={2} amplitude={25} phaseSpeed={0.04} color="#3b82f6" strokeWidth={2} />
          </div>
          <div style={{ color: theme.textColor, fontSize: 20, fontWeight: 600 }}>+</div>
          <div style={{ opacity: wave2Opacity }}>
            <SineWave width={500} height={60} frequency={6} amplitude={15} phaseSpeed={0.06} color="#8b5cf6" strokeWidth={2} />
          </div>
          <div style={{ color: theme.textColor, fontSize: 20, fontWeight: 600 }}>+</div>
          <div style={{ opacity: wave3Opacity }}>
            <SineWave width={500} height={60} frequency={10} amplitude={8} phaseSpeed={0.088} color="#ec4899" strokeWidth={2} />
          </div>
        </div>

        {/* Merged composite wave */}
        <div
          style={{
            opacity: mergeProgress,
            display: "flex",
            alignItems: "center",
            gap: 30,
          }}
        >
          {/* Composite wave */}
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div style={{ color: "#f59e0b", fontSize: 18, fontWeight: 600, marginBottom: 4 }}>
              Time Domain
            </div>
            <svg width={compositeWavePoints.width} height={compositeWavePoints.height}>
              <path
                d={compositeWavePoints.points}
                fill="none"
                stroke="#f59e0b"
                strokeWidth={3}
                strokeLinecap="round"
              />
            </svg>
          </div>

          {/* Transform arrow */}
          <div
            style={{
              opacity: transformOpacity,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 4,
            }}
          >
            <div style={{ color: "#10b981", fontSize: 40, fontWeight: 700 }}>⇌</div>
            <div style={{ color: "#10b981", fontSize: 14, fontWeight: 600 }}>FT</div>
          </div>

          {/* Spectrum */}
          <div
            style={{
              opacity: transformOpacity,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <div style={{ color: "#10b981", fontSize: 18, fontWeight: 600, marginBottom: 4 }}>
              Frequency Domain
            </div>
            <div
              style={{
                display: "flex",
                alignItems: "flex-end",
                gap: 20,
                height: 120,
                padding: "0 20px",
                borderLeft: "2px solid #333",
                borderBottom: "2px solid #333",
              }}
            >
              {spectrumBars.map((bar, i) => {
                const barEntrance = spring({
                  frame,
                  fps,
                  delay: 130 + i * 8,
                  config: { damping: 15, stiffness: 80 },
                });
                return (
                  <div key={bar.label} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
                    <div style={{ color: bar.color, fontSize: 14, fontWeight: 600 }}>
                      {bar.value}
                    </div>
                    <div
                      style={{
                        width: 50,
                        height: bar.value * 3 * barEntrance,
                        backgroundColor: bar.color,
                        borderRadius: "4px 4px 0 0",
                      }}
                    />
                    <div style={{ color: "#888", fontSize: 13 }}>{bar.label}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Closing message */}
        <div
          style={{
            opacity: closingOpacity,
            textAlign: "center",
            marginTop: 20,
          }}
        >
          <div
            style={{
              color: theme.primaryColor,
              fontSize: 32,
              fontWeight: 700,
              fontFamily: theme.fontFamily,
              marginBottom: 8,
            }}
          >
            Any complex signal = Sum of simple sine waves
          </div>
          <div
            style={{
              color: "#f59e0b",
              fontSize: 26,
              fontWeight: 600,
              fontFamily: theme.fontFamily,
            }}
          >
            Thank you for watching! 🎬
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
