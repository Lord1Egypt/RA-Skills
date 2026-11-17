import React from "react";
import {
  AbsoluteFill,
  Easing,
  Html5Audio,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { AFFIX, PUNCH, STAGGER, formatStat, loadFonts, statParts } from "./layout";
import { FONTS, HEIGHT, LEFT_INSET, SAFE, SAFE_H, SAFE_W, SMALL, WIDTH, resolveTheme } from "./theme";
import type { Block, Scene, SceneLayout, ShortProps, Theme } from "./types";
import { Words, settleFrame } from "./Words";

loadFonts();

const isVideo = (src: string) => /\.(mp4|mov|webm|m4v)$/i.test(src);
const CLAMP = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
// Centred scenes punch around the frame's centre line; left-aligned ones around the safe box centre.
const ORIGIN_CENTER = `${WIDTH / 2}px ${SAFE.top + SAFE_H / 2}px`;
const ORIGIN_LEFT = `${SAFE.left + SAFE_W / 2}px ${SAFE.top + SAFE_H / 2}px`;

const Media: React.FC<{ src: string; frames: number }> = ({ src, frames }) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, Math.max(1, frames)], [1.08, 1.0], CLAMP);
  const style: React.CSSProperties = { width: "100%", height: "100%", objectFit: "cover", transform: `scale(${scale})` };
  return isVideo(src) ? <OffthreadVideo src={staticFile(src)} muted style={style} /> : <Img src={staticFile(src)} style={style} />;
};

/** Theme colour with two soft light spots drifting slowly; seeded so every short moves differently. */
const Ambient: React.FC<{ theme: Theme; seed: string }> = ({ theme, seed }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const r = (k: string) => random(`${seed}-${k}`);
  const spot = (k: string, base: [number, number]) => {
    const x = base[0] + 14 * Math.sin(t * (0.18 + 0.1 * r(`${k}sx`)) + 6 * r(`${k}px`));
    const y = base[1] + 10 * Math.cos(t * (0.14 + 0.1 * r(`${k}sy`)) + 6 * r(`${k}py`));
    return `${x.toFixed(2)}% ${y.toFixed(2)}%`;
  };
  return (
    <AbsoluteFill
      style={{
        background: [
          `radial-gradient(60% 40% at ${spot("a", [30, 30])}, color-mix(in srgb, ${theme.accent} 14%, transparent) 0%, transparent 70%)`,
          `radial-gradient(70% 45% at ${spot("b", [70, 62])}, color-mix(in srgb, ${theme.fg} 8%, transparent) 0%, transparent 70%)`,
          theme.bg,
        ].join(", "),
      }}
    />
  );
};

const Backdrop: React.FC<{ theme: Theme; src?: string | null; frames: number; seed: string }> = ({ theme, src, frames, seed }) => (
  <AbsoluteFill>
    {src ? (
      <>
        <Media src={src} frames={frames} />
        <AbsoluteFill style={{ background: theme.bg, opacity: 0.66 }} />
      </>
    ) : (
      <Ambient theme={theme} seed={seed} />
    )}
  </AbsoluteFill>
);

/** The safe box. Content is centred in it unless top is set. */
const Safe: React.FC<{ children: React.ReactNode; align?: "center" | "left"; footer?: Block; top?: boolean }> = ({ children, align = "center", footer, top }) => (
  <div
    style={{
      position: "absolute",
      // Centred text gets equal margins, so its centre is the frame's centre.
      left: align === "center" ? SAFE.right : SAFE.left,
      right: SAFE.right,
      top: SAFE.top,
      bottom: SAFE.bottom + (footer ? footer.lines.length * footer.fontSize * 1.25 + 24 : 0),
      display: "flex",
      flexDirection: "column",
      justifyContent: top ? "flex-start" : "center",
      alignItems: align === "center" ? "center" : "flex-start",
      paddingTop: top ? 24 : 0,
      // Left-aligned text sits in from the edge by what the punch adds, so it never crosses the safe box.
      paddingLeft: align === "left" ? LEFT_INSET : 0,
    }}
  >
    {children}
  </div>
);

