import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring, AbsoluteFill } from "remotion";

/** Apple风格渐变背景 */
export const AppleBg: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{
    background: "linear-gradient(135deg, #0a0a0f 0%, #111118 50%, #0d1a2d 100%)",
  }}>
    {children}
  </AbsoluteFill>
);

/** 主标题：大字，fade-up动画 */
export const HeroTitle: React.FC<{ text: string; startFrame: number; size?: number; color?: string }> = ({
  text, startFrame, size = 80, color = "#FFFFFF"
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 14], [0, 1], { extrapolateRight: "clamp" });
  const translateY = interpolate(frame, [startFrame, startFrame + 14], [40, 0], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      transform: `translateY(${translateY}px)`,
      fontSize: size,
      fontWeight: 800,
      color,
      fontFamily: "Inter, -apple-system, sans-serif",
      letterSpacing: "-0.035em",
      lineHeight: 1.05,
      textAlign: "center",
      padding: "0 80px",
    }}>
      {text}
    </div>
  );
};

/** 场景标签 */
export const SceneTag: React.FC<{ text: string; startFrame: number; color?: string }> = ({
  text, startFrame, color = "#0A84FF"
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 8], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      position: "absolute",
      top: 56,
      left: 60,
      display: "flex",
      alignItems: "center",
      gap: 10,
    }}>
      <div style={{
        width: 8,
        height: 8,
        borderRadius: "50%",
        backgroundColor: color,
        boxShadow: `0 0 12px ${color}`,
      }} />
      <div style={{
        fontSize: 13,
        fontWeight: 600,
        color: "#8E8E93",
        letterSpacing: "0.12em",
        textTransform: "uppercase",
        fontFamily: "Inter, -apple-system, sans-serif",
      }}>
        {text}
      </div>
    </div>
  );
};

/** 层次栈 */
export const LayerStack: React.FC<{
  layers: { label: string; sub: string; color: string }[];
  startFrame: number;
}> = ({ layers, startFrame }) => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 14 }}>
    {layers.map((layer, i) => {
      const frame = useCurrentFrame();
      const delay = startFrame + i * 14;
      const opacity = interpolate(frame, [delay, delay + 20], [0, 1], { extrapolateRight: "clamp" });
      const translateY = interpolate(frame, [delay, delay + 20], [30, 0], { extrapolateRight: "clamp" });
      return (
        <div key={i} style={{
          opacity,
          transform: `translateY(${translateY}px)`,
          backgroundColor: layer.color + "16",
          border: `1px solid ${layer.color}40`,
          borderRadius: 18,
          padding: "20px 52px",
          minWidth: 440,
          textAlign: "center",
          boxShadow: `0 0 40px ${layer.color}14`,
        }}>
          <div style={{
            fontSize: 28,
            fontWeight: 700,
            color: layer.color,
            fontFamily: "Inter, -apple-system, sans-serif",
            letterSpacing: "-0.01em",
          }}>
            {layer.label}
          </div>
          <div style={{
            fontSize: 15,
            color: "#8E8E93",
            fontFamily: "Inter, -apple-system, sans-serif",
            marginTop: 5,
          }}>
            {layer.sub}
          </div>
        </div>
      );
    })}
  </div>
);

/** 节点圆 */
export const NodeCircle: React.FC<{
  label: string; sub?: string; x: number; y: number;
  color: string; startFrame: number; size?: number;
}> = ({ label, sub, x, y, color, startFrame, size = 100 }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 16], [0, 1], { extrapolateRight: "clamp" });
  const scale = interpolate(frame, [startFrame, startFrame + 16], [0.4, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      position: "absolute",
      left: `${x}%`,
      top: `${y}%`,
      transform: `translate(-50%, -50%) scale(${scale})`,
      opacity,
      width: size,
      height: size,
      borderRadius: "50%",
      backgroundColor: color + "20",
      border: `2px solid ${color}`,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      boxShadow: `0 0 30px ${color}30`,
    }}>
      <div style={{
        fontSize: 11,
        fontWeight: 700,
        color: color,
        textAlign: "center",
        fontFamily: "Inter, -apple-system, sans-serif",
        lineHeight: 1.3,
        padding: "0 8px",
      }}>
        {label}
      </div>
      {sub && (
        <div style={{
          fontSize: 9,
          color: color + "88",
          textAlign: "center",
          fontFamily: "Inter, -apple-system, sans-serif",
          marginTop: 2,
        }}>
          {sub}
        </div>
      )}
    </div>
  );
};

