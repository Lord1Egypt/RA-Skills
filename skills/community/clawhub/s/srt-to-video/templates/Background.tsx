import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

function sr(seed: number): number {
  const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
}

// 40 stars
const STARS: { x: number; y: number; s: number; b: number; sp: number; ph: number }[] = [];
for (let i = 0; i < 40; i++) {
  STARS.push({
    x: sr(i * 1.1) * 100, y: sr(i * 2.3) * 100,
    s: 1.5 + sr(i * 3.7) * 2, b: 0.4 + sr(i * 4.1) * 0.6,
    sp: 0.02 + sr(i * 5.3) * 0.05, ph: sr(i * 6.7) * 6.28,
  });
}

// 5 shooting stars
const SHOOTS: { sx: number; sy: number; a: number; spd: number; len: number; trig: number; dur: number; h: number }[] = [];
for (let i = 0; i < 5; i++) {
  SHOOTS.push({
    sx: sr(i * 11) * 100, sy: sr(i * 12) * 30,
    a: 25 + sr(i * 13) * 20, spd: 2 + sr(i * 14) * 2,
    len: 100 + sr(i * 15) * 80, trig: Math.floor(sr(i * 16) * 2700),
    dur: 18 + Math.floor(sr(i * 17) * 12), h: 190 + Math.floor(sr(i * 18) * 40),
  });
}

export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const hShift = Math.sin(frame * 0.002) * 15;
  const angle = frame * 0.03;

  return (
    <div style={{
      position: 'absolute', inset: 0, overflow: 'hidden',
      background: `linear-gradient(${135 + angle}deg, 
        hsl(${220 + hShift}, 50%, 3%) 0%, 
        hsl(${250 + hShift}, 40%, 6%) 40%,
        hsl(${280 + hShift}, 35%, 5%) 100%)`,
    }}>
      {/* Nebula glow 1 */}
      <div style={{
        position: 'absolute',
        left: `${45 + Math.sin(frame * 0.001) * 8}%`,
        top: `${35 + Math.cos(frame * 0.0015) * 5}%`,
        width: '50%', height: '40%',
        borderRadius: '50%',
        background: `radial-gradient(ellipse, hsla(240, 70%, 40%, 0.07) 0%, transparent 65%)`,
        filter: 'blur(50px)',
        transform: 'translate(-50%, -50%)',
      }} />
      {/* Nebula glow 2 */}
      <div style={{
        position: 'absolute',
        left: `${60 + Math.cos(frame * 0.0012) * 6}%`,
        top: `${65 + Math.sin(frame * 0.001) * 5}%`,
        width: '45%', height: '35%',
        borderRadius: '50%',
        background: `radial-gradient(ellipse, hsla(300, 50%, 35%, 0.05) 0%, transparent 65%)`,
        filter: 'blur(50px)',
        transform: 'translate(-50%, -50%)',
      }} />

      {/* Stars */}
      {STARS.map((s, i) => {
        const tw = 0.3 + (Math.sin(frame * s.sp + s.ph) * 0.5 + 0.5) * 0.7;
        const op = s.b * tw;
        return (
          <div key={i} style={{
            position: 'absolute',
            left: `${s.x}%`, top: `${s.y}%`,
            width: s.s, height: s.s,
            borderRadius: '50%',
            backgroundColor: `rgba(220, 235, 255, ${op})`,
            boxShadow: `0 0 ${s.s * 3}px rgba(180, 220, 255, ${op * 0.5})`,
          }} />
        );
      })}

      {/* Shooting stars */}
      {SHOOTS.map((ss, i) => {
        const cycle = 500 + Math.floor(sr(i * 30) * 300);
        const localF = ((frame - ss.trig) % cycle + cycle) % cycle;
        if (localF > ss.dur) return null;
        const p = localF / ss.dur;
        const rad = (ss.a * Math.PI) / 180;
        const d = p * ss.len * ss.spd * 0.3;
        const x = ss.sx + Math.cos(rad) * d;
        const y = ss.sy + Math.sin(rad) * d;
        const op = p < 0.3 ? p / 0.3 : p > 0.7 ? (1 - p) / 0.3 : 1;
        return (
          <div key={`ss${i}`} style={{
            position: 'absolute',
            left: `${x}%`, top: `${y}%`,
            width: ss.len * 0.3, height: 2,
            borderRadius: 1,
            background: `linear-gradient(90deg, hsla(${ss.h}, 90%, 80%, ${op * 0.8}) 0%, transparent 100%)`,
            boxShadow: `0 0 8px hsla(${ss.h}, 90%, 70%, ${op * 0.4})`,
            transform: `rotate(${ss.a}deg)`,
            transformOrigin: '0% 50%',
          }} />
        );
      })}

      {/* Aurora ribbon */}
      <div style={{
        position: 'absolute',
        left: `${25 + Math.sin(frame * 0.003) * 8}%`,
        top: `${45 + Math.sin(frame * 0.004) * 10}%`,
        width: '55%', height: '25%',
        background: `radial-gradient(ellipse, hsla(200, 80%, 50%, ${0.035 + Math.sin(frame * 0.005) * 0.02}) 0%, transparent 70%)`,
        filter: 'blur(60px)',
        transform: `skewX(${Math.sin(frame * 0.002) * 8}deg)`,
      }} />

      {/* Vignette */}
      <div style={{
        position: 'absolute', inset: 0,
        background: 'radial-gradient(ellipse at center, transparent 30%, rgba(0,0,0,0.6) 100%)',
      }} />
    </div>
  );
};
