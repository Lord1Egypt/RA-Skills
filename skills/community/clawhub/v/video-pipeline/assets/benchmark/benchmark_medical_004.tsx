import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

/**
 * Slide004 - 不只是看片子那么简单
 * narrationId: slide_02
 */
export const Slide004: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateRight: 'clamp' });
  const titleY = interpolate(frame, [0, fps * 0.5], [40, 0], { extrapolateRight: 'clamp' });

  // Staggered cards
  const card1Op = interpolate(frame, [fps * 0.4, fps * 0.8], [0, 1], { extrapolateRight: 'clamp' });
  const card1Y = interpolate(frame, [fps * 0.4, fps * 0.8], [30, 0], { extrapolateRight: 'clamp' });
  const card2Op = interpolate(frame, [fps * 0.8, fps * 1.2], [0, 1], { extrapolateRight: 'clamp' });
  const card2Y = interpolate(frame, [fps * 0.8, fps * 1.2], [30, 0], { extrapolateRight: 'clamp' });
  const card3Op = interpolate(frame, [fps * 1.2, fps * 1.6], [0, 1], { extrapolateRight: 'clamp' });
  const card3Y = interpolate(frame, [fps * 1.2, fps * 1.6], [30, 0], { extrapolateRight: 'clamp' });

  // Bokeh
  const bokehDrift = interpolate(frame, [0, fps * 5], [0, 35], { extrapolateRight: 'clamp' });

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
        position: 'absolute', width: 250, height: 250, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(168,85,247,0.1) 0%, transparent 70%)',
        left: 50 + bokehDrift, top: 350, filter: 'blur(40px)',
      }} />
      <div style={{
        position: 'absolute', width: 220, height: 220, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(59,130,246,0.1) 0%, transparent 70%)',
        right: 60, bottom: 400 - bokehDrift, filter: 'blur(35px)',
      }} />

      {/* Title */}
      <div style={{ opacity, transform: `translateY(${titleY}px)`, textAlign: 'center', marginBottom: 50 }}>
        <div style={{ fontSize: 48, marginBottom: 16 }}>🧠</div>
        <div style={{
          fontSize: 48, fontWeight: 800, color: '#ffffff',
          textShadow: '0 4px 20px rgba(0,0,0,0.3)',
        }}>
          不只是看片子那么简单
        </div>
        <div style={{ fontSize: 26, color: 'rgba(255,255,255,0.5)', marginTop: 8 }}>
          AI在医疗全链条的渗透
        </div>
      </div>

      {/* Three scenario cards */}
      <div style={{ padding: '0 60px', width: '100%', boxSizing: 'border-box' }}>
        {/* Card 1: 病历书写 */}
        <div style={{
          opacity: card1Op, transform: `translateY(${card1Y}px)`,
          background: 'rgba(168,85,247,0.12)',
          border: '2px solid rgba(168,85,247,0.25)',
          borderRadius: 20, padding: '28px 32px', marginBottom: 24,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 12 }}>
            <span style={{ fontSize: 36 }}>📝</span>
            <span style={{ fontSize: 32, color: '#c084fc', fontWeight: 700 }}>智能病历</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <div style={{
              background: 'rgba(255,255,255,0.08)', borderRadius: 12, padding: '12px 20px',
              flex: 1, textAlign: 'center',
            }}>
              <div style={{ fontSize: 36, fontWeight: 800, color: '#f87171' }}>2-3h</div>
              <div style={{ fontSize: 20, color: 'rgba(255,255,255,0.5)' }}>日均手写时间</div>
            </div>
            <div style={{ fontSize: 32, color: 'rgba(255,255,255,0.4)' }}>→</div>
            <div style={{
              background: 'rgba(255,255,255,0.08)', borderRadius: 12, padding: '12px 20px',
              flex: 1, textAlign: 'center',
            }}>
              <div style={{ fontSize: 36, fontWeight: 800, color: '#34d399' }}>30%</div>
              <div style={{ fontSize: 20, color: 'rgba(255,255,255,0.5)' }}>工作时间占比</div>
            </div>
          </div>
        </div>

        {/* Card 2: 质控覆盖 */}
        <div style={{
          opacity: card2Op, transform: `translateY(${card2Y}px)`,
          background: 'rgba(59,130,246,0.12)',
          border: '2px solid rgba(59,130,246,0.25)',
          borderRadius: 20, padding: '28px 32px', marginBottom: 24,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 12 }}>
            <span style={{ fontSize: 36 }}>🔍</span>
            <span style={{ fontSize: 32, color: '#60a5fa', fontWeight: 700 }}>病历质控</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <div style={{
              background: 'rgba(255,255,255,0.08)', borderRadius: 12, padding: '12px 20px',
              flex: 1, textAlign: 'center',
            }}>
              <div style={{ fontSize: 36, fontWeight: 800, color: '#f87171' }}>10-20%</div>
              <div style={{ fontSize: 20, color: 'rgba(255,255,255,0.5)' }}>人工抽查覆盖率</div>
            </div>
            <div style={{ fontSize: 32, color: 'rgba(255,255,255,0.4)' }}>→</div>
            <div style={{
              background: 'rgba(255,255,255,0.08)', borderRadius: 12, padding: '12px 20px',
              flex: 1, textAlign: 'center',
            }}>
              <div style={{ fontSize: 36, fontWeight: 800, color: '#34d399' }}>100%</div>
              <div style={{ fontSize: 20, color: 'rgba(255,255,255,0.5)' }}>AI全量覆盖</div>
            </div>
          </div>
        </div>

        {/* Card 3: 药物研发 */}
        <div style={{
          opacity: card3Op, transform: `translateY(${card3Y}px)`,
          background: 'rgba(251,191,36,0.12)',
          border: '2px solid rgba(251,191,36,0.25)',
          borderRadius: 20, padding: '28px 32px', marginBottom: 24,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 12 }}>
            <span style={{ fontSize: 36 }}>💊</span>
            <span style={{ fontSize: 32, color: '#fbbf24', fontWeight: 700 }}>药物研发</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <div style={{
              background: 'rgba(255,255,255,0.08)', borderRadius: 12, padding: '12px 20px',
              flex: 1, textAlign: 'center',
            }}>
              <div style={{ fontSize: 36, fontWeight: 800, color: '#f87171' }}>10-15年</div>
              <div style={{ fontSize: 20, color: 'rgba(255,255,255,0.5)' }}>传统研发周期</div>
            </div>
            <div style={{ fontSize: 32, color: 'rgba(255,255,255,0.4)' }}>→</div>
            <div style={{
              background: 'rgba(255,255,255,0.08)', borderRadius: 12, padding: '12px 20px',
              flex: 1, textAlign: 'center',
            }}>
              <div style={{ fontSize: 28, fontWeight: 800, color: '#34d399' }}>&lt;10%</div>
              <div style={{ fontSize: 20, color: 'rgba(255,255,255,0.5)' }}>传统成功率</div>
            </div>
          </div>
          <div style={{
            marginTop: 12, fontSize: 24, color: 'rgba(255,255,255,0.55)', textAlign: 'center',
          }}>
            研发成本：10-20亿美元/款
          </div>
        </div>
      </div>

      {/* Bottom note */}
      <div style={{
        position: 'absolute', bottom: 120, left: 0, right: 0, textAlign: 'center',
        padding: '0 80px',
      }}>
        <div style={{
          fontSize: 26, color: 'rgba(255,255,255,0.6)', fontWeight: 500,
        }}>
          🎯 每个环节都有AI的用武之地
        </div>
      </div>
    </div>
  );
};
