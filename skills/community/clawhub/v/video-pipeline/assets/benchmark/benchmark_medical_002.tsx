import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

/**
 * Slide002 - 影像科的真实困境
 * narrationId: hook
 */
export const Slide002: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateRight: 'clamp' });
  const titleY = interpolate(frame, [0, fps * 0.5], [40, 0], { extrapolateRight: 'clamp' });

  // Staggered card animations
  const card1Op = interpolate(frame, [fps * 0.3, fps * 0.7], [0, 1], { extrapolateRight: 'clamp' });
  const card1Y = interpolate(frame, [fps * 0.3, fps * 0.7], [30, 0], { extrapolateRight: 'clamp' });
  const card2Op = interpolate(frame, [fps * 0.6, fps * 1.0], [0, 1], { extrapolateRight: 'clamp' });
  const card2Y = interpolate(frame, [fps * 0.6, fps * 1.0], [30, 0], { extrapolateRight: 'clamp' });
  const card3Op = interpolate(frame, [fps * 0.9, fps * 1.3], [0, 1], { extrapolateRight: 'clamp' });
  const card3Y = interpolate(frame, [fps * 0.9, fps * 1.3], [30, 0], { extrapolateRight: 'clamp' });

  // Bokeh
  const bokehDrift = interpolate(frame, [0, fps * 4], [0, 30], { extrapolateRight: 'clamp' });

  return (
    <div style={{
      width: 1080, height: 1920, position: 'relative', overflow: 'hidden',
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start',
      paddingTop: 180,
      background: 'linear-gradient(160deg, #0a0a2e 0%, #16213e 50%, #1a1a3e 100%)',
      fontFamily: "'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
    }}>
      {/* Bokeh circles */}
      <div style={{
        position: 'absolute', width: 240, height: 240, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(239,68,68,0.1) 0%, transparent 70%)',
        right: 80 + bokehDrift, top: 300, filter: 'blur(35px)',
      }} />
      <div style={{
        position: 'absolute', width: 180, height: 180, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%)',
        left: 60, top: 900 - bokehDrift, filter: 'blur(30px)',
      }} />
      <div style={{
        position: 'absolute', width: 300, height: 300, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(251,191,36,0.08) 0%, transparent 70%)',
        left: 400, bottom: 200 + bokehDrift, filter: 'blur(45px)',
      }} />

      {/* Title */}
      <div style={{ opacity, transform: `translateY(${titleY}px)`, textAlign: 'center', marginBottom: 50 }}>
        <div style={{ fontSize: 48, marginBottom: 16 }}>😰</div>
        <div style={{
          fontSize: 52, fontWeight: 800, color: '#ffffff',
          textShadow: '0 4px 20px rgba(0,0,0,0.3)',
        }}>
          影像科的真实困境
        </div>
        <div style={{ fontSize: 26, color: 'rgba(255,255,255,0.5)', marginTop: 8 }}>
          数据来源：《中国医师杂志》
        </div>
      </div>

      {/* Data highlight cards */}
      <div style={{ padding: '0 60px', width: '100%', boxSizing: 'border-box' }}>
        {/* Card 1: 日均阅片量 */}
        <div style={{
          opacity: card1Op, transform: `translateY(${card1Y}px)`,
          background: 'rgba(239,68,68,0.12)',
          border: '2px solid rgba(239,68,68,0.25)',
          borderRadius: 20, padding: '28px 32px', marginBottom: 24,
          display: 'flex', alignItems: 'center', gap: 24,
        }}>
          <div style={{ minWidth: 160, textAlign: 'center' }}>
            <div style={{ fontSize: 56, fontWeight: 800, color: '#f87171', lineHeight: 1 }}>
              300-500
            </div>
            <div style={{ fontSize: 22, color: 'rgba(255,255,255,0.6)', marginTop: 6 }}>
              张/天
            </div>
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 30, color: '#ffffff', fontWeight: 600 }}>
              影像科医生日均阅片量
            </div>
            <div style={{ fontSize: 24, color: 'rgba(255,255,255,0.55)', marginTop: 6 }}>
              连续工作8小时+，疲劳出错率↑25%
            </div>
          </div>
        </div>

        {/* Card 2: 误诊率 */}
        <div style={{
          opacity: card2Op, transform: `translateY(${card2Y}px)`,
          background: 'rgba(251,191,36,0.12)',
          border: '2px solid rgba(251,191,36,0.25)',
          borderRadius: 20, padding: '28px 32px', marginBottom: 24,
          display: 'flex', alignItems: 'center', gap: 24,
        }}>
          <div style={{ minWidth: 160, textAlign: 'center' }}>
            <div style={{ fontSize: 56, fontWeight: 800, color: '#fbbf24', lineHeight: 1 }}>
              10-20%
            </div>
            <div style={{ fontSize: 22, color: 'rgba(255,255,255,0.6)', marginTop: 6 }}>
              误诊率
            </div>
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 30, color: '#ffffff', fontWeight: 600 }}>
              国内医疗机构平均误诊率
            </div>
            <div style={{ fontSize: 24, color: 'rgba(255,255,255,0.55)', marginTop: 6 }}>
              影像科漏诊率 5%-15%
            </div>
          </div>
        </div>

        {/* Card 3: 医生缺口 */}
        <div style={{
          opacity: card3Op, transform: `translateY(${card3Y}px)`,
          background: 'rgba(99,102,241,0.12)',
          border: '2px solid rgba(99,102,241,0.25)',
          borderRadius: 20, padding: '28px 32px', marginBottom: 24,
          display: 'flex', alignItems: 'center', gap: 24,
        }}>
          <div style={{ minWidth: 160, textAlign: 'center' }}>
            <div style={{ fontSize: 56, fontWeight: 800, color: '#818cf8', lineHeight: 1 }}>
              ~5万
            </div>
            <div style={{ fontSize: 22, color: 'rgba(255,255,255,0.6)', marginTop: 6 }}>
              人
            </div>
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 30, color: '#ffffff', fontWeight: 600 }}>
              全国影像科医生缺口
            </div>
            <div style={{ fontSize: 24, color: 'rgba(255,255,255,0.55)', marginTop: 6 }}>
              基层医院诊断能力严重不足
            </div>
          </div>
        </div>
      </div>

      {/* Bottom emphasis */}
      <div style={{
        position: 'absolute', bottom: 120, left: 0, right: 0, textAlign: 'center',
        padding: '0 80px',
      }}>
        <div style={{
          background: 'rgba(239,68,68,0.15)',
          border: '1px solid rgba(239,68,68,0.3)',
          borderRadius: 16, padding: '16px 24px',
          fontSize: 28, color: 'rgba(255,255,255,0.8)', fontWeight: 600,
        }}>
          ⚠️ 医生不够用 + 看不过来 = 患者被耽误
        </div>
      </div>
    </div>
  );
};