/** A single line that rises behind a mask (big numbers, ranks, big words). */
const Rise: React.FC<{ at: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ at, children, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - at, fps, config: { damping: 18, stiffness: 200, mass: 0.6 } });
  return (
    <div style={{ overflow: "hidden", padding: "0.24em 0.04em 0.22em", margin: "-0.24em -0.04em -0.22em", ...style }}>
      <div style={{ transform: `translateY(${(1 - p) * 110}%)` }}>{children}</div>
    </div>
  );
};

type SceneProps = { scene: Scene; l: SceneLayout; theme: Theme; first: boolean; props: ShortProps; seed: string };

/** Frames, inside the scene, of the moments the motion and sound effects key off. */
export const sceneTimes = (scene: Scene, l: SceneLayout, first: boolean, fps: number) => {
  const st = Math.max(1, Math.round(fps * STAGGER));
  // The first scene is fully set on frame 0; only its highlight wipe and punch move.
  const lead = first ? -(l.reveal + 12) : -3;
  const main = l.blocks.main ?? l.blocks.title ?? l.blocks.label;
  const boxStart = first ? 2 : undefined;
  const textStart =
    scene.type === "item" ? lead + 5 : scene.type === "stat" ? (first ? lead : Math.round(l.reveal * 0.25)) : lead + (l.blocks.big ? 4 : 0);
  const marks = main ? main.marks.flat() : [];
  const lastMark = marks.lastIndexOf(true);
  const settle = main ? settleFrame(main, textStart, st, boxStart) : l.reveal;
  const markAt = lastMark >= 0 ? (boxStart ?? textStart + lastMark * st + 3) : null;
  return { st, lead, boxStart, textStart, settle, markAt, countAt: 0, countEnd: Math.round(0.75 * fps) };
};