/** 箭头SVG */
export const ArrowSVG: React.FC<{
  x1: number; y1: number; x2: number; y2: number;
  color?: string; startFrame?: number;
}> = ({ x1, y1, x2, y2, color = "#0A84FF", startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [startFrame, startFrame + 20], [0, 1], { extrapolateRight: "clamp" });
  const dx = x2 - x1;
  const dy = y2 - y1;
  const length = Math.sqrt(dx * dx + dy * dy) * progress;
  const angle = Math.atan2(dy, dx) * 180 / Math.PI;
  return (
    <div style={{
      position: "absolute",
      left: `${x1}%`,
      top: `${y1}%`,
      width: length,
      height: 2,
      background: `linear-gradient(90deg, ${color}88, ${color})`,
      transform: `rotate(${angle}deg)`,
      transformOrigin: "0 50%",
      opacity: progress,
    }} />
  );
};

/** 九宫格 */
export const NineGrid: React.FC<{
  items: string[]; startFrame: number;
}> = ({ items, startFrame }) => {
  const colors = ["#0A84FF", "#BF5AF2", "#30D158", "#FF9F0A", "#FF453A", "#64D2FF", "#FFD60A", "#AC8E68", "#8E8E93"];
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, padding: "0 40px", maxWidth: 800 }}>
      {items.map((item, i) => {
        const frame = useCurrentFrame();
        const delay = startFrame + i * 9;
        const opacity = interpolate(frame, [delay, delay + 12], [0, 1], { extrapolateRight: "clamp" });
        const scale = interpolate(frame, [delay, delay + 12], [0.7, 1], { extrapolateRight: "clamp" });
        return (
          <div key={i} style={{
            opacity,
            transform: `scale(${scale})`,
            backgroundColor: colors[i] + "16",
            border: `1px solid ${colors[i]}40`,
            borderRadius: 14,
            padding: "16px 12px",
            textAlign: "center",
            fontSize: 15,
            fontWeight: 600,
            color: colors[i],
            fontFamily: "Inter, -apple-system, sans-serif",
          }}>
            {item}
          </div>
        );
      })}
    </div>
  );
};

/** 工具网格 */
export const ToolGrid: React.FC<{ tools: string[]; startFrame: number }> = ({ tools, startFrame }) => (
  <div style={{ display: "grid", gridTemplateColumns: "repeat(6, 1fr)", gap: 8, padding: "0 60px", maxWidth: 900 }}>
    {tools.map((tool, i) => {
      const frame = useCurrentFrame();
      const delay = startFrame + i * 5;
      const opacity = interpolate(frame, [delay, delay + 8], [0, 1], { extrapolateRight: "clamp" });
      const scale = interpolate(frame, [delay, delay + 8], [0.6, 1], { extrapolateRight: "clamp" });
      return (
        <div key={i} style={{
          opacity,
          transform: `scale(${scale})`,
          backgroundColor: "#1a1a24",
          border: "1px solid #2C2C2E",
          borderRadius: 10,
          padding: "10px 4px",
          textAlign: "center",
          fontSize: 12,
          fontWeight: 500,
          color: "#8E8E93",
          fontFamily: "Menlo, monospace",
        }}>
          {tool}
        </div>
      );
    })}
  </div>
);

/** 熔断器步骤列表 */
export const FuseSteps: React.FC<{ startFrame: number }> = ({ startFrame }) => {
  const items = [
    { label: "Token 超阈值", color: "#FF9F0A" },
    { label: "触发压缩", color: "#0A84FF" },
    { label: "尝试会话记忆压缩", color: "#30D158" },
    { label: "失败 ≥ 3 次 → 熔断", color: "#FF453A" },
    { label: "停止重试，防止失控", color: "#8E8E93" },
  ];
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14, padding: "0 80px", maxWidth: 680 }}>
      {items.map((item, i) => {
        const frame = useCurrentFrame();
        const delay = startFrame + i * 12;
        const opacity = interpolate(frame, [delay, delay + 12], [0, 1], { extrapolateRight: "clamp" });
        const tx = interpolate(frame, [delay, delay + 12], [-24, 0], { extrapolateRight: "clamp" });
        return (
          <div key={i} style={{
            opacity,
            transform: `translateX(${tx}px)`,
            display: "flex",
            alignItems: "center",
            gap: 16,
            backgroundColor: item.color + "12",
            border: `1px solid ${item.color}30`,
            borderRadius: 14,
            padding: "16px 24px",
          }}>
            <div style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              backgroundColor: item.color,
              boxShadow: `0 0 12px ${item.color}`,
              flexShrink: 0,
            }} />
            <div style={{
              fontSize: 18,
              fontWeight: 600,
              color: item.color,
              fontFamily: "Inter, -apple-system, sans-serif",
            }}>
              {item.label}
            </div>
          </div>
        );
      })}
    </div>
  );
};

