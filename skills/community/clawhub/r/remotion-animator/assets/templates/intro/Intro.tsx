import { useCurrentFrame } from "remotion";
import React from "react";
import { FadeIn, SlideIn, ScaleIn, FloatingOrb } from "./components";

// ═══════════════════════════════════════════════
//  TEMPLATE: Logo Intro / Title Reveal
//  Animated logo + title + subtitle sequence.
//  Great for YouTube intros, product reveals, etc.
// ═══════════════════════════════════════════════

export const INTRO_DURATION = 150;

export const IntroVideo: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{
      width: "100%", height: "100%", position: "relative",
      display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
      background: "radial-gradient(circle at center, #1a1a2e 0%, #0a0a0f 70%)",
      color: "#ffffff",
    }}>
      {/* Ambient orbs */}
      <div style={{ position: "absolute", inset: 0, overflow: "hidden", pointerEvents: "none" }}>
        <FloatingOrb x="20%" y="30%" size={400} color="rgba(99,102,241,0.08)" speed={120} />
        <FloatingOrb x="70%" y="60%" size={300} color="rgba(244,114,182,0.06)" speed={150} />
      </div>

      {/* Logo / Icon placeholder */}
      <ScaleIn start={10} duration={20}>
        <div style={{
          width: 120, height: 120, borderRadius: 24,
          background: "linear-gradient(135deg, #6366f1, #a78bfa)",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 48, fontWeight: 800,
          boxShadow: "0 20px 60px rgba(99,102,241,0.3)",
        }}>
          R
        </div>
      </ScaleIn>

      {/* Title */}
      <SlideIn start={35} duration={25} direction="up" distance={30}>
        <h1 style={{
          fontSize: 72, fontWeight: 800, letterSpacing: -2,
          margin: "24px 0 8px 0", lineHeight: 1.1,
        }}>
          Your Product
        </h1>
      </SlideIn>

      {/* Tagline */}
      <FadeIn start={55} duration={20}>
        <p style={{ fontSize: 28, color: "#a0a0b0", margin: 0 }}>
          The tagline goes here
        </p>
      </FadeIn>

      {/* CTA */}
      <FadeIn start={80} duration={20}>
        <div style={{
          marginTop: 40, padding: "14px 36px", borderRadius: 100,
          background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)",
          fontSize: 16, fontWeight: 600, color: "#a0a0b0",
        }}>
          yourcompany.com
        </div>
      </FadeIn>
    </div>
  );
};
