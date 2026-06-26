import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

/**
 * Slide007 - 总结与展望
 * narrationId: summary
 */
export const Slide007: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps * 0.5], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const titleY = interpolate(frame, [0, fps * 0.5], [40, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        position: 'relative',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(160deg, #0a0a2e 0%, #16213e 50%, #1a1a3e 100%)',
        fontFamily: "'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
      }}
    >
      <div style={{ opacity, transform: `translateY(${titleY}px)` }}>
        <div style={{
          fontSize: 56, fontWeight: 800, color: '#ffffff',
          textAlign: 'center', lineHeight: 1.3, padding: '0 60px',
          textShadow: '0 4px 20px rgba(0,0,0,0.3)',
        }}>
          总结与展望
        </div>
        <div style={{
          marginTop: 60, 
          padding: '0 80px', 
          fontSize: 36, 
          color: 'rgba(255,255,255,0.85)', 
          lineHeight: 1.8,
          maxWidth: 900,
        }}>
          <div style={{
            margin: '24px 0', 
            paddingLeft: 40, 
            borderLeft: '6px solid rgba(99,102,241,0.5)',
            position: 'relative',
            background: 'rgba(255, 255, 255, 0.05)',
            borderRadius: 12,
            padding: '20px 20px 20px 50px',
          }}>
            <div style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', color: '#6366f1', fontSize: 32 }}>•</div>
            影像诊断、临床决策、健康管理三大方向
          </div>
          <div style={{
            margin: '24px 0', 
            paddingLeft: 40, 
            borderLeft: '6px solid rgba(99,102,241,0.5)',
            position: 'relative',
            background: 'rgba(255, 255, 255, 0.05)',
            borderRadius: 12,
            padding: '20px 20px 20px 50px',
          }}>
            <div style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', color: '#6366f1', fontSize: 32 }}>•</div>
            重塑整个医疗生态
          </div>
          <div style={{
            background: 'rgba(99,102,241,0.15)',
            border: '2px solid rgba(99,102,241,0.3)',
            borderRadius: 16,
            padding: 20,
            marginBottom: 20,
            textAlign: 'center',
          }}>
            <div style={{
              fontSize: 64,
              fontWeight: 800,
              color: '#818cf8',
              lineHeight: 1,
            }}>
              千亿
            </div>
            <div style={{
              fontSize: 28,
              color: 'rgba(255,255,255,0.7)',
              marginTop: 10,
            }}>
              未来5年市场规模
            </div>
          </div>
          <div style={{
            margin: '24px 0', 
            paddingLeft: 40, 
            borderLeft: '6px solid rgba(99,102,241,0.5)',
            position: 'relative',
            background: 'rgba(255, 255, 255, 0.05)',
            borderRadius: 12,
            padding: '20px 20px 20px 50px',
          }}>
            <div style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', color: '#6366f1', fontSize: 32 }}>•</div>
            巨大商业机会等待发掘
          </div>
          <div style={{
            margin: '24px 0', 
            paddingLeft: 40, 
            borderLeft: '6px solid rgba(99,102,241,0.5)',
            position: 'relative',
            background: 'rgba(255, 255, 255, 0.05)',
            borderRadius: 12,
            padding: '20px 20px 20px 50px',
          }}>
            <div style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', color: '#6366f1', fontSize: 32 }}>•</div>
            下期：AI药物研发的革命性进展
          </div>
        </div>
      </div>
    </div>
  );
};