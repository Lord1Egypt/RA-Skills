/**
 * Scene 06 — "Application: Audio Processing"
 * Animation: Audio waveform → frequency spectrum → MP3 compression (remove inaudible frequencies).
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

const spectrumBars = [
  { freq: "20Hz", height: 30, audible: true },
  { freq: "100Hz", height: 70, audible: true },
  { freq: "500Hz", height: 90, audible: true },
  { freq: "1kHz", height: 100, audible: true },
  { freq: "2kHz", height: 85, audible: true },
  { freq: "4kHz", height: 60, audible: true },
  { freq: "8kHz", height: 40, audible: true },
  { freq: "12kHz", height: 25, audible: false },
  { freq: "16kHz", height: 15, audible: false },
  { freq: "20kHz", height: 8, audible: false },
];

export const FourierScene06: React.FC<SceneProps> = ({ title, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEntrance = spring({ frame, fps, config: { damping: 200 } });
  const titleOpacity = interpolate(titleEntrance, [0, 1], [0, 1]);
  const titleY = interpolate(titleEntrance, [0, 1], [30, 0]);

  // Phase 1: Show spectrum
  const spectrumOpacity = interpolate(frame, [20, 45], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Phase 2: Highlight inaudible frequencies (red)
  const highlightProgress = interpolate(frame, [90, 120], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Phase 3: Remove inaudible frequencies (fade out)
  const removeProgress = interpolate(frame, [140, 170], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // File size comparison
  const fileSizeOpacity = interpolate(frame, [170, 195], [0, 1], {
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
          marginBottom: 24,
        }}
      >
        {title}
      </div>

      {/* Spectrum visualization */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 24,
          opacity: spectrumOpacity,
        }}
      >
        {/* Spectrum bars */}
        <div
          style={{
            display: "flex",
            alignItems: "flex-end",
            gap: 12,
            height: 300,
            padding: "0 40px",
          }}
        >
          {spectrumBars.map((bar, i) => {
            const barEntrance = spring({
              frame,
              fps,
              delay: 30 + i * 5,
              config: { damping: 18, stiffness: 80 },
            });

            const barHeight = bar.height * 2.5 * barEntrance;

            // Determine bar color based on phase
            let barColor = "#3b82f6";
            let barOpacity = 1;

            if (!bar.audible) {
              if (highlightProgress > 0) {
                barColor = interpolate(highlightProgress, [0, 1], [0, 1]) > 0.5
                  ? "#ef4444"
                  : "#3b82f6";
                if (barColor === "#ef4444") barColor = "#ef4444";
              }
              if (removeProgress > 0) {
                barOpacity = interpolate(removeProgress, [0, 1], [1, 0.1]);
              }
            }

            return (
              <div
                key={bar.freq}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 8,
                }}
              >
                <div
                  style={{
                    width: 60,
                    height: barHeight,
                    backgroundColor: !bar.audible && highlightProgress > 0.5
                      ? "#ef4444"
                      : "#3b82f6",
                    borderRadius: "6px 6px 0 0",
                    opacity: barOpacity,
                  }}
                />
                <div
                  style={{
                    color: "#888",
                    fontSize: 13,
                    fontFamily: theme.fontFamily,
                  }}
                >
                  {bar.freq}
                </div>
              </div>
            );
          })}
        </div>

        {/* Labels */}
        <div style={{ display: "flex", gap: 40, alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <div
              style={{
                width: 20,
                height: 20,
                backgroundColor: "#3b82f6",
                borderRadius: 4,
              }}
            />
            <span style={{ color: theme.textColor, fontSize: 18, fontFamily: theme.fontFamily }}>
              Audible frequencies
            </span>
          </div>
          {highlightProgress > 0.5 && (
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <div
                style={{
                  width: 20,
                  height: 20,
                  backgroundColor: "#ef4444",
                  borderRadius: 4,
                }}
              />
              <span style={{ color: "#ef4444", fontSize: 18, fontFamily: theme.fontFamily }}>
                Inaudible (removed in MP3)
              </span>
            </div>
          )}
        </div>

        {/* File size comparison */}
        {fileSizeOpacity > 0 && (
          <div
            style={{
              opacity: fileSizeOpacity,
              display: "flex",
              gap: 60,
              alignItems: "center",
            }}
          >
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 48, marginBottom: 8 }}>📁</div>
              <div style={{ color: "#ef4444", fontSize: 22, fontWeight: 700 }}>WAV: 50 MB</div>
            </div>
            <div style={{ color: "#f59e0b", fontSize: 40, fontWeight: 700 }}>→</div>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 48, marginBottom: 8 }}>🎵</div>
              <div style={{ color: "#10b981", fontSize: 22, fontWeight: 700 }}>MP3: 5 MB</div>
            </div>
            <div
              style={{
                color: "#f59e0b",
                fontSize: 24,
                fontWeight: 700,
                fontFamily: theme.fontFamily,
              }}
            >
              10× smaller!
            </div>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
