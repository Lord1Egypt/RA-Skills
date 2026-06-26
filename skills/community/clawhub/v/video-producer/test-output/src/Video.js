import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import React from 'react';
import bgimg0 from '/home/cxp/.openclaw/skills/video-producer/test-output/materials/s00_科技背景.png';
import bgimg1 from '/home/cxp/.openclaw/skills/video-producer/test-output/materials/s01_牛顿.png';
import bgimg2 from '/home/cxp/.openclaw/skills/video-producer/test-output/materials/s01_苹果.png';

const popIn = (frame, delay) => {
  const progress = Math.max(0, Math.min(1, (frame - delay) / 15));
  const scale = 0.5 + progress * 0.5;
  return { scale, opacity: progress };
};

const fadeSlideUp = (frame, delay, duration) => {
  const d = duration || 20;
  const progress = Math.max(0, Math.min(1, (frame - delay) / d));
  return { opacity: progress, translateY: interpolate(progress, [0, 1], [30, 0]) };
};

// Scene0
const Scene0 = () => {
  const frame = useCurrentFrame();
  const f = frame - 0;
  const iconAnim = popIn(f, 0);
  const titleAnim = fadeSlideUp(f, 25);
  const descAnim = fadeSlideUp(f, 50);
  return (
    <>
      <img src={bgimg0} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", opacity: 0.3 }} />
      <AbsoluteFill style={{ width: "100%", height: "100%", backgroundColor: "#0a0a0a", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", fontFamily: "Noto Color Emoji, sans-serif" }}>
        <div style={{ opacity: iconAnim.opacity, transform: "scale(" + iconAnim.scale + ")", fontSize: 160, marginBottom: 40, zIndex: 1 }}>🤖</div>
        <div style={{ opacity: titleAnim.opacity, transform: "translateY(" + titleAnim.translateY + "px)", fontSize: 72, color: '#FFD700', fontWeight: '900', textAlign: 'center', padding: '0 60px', zIndex: 1 }}>牛顿发现苹果</div>
      </AbsoluteFill>
    </>
  );
};

// Scene1
const Scene1 = () => {
  const frame = useCurrentFrame();
  const f = frame - 54;
  const iconAnim = popIn(f, 0);
  const titleAnim = fadeSlideUp(f, 25);
  const descAnim = fadeSlideUp(f, 50);
  return (
    <>
      <img src={bgimg1} style={{ position: "absolute", width: 120, height: 120, objectFit: "contain", opacity: 0.85, right: 30, top: 80 }} />
      <AbsoluteFill style={{ width: "100%", height: "100%", backgroundColor: "#0a0a0a", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", fontFamily: "Noto Color Emoji, sans-serif" }}>
        <div style={{ opacity: iconAnim.opacity, transform: "scale(" + iconAnim.scale + ")", fontSize: 160, marginBottom: 40, zIndex: 1 }}>🍎</div>
        <div style={{ opacity: titleAnim.opacity, transform: "translateY(" + titleAnim.translateY + "px)", fontSize: 56, color: 'white', fontWeight: '900', textAlign: 'center', padding: '0 60px', zIndex: 1 }}>发现苹果</div>
      </AbsoluteFill>
    </>
  );
};

// Scene2
const Scene2 = () => {
  const frame = useCurrentFrame();
  const f = frame - 129;
  const iconAnim = popIn(f, 0);
  const titleAnim = fadeSlideUp(f, 25);
  const descAnim = fadeSlideUp(f, 50);
  return (
    <>
      <AbsoluteFill style={{ width: "100%", height: "100%", backgroundColor: "#0a0a0a", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", fontFamily: "Noto Color Emoji, sans-serif" }}>
        <div style={{ opacity: iconAnim.opacity, transform: "scale(" + iconAnim.scale + ")", fontSize: 160, marginBottom: 40, zIndex: 1 }}>🔧</div>
        <div style={{ opacity: titleAnim.opacity, transform: "translateY(" + titleAnim.translateY + "px)", fontSize: 56, color: 'white', fontWeight: '900', textAlign: 'center', padding: '0 60px', zIndex: 1 }}>牛顿由此发现万有引力定律</div>
        <div style={{ opacity: descAnim.opacity, transform: 'translateY(' + descAnim.translateY + 'px)', fontSize: 36, color: '#9ca3af', marginTop: 30, textAlign: 'center', padding: '0 40px', zIndex: 1 }}>解锁你的第一个AI技能</div>
      </AbsoluteFill>
    </>
  );
};


export const Video = () => {
  const frame = useCurrentFrame();
  if (frame < 54) return <Scene0 />;
  if (frame < 129) return <Scene1 />;
  if (frame < 218) return <Scene2 />;
  return <Scene2 />;
};
