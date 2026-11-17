import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EDGE } from "./layout";
import { FONTS, SMALL } from "./theme";
import type { Block, Theme } from "./types";

type Props = {
  block: Block;
  theme: Theme;
  /** Frame (inside the scene) at which the first word starts to rise. */
  start: number;
  /** Frames between words. */
  stagger: number;
  /** Frame at which the first highlight box starts its wipe (default: just after its last word lands). */
  boxStart?: number;
  align?: "center" | "left";
  small?: boolean;
  color?: string;
  opacity?: number;
  highlightStyle?: "box" | "color";
  letterSpacing?: string;
};

const RISE = { damping: 18, stiffness: 210, mass: 0.6 };
const WIPE = { damping: 22, stiffness: 170 };

/** Frame (inside the scene) at which the last highlight box has finished, or the last word has landed. */
export const settleFrame = (block: Block, start: number, stagger: number, boxStart?: number) => {
  const marks = block.marks.flat();
  const lastMark = marks.lastIndexOf(true);
  if (lastMark < 0) return start + (marks.length - 1) * stagger + 8;
  let runs = 0;
  block.marks.forEach((line) => line.forEach((m, i) => m && !line[i - 1] && runs++));
  return (boxStart != null ? boxStart + (runs - 1) * 5 : start + lastMark * stagger + 3) + 9;
};

/**
 * Words rise into place behind a mask, one by one. Highlighted runs get an accent
 * block that wipes in behind them; the text over the block switches colour exactly
 * at the wipe edge, so it is readable at every frame.
 */
export const Words: React.FC<Props> = ({
  block,
  theme,
  start,
  stagger,
  boxStart,
  align = "center",
  small,
  color,
  opacity = 1,
  highlightStyle = "box",
  letterSpacing,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const font = small ? SMALL : FONTS[theme.font];
  const fg = color ?? theme.fg;
  const size = block.fontSize;
  let k = 0;
  let runIdx = 0;

  const word = (w: string, idx: number, tint: string, still?: boolean) => {
    const p = still ? 1 : spring({ frame: frame - start - idx * stagger, fps, config: RISE });
    return (
      <span
        key={idx}
        style={{
          display: "inline-block",
          overflow: "hidden",
          verticalAlign: "bottom",
          // Room for accents above capitals (É, Ö, Å) and descenders (Ç, g), so the mask never cuts them.
          padding: "0.24em 0.02em 0.22em",
          margin: "-0.24em -0.02em -0.22em",
        }}
      >
        <span style={{ display: "inline-block", transform: `translateY(${(1 - p) * 110}%)`, color: tint }}>{w}</span>
      </span>
    );
  };

  const join = (nodes: React.ReactNode[]) => {
    const out: React.ReactNode[] = [];
    nodes.forEach((n, i) => {
      if (i) out.push(" ");
      out.push(n);
    });
    return out;
  };

  return (
    <div
      style={{
        fontFamily: font.family,
        fontWeight: font.weight as React.CSSProperties["fontWeight"],
        fontSize: size,
        lineHeight: font.lineHeight,
        textAlign: align,
        opacity,
        color: fg,
        letterSpacing,
      }}
    >
      {block.lines.map((line, li) => {
        const parts: React.ReactNode[] = [];
        let i = 0;
        while (i < line.length) {
          if (block.marks[li][i]) {
            let j = i;
            while (j < line.length && block.marks[li][j]) j++;
            const first = k;
            const last = k + (j - i) - 1;
            // In the first scene every run wipes in order from boxStart; elsewhere just after its last word lands.
            const at = boxStart != null ? boxStart + runIdx * 5 : start + last * stagger + 3;
            runIdx += 1;
            const boxP = Math.min(1, spring({ frame: frame - at, fps, config: WIPE }));
            const runWords = line.slice(i, j);
            if (highlightStyle === "box") {
              const edge = (1 - boxP) * 100;
              parts.push(
                <span key={`r${li}-${i}`} style={{ position: "relative", display: "inline-block", margin: `0 ${EDGE * size}px` }}>
                  <span
                    style={{
                      position: "absolute",
                      left: -EDGE * size,
                      right: -EDGE * size,
                      top: 0.04 * size,
                      bottom: -0.02 * size,
                      background: theme.accent,
                      borderRadius: 0.06 * size,
                      clipPath: `inset(0 ${edge}% 0 0)`,
                    }}
                  />
                  <span style={{ position: "relative" }}>{join(runWords.map((w, n) => word(w, first + n, fg)))}</span>
                  {/* Accent-coloured copy, drawn only where the block is, so accents above it stay in the normal colour. */}
                  <span
                    style={{
                      position: "absolute",
                      left: 0,
                      top: 0,
                      whiteSpace: "nowrap",
                      clipPath: `inset(${0.04 * size}px ${edge}% ${-0.02 * size}px ${-EDGE * size}px)`,
                    }}
                  >
                    {join(runWords.map((w, n) => word(w, first + n, theme.accentText)))}
                  </span>
                </span>,
              );
            } else {
              parts.push(...join(runWords.map((w, n) => word(w, first + n, theme.accent))));
            }
            k += j - i;
            i = j;
          } else {
            parts.push(word(line[i], k, fg));
            k += 1;
            i += 1;
          }
          if (i < line.length) parts.push(" ");
        }
        return (
          <div key={li} style={{ whiteSpace: "nowrap" }}>
            {parts}
          </div>
        );
      })}
    </div>
  );
};
