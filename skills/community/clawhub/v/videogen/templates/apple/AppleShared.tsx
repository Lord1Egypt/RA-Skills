import React from "react";
import { useCurrentFrame, interpolate, AbsoluteFill } from "remotion";

/** Apple 风格深空黑渐变背景 */
export const AppleBg: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{
    background: "linear-gradient(180deg, #111111 0%, #1c1c1e 100%)",
  }}>
    {children}
  </AbsoluteFill>
);

/** 主标题：72px Semibold */
export const HeroTitle: React.FC<{
  text: string;
  startFrame: number;
  color?: string;
}> = ({ text, startFrame, color = "#FFFFFF" }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 14], [0, 1], { extrapolateRight: "clamp" });
  const translateY = interpolate(frame, [startFrame, startFrame + 14], [30, 0], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      transform: `translateY(${translateY}px)`,
      fontSize: 72,
      fontWeight: 600,
      color,
      fontFamily: "SF Pro Display, PingFang SC, -apple-system, sans-serif",
      lineHeight: 1.1,
      letterSpacing: "-0.02em",
      textAlign: "center",
      padding: "0 60px",
    }}>
      {text}
    </div>
  );
};

/** 二级标题/节点：32px Medium */
export const NodeTitle: React.FC<{
  text: string;
  startFrame: number;
  color?: string;
}> = ({ text, startFrame, color = "#FFFFFF" }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 14], [0, 1], { extrapolateRight: "clamp" });
  const translateY = interpolate(frame, [startFrame, startFrame + 14], [20, 0], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      transform: `translateY(${translateY}px)`,
      fontSize: 32,
      fontWeight: 500,
      color,
      fontFamily: "SF Pro Display, PingFang SC, -apple-system, sans-serif",
      lineHeight: 1.3,
      textAlign: "center",
      padding: "0 60px",
    }}>
      {text}
    </div>
  );
};

/** 注释/标签：20px Regular */
export const Caption: React.FC<{
  text: string;
  startFrame: number;
  color?: string;
}> = ({ text, startFrame, color = "#8E8E93" }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 10], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      fontSize: 20,
      fontWeight: 400,
      color,
      fontFamily: "SF Pro Text, PingFang SC, -apple-system, sans-serif",
      lineHeight: 1.4,
      textAlign: "center",
      padding: "0 60px",
    }}>
      {text}
    </div>
  );
};

/** 场景标签（左上角）：20px Regular */
export const SceneTag: React.FC<{
  text: string;
  startFrame: number;
  color?: string;
}> = ({ text, startFrame, color = "#007AFF" }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 8], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      position: "absolute",
      top: 60,
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
        boxShadow: `0 0 10px ${color}`,
      }} />
      <div style={{
        fontSize: 20,
        fontWeight: 400,
        color: "#8E8E93",
        fontFamily: "SF Pro Text, PingFang SC, -apple-system, sans-serif",
        letterSpacing: "0.08em",
      }}>
        {text}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════
// Apple 色板（精简：只有一种强调色）
// ═══════════════════════════════════════════════
const ACCENT = "#007AFF";     // Apple 蓝（唯一强调色）
const TEXT = "#FFFFFF";       // 主文字
const MUTED = "#8E8E93";     // 次要文字
const BORDER = "#3a3a3c";     // 边框
const CARD = "#2c2c2e";       // 卡片背景

/** 强调文字（32px Medium） */
export const AccentText: React.FC<{
  text: string;
  startFrame: number;
}> = ({ text, startFrame }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 12], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      fontSize: 32,
      fontWeight: 500,
      color: ACCENT,
      fontFamily: "SF Pro Display, PingFang SC, -apple-system, sans-serif",
      lineHeight: 1.3,
      textAlign: "center",
    }}>
      {text}
    </div>
  );
};

/** 分隔线 */
export const Divider: React.FC<{
  startFrame?: number;
  color?: string;
}> = ({ startFrame = 0, color = BORDER }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 12], [0, 0.6], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      width: "100%",
      height: 1,
      backgroundColor: color,
    }} />
  );
};

// ═══════════════════════════════════════════════
// 布局常量（竖屏 9:16 安全区 60px）
// ═══════════════════════════════════════════════
export const SAFE = {
  top: 60,
  bottom: 60,
  left: 60,
  right: 60,
  titleTop: 80,       // 标题区 top
  contentTop: 280,    // 内容区 top
  bottomPos: 0.88,    // 底部标签位置
};

// ═══════════════════════════════════════════════
// 动画工具
// ═══════════════════════════════════════════════

/** fade-up */
function fadeUp(frame: number, start: number, duration = 14) {
  return {
    opacity: interpolate(frame, [start, start + duration], [0, 1], { extrapolateRight: "clamp" }),
    transform: `translateY(${interpolate(frame, [start, start + duration], [24, 0], { extrapolateRight: "clamp" })}px)`,
  };
}