/** 管线流 */
export const PipelineFlow: React.FC<{
  steps: { label: string; sub: string; color: string }[];
  startFrame: number;
}> = ({ steps, startFrame }) => (
  <div style={{ display: "flex", alignItems: "center", padding: "0 60px" }}>
    {steps.map((step, i) => {
      const frame = useCurrentFrame();
      const delay = startFrame + i * 16;
      const opacity = interpolate(frame, [delay, delay + 16], [0, 1], { extrapolateRight: "clamp" });
      const scale = interpolate(frame, [delay, delay + 16], [0.7, 1], { extrapolateRight: "clamp" });
      return (
        <React.Fragment key={i}>
          <div style={{ opacity, transform: `scale(${scale})`, textAlign: "center", minWidth: 120 }}>
            <div style={{
              fontSize: 20,
              fontWeight: 700,
              color: step.color,
              fontFamily: "Inter, -apple-system, sans-serif",
            }}>
              {step.label}
            </div>
            <div style={{ fontSize: 12, color: "#48484A", fontFamily: "Inter, -apple-system, sans-serif", marginTop: 4 }}>
              {step.sub}
            </div>
          </div>
          {i < steps.length - 1 && (
            <div style={{
              width: 32,
              height: 2,
              background: `linear-gradient(90deg, ${step.color}, ${steps[i + 1].color})`,
              opacity: 0.7,
              marginBottom: 20,
            }} />
          )}
        </React.Fragment>
      );
    })}
  </div>
);

/** 标签组 */
export const TagPill: React.FC<{ text: string; color?: string }> = ({ text, color = "#8E8E93" }) => (
  <div style={{
    backgroundColor: "#1a1a24",
    border: "1px solid #2C2C2E",
    borderRadius: 20,
    padding: "8px 20px",
    fontSize: 14,
    color: color,
    fontFamily: "Inter, -apple-system, sans-serif",
  }}>
    {text}
  </div>
);

export const TagGroup: React.FC<{ tags: { text: string; color?: string }[]; startFrame: number }> = ({ tags, startFrame }) => (
  <div style={{ display: "flex", gap: 12, flexWrap: "wrap", justifyContent: "center", padding: "0 60px" }}>
    {tags.map((tag, i) => {
      const frame = useCurrentFrame();
      const delay = startFrame + i * 9;
      const opacity = interpolate(frame, [delay, delay + 10], [0, 1], { extrapolateRight: "clamp" });
      return (
        <div key={i} style={{
          opacity,
          backgroundColor: "#1a1a24",
          border: "1px solid #2C2C2E",
          borderRadius: 20,
          padding: "8px 20px",
          fontSize: 14,
          color: tag.color || "#8E8E93",
          fontFamily: "Inter, -apple-system, sans-serif",
        }}>
          {tag.text}
        </div>
      );
    })}
  </div>
);

/** 引擎动画SVG */
export const EngineSpin: React.FC<{ startFrame: number }> = ({ startFrame }) => {
  const frame = useCurrentFrame();
  const rotation = interpolate(frame, [startFrame, startFrame + 90], [0, 360], { extrapolateRight: "clamp" });
  const opacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], { extrapolateRight: "clamp" });
  return (
    <svg width="260" height="260" viewBox="0 0 260 260" style={{ opacity }}>
      <defs>
        <radialGradient id="eg" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#0A84FF" stopOpacity="0.25" />
          <stop offset="100%" stopColor="#0A84FF" stopOpacity="0" />
        </radialGradient>
      </defs>
      <circle cx="130" cy="130" r="100" fill="url(#eg)" />
      <circle cx="130" cy="130" r="70" fill="none" stroke="#0A84FF" strokeWidth="1.5" strokeDasharray="6 3"
        style={{ transform: `rotate(${rotation}deg)`, transformOrigin: "130px 130px" }} />
      <circle cx="130" cy="130" r="44" fill="none" stroke="#BF5AF2" strokeWidth="2.5" />
      <text x="130" y="124" textAnchor="middle" fill="#FFFFFF" fontSize="16" fontWeight="700"
        fontFamily="Inter, -apple-system, sans-serif">ENGINE</text>
      <text x="130" y="143" textAnchor="middle" fill="#0A84FF" fontSize="12"
        fontFamily="Inter, -apple-system, sans-serif">上下文 = 燃油</text>
    </svg>
  );
};
