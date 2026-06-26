import { useCurrentFrame, Audio, staticFile, interpolate, Easing } from "remotion";
import React from "react";
import { FadeIn, DriftingGrid, FloatingOrb } from "./components";

// ═══════════════════════════════════════════════
//  TEMPLATE: Conversation / Dialogue Video
//  Multi-speaker text bubbles with voice-colored
//  labels, animated background, optional audio sync.
// ═══════════════════════════════════════════════

interface Line {
  speaker: string;
  text: string;
  duration: number; // frames
  align: "left" | "right" | "center";
}

const SPEAKERS: Record<string, { color: string; align: "left" | "right" | "center" }> = {
  INTERVIEWER: { color: "#60a5fa", align: "left" },
  CUSTOMER:    { color: "#34d399", align: "right" },
  NARRATOR:    { color: "#cbd5e1", align: "center" },
  HOST:        { color: "#f472b6", align: "left" },
  GUEST:       { color: "#a78bfa", align: "right" },
};

const conversation: Line[] = [
  { speaker: "HOST",  text: "Welcome to the show!", duration: 60, align: "left" },
  { speaker: "GUEST", text: "Thanks for having me.", duration: 55, align: "right" },
  { speaker: "HOST",  text: "Let's dive in.", duration: 50, align: "left" },
];

const GAP = 10;
const starts = conversation.reduce((acc, line, i) => {
  acc.push(i === 0 ? 0 : acc[i - 1] + conversation[i - 1].duration + GAP);
  return acc;
}, [] as number[]);

export const CONVERSATION_DURATION =
  starts[starts.length - 1] + conversation[conversation.length - 1].duration + 30;

const Bubble: React.FC<{ line: Line; start: number }> = ({ line, start }) => {
  const frame = useCurrentFrame();
  const cfg = SPEAKERS[line.speaker] || SPEAKERS.NARRATOR;

  const enter = interpolate(frame, [start, start + 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const exit = interpolate(
    frame, [start + line.duration - 12, start + line.duration], [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  if (frame < start || frame >= start + line.duration) return null;

  return (
    <div style={{
      position: "absolute", inset: 0, display: "flex",
      flexDirection: "column", justifyContent: "center",
      alignItems: cfg.align === "left" ? "flex-start" : cfg.align === "right" ? "flex-end" : "center",
      padding: "0 80px", opacity: enter * exit,
      transform: `translateX(${(1 - enter) * (cfg.align === "left" ? -30 : cfg.align === "right" ? 30 : 0)}px)`,
      pointerEvents: "none",
    }}>
      <div style={{
        maxWidth: "760px", padding: "22px 30px", borderRadius: "14px",
        background: "rgba(15, 23, 42, 0.9)",
        border: `1.5px solid ${cfg.color}30`,
        boxShadow: `0 8px 28px ${cfg.color}12`,
      }}>
        <div style={{
          fontSize: 11, fontWeight: 700, letterSpacing: 1.2,
          color: cfg.color, marginBottom: 8, textTransform: "uppercase",
        }}>
          {line.speaker}
        </div>
        <div style={{ fontSize: 26, lineHeight: 1.4, color: "#f8fafc", fontWeight: 500 }}>
          {line.text}
        </div>
      </div>
    </div>
  );
};

export const ConversationVideo: React.FC = () => {
  return (
    <div style={{ width: "100%", height: "100%", position: "relative" }}>
      {/* Uncomment for audio sync:
      <Audio src={staticFile("audio.wav")} />
      */}
      <div style={{
        position: "absolute", inset: 0,
        background: "linear-gradient(145deg, #0b1021 0%, #131a3a 50%, #0b1021 100%)",
        overflow: "hidden",
      }}>
        <DriftingGrid />
        <FloatingOrb x="15%" y="20%" size={300} color="rgba(99,102,241,0.1)" speed={90} />
        <FloatingOrb x="60%" y="65%" size={250} color="rgba(52,211,153,0.08)" speed={110} />
      </div>
      <FadeIn start={0} duration={20}>
        <div style={{
          position: "absolute", top: 28, left: "50%",
          transform: "translateX(-50%)", display: "flex", alignItems: "center", gap: 10,
        }}>
          <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#34d399", boxShadow: "0 0 10px #34d39950" }} />
          <span style={{ fontSize: 13, fontWeight: 600, color: "#94a3b8", letterSpacing: 2, textTransform: "uppercase" }}>
            Live Discussion
          </span>
        </div>
      </FadeIn>
      {conversation.map((line, i) => (
        <Bubble key={i} line={line} start={starts[i]} />
      ))}
    </div>
  );
};
