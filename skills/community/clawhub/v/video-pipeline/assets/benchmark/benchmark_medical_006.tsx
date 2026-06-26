import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

/**
 * Slide006 - 这跟你有什么关系？
 * narrationId: action
 */
export const Slide006: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateRight: 'clamp' });
  const titleY = interpolate(frame, [0, fps * 0.5], [40, 0], { extrapolateRight: 'clamp' });

  // Staggered items
  const item1Op = interpolate(frame, [fps * 0.4, fps * 0.8], [0, 1], { extrapolateRight: 'clamp' });
  const item1X = interpolate(frame, [fps * 0.4, fps * 0.8], [-40, 0], { extrapolateRight: 'clamp' });
  const item2Op = interpolate(frame, [fps * 0.8, fps * 1.2], [0, 1], { extrapolateRight: 'clamp' });
  const item2X = interpolate(frame, [fps * 0.8, fps * 1.2], [-40, 0], { extrapolateRight: 'clamp' });
  const item3Op = interpolate(frame, [fps * 1.2, fps * 1.6], [0, 1], { extrapolateRight: 'clamp' });
  const item3X = interpolate(frame, [fps * 1.2, fps * 1.6], [-40, 0], { extrapolateRight: 'clamp' });

  const ctaOp = interpolate(frame, [fps * 2.0, fps * 2.5], [0, 1], { extrapolateRight: 'clamp' });
  const ctaScale = interpolate(frame, [fps * 2.0, fps * 2.5], [0.9, 1], { extrapolateRight: 'clamp' });

  // Bokeh
  const bokehDrift = interpolate(frame, [0, fps * 5], [0, 30], { extrapolateRight: 'clamp' });

  return (
    <div style={{
      width: 1080, height: 1920, position: 'relative', overflow: 'hidden',
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start',
      paddingTop: 160,
      background: 'linear-gradient(160deg, #0f0c29 0%, #1a1145 30%, #302b63 60%, #24243e 100%)',
      fontFamily: "'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
    }}>
      {/* Bokeh */}
      <div style={{
        position: 'absolute', width: 280, height: 280, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%)',
        left: 80 + bokehDrift, top: 400, filter: 'blur(40px)',
      }} />
      <div style={{
        position: 'absolute', width: 240, height: 240, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(59,130,246,0.1) 0%, transparent 70%)',
        right: 60 - bokehDrift, top: 1000, filter: 'blur(35px)',
      }} />
      <div style={{
        position: 'absolute', width: 200, height: 200, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(34,197,94,0.08) 0%, transparent 70%)',
        left: 400, bottom: 200 + bokehDrift, filter: 'blur(30px)',
      }} />

      {/* Title */}
      <div style={{ opacity, transform: `translateY(${titleY}px)`, textAlign: 'center', marginBottom: 50 }}>
        <div style={{ fontSize: 48, marginBottom: 16 }}>🤔</div>
        <div style={{
          fontSize: 52, fontWeight: 800, color: '#ffffff',
          textShadow: '0 4px 20px rgba(0,0,0,0.3)',
        }}>
          这跟你有什么关系？
        </div>
      </div>

      {/* Three audience segments */}
      <div style={{ padding: '0 60px', width: '100%', boxSizing: 'border-box' }}>
        {/* Segment 1: 医疗从业者 */}
        <div style={{
          opacity: item1Op, transform: `translateX(${item1X}px)`,
          background: 'rgba(139,92,246,0.12)',
          border: '2px solid rgba(139,92,246,0.25)',
          borderRadius: 20, padding: '28px 32px', marginBottom: 24,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 12 }}>
            <div style={{
              width: 56, height: 56, borderRadius: 14,
              background: 'rgba(139,92,246,0.25)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 30,
            }}>
              👨‍⚕️
            </div>
            <span style={{ fontSize: 32, color: '#c084fc', fontWeight: 700 }}>医疗从业者</span>
          </div>
          <div style={{ fontSize: 28, color: 'rgba(255,255,255,0.8)', lineHeight: 1.6 }}>
            现在就该了解AI辅助诊断工具，<span style={{ color: '#c084fc', fontWeight: 700 }}>别等同行都用上了你还在手动翻片子</span>
          </div>
        </div>

        {/* Segment 2: 技术从业者 */}
        <div style={{
          opacity: item2Op, transform: `translateX(${item2X}px)`,
          background: 'rgba(59,130,246,0.12)',
          border: '2px solid rgba(59,130,246,0.25)',
          borderRadius: 20, padding: '28px 32px', marginBottom: 24,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 12 }}>
            <div style={{
              width: 56, height: 56, borderRadius: 14,
              background: 'rgba(59,130,246,0.25)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 30,
            }}>
              💻
            </div>
            <span style={{ fontSize: 32, color: '#60a5fa', fontWeight: 700 }}>技术从业者</span>
          </div>
          <div style={{ fontSize: 28, color: 'rgba(255,255,255,0.8)', lineHeight: 1.6 }}>
            医疗AI是最大蓝海市场之一
          </div>
          <div style={{
            marginTop: 12,
            background: 'rgba(34,197,94,0.15)',
            border: '1px solid rgba(34,197,94,0.3)',
            borderRadius: 12, padding: '10px 16px',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 12,
          }}>
            <span style={{ fontSize: 36, fontWeight: 800, color: '#34d399' }}>127%</span>
            <span style={{ fontSize: 22, color: 'rgba(255,255,255,0.6)' }}>三年期投资回报率</span>
          </div>
        </div>

        {/* Segment 3: 普通人 */}
        <div style={{
          opacity: item3Op, transform: `translateX(${item3X}px)`,
          background: 'rgba(251,191,36,0.12)',
          border: '2px solid rgba(251,191,36,0.25)',
          borderRadius: 20, padding: '28px 32px', marginBottom: 24,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 12 }}>
            <div style={{
              width: 56, height: 56, borderRadius: 14,
              background: 'rgba(251,191,36,0.25)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 30,
            }}>
              🙋
            </div>
            <span style={{ fontSize: 32, color: '#fbbf24', fontWeight: 700 }}>普通人</span>
          </div>
          <div style={{ fontSize: 28, color: 'rgba(255,255,255,0.8)', lineHeight: 1.6 }}>
            下次体检时问一句：<span style={{ color: '#fbbf24', fontWeight: 700 }}>"片子有没有过AI筛查？"</span>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div style={{
        opacity: ctaOp, transform: `scale(${ctaScale})`,
        position: 'absolute', bottom: 120, left: 0, right: 0, textAlign: 'center',
        padding: '0 80px',
      }}>
        <div style={{
          background: 'linear-gradient(135deg, rgba(99,102,241,0.25) 0%, rgba(139,92,246,0.2) 100%)',
          border: '2px solid rgba(99,102,241,0.4)',
          borderRadius: 20, padding: '20px 28px',
        }}>
          <div style={{ fontSize: 30, color: '#ffffff', fontWeight: 700 }}>
            👉 关注我
          </div>
          <div style={{ fontSize: 24, color: 'rgba(255,255,255,0.6)', marginTop: 6 }}>
            下期：AI在药物研发里的颠覆性应用
          </div>
        </div>
      </div>
    </div>
  );
};
