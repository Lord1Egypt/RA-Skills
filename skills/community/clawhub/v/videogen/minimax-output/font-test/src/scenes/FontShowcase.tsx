import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, Img } from "remotion";
import { useCurrentDimension } from "../hooks/useCurrentDimension";
import { BASE_FONT_SIZES, getFontSize, COLORS } from "../theme";

// 字号自适应展示（15秒）
export const FontShowcase: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const sec = frame / fps;
  const section = Math.floor(sec / 5);
  const { scaleY } = useCurrentDimension();

  // 当前缩放后的实际字号
  const hero = getFontSize("hero", height);
  const h1 = getFontSize("h1", height);
  const h2 = getFontSize("h2", height);
  const body = getFontSize("body", height);
  const caption = getFontSize("caption", height);
  const subtitle = getFontSize("subtitle", height);
  const tiny = getFontSize("tiny", height);

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>

      {/* 段落1：0-5秒 —— 自适应金句 */}
      {section === 0 && (
        <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", padding: "0 60px" }}>
          <div style={{ fontSize: hero, fontWeight: "bold", color: COLORS.text, fontFamily: "system-ui, sans-serif", textAlign: "center", lineHeight: 1.2 }}>
            Claude Code 的核心创新
          </div>
          <div style={{ fontSize: h1, color: COLORS.primary, fontFamily: "system-ui, sans-serif", marginTop: 24, textAlign: "center" }}>
            不在于 AI 有多强
          </div>
          <div style={{ fontSize: caption, color: COLORS.muted, fontFamily: "system-ui, sans-serif", marginTop: 40, textAlign: "center" }}>
            — 自适应金句 {hero}px（基准144px × {scaleY.toFixed(3)}）—
          </div>
        </div>
      )}

      {/* 段落2：5-10秒 —— 正文层级 */}
      {section === 1 && (
        <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", padding: "0 60px" }}>
          <div style={{ fontSize: h2, color: COLORS.accent, fontFamily: "system-ui, sans-serif", textAlign: "center", lineHeight: 1.3, fontWeight: "bold" }}>
            H2 二级标题 {h2}px
          </div>
          <div style={{ fontSize: body, color: COLORS.text, fontFamily: "system-ui, sans-serif", marginTop: 32, textAlign: "center", lineHeight: 1.6 }}>
            正文内容 {body}px — 它把一个不确定的模型，变成了一个可靠的工具。
          </div>
          <div style={{ fontSize: caption, color: COLORS.muted, fontFamily: "system-ui, sans-serif", marginTop: 28, textAlign: "center" }}>
            说明文字 {caption}px
          </div>
          <div style={{ fontSize: subtitle, color: COLORS.faint, fontFamily: "system-ui, sans-serif", marginTop: 20, textAlign: "center" }}>
            字幕 {subtitle}px / 水印 {tiny}px
          </div>
        </div>
      )}

      {/* 段落3：10-15秒 —— 字号速查表 */}
      {section === 2 && (
        <div style={{ position: "absolute", inset: 0, padding: "80px 80px" }}>
          <div style={{ fontSize: h1, color: COLORS.primary, fontFamily: "system-ui, sans-serif", fontWeight: "bold", marginBottom: 16 }}>
            字号速查表
          </div>
          <div style={{ fontSize: tiny, color: COLORS.muted, fontFamily: "system-ui, sans-serif", marginBottom: 40 }}>
            当前分辨率：{width}×{height} · 缩放比：{scaleY.toFixed(3)}
          </div>

          {[
            { label: "hero", base: BASE_FONT_SIZES.hero, actual: hero, color: COLORS.text },
            { label: "h1", base: BASE_FONT_SIZES.h1, actual: h1, color: COLORS.primary },
            { label: "h2", base: BASE_FONT_SIZES.h2, actual: h2, color: COLORS.accent },
            { label: "body", base: BASE_FONT_SIZES.body, actual: body, color: COLORS.text },
            { label: "caption", base: BASE_FONT_SIZES.caption, actual: caption, color: COLORS.muted },
            { label: "subtitle", base: BASE_FONT_SIZES.subtitle, actual: subtitle, color: COLORS.faint },
            { label: "tiny", base: BASE_FONT_SIZES.tiny, actual: tiny, color: COLORS.faint },
          ].map(({ label, base, actual, color }) => (
            <div key={label} style={{ display: "flex", alignItems: "baseline", gap: 20, marginBottom: 16 }}>
              <span style={{ fontSize: caption, color: COLORS.muted, fontFamily: "system-ui, sans-serif", width: 80 }}>
                {label}
              </span>
              <span style={{ fontSize: actual, color, fontFamily: "system-ui, sans-serif", fontWeight: "bold", lineHeight: 1 }}>
                Aa
              </span>
              <span style={{ fontSize: tiny, color: COLORS.muted, fontFamily: "system-ui, sans-serif" }}>
                基准 {base}px → 实际 {actual}px
              </span>
            </div>
          ))}

          <div style={{ marginTop: 40, fontSize: tiny, color: COLORS.faint, fontFamily: "system-ui, sans-serif" }}>
            公式：实际字号 = 基准字号 × (当前高度 / 1920)
          </div>
        </div>
      )}

      {/* 左上角分辨率标注 */}
      <div style={{ position: "absolute", top: 40, left: 40, color: COLORS.primary, fontSize: tiny, fontFamily: "system-ui, sans-serif" }}>
        {width}×{height} · scale={scaleY.toFixed(3)}
      </div>

      {/* 底部进度条 */}
      <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: 6, backgroundColor: "#1a2035" }}>
        <div style={{ height: "100%", width: `${(sec / 15) * 100}%`, backgroundColor: COLORS.primary }} />
      </div>

      <div style={{ position: "absolute", bottom: 20, right: 40, color: "#444", fontSize: 20, fontFamily: "system-ui, sans-serif" }}>
        {sec.toFixed(1)}s
      </div>
    </AbsoluteFill>
  );
};
