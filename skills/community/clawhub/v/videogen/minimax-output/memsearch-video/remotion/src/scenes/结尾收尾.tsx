import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";

export const 结尾收尾: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame();
  const dur = 17;
  const progress = Math.min(frame / dur, 1);
  const phase = (s: number, e: number) => Math.max(0, Math.min((progress - s) / (e - s), 1));

  const safeBottom = 120;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000", alignItems: "center", justifyContent: "center" }}>
      {/* 金句 */}
      <div style={{
        display: "flex", flexDirection: "column", alignItems: "center",
        opacity: phase(0, 0.2),
        transform: `scale(${0.9 + phase(0, 0.15) * 0.1})`,
        padding: "0 60px", textAlign: "center",
      }}>
        <div style={{ fontSize: 120, color: "#333", lineHeight: 0.5, marginBottom: -20 }}>
          "
        </div>
        <div style={{
          fontSize: 58, fontWeight: "bold", color: "#fff",
          lineHeight: 1.3, maxWidth: 700,
        }}>
          记忆应该比任何一个
          <span style={{ color: "#6bcb77" }}> agent </span>
          都活得更长
        </div>
        <div style={{ fontSize: 120, color: "#333", lineHeight: 0.5, marginTop: -10 }}>
          "
        </div>
      </div>

      {/* 分隔线 */}
      <div style={{
        width: "80%", maxWidth: 600, height: 2,
        backgroundColor: "#333", marginTop: 10,
        opacity: phase(0.2, 0.5),
      }} />

      {/* 项目地址 */}
      <div style={{
        marginTop: 20, textAlign: "center",
        opacity: phase(0.5, 0.65),
      }}>
        <div style={{ fontSize: 26, color: "#444", marginBottom: 8 }}>项目地址</div>
        <div style={{ fontSize: 34, color: "#48dbfb", fontFamily: "monospace", fontWeight: "bold" }}>
          github.com/zilliztech/memsearch
        </div>
      </div>

      {/* 底部绿条 */}
      <div style={{
        position: "absolute", bottom: 0, left: 0, right: 0, height: 6,
        backgroundColor: "#6bcb77",
        opacity: phase(0.8, 1),
      }} />
    </AbsoluteFill>
  );
};
