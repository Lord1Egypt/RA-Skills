import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

/**
 * Slide001 - AI+医疗：一场正在发生的革命
 * narrationId: cover
 */
export const Slide001: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps * 0.5], [0, 1], { extrapolateRight: 'clamp' });
  const titleY = interpolate(frame, [0, fps * 0.8], [60, 0], { extrapolateRight: 'clamp' });
  const subtitleOpacity = interpolate(frame, [fps * 0.3, fps * 0.8], [0, 1], { extrapolateRight: 'clamp' });
  const pulseScale = interpolate(frame, [0, fps * 2], [1, 1.08], { extrapolateRight: 'clamp' });

  // Bokeh animation
  const bokeh1X = interpolate(frame, [0, fps * 3], [100, 180], { extrapolateRight: 'clamp' });
  const bokeh2X = interpolate(frame, [0, fps * 3], [800, 720], { extrapolateRight: 'clamp' });
  const bokeh3Y = interpolate(frame, [0, fps * 3], [1400, 1300], { extrapolateRight: 'clamp' });

  return (
    <div style={{
      width: 1080, height: 1920, position: 'relative', overflow: 'hidden',
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(160deg, #0f0c29 0%, #1a1145 30%, #302b63 60%, #24243e 100%)',
      fontFamily: "'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
    }}>
      {/* Bokeh decorations */}
      <div style={{
        position: 'absolute', width: 280, height: 280, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%)',
        left: bokeh1X, top: 200, filter: 'blur(40px)',
      }} />
      <div style={{
        position: 'absolute', width: 200, height: 200, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%)',
        left: bokeh2X, top: 600, filter: 'blur(30px)',
      }} />
      <div style={{
        position: 'absolute', width: 320, height: 320, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(59,130,246,0.1) 0%, transparent 70%)',
        left: 400, top: bokeh3Y, filter: 'blur(50px)',
      }} />

      {/* Main content */}
      <div style={{ opacity, transform: `translateY(${titleY}px) scale(${pulseScale})`, textAlign: 'center' }}>
        {/* Emoji decoration */}
        <div style={{ fontSize: 80, marginBottom: 30 }}>🏥</div>
        
        <div style={{
          fontSize: 64, fontWeight: 800, color: '#ffffff',
          textAlign: 'center', lineHeight: 1.2, padding: '0 60px',
          textShadow: '0 4px 30px rgba(99,102,241,0.5)',
        }}>
          AI+医疗
        </div>
        <div style={{
          fontSize: 44, fontWeight: 600, color: '#818cf8',
          marginTop: 16, textAlign: 'center',
          textShadow: '0 2px 15px rgba(99,102,241,0.3)',
        }}>
          一场正在发生的革命
        </div>
      </div>

      {/* Subtitle area */}
      <div style={{
        opacity: subtitleOpacity, marginTop: 60, textAlign: 'center',
      }}>
        <div style={{
          fontSize: 28, color: 'rgba(255,255,255,0.5)', marginBottom: 20,
          letterSpacing: 4,
        }}>
          ━━━━━━━━━━━━
        </div>
        <div style={{
          fontSize: 32, color: 'rgba(255,255,255,0.7)', fontWeight: 500,
        }}>
          智慧健康研究院 · 张博士
        </div>
        <div style={{
          fontSize: 26, color: 'rgba(255,255,255,0.4)', marginTop: 12,
        }}>
          3分钟 · 用数据说话
        </div>
      </div>

      {/* Bottom decoration line */}
      <div style={{
        position: 'absolute', bottom: 100, left: '50%', transform: 'translateX(-50%)',
        width: 200, height: 3,
        background: 'linear-gradient(90deg, transparent, rgba(99,102,241,0.6), transparent)',
      }} />
    </div>
  );
};
