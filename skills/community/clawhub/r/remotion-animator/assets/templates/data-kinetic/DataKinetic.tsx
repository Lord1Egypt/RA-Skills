import { useCurrentFrame } from "remotion";
import React from "react";
import { FadeIn, SlideIn, ScaleIn, CountUp, ProgressBar } from "./components";

// ═══════════════════════════════════════════════
//  TEMPLATE: Data Kinetic — Animated Stats
//  Number counters, progress bars, metric reveals.
//  Great for dashboards, reports, social proof clips.
// ═══════════════════════════════════════════════

export const DATA_DURATION = 240;

const metrics = [
  { label: "Active Users", value: 42_500, prefix: "", suffix: "", decimals: 0 },
  { label: "Growth Rate",  value: 127.5,  prefix: "", suffix: "%", decimals: 1 },
  { label: "Revenue",      value: 2.4,    prefix: "$", suffix: "M", decimals: 1 },
];

export const DataKineticVideo: React.FC = () => {
  return (
    <div style={{
      width: "100%", height: "100%", position: "relative",
      display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
      background: "#0a0a0f", color: "#ffffff", padding: "80px",
    }}>
      <FadeIn start={0} duration={20}>
        <div style={{
          fontSize: 16, fontWeight: 700, letterSpacing: 3,
          textTransform: "uppercase", color: "#6366f1", marginBottom: 16,
        }}>
          Q3 Performance
        </div>
      </FadeIn>

      <SlideIn start={10} duration={25} direction="up">
        <h1 style={{ fontSize: 64, fontWeight: 800, margin: "0 0 60px 0" }}>
          The Numbers
        </h1>
      </SlideIn>

      <div style={{
        display: "grid", gridTemplateColumns: "repeat(3, 1fr)",
        gap: 40, width: "100%", maxWidth: 1200,
      }}>
        {metrics.map((m, i) => (
          <div key={i} style={{ textAlign: "center" }}>
            <FadeIn start={30 + i * 20} duration={15}>
              <div style={{
                fontSize: 16, fontWeight: 600, letterSpacing: 1.5,
                textTransform: "uppercase", color: "#a0a0b0", marginBottom: 12,
              }}>
                {m.label}
              </div>
            </FadeIn>

            <ScaleIn start={35 + i * 20} duration={20}>
              <div style={{ fontSize: 56, fontWeight: 800, color: "#6366f1", lineHeight: 1 }}>
                <CountUp
                  value={m.value}
                  start={40 + i * 20}
                  duration={40}
                  prefix={m.prefix}
                  suffix={m.suffix}
                  decimals={m.decimals}
                />
              </div>
            </ScaleIn>
          </div>
        ))}
      </div>

      {/* Progress bars appear later */}
      <div style={{ width: "100%", maxWidth: 800, marginTop: 60 }}>
        <FadeIn start={120} duration={20}>
          <div style={{ fontSize: 14, color: "#a0a0b0", marginBottom: 8 }}>Server Uptime</div>
          <ProgressBar start={130} end={180} color="#34d399" height={6} />
        </FadeIn>
        <FadeIn start={140} duration={20}>
          <div style={{ fontSize: 14, color: "#a0a0b0", margin: "16px 0 8px" }}>API Response</div>
          <ProgressBar start={150} end={200} color="#60a5fa" height={6} />
        </FadeIn>
        <FadeIn start={160} duration={20}>
          <div style={{ fontSize: 14, color: "#a0a0b0", margin: "16px 0 8px" }}>User Satisfaction</div>
          <ProgressBar start={170} end={220} color="#f472b6" height={6} />
        </FadeIn>
      </div>
    </div>
  );
};
