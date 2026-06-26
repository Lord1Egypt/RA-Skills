import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

/**
 * Slide001 - 医疗健康行业AI应用解析
 * narrationId: cover
 */
export const Slide001: React.FC = () => {
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
        background: 'linear-gradient(160deg, #0f0c29 0%, #1a1145 30%, #302b63 60%, #24243e 100%)',
        fontFamily: "'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
      }}
    >
      <div style={{ opacity, transform: `translateY(${titleY}px)` }}>
        <div style={{
          fontSize: 56, fontWeight: 800, color: '#ffffff',
          textAlign: 'center', lineHeight: 1.3, padding: '0 60px',
          textShadow: '0 4px 20px rgba(0,0,0,0.3)',
        }}>
          医疗健康行业AI应用解析
        </div>
        <div style={{
          fontSize: 32, 
          color: 'rgba(255,255,255,0.6)', 
          marginTop: 24,
        }}>
          AI驱动的医疗变革
        </div>
      </div>
    </div>
  );
};