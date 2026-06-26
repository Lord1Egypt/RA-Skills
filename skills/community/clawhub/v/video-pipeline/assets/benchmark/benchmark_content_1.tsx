import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

/**
 * Slide003 - AI影像诊断：从82%到97%
 * narrationId: slide_01
 */
export const Slide003: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateRight: 'clamp' });
  const titleY = interpolate(frame, [0, fps * 0.5], [40, 0], { extrapolateRight: 'clamp' });

  // Progress bar animations
  const beforeWidth = interpolate(frame, [fps * 0.5, fps * 1.2], [0, 82], { extrapolateRight: 'clamp' });
  const afterWidth = interpolate(frame, [fps * 1.0, fps * 1.7], [0, 97], { extrapolateRight: 'clamp' });

  // Staggered items
  const item1Op = interpolate(frame, [fps * 1.5, fps * 1.9], [0, 1], { extrapolateRight: 'clamp' });
  const item2Op = interpolate(frame, [fps * 1.8, fps * 2.2], [0, 1], { extrapolateRight: 'clamp' });
  const item3Op = interpolate(frame, [fps * 2.1, fps * 2.5], [0, 1], { extrapolateRight: 'clamp' });

  // Bokeh
  const bokehDrift = interpolate(frame, [0, fps * 5], [0, 40], { extrapolateRight: 'clamp' });

  return (
    <div style={{
      width: 1080, height: 1920, position: 'relative', overflow: 'hidden',
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start',
      paddingTop: 160,
      background: 'linear-gradient(160deg, #0a0a2e 0%, #0d1b2a 50%, #1a1a3e 100%)',
      fontFamily: "'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
    }}>
      {/* Bokeh */}
      <div style={{
        position: 'absolute', width: 260, height: 260, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(34,197,94,0.1) 0%, transparent 70%)',
        left: 60 + bokehDrift, top: 400, filter: 'blur(35px)',
      }} />
      <div style={{
        position: 'absolute', width: 200, height: 200, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%)',
        right: 100, top: 800 - bokehDrift, filter: 'blur(30px)',
      }} />

      {/* Title */}
      <div style={{ opacity, transform: `translateY(${titleY}px)`, textAlign: 'center', marginBottom: 40 }}>
        <div style={{ fontSize: 48, marginBottom: 16 }}>🔬</div>
        <div style={{
          fontSize: 48, fontWeight: 800, color: '#ffffff',
          textShadow: '0 4px 20px rgba(0,0,0,0.3)',
        }}>
          AI影像诊断实战数据
        </div>
        <div style={{ fontSize: 26, color: 'rgba(255,255,255,0.5)', marginTop: 8 }}>
          上海中山医院 · 肺结节AI检测试点
        </div>
      </div>

      {/* Comparison bars */}
      <div style={{ padding: '0 60px', width: '100%', boxSizing: 'border-box', marginBottom: 40 }}>
        {/* Before AI */}
        <div style={{ marginBottom: 32 }}>
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            marginBottom: 10,
          }}>
            <span style={{ fontSize: 28, color: 'rgba(255,255,255,0.7)', fontWeight: 600 }}>
              👨‍⚕️ 人工阅片检出率
            </span>
            <span style={{ fontSize: 32, color: '#f87171', fontWeight: 800 }}>
              {Math.round(beforeWidth)}%
            </span>
          </div>
          <div style={{
            width: '100%', height: 32, borderRadius: 16,
            background: 'rgba(255,255,255,0.08)',
            overflow: 'hidden',
          }}>
            <div style={{
              width: `${beforeWidth}%`, height: '100%', borderRadius: 16,
              background: 'linear-gradient(90deg, #ef4444, #f87171)',
              transition: 'width 0.1s',
            }} />
          </div>
        </div>

        {/* After AI */}
        <div style={{ marginBottom: 16 }}>
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            marginBottom: 10,
          }}>
            <span style={{ fontSize: 28, color: 'rgba(255,255,255,0.7)', fontWeight: 600 }}>
              🤖 AI辅助检出率
            </span>
            <span style={{ fontSize: 32, color: '#34d399', fontWeight: 800 }}>
              {Math.round(afterWidth)}%
            </span>
          </div>
          <div style={{
            width: '100%', height: 32, borderRadius: 16,
            background: 'rgba(255,255,255,0.08)',
            overflow: 'hidden',
          }}>
            <div style={{
              width: `${afterWidth}%`, height: '100%', borderRadius: 16,
              background: 'linear-gradient(90deg, #059669, #34d399)',
            }} />
          </div>
        </div>
      </div>

      {/* Key metrics cards */}
      <div style={{
        padding: '0 60px', width: '100%', boxSizing: 'border-box',
        display: 'flex', gap: 20, justifyContent: 'center',
      }}>
        {/* Metric 1 */}
        <div style={{
          opacity: item1Op, flex: 1,
          background: 'rgba(34,197,94,0.12)',
          border: '2px solid rgba(34,197,94,0.25)',
          borderRadius: 20, padding: '24px 16px', textAlign: 'center',
        }}>
          <div style={{ fontSize: 44, fontWeight: 800, color: '#34d399', lineHeight: 1 }}>5x</div>
          <div style={{ fontSize: 22, color: 'rgba(255,255,255,0.6)', marginTop: 8 }}>效率提升</div>
          <div style={{ fontSize: 18, color: 'rgba(255,255,255,0.4)', marginTop: 4 }}>15分→3分</div>
        </div>
        {/* Metric 2 */}
        <div style={{
          opacity: item2Op, flex: 1,
          background: 'rgba(99,102,241,0.12)',
          border: '2px solid rgba(99,102,241,0.25)',
          borderRadius: 20, padding: '24px 16px', textAlign: 'center',
        }}>
          <div style={{ fontSize: 44, fontWeight: 800, color: '#818cf8', lineHeight: 1 }}>0.5%</div>
          <div style={{ fontSize: 22, color: 'rgba(255,255,255,0.6)', marginTop: 8 }}>漏诊率</div>
          <div style={{ fontSize: 18, color: 'rgba(255,255,255,0.4)', marginTop: 4 }}>原8%→0.5%</div>
        </div>
        {/* Metric 3 */}
        <div style={{
          opacity: item3Op, flex: 1,
          background: 'rgba(251,191,36,0.12)',
          border: '2px solid rgba(251,191,36,0.25)',
          borderRadius: 20, padding: '24px 16px', textAlign: 'center',
        }}>
          <div style={{ fontSize: 44, fontWeight: 800, color: '#fbbf24', lineHeight: 1 }}>10万+</div>
          <div style={{ fontSize: 22, color: 'rgba(255,255,255,0.6)', marginTop: 8 }}>训练数据</div>
          <div style={{ fontSize: 18, color: 'rgba(255,255,255,0.4)', marginTop: 4 }}>标注CT影像</div>
        </div>
      </div>

      {/* Bottom highlight */}
      <div style={{
        position: 'absolute', bottom: 120, left: 0, right: 0, textAlign: 'center',
        padding: '0 80px',
      }}>
        <div style={{
          background: 'rgba(34,197,94,0.15)',
          border: '1px solid rgba(34,197,94,0.3)',
          borderRadius: 16, padding: '16px 24px',
          fontSize: 28, color: 'rgba(255,255,255,0.85)', fontWeight: 600,
        }}>
          ✅ 医生满意度提升60% — 真正的人机协作
        </div>
      </div>
    </div>
  );
};