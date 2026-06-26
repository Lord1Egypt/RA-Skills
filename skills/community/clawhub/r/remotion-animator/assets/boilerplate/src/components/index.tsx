// ═══════════════════════════════════════════════
//  Animation Primitives Library
//  Import these for fade, slide, scale, typewriter,
//  progress bars, backgrounds, and more.
// ═══════════════════════════════════════════════

import { useCurrentFrame, interpolate, Easing } from "remotion";
import React from "react";

// ─── FadeIn ─────────────────────────────────────
interface FadeInProps {
  children: React.ReactNode;
  start: number;
  duration?: number;
  from?: number;
  to?: number;
}
export const FadeIn: React.FC<FadeInProps> = ({
  children,
  start,
  duration = 15,
  from = 0,
  to = 1,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [start, start + duration], [from, to], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return <div style={{ opacity }}>{children}</div>;
};

// ─── SlideIn ────────────────────────────────────
interface SlideInProps {
  children: React.ReactNode;
  start: number;
  duration?: number;
  direction?: "up" | "down" | "left" | "right";
  distance?: number;
}
export const SlideIn: React.FC<SlideInProps> = ({
  children,
  start,
  duration = 20,
  direction = "up",
  distance = 60,
}) => {
  const frame = useCurrentFrame();
  const d = interpolate(frame, [start, start + duration], [distance, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const op = interpolate(frame, [start, start + duration - 5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const transform =
    direction === "up"
      ? `translateY(${d}px)`
      : direction === "down"
      ? `translateY(-${d}px)`
      : direction === "left"
      ? `translateX(${d}px)`
      : `translateX(-${d}px)`;

  return <div style={{ opacity: op, transform }}>{children}</div>;
};

// ─── ScaleIn ────────────────────────────────────
interface ScaleInProps {
  children: React.ReactNode;
  start: number;
  duration?: number;
  from?: number;
  to?: number;
}
export const ScaleIn: React.FC<ScaleInProps> = ({
  children,
  start,
  duration = 15,
  from = 0.8,
  to = 1,
}) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [start, start + duration], [from, to], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(1.2)),
  });
  const op = interpolate(frame, [start, start + duration - 5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <div style={{ opacity: op, transform: `scale(${s})` }}>{children}</div>;
};

// ─── Typewriter ─────────────────────────────────
interface TypewriterProps {
  text: string;
  start: number;
  speed?: number; // frames per character
}
export const Typewriter: React.FC<TypewriterProps> = ({
  text,
  start,
  speed = 2,
}) => {
  const frame = useCurrentFrame();
  const chars = Math.min(
    text.length,
    Math.max(0, Math.floor((frame - start) / speed))
  );
  const visible = text.slice(0, chars);
  const cursorOn = Math.floor(frame / 15) % 2 === 0;

  return (
    <span>
      {visible}
      <span style={{ opacity: cursorOn ? 1 : 0 }}>|</span>
    </span>
  );
};

// ─── ProgressBar ────────────────────────────────
interface ProgressBarProps {
  start: number;
  end: number;
  color?: string;
  height?: number;
}
export const ProgressBar: React.FC<ProgressBarProps> = ({
  start,
  end,
  color = "#6366f1",
  height = 4,
}) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [start, end], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  return (
    <div
      style={{
        width: "100%",
        height,
        background: "rgba(255,255,255,0.1)",
        borderRadius: height / 2,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          width: `${progress}%`,
          height: "100%",
          background: color,
          borderRadius: height / 2,
        }}
      />
    </div>
  );
};

// ─── FloatingOrb ────────────────────────────────
interface FloatingOrbProps {
  x: string;
  y: string;
  size: number;
  color: string;
  speed?: number;
}
export const FloatingOrb: React.FC<FloatingOrbProps> = ({
  x,
  y,
  size,
  color,
  speed = 90,
}) => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: size,
        height: size,
        borderRadius: "50%",
        background: `radial-gradient(circle, ${color} 0%, transparent 70%)`,
        transform: `translate(${Math.sin(frame / speed) * 20}px, ${
          Math.cos(frame / speed) * 20
        }px)`,
      }}
    />
  );
};

// ─── DriftingGrid ───────────────────────────────
interface DriftingGridProps {
  color?: string;
  size?: number;
  speed?: number;
}
export const DriftingGrid: React.FC<DriftingGridProps> = ({
  color = "rgba(99,102,241,0.04)",
  size = 50,
  speed = 0.2,
}) => {
  const frame = useCurrentFrame();
  const drift = frame * speed;
  return (
    <div
      style={{
        position: "absolute",
        inset: -60,
        backgroundImage: `
          linear-gradient(${color} 1px, transparent 1px),
          linear-gradient(90deg, ${color} 1px, transparent 1px)
        `,
        backgroundSize: `${size}px ${size}px`,
        transform: `translate(${drift % size}px, ${(drift * 0.5) % size}px)`,
      }}
    />
  );
};

// ─── StaggerChildren ────────────────────────────
interface StaggerChildrenProps {
  children: React.ReactNode[];
  start: number;
  stagger?: number;
  renderChild: (child: React.ReactNode, style: React.CSSProperties) => React.ReactNode;
}
export const StaggerChildren: React.FC<StaggerChildrenProps> = ({
  children,
  start,
  stagger = 10,
  renderChild,
}) => {
  const frame = useCurrentFrame();
  return (
    <>
      {children.map((child, i) => {
        const childStart = start + i * stagger;
        const op = interpolate(
          frame,
          [childStart, childStart + 15],
          [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );
        const y = interpolate(
          frame,
          [childStart, childStart + 15],
          [20, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );
        return renderChild(child, { opacity: op, transform: `translateY(${y}px)` });
      })}
    </>
  );
};

// ─── CountUp ────────────────────────────────────
interface CountUpProps {
  value: number;
  start: number;
  duration: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
}
export const CountUp: React.FC<CountUpProps> = ({
  value,
  start,
  duration,
  prefix = "",
  suffix = "",
  decimals = 0,
}) => {
  const frame = useCurrentFrame();
  const v = interpolate(frame, [start, start + duration], [0, value], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <span>
      {prefix}
      {v.toFixed(decimals)}
      {suffix}
    </span>
  );
};

// ─── PulseRing ──────────────────────────────────
interface PulseRingProps {
  start: number;
  color?: string;
  size?: number;
}
export const PulseRing: React.FC<PulseRingProps> = ({
  start,
  color = "#6366f1",
  size = 200,
}) => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, Math.max(0, (frame - start) / 60));
  const scale = 1 + progress * 0.5;
  const opacity = 1 - progress;

  return (
    <div
      style={{
        position: "absolute",
        width: size,
        height: size,
        borderRadius: "50%",
        border: `2px solid ${color}`,
        transform: `scale(${scale})`,
        opacity,
      }}
    />
  );
};
