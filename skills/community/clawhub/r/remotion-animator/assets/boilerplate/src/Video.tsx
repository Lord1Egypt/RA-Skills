import { useCurrentFrame } from "remotion";
import React from "react";
import { FadeIn, SlideIn, ScaleIn } from "./components";

// ═══════════════════════════════════════════════
//  STARTER: Generic animation canvas
//  Customize this or swap in a template
// ═══════════════════════════════════════════════

export const DURATION = 180; // 6 seconds at 30fps

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%)",
        color: "#ffffff",
      }}
    >
      <FadeIn start={0} duration={15}>
        <div style={{ fontSize: 72, fontWeight: 800, letterSpacing: -2 }}>
          Hello World
        </div>
      </FadeIn>

      <SlideIn start={20} duration={20} direction="up" distance={40}>
        <div style={{ fontSize: 32, color: "#a0a0b0", marginTop: 20 }}>
          Animated with Remotion
        </div>
      </SlideIn>

      <ScaleIn start={50} duration={20}>
        <div
          style={{
            marginTop: 40,
            padding: "16px 40px",
            borderRadius: 12,
            background: "#6366f1",
            fontSize: 20,
            fontWeight: 600,
          }}
        >
          Get Started
        </div>
      </ScaleIn>
    </div>
  );
};
