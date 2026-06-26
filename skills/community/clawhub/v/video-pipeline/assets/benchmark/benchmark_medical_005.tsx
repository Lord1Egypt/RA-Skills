import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

/**
 * Slide005 - 三个关键数字
 * narrationId: summary
 */
export const Slide005: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateRight: 'clamp' });
  const titleY = interpolate(frame, [0, fps * 0.5], [40, 0], { extrapolateRight: 'clamp' });

  // Three numbers staggered
  const n1Op = interpolate(frame, [fps * 0.4, fps * 0.9], [0, 1], { extrapolateRight: 'clamp' });
  const n1Scale = interpolate(frame, [fps * 0.4, fps * 0.9], [0.8, 1], { extrapolateRight: 'clamp' });
  const n2Op = interpolate(frame, [fps * 0.8, fps * 1.3], [0, 1], { extrapolateRight: 'clamp' });
  const n2Scale = interpolate(frame, [fps * 0.8, fps * 1.3], [0.8, 1], { extrapolateRight: 'clamp' });
  const n3Op = interpolate(frame, [fps * 1.2, fps * 1.7], [0, 1], { extrapolateRight: 'clamp' });
  const n3Scale = interpolate(frame, [fps * 1.2, fps * 1.7], [0.8, 1], { extrapolateRight: 'clamp' });

  const conclusionOp = interpolate(frame, [fps * 2.0, fps * 2.5], [0, 1], { extrapolateRight: 'clamp' });

  // Bokeh
  const bokehDrift = interpolate(frame, [0, fps * 4], [0, 25], { extrapolateRight: 'clamp' });

  return (
    <div style={{
      width: 1080, height: 1920, position: 'relative', overflow: 'hidden',
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start',
      paddingTop: 160,
      background: 'linear-gradient(160deg, #0a0a2e 0%, #16213e 50%, #1a1a3e 100%)',
      fontFamily: "'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
    }}>
      {/* Bokeh */}
      <div style={{
        position: 'absolute', width: 300, height: 300, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(34,197,94,0.08) 0%, transparent 70%)',
        left: 100 + bokehDrift, top: 500, filter: 'blur(45px)',
      }} />
      <div style={{
        position: 'absolute', width: 220, height: 220, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%)',
        right: 80, top: 900 - bokehDrift, filter: 'blur(35px)',
      }} />
      <div style={{
        position: 'absolute', width: 260, height: 260, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(251,191,36,0.08) 0%, transparent 70%)',
        left: 300, bottom: 300 + bokehDrift, filter: 'blur(40px)',
      }} />

      {/* Title */}
      <div style={{ opacity, transform: `translateY(${titleY}px)`, textAlign: 'center', marginBottom: 60 }}>
        <div style={{ fontSize: 48, marginBottom: 16 }}>📊</div>
        <div style={{
          fontSize: 52, fontWeight: 800, color: '#ffffff',
          textShadow: '0 4px 20px rgba(0,0,0,0.3)',
        }}>
          三个关键数字
        </div>
        <div style={{ fontSize: 26, color: 'rgba(255,255,255,0.5)', marginTop: 8 }}>
          今天你需要记住的核心结论
        </div>
      </div>

      {/* Three big number cards */}
      <div style={{ padding: '0 60px', width: '100%', boxSizing: 'border-box' }}>
        {/* Number 1 */}
        <div style={{
          opacity: n1Op, transform: `scale(${n1Scale})`,
          background: 'linear-gradient(135deg, rgba(34,197,94,0.15) 0%, rgba(34,197,94,0.05) 100%)',
          border: '2px solid rgba(34,197,94,0.3)',
          borderRadius: 24, padding: '32px 36px', marginBottom: 28,
          display: 'flex', alignItems: 'center', gap: 28,
        }}>
          <div style={{
            minWidth: 100, height: 100, borderRadius: 20,
            background: 'rgba(34,197,94,0.2)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 48,
          }}>
            ①
          </div>
          <div>
            <div style={{
              fontSize: 48, fontWeight: 800, color: '#34d399', lineHeight: 1,
            }}>
              82% → 97%
            </div>
            <div style={{ fontSize: 26, color: 'rgba(255,255,255,0.7)', marginTop: 8 }}>
              AI影像检出率的真实提升
            </div>
          </div>
        </div>

        {/* Number 2 */}
        <div style={{
          opacity: n2Op, transform: `scale(${n2Scale})`,
          background: 'linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(99,102,241,0.05) 100%)',
          border: '2px solid rgba(99,102,241,0.3)',
          borderRadius: 24, padding: '32px 36px', marginBottom: 28,
          display: 'flex', alignItems: 'center', gap: 28,
        }}>
          <div style={{
            minWidth: 100, height: 100, borderRadius: 20,
            background: 'rgba(99,102,241,0.2)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 48,
          }}>
            ②
          </div>
          <div>
            <div style={{
              fontSize: 48, fontWeight: 800, color: '#818cf8', lineHeight: 1,
            }}>
              15分 → 3分
            </div>
            <div style={{ fontSize: 26, color: 'rgba(255,255,255,0.7)', marginTop: 8 }}>
              单例阅片效率提升5倍
            </div>
          </div>
        </div>

        {/* Number 3 */}
        <div style={{
          opacity: n3Op, transform: `scale(${n3Scale})`,
          background: 'linear-gradient(135deg, rgba(251,191,36,0.15) 0%, rgba(251,191,36,0.05) 100%)',
          border: '2px solid rgba(251,191,36,0.3)',
          borderRadius: 24, padding: '32px 36px', marginBottom: 28,
          display: 'flex', alignItems: 'center', gap: 28,
        }}>
          <div style={{
            minWidth: 100, height: 100, borderRadius: 20,
            background: 'rgba(251,191,36,0.2)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 48,
          }}>
            ③
          </div>
          <div>
            <div style={{
              fontSize: 48, fontWeight: 800, color: '#fbbf24', lineHeight: 1,
            }}>
              8% → 0.5%
            </div>
            <div style={{ fontSize: 26, color: 'rgba(255,255,255,0.7)', marginTop: 8 }}>
              漏诊率大幅下降
            </div>
          </div>
        </div>
      </div>

      {/* Conclusion */}
      <div style={{
        opacity: conclusionOp,
        position: 'absolute', bottom: 120, left: 0, right: 0, textAlign: 'center',
        padding: '0 80px',
      }}>
        <div style={{
          background: 'rgba(99,102,241,0.15)',
          border: '1px solid rgba(99,102,241,0.3)',
          borderRadius: 16, padding: '20px 28px',
        }}>
          <div style={{ fontSize: 30, color: '#ffffff', fontWeight: 700 }}>
            👁️ AI不是替代医生
          </div>
          <div style={{ fontSize: 24, color: 'rgba(255,255,255,0.6)', marginTop: 6 }}>
            而是一双不会疲劳的眼睛
          </div>
        </div>
      </div>
    </div>
  );
};
