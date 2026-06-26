import { useCurrentFrame } from "remotion";
import React from "react";
import { FadeIn, SlideIn, ScaleIn, FloatingOrb } from "./components";

// ═══════════════════════════════════════════════
//  TEMPLATE: Explainer — Concept + Detail Layout
//  Step-by-step reveal pattern with icons and text.
//  Great for feature explainers, tutorials, how-tos.
// ═══════════════════════════════════════════════

export const EXPLAINER_DURATION = 300;

const STEPS = [
  { icon: "1", title: "Connect",   detail: "Link your data sources in one click" },
  { icon: "2", title: "Analyze",   detail: "AI finds patterns you would miss" },
  { icon: "3", title: "Act",       detail: "Get actionable insights instantly" },
];

export const ExplainerVideo: React.FC = () => {
  return (
    <div style={{
      width: "100%", height: "100%", position: "relative",
      display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
      background: "linear-gradient(160deg, #0a0a0f 0%, #121230 100%)",
      color: "#ffffff", padding: 60,
    }}>
      <div style={{ position: "absolute", inset: 0, overflow: "hidden", pointerEvents: "none" }}>
        <FloatingOrb x="10%" y="80%" size={350} color="rgba(99,102,241,0.05)" speed={140} />
      </div>

      {/* Headline */}
      <FadeIn start={0} duration={20}>
        <div style={{ fontSize: 20, fontWeight: 600, color: "#6366f1", marginBottom: 8, letterSpacing: 2, textTransform: "uppercase" }}>
          How It Works
        </div>
      </FadeIn>

      <SlideIn start={10} duration={25} direction="up" distance={40}>
        <h1 style={{ fontSize: 56, fontWeight: 800, margin: "0 0 60px 0", textAlign: "center" }}>
          Three steps to clarity
        </h1>
      </SlideIn>

      {/* Steps */}
      <div style={{ display: "flex", gap: 40, justifyContent: "center", width: "100%", maxWidth: 1200 }}>
        {STEPS.map((step, i) => (
          <div key={i} style={{ flex: 1, maxWidth: 340, textAlign: "center" }}>
            <ScaleIn start={40 + i * 40} duration={20}>
              <div style={{
                width: 80, height: 80, borderRadius: 20,
                background: "linear-gradient(135deg, #6366f1, #a78bfa)",
                display: "flex", alignItems: "center", justifyContent: "center",
                margin: "0 auto 24px", fontSize: 32, fontWeight: 800,
                boxShadow: "0 12px 40px rgba(99,102,241,0.25)",
              }}>
                {step.icon}
              </div>
            </ScaleIn>

            <FadeIn start={50 + i * 40} duration={20}>
              <h3 style={{ fontSize: 28, fontWeight: 700, margin: "0 0 12px 0" }}>
                {step.title}
              </h3>
            </FadeIn>

            <FadeIn start={60 + i * 40} duration={20}>
              <p style={{ fontSize: 18, color: "#a0a0b0", lineHeight: 1.5, margin: 0 }}>
                {step.detail}
              </p>
            </FadeIn>
          </div>
        ))}
      </div>

      {/* Bottom CTA */}
      <FadeIn start={200} duration={20}>
        <div style={{
          marginTop: 60, padding: "16px 40px", borderRadius: 12,
          background: "#6366f1", fontSize: 20, fontWeight: 700,
          cursor: "default",
        }}>
          Get Started Free
        </div>
      </FadeIn>
    </div>
  );
};
