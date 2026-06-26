// Complete Remotion component template for website-to-video
// Copy and customize for each project

import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  AbsoluteFill,
  Sequence,
  Audio,
  staticFile,
} from 'remotion';

// ============ Brand Colors (extract from website) ============
const COLORS = {
  background: '#1a1a2e',
  primary: '#ff6b35',
  secondary: '#2ec4b6',
  text: '#ffffff',
  textMuted: '#999999',
  darkCard: 'rgba(255,255,255,0.06)',
};

// ============ SVG Icons ============
const IconEye = ({ size = 40, color = COLORS.textMuted }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" />
  </svg>
);

const IconRocket = ({ size = 40, color = COLORS.primary }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" />
    <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" />
  </svg>
);

const IconBook = ({ size = 40, color = COLORS.primary }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" /><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
  </svg>
);

const IconTarget = ({ size = 40, color = COLORS.primary }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" />
  </svg>
);

const IconWrench = ({ size = 40, color = COLORS.primary }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
  </svg>
);

const IconArrow = ({ size = 40, color = COLORS.primary }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" />
  </svg>
);

// ============ Background & Deco ============
const TechBackground = () => {
  const frame = useCurrentFrame();
  const gridOffset = (frame * 0.5) % 60;
  return (
    <AbsoluteFill style={{ background: COLORS.background }}>
      <div style={{
        position: 'absolute', inset: 0,
        backgroundImage: `linear-gradient(${COLORS.primary}06 1px, transparent 1px), linear-gradient(90deg, ${COLORS.primary}06 1px, transparent 1px)`,
        backgroundSize: '60px 60px',
        backgroundPosition: `${gridOffset}px ${gridOffset}px`,
        opacity: 0.4,
      }} />
      <div style={{
        position: 'absolute', top: '-30%', left: '-30%', width: '160%', height: '160%',
        background: `radial-gradient(circle at 25% 25%, ${COLORS.primary}10 0%, transparent 40%), radial-gradient(circle at 75% 75%, ${COLORS.secondary}08 0%, transparent 40%)`,
      }} />
    </AbsoluteFill>
  );
};

// ============ Subtitle ============
const Subtitle = ({ text, active }: { text: string; active: boolean }) => {
  const frame = useCurrentFrame();
  const opacity = active
    ? interpolate(frame, [0, 8], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
    : interpolate(frame, [0, 8], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <div style={{ position: 'absolute', bottom: 8, left: 0, right: 0, textAlign: 'center', opacity, zIndex: 100 }}>
      <div style={{ display: 'inline-block', padding: '6px 20px', background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(8px)', borderRadius: 8, border: `1px solid ${COLORS.primary}25` }}>
        <span style={{ fontSize: 22, color: COLORS.text, fontFamily: 'system-ui, sans-serif' }}>{text}</span>
      </div>
    </div>
  );
};

// ============ Scenes (customize content) ============
const Scene1 = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logoScale = spring({ frame, fps, config: { damping: 12, stiffness: 100 } });
  const taglineOpacity = interpolate(frame, [30, 60], [0, 1]);
  const glowPulse = Math.sin(frame * 0.1) * 0.3 + 0.7;

  return (
    <AbsoluteFill>
      <TechBackground />
      <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', paddingBottom: 80 }}>
        <div style={{ position: 'absolute', width: 280, height: 280, borderRadius: '50%', background: `radial-gradient(circle, ${COLORS.primary}${Math.floor(glowPulse * 30).toString(16).padStart(2, '0')} 0%, transparent 70%)`, transform: `scale(${logoScale})` }} />
        <div style={{ fontSize: 84, fontWeight: 'bold', color: COLORS.text, transform: `scale(${interpolate(logoScale, [0, 1], [0.5, 1])})`, textShadow: `0 0 ${40 * glowPulse}px ${COLORS.primary}80`, letterSpacing: 4, marginBottom: 24 }}>BRAND</div>
        <div style={{ fontSize: 36, color: COLORS.primary, opacity: taglineOpacity, fontWeight: 300, marginBottom: 12 }}>Tagline Here</div>
        <div style={{ fontSize: 22, color: COLORS.textMuted, opacity: taglineOpacity }}>Subtitle description</div>
      </div>
      <Subtitle text="Narration text for scene 1." active={frame > 20} />
    </AbsoluteFill>
  );
};

// Scene2, Scene3, Scene4, Scene5 follow same pattern...
// See SKILL.md for full structure

// ============ Main ============
export const Promo = () => {
  return (
    <AbsoluteFill>
      <Audio src={staticFile('bgm.mp3')} volume={0.15} />
      <Audio src={staticFile('narration.mp3')} volume={0.9} />
      <Sequence from={0} durationInFrames={288}><Scene1 /></Sequence>
      {/* Add Scene2-5 */}
    </AbsoluteFill>
  );
};