/** scale-in */
function scaleIn(frame: number, start: number, duration = 16) {
  return {
    opacity: interpolate(frame, [start, start + duration], [0, 1], { extrapolateRight: "clamp" }),
    transform: `scale(${interpolate(frame, [start, start + duration], [0.5, 1], { extrapolateRight: "clamp" })})`,
  };
}

/** 层次堆栈 */
export const LayerStack: React.FC<{
  layers: { label: string; sub?: string }[];
  startFrame: number;
  accent?: boolean;
}> = ({ layers, startFrame, accent = true }) => {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 16 }}>
      {layers.map((layer, i) => {
        const frame = useCurrentFrame();
        const delay = startFrame + i * 14;
        const anim = fadeUp(frame, delay);
        const color = accent ? ACCENT : TEXT;
        return (
          <div key={i} style={{
            ...anim,
            backgroundColor: CARD,
            border: `1px solid ${BORDER}`,
            borderRadius: 16,
            padding: "20px 48px",
            minWidth: 480,
            textAlign: "center",
          }}>
            <div style={{
              fontSize: 32,
              fontWeight: 500,
              color: accent ? ACCENT : TEXT,
              fontFamily: "SF Pro Display, PingFang SC, -apple-system, sans-serif",
              lineHeight: 1.3,
            }}>
              {layer.label}
            </div>
            {layer.sub && (
              <div style={{
                fontSize: 20,
                fontWeight: 400,
                color: MUTED,
                fontFamily: "SF Pro Text, PingFang SC, -apple-system, sans-serif",
                marginTop: 6,
              }}>
                {layer.sub}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

/** 标签胶囊 */
export const TagPill: React.FC<{
  text: string;
  startFrame: number;
  accent?: boolean;
}> = ({ text, startFrame, accent = false }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 10], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      backgroundColor: accent ? ACCENT + "22" : CARD,
      border: `1px solid ${accent ? ACCENT + "44" : BORDER}`,
      borderRadius: 20,
      padding: "8px 20px",
      fontSize: 20,
      fontWeight: 400,
      color: accent ? ACCENT : MUTED,
      fontFamily: "SF Pro Text, PingFang SC, -apple-system, sans-serif",
    }}>
      {text}
    </div>
  );
};

/** 标签组 */
export const TagGroup: React.FC<{
  tags: { text: string; accent?: boolean }[];
  startFrame: number;
}> = ({ tags, startFrame }) => (
  <div style={{ display: "flex", gap: 12, flexWrap: "wrap", justifyContent: "center", padding: "0 60px" }}>
    {tags.map((tag, i) => (
      <TagPill key={i} text={tag.text} accent={tag.accent} startFrame={startFrame + i * 8} />
    ))}
  </div>
);

/** 双栏对比卡片 */
export const TwoColumn: React.FC<{
  left: { title: string; items: string[] };
  right: { title: string; items: string[] };
  startFrame: number;
}> = ({ left, right, startFrame }) => {
  const colWidth = "46%";
  const gap = "8%";

  return (
    <div style={{
      position: "absolute",
      top: SAFE.contentTop,
      left: SAFE.left,
      right: SAFE.right,
      display: "flex",
      justifyContent: "space-between",
      gap,
    }}>
      {/* 左栏 */}
      <div style={{ width: colWidth, display: "flex", flexDirection: "column", gap: 16 }}>
        <div style={{
          ...fadeUp(useCurrentFrame(), startFrame),
          backgroundColor: CARD,
          border: `2px solid ${ACCENT}55`,
          borderRadius: 16,
          padding: "20px 24px",
        }}>
          <div style={{
            fontSize: 32,
            fontWeight: 500,
            color: ACCENT,
            fontFamily: "SF Pro Display, PingFang SC, -apple-system, sans-serif",
            marginBottom: 12,
          }}>
            {left.title}
          </div>
          {left.items.map((item, i) => (
            <div key={i} style={{
              fontSize: 20,
              fontWeight: 400,
              color: MUTED,
              fontFamily: "SF Pro Text, PingFang SC, -apple-system, sans-serif",
              lineHeight: 1.5,
              marginBottom: 8,
            }}>
              • {item}
            </div>
          ))}
        </div>
      </div>

      {/* 右栏 */}
      <div style={{ width: colWidth, display: "flex", flexDirection: "column", gap: 16 }}>
        <div style={{
          ...fadeUp(useCurrentFrame(), startFrame + 10),
          backgroundColor: CARD,
          border: `2px solid ${BORDER}`,
          borderRadius: 16,
          padding: "20px 24px",
        }}>
          <div style={{
            fontSize: 32,
            fontWeight: 500,
            color: TEXT,
            fontFamily: "SF Pro Display, PingFang SC, -apple-system, sans-serif",
            marginBottom: 12,
          }}>
            {right.title}
          </div>
          {right.items.map((item, i) => (
            <div key={i} style={{
              fontSize: 20,
              fontWeight: 400,
              color: MUTED,
              fontFamily: "SF Pro Text, PingFang SC, -apple-system, sans-serif",
              lineHeight: 1.5,
              marginBottom: 8,
            }}>
              • {item}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

/** 九宫格 */
export const NineGrid: React.FC<{
  items: string[];
  startFrame: number;
}> = ({ items, startFrame }) => {
  const colors = [ACCENT, "#34C759", "#FF9500", "#FF3B30", "#5856D6", "#00C7BE", "#FF2D55", "#8E8E93", "#8E8E93"];
  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(3, 1fr)",
      gap: 12,
      padding: `0 ${SAFE.left}px`,
      maxWidth: 960,
    }}>
      {items.map((item, i) => {
        const frame = useCurrentFrame();
        const delay = startFrame + i * 9;
        const opacity = interpolate(frame, [delay, delay + 12], [0, 1], { extrapolateRight: "clamp" });
        const scale = interpolate(frame, [delay, delay + 12], [0.8, 1], { extrapolateRight: "clamp" });
        return (
          <div key={i} style={{
            opacity,
            transform: `scale(${scale})`,
            backgroundColor: colors[i] + "18",
            border: `1px solid ${colors[i]}40`,
            borderRadius: 14,
            padding: "16px 12px",
            textAlign: "center",
            fontSize: 20,
            fontWeight: 500,
            color: colors[i],
            fontFamily: "SF Pro Text, PingFang SC, -apple-system, sans-serif",
            lineHeight: 1.3,
          }}>
            {item}
          </div>
        );
      })}
    </div>
  );
};

/** 步骤列表 */
export const StepList: React.FC<{
  steps: { title: string; sub?: string }[];
  startFrame: number;
}> = ({ steps, startFrame }) => (
  <div style={{ display: "flex", flexDirection: "column", gap: 14, padding: `0 ${SAFE.left}px`, maxWidth: 720 }}>
    {steps.map((step, i) => {
      const frame = useCurrentFrame();
      const delay = startFrame + i * 14;
      const tx = interpolate(frame, [delay, delay + 14], [-20, 0], { extrapolateRight: "clamp" });
      const opacity = interpolate(frame, [delay, delay + 14], [0, 1], { extrapolateRight: "clamp" });
      return (
        <div key={i} style={{
          opacity,
          transform: `translateX(${tx}px)`,
          display: "flex",
          alignItems: "center",
          gap: 16,
          backgroundColor: CARD,
          border: `1px solid ${BORDER}`,
          borderRadius: 14,
          padding: "16px 24px",
        }}>
          <div style={{
            width: 10,
            height: 10,
            borderRadius: "50%",
            backgroundColor: ACCENT,
            boxShadow: `0 0 10px ${ACCENT}`,
            flexShrink: 0,
          }} />
          <div>
            <div style={{
              fontSize: 32,
              fontWeight: 500,
              color: TEXT,
              fontFamily: "SF Pro Display, PingFang SC, -apple-system, sans-serif",
              lineHeight: 1.3,
            }}>
              {step.title}
            </div>
            {step.sub && (
              <div style={{
                fontSize: 20,
                fontWeight: 400,
                color: MUTED,
                fontFamily: "SF Pro Text, PingFang SC, -apple-system, sans-serif",
                marginTop: 4,
              }}>
                {step.sub}
              </div>
            )}
          </div>
        </div>
      );
    })}
  </div>
);

/** 引擎 SVG 动画 */
export const EngineSpin: React.FC<{ startFrame: number }> = ({ startFrame }) => {
  const frame = useCurrentFrame();
  const rotation = interpolate(frame, [startFrame, startFrame + 90], [0, 360], { extrapolateRight: "clamp" });
  const opacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], { extrapolateRight: "clamp" });
  return (
    <svg width="240" height="240" viewBox="0 0 240 240" style={{ opacity }}>
      <defs>
        <radialGradient id="eg" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor={ACCENT} stopOpacity="0.2" />
          <stop offset="100%" stopColor={ACCENT} stopOpacity="0" />
        </radialGradient>
      </defs>
      <circle cx="120" cy="120" r="100" fill="url(#eg)" />
      <circle cx="120" cy="120" r="70" fill="none" stroke={ACCENT} strokeWidth="1.5" strokeDasharray="6 3"
        style={{ transform: `rotate(${rotation}deg)`, transformOrigin: "120px 120px" }} />
      <circle cx="120" cy="120" r="44" fill="none" stroke={MUTED} strokeWidth="2" />
      <text x="120" y="114" textAnchor="middle" fill={TEXT} fontSize="16" fontWeight="600"
        fontFamily="SF Pro Display, PingFang SC, -apple-system, sans-serif">ENGINE</text>
      <text x="120" y="132" textAnchor="middle" fill={ACCENT} fontSize="12"
        fontFamily="SF Pro Text, PingFang SC, -apple-system, sans-serif">上下文 = 燃油</text>
    </svg>
  );
};