const SceneView: React.FC<SceneProps> = ({ scene, l, theme, first, props, seed }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const hs = props.highlightStyle ?? "box";
  const tm = sceneTimes(scene, l, first, fps);
  const footer = l.blocks.footer;
  const font = FONTS[theme.font];
  const fontStyle: React.CSSProperties = { fontFamily: font.family, fontWeight: font.weight as React.CSSProperties["fontWeight"] };
  // A small punch when the emphasis lands, then hold. The layout leaves room for it.
  const punchAt = scene.type === "stat" ? tm.countEnd : first ? Math.max(3, tm.settle) : tm.settle;
  const punch = 1 + (PUNCH - 1) * Math.min(1, spring({ frame: frame - punchAt, fps, config: { damping: 26, stiffness: 120 } }));

  let body: React.ReactNode = null;
  switch (scene.type) {
    case "hook":
    case "text":
      body = (
        <Safe footer={footer}>
          {l.blocks.big ? (
            <Rise
              at={tm.lead}
              style={{ ...fontStyle, fontSize: l.blocks.big.fontSize, lineHeight: 1, color: theme.accent, fontVariantNumeric: "tabular-nums", marginBottom: 24, whiteSpace: "nowrap" }}
            >
              {l.blocks.big.lines[0][0]}
            </Rise>
          ) : null}
          <Words block={l.blocks.main} theme={theme} start={tm.textStart} stagger={tm.st} boxStart={tm.boxStart} highlightStyle={hs} />
        </Safe>
      );
      break;
    case "stat": {
      const p = statParts(scene.value!);
      const t = p.numeric ? interpolate(frame, [tm.countAt, tm.countEnd], [0, 1], { ...CLAMP, easing: Easing.bezier(0.16, 1, 0.3, 1) }) : 1;
      const v = p.numeric ? formatStat(p.num * t, p) : p.str;
      const land = interpolate(frame, [tm.countEnd, tm.countEnd + 4, tm.countEnd + 10], [1, 1.06, 1], CLAMP);
      const vb = l.blocks.value;
      body = (
        <Safe footer={footer}>
          <Rise at={first ? tm.lead : -3} style={{ marginBottom: 36 }}>
            <div
              style={{
                ...fontStyle,
                fontSize: vb.fontSize,
                lineHeight: 1,
                color: theme.accent,
                fontVariantNumeric: "tabular-nums",
                whiteSpace: "nowrap",
                transform: `scale(${land})`,
              }}
            >
              {scene.prefix ? <span style={{ fontSize: `${AFFIX}em` }}>{scene.prefix}</span> : null}
              {v}
              {scene.suffix ? <span style={{ fontSize: `${AFFIX}em` }}>{scene.suffix}</span> : null}
            </div>
          </Rise>
          <Words block={l.blocks.label} theme={theme} start={tm.textStart} stagger={tm.st} highlightStyle={hs} />
        </Safe>
      );
      break;
    }
    case "item": {
      body = (
        <Safe align="left" footer={footer} top>
          {l.blocks.progress ? (
            <div
              style={{
                fontFamily: SMALL.family,
                fontWeight: 700,
                fontSize: 40,
                color: theme.bg,
                background: theme.fg,
                borderRadius: 999,
                padding: "6px 22px",
                marginBottom: 28,
                opacity: 0.9,
              }}
            >
              {l.blocks.progress.lines[0][0]}
            </div>
          ) : null}
          {l.blocks.rank ? (
            <Rise at={tm.lead} style={{ ...fontStyle, fontSize: l.blocks.rank.fontSize, lineHeight: 0.95, color: theme.accent, marginBottom: 20, whiteSpace: "nowrap" }}>
              {l.blocks.rank.lines[0][0]}
            </Rise>
          ) : null}
          <Words block={l.blocks.title} theme={theme} start={tm.textStart} stagger={tm.st} align="left" highlightStyle={hs} />
          {l.blocks.body ? (
            <div style={{ marginTop: 32 }}>
              <Words block={l.blocks.body} theme={theme} start={tm.textStart + 6} stagger={1} align="left" small opacity={0.85} />
            </div>
          ) : null}
        </Safe>
      );
      break;
    }
    case "quote": {
      const bar = Math.min(1, spring({ frame: frame - tm.lead, fps, config: { damping: 20, stiffness: 150 } }));
      body = (
        <Safe align="left" footer={footer}>
          <div style={{ position: "relative", paddingLeft: 52 }}>
            <div
              style={{
                position: "absolute",
                left: 0,
                top: 8,
                bottom: 8,
                width: 14,
                borderRadius: 7,
                background: theme.accent,
                transform: `scaleY(${bar})`,
                transformOrigin: "top center",
              }}
            />
            <Words block={l.blocks.main} theme={theme} start={tm.textStart + 3} stagger={tm.st} align="left" highlightStyle={hs} />
            {l.blocks.author ? (
              <div style={{ marginTop: 40 }}>
                <Words block={l.blocks.author} theme={theme} start={tm.settle} stagger={2} align="left" small color={theme.accent} letterSpacing="0.04em" />
              </div>
            ) : null}
          </div>
        </Safe>
      );
      break;
    }
    case "end": {
      body = (
        <Safe footer={footer}>
          <Words block={l.blocks.main} theme={theme} start={tm.textStart} stagger={tm.st} boxStart={tm.boxStart} highlightStyle={hs} />
          {l.blocks.sub ? (
            <div style={{ marginTop: 36 }}>
              <Words block={l.blocks.sub} theme={theme} start={tm.settle - 4} stagger={1} small opacity={0.85} />
            </div>
          ) : null}
          {l.blocks.handle ? (
            <div style={{ marginTop: 44 }}>
              <Words block={l.blocks.handle} theme={theme} start={tm.settle} stagger={1} small color={theme.accent} />
            </div>
          ) : null}
        </Safe>
      );
      break;
    }
  }

  return (
    <AbsoluteFill>
      {scene.image || !props.background ? <Backdrop theme={theme} src={scene.image} frames={l.frames} seed={seed} /> : null}
      <AbsoluteFill style={{ transform: `scale(${punch})`, transformOrigin: scene.type === "item" || scene.type === "quote" ? ORIGIN_LEFT : ORIGIN_CENTER }}>
        {body}
      </AbsoluteFill>
      {footer ? (
        <div
          style={{
            position: "absolute",
            left: SAFE.right,
            right: SAFE.right,
            bottom: SAFE.bottom,
            textAlign: "center",
            fontFamily: SMALL.family,
            fontWeight: 700,
            fontSize: footer.fontSize,
            lineHeight: 1.25,
            color: theme.fg,
            opacity: 0.8,
          }}
        >
          {footer.lines.map((w) => w.join(" ")).join(" ")}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

/** Sound effects made for this template (public/sfx, MIT): hook hit, cut whoosh, highlight pop, count ticks. */
const Sfx: React.FC<{ props: ShortProps; layout: SceneLayout[] }> = ({ props, layout }) => {
  const { fps } = useVideoConfig();
  if (props.sfx === false) return null;
  const v = Math.min(1, Math.max(0, props.sfxVolume ?? 1));
  const cues: { at: number; file: string; vol: number; len: number }[] = [{ at: 0, file: "hit", vol: 0.55, len: 21 }];
  layout.forEach((l, i) => {
    const scene = props.scenes[i];
    const tm = sceneTimes(scene, l, i === 0, fps);
    if (i > 0) cues.push({ at: Math.max(0, l.from - 4), file: "whoosh", vol: 0.5, len: 10 });
    if (scene.type === "stat" && statParts(scene.value!).numeric) cues.push({ at: l.from + tm.countAt, file: "tick", vol: 0.45, len: 21 });
    if (tm.markAt != null && tm.markAt + 2 < l.frames) cues.push({ at: l.from + Math.max(0, tm.markAt), file: "pop", vol: 0.5, len: 5 });
  });
  return (
    <>
      {cues.map((c, i) => (
        <Sequence key={i} from={c.at} durationInFrames={c.len} layout="none">
          <Html5Audio src={staticFile(`sfx/${c.file}.wav`)} volume={c.vol * v} />
        </Sequence>
      ))}
    </>
  );
};

/** A thin dashed line around the safe area, for the review sheets only. The frame itself is shown as the video looks. */
const Guides: React.FC = () => (
  <AbsoluteFill>
    <div
      style={{
        position: "absolute",
        left: SAFE.left,
        right: SAFE.right,
        top: SAFE.top,
        bottom: SAFE.bottom,
        border: "3px dashed rgba(255,80,80,0.75)",
      }}
    />
  </AbsoluteFill>
);

export const Short: React.FC<ShortProps & { guides?: boolean; mute?: boolean }> = (props) => {
  const { fps, durationInFrames } = useVideoConfig();
  const theme = props.resolvedTheme ?? resolveTheme(props.theme ?? undefined, props.font ?? undefined);
  const layout = props.layout ?? [];
  const music = props.music;
  const seed = props.scenes.map((s) => s.text ?? s.title ?? s.label ?? "").join("|");
  return (
    <AbsoluteFill style={{ background: theme.bg, width: WIDTH, height: HEIGHT }}>
      {props.background ? <Backdrop theme={theme} src={props.background} frames={durationInFrames} seed={seed} /> : null}
      {layout.map((l, i) => (
        <Sequence key={i} from={l.from} durationInFrames={l.frames} name={`${i + 1} ${props.scenes[i].type}`}>
          <SceneView scene={props.scenes[i]} l={l} theme={theme} first={i === 0} props={props} seed={`${seed}-${i}`} />
        </Sequence>
      ))}
      {!props.mute ? <Sfx props={props} layout={layout} /> : null}
      {music && !props.mute ? (
        <Html5Audio
          src={staticFile(music.src)}
          trimBefore={Math.round((music.start ?? 0) * fps)}
          volume={(f) => (music.volume ?? 0.6) * interpolate(f, [0, 6, durationInFrames - fps, durationInFrames], [0, 1, 1, 0], CLAMP)}
        />
      ) : null}
      {props.guides ? <Guides /> : null}
    </AbsoluteFill>
  );
};
