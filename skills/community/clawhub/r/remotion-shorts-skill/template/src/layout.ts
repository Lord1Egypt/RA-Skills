import { loadFont } from "@remotion/fonts";
import { measureText } from "@remotion/layout-utils";
import { staticFile } from "remotion";
import { CENTER_W, FONTS, LEFT_W, SAFE_H, SMALL, resolveTheme } from "./theme";
import type { Block, FontName, Scene, SceneLayout, ShortProps, Theme } from "./types";

let fontsLoaded: Promise<unknown> | null = null;

export const loadFonts = () => {
  if (!fontsLoaded) {
    const all = [
      ...Object.values(FONTS).map((f) => ({ family: f.family, url: staticFile(f.file), weight: f.weight })),
      { family: SMALL.family, url: staticFile(SMALL.file), weight: SMALL.weight },
    ];
    fontsLoaded = Promise.all(all.map((f) => loadFont(f)));
  }
  return fontsLoaded;
};

/** Reading speed for big on-screen text, characters per second (Netflix allows 17 to 20 for subtitles). */
const CPS = 17;
/** BBC subtitle guidance is about 0.33 seconds per word; big text with nothing else on screen reads a bit faster. */
const PER_WORD = 0.3;
/** Time for a scene's entry to settle. */
const ENTRY = 0.3;
/** Seconds between words in the word-by-word reveal. */
export const STAGGER = 0.06;

/** The emphasis punch scales a block up by this much; layout leaves room for it. */
export const PUNCH = 1.04;
/** Room around a highlighted run (margin plus box overhang), in em, on each side. */
export const EDGE = 0.12;
/** Ratio of a prefix or suffix to the number in a stat. */
export const AFFIX = 0.62;

/** Anton is condensed, so it can run larger than the wide fonts. */
const FONT_SCALE: Record<FontName, number> = { Anton: 1, Poppins: 0.74, Inter: 0.76 };

type Spec = {
  text: string;
  small?: boolean;
  max: number;
  min: number;
  maxLines: number;
  height: number;
  width?: number;
  highlight?: string[];
  /** Throw instead of warning when it can't fit (one-line labels like handles). */
  strict?: boolean;
  /** What to tell the user when it doesn't fit. */
  tooLong?: string;
};

const norm = (w: string) => w.toLowerCase().replace(/[^\p{L}\p{N}%$€£.]/gu, "").replace(/\.$/, "");

const markWords = (words: string[], phrases: string[]) => {
  const marks = words.map(() => false);
  const toks = words.map(norm);
  const missing: string[] = [];
  for (const p of phrases) {
    const pt = p.split(/\s+/).map(norm).filter(Boolean);
    let found = false;
    for (let i = 0; i + pt.length <= toks.length; i++) {
      if (pt.every((t, j) => toks[i + j] === t)) {
        for (let j = 0; j < pt.length; j++) marks[i + j] = true;
        found = true;
      }
    }
    if (!found && pt.length) missing.push(p);
  }
  return { marks, missing };
};

/** Greedy wrap of word widths (already in px) into lines no wider than maxW. */
const wrap = (widths: number[], space: number, maxW: number) => {
  const lines: number[][] = [];
  let cur: number[] = [];
  let w = 0;
  widths.forEach((ww, i) => {
    const add = cur.length ? space + ww : ww;
    if (cur.length && w + add > maxW) {
      lines.push(cur);
      cur = [i];
      w = ww;
    } else {
      cur.push(i);
      w += add;
    }
  });
  if (cur.length) lines.push(cur);
  return lines;
};

const lineWidth = (line: number[], widths: number[], space: number) =>
  line.reduce((a, i) => a + widths[i], 0) + space * (line.length - 1);

const measurer = (family: string, weight: string, numeric?: boolean) => (t: string) =>
  measureText({
    text: t,
    fontFamily: family,
    fontWeight: weight,
    fontSize: 100,
    validateFontIsLoaded: true,
    ...(numeric ? { fontVariantNumeric: "tabular-nums" } : {}),
  }).width / 100;

const clip = (s: string) => `"${s.slice(0, 48)}${s.length > 48 ? "..." : ""}"`;

/**
 * Pick a font size and line breaks: as big as possible, 2 to 3 lines preferred,
 * no single-word last line, lines of similar length. Room is left for the
 * emphasis punch and for highlight boxes, so text never leaves the safe box.
 */
const fitBlock = (spec: Spec, theme: Theme, warnings: string[], label: string): Block => {
  const font = spec.small ? SMALL : FONTS[theme.font];
  const scale = spec.small ? 1 : FONT_SCALE[theme.font];
  const raw = spec.text.trim();
  const shown = theme.uppercase && !spec.small ? raw.toUpperCase() : raw;
  const words = shown.split(/\s+/).filter(Boolean);
  const { marks, missing } = markWords(words, spec.highlight ?? []);
  for (const m of missing) warnings.push(`${label}: highlight "${m}" is not in the text, so nothing is marked.`);
  const m = measurer(font.family, font.weight);
  const em = words.map(
    (w, i) => m(w) + (marks[i] && !marks[i - 1] ? EDGE : 0) + (marks[i] && !marks[i + 1] ? EDGE : 0),
  );
  const space = m("a a") - m("aa");
  const maxW = (spec.width ?? CENTER_W) / PUNCH;
  const max = Math.round(spec.max * scale);
  const min = Math.round(spec.min * scale);

  const widest = Math.max(...em);
  if (widest * min > maxW) {
    const word = words[em.indexOf(widest)];
    throw new Error(
      `${label}: "${word}" is too wide for the screen even at the smallest size. Shorten it, break it up, or move it to the caption.`,
    );
  }

  type Cand = { size: number; lines: number[][]; cost: number };
  let best: Cand | null = null;
  for (let size = max; size >= min; size -= 2) {
    const px = em.map((w) => w * size);
    const sp = space * size;
    if (Math.max(...px) > maxW) continue;
    const fewest = wrap(px, sp, maxW).length;
    for (let n = fewest; n <= spec.maxLines; n++) {
      if (n * size * font.lineHeight > spec.height) break;
      // Narrowest measure that still gives n lines: balanced lines.
      let lo = Math.max(...px);
      let hi = maxW;
      for (let k = 0; k < 18; k++) {
        const mid = (lo + hi) / 2;
        if (wrap(px, sp, mid).length <= n) hi = mid;
        else lo = mid;
      }
      const lines = wrap(px, sp, hi + 0.5);
      if (lines.length !== n && n > fewest) continue;
      const lw = lines.map((l) => lineWidth(l, px, sp));
      const longest = Math.max(...lw);
      const ragged = lw.reduce((a, w) => a + ((longest - w) / maxW) ** 2, 0);
      // No line of a single word (worst on the last line), unless the text is that short.
      const lonely = words.length > 2 ? lines.filter((l) => l.length === 1).length * 0.2 : 0;
      const widow = lines.length > 1 && lines[lines.length - 1].length === 1 && words.length > 2 ? 0.1 : 0;
      const cost = (max - size) / max + 0.3 * Math.max(0, lines.length - 3) + lonely + widow + 0.05 * ragged;
      if (!best || cost < best.cost) best = { size, lines, cost };
    }
  }

  if (!best) {
    const lines = wrap(em.map((w) => w * min), space * min, maxW);
    const msg = spec.tooLong ?? `${label}: ${clip(raw)} is too long for one screen (${words.length} words). Split it into two scenes or cut words.`;
    if (spec.strict) throw new Error(msg);
    warnings.push(msg);
    best = { size: min, lines, cost: 9 };
  }
  return {
    fontSize: best.size,
    lines: best.lines.map((l) => l.map((i) => words[i])),
    marks: best.lines.map((l) => l.map((i) => marks[i])),
  };
};

/** One line, as large as fits: for numbers and ranks. */
const fitLine = (
  parts: { text: string; rel: number; numeric?: boolean }[],
  theme: Theme,
  max: number,
  min: number,
  label: string,
  what: string,
  boxW: number = CENTER_W,
): Block => {
  const font = FONTS[theme.font];
  const scale = FONT_SCALE[theme.font];
  const width = parts.reduce((a, p) => a + measurer(font.family, font.weight, p.numeric)(p.text) * p.rel, 0);
  const maxW = boxW / PUNCH;
  const size = Math.min(Math.round(max * scale), Math.floor(maxW / width));
  if (size < Math.round(min * scale)) {
    throw new Error(`${label}: the ${what} "${parts.map((p) => p.text).join("")}" is too wide for the screen. Shorten it (for big numbers use a suffix, e.g. value "8" with suffix "B").`);
  }
  return { fontSize: size, lines: [[parts.map((p) => p.text).join("")]], marks: [[false]] };
};

const countWords = (s?: string | null) => (s ? s.trim().split(/\s+/).filter(Boolean).length : 0);
const read = (s?: string | null) => (s ? Math.max(s.length / CPS, countWords(s) * PER_WORD) : 0);
const asList = (h?: string | string[]) => (h == null ? [] : Array.isArray(h) ? h : [h]);

const need = (s: Scene, label: string, fields: (keyof Scene)[]) => {
  for (const f of fields) {
    if (s[f] == null || String(s[f]).trim() === "") throw new Error(`${label}: a "${s.type}" scene needs "${f}".`);
  }
};

/** Only plain numbers ("96.5", "1,200", "-3") count up; anything else is shown as written. */
export const statParts = (value: string | number) => {
  const str = String(value).trim();
  const plain = /^-?(\d{1,3}(,\d{3})+|\d+)(\.\d+)?$/.test(str);
  const num = plain ? Number(str.replace(/,/g, "")) : NaN;
  const decimals = (str.split(".")[1] ?? "").length;
  return { str, num, decimals, commas: str.includes(","), numeric: plain };
};

export const formatStat = (n: number, p: ReturnType<typeof statParts>) =>
  n.toLocaleString("en-US", { minimumFractionDigits: p.decimals, maximumFractionDigits: p.decimals, useGrouping: p.commas });

/** How a rank is shown: whole numbers as "#3", anything else ("01", "Bonus") as written. */
export const rankText = (rank: Scene["rank"]) =>
  rank == null ? "" : /^[1-9]\d*$/.test(String(rank)) ? `#${rank}` : String(rank);

export const planShort = async (props: ShortProps, fps: number) => {
  await loadFonts();
  const theme = resolveTheme(props.theme ?? undefined, props.font ?? undefined);
  const warnings: string[] = [];
  const pace = props.pace && props.pace > 0 ? props.pace : 1;
  if (props.pace != null && (props.pace < 0.85 || props.pace > 1.25)) {
    warnings.push(`pace ${props.pace} is outside 0.85 to 1.25. If the short feels slow, cut words; if it feels fast, add a scene.`);
  }
  if (!props.scenes?.length) throw new Error("The short has no scenes.");
  if (props.bpm != null && (props.bpm < 40 || props.bpm > 220)) throw new Error(`bpm ${props.bpm} is out of range (40 to 220).`);

  const items = props.scenes.filter((s) => s.type === "item").length;
  let itemNo = 0;
  const layout: SceneLayout[] = [];
  const secs: number[] = [];
  const needs: number[] = [];

  props.scenes.forEach((s, i) => {
    const label = `Scene ${i + 1} (${s.type})`;
    const hl = asList(s.highlight);
    const blocks: Record<string, Block> = {};
    let reveal = 0;
    let hold = 0;
    if (s.seconds != null && !(Number(s.seconds) >= 0.5)) throw new Error(`${label}: "seconds" must be at least 0.5.`);

    // An optional big word or number on its own line, above the text.
    const big = (maxMain: number) => {
      if (!s.big) return 0;
      const shownBig = theme.uppercase ? s.big.toUpperCase() : s.big;
      blocks.big = fitLine([{ text: shownBig, rel: 1, numeric: /\d/.test(s.big) }], theme, Math.min(330, maxMain * 1.9), maxMain * 1.1, label, "big text");
      return blocks.big.fontSize * 1.05 + 24;
    };

    switch (s.type) {
      case "hook":
      case "text": {
        need(s, label, ["text"]);
        const hook = s.type === "hook";
        const maxMain = hook ? 172 : 140;
        const used = big(maxMain);
        const mainMax = s.big ? Math.round(maxMain * 0.62) : maxMain;
        blocks.main = fitBlock(
          { text: s.text!, max: mainMax, min: s.big ? 60 : hook ? 96 : 74, maxLines: s.big ? 3 : hook ? 4 : 5, height: 820 - used, highlight: hl },
          theme,
          warnings,
          label,
        );
        const n = countWords(s.text) + countWords(s.big);
        reveal = Math.min(n * STAGGER, 0.8);
        hold = Math.max(0.8, read(`${s.big ?? ""} ${s.text}`));
        if (hook && n > 12) warnings.push(`${label}: the hook has ${n} words. Hooks that land in the first second are about 10 words or fewer.`);
        if (hook && i !== 0) warnings.push(`${label}: a hook works only as the first scene.`);
        if (!hook && n > 14) warnings.push(`${label}: ${n} words on one screen is a paragraph, not a beat. Split it so each scene says one thing.`);
        break;
      }
      case "stat": {
        need(s, label, ["value", "label"]);
        const p = statParts(s.value!);
        const shownValue = p.numeric ? formatStat(p.num, p) : p.str;
        blocks.value = fitLine(
          [
            ...(s.prefix ? [{ text: s.prefix, rel: AFFIX }] : []),
            { text: shownValue, rel: 1, numeric: p.numeric },
            ...(s.suffix ? [{ text: s.suffix, rel: AFFIX }] : []),
          ],
          theme,
          330,
          120,
          label,
          "number",
        );
        if (p.numeric && Math.abs(p.num) >= 1e6 && !p.commas) warnings.push(`${label}: write ${p.str} with commas, or as a smaller number with a suffix ("8" and "B"), so it reads at a glance.`);
        blocks.label = fitBlock({ text: s.label!, max: 96, min: 58, maxLines: 3, height: 300, highlight: hl }, theme, warnings, label);
        reveal = p.numeric ? 0.7 : 0.3;
        hold = Math.max(0.8, read(s.label)) + 0.2;
        break;
      }
      case "item": {
        need(s, label, ["title"]);
        itemNo += 1;
        const rank = theme.uppercase ? rankText(s.rank).toUpperCase() : rankText(s.rank);
        if (rank) blocks.rank = fitLine([{ text: rank, rel: 1, numeric: /\d/.test(rank) }], theme, 200, 90, label, "rank", LEFT_W);
        blocks.title = fitBlock({ text: s.title!, max: 124, min: 72, maxLines: 3, height: 340, width: LEFT_W, highlight: hl }, theme, warnings, label);
        if (s.text) blocks.body = fitBlock({ text: s.text, small: true, max: 64, min: 56, maxLines: 2, height: 170, width: LEFT_W }, theme, warnings, label);
        if (countWords(s.text) > 10) warnings.push(`${label}: the line under the title has ${countWords(s.text)} words. People skim it; keep it under 10.`);
        if (props.progress) blocks.progress = { fontSize: 40, lines: [[`${itemNo}/${items}`]], marks: [[false]] };
        reveal = 0.3 + Math.min(countWords(s.title) * STAGGER, 0.5);
        hold = Math.max(1.2, read(s.title) + 0.6 * read(s.text));
        break;
      }
      case "quote":
        need(s, label, ["text"]);
        blocks.main = fitBlock({ text: s.text!, max: 104, min: 62, maxLines: 7, height: 700, width: LEFT_W - 52, highlight: hl }, theme, warnings, label);
        if (s.author) blocks.author = fitBlock({ text: s.author, small: true, max: 52, min: 48, maxLines: 2, height: 140, width: LEFT_W - 52 }, theme, warnings, label);
        reveal = Math.min(countWords(s.text) * STAGGER, 1.2);
        hold = Math.max(1.4, read(s.text) + 0.3);
        break;
      case "end":
        need(s, label, ["text"]);
        blocks.main = fitBlock({ text: s.text!, max: 140, min: 76, maxLines: 4, height: 520, highlight: hl }, theme, warnings, label);
        if (s.sub) blocks.sub = fitBlock({ text: s.sub, small: true, max: 64, min: 56, maxLines: 2, height: 170 }, theme, warnings, label);
        if (props.handle) blocks.handle = fitBlock({ text: props.handle, small: true, max: 52, min: 44, maxLines: 1, height: 80, strict: true }, theme, warnings, `${label} handle`);
        reveal = Math.min(countWords(s.text) * STAGGER, 0.8);
        hold = Math.max(1.4, read(s.text) + 0.6 * read(s.sub));
        if (i !== props.scenes.length - 1) warnings.push(`${label}: an end scene works only as the last scene.`);
        break;
      default:
        throw new Error(`${label}: unknown scene type "${(s as Scene).type}". Use hook, text, stat, item, quote or end.`);
    }
    const needed = ENTRY + 0.4 * reveal + hold;
    // Floors so a number or list item stays up long enough to register after it lands.
    const floor = s.type === "stat" ? 2.0 : s.type === "item" ? 1.8 : 1.0;
    let sec = Math.min(Math.max(needed / pace, floor), 8);
    if (s.seconds != null) sec = Number(s.seconds);
    secs.push(sec);
    needs.push(needed);
    layout.push({ from: 0, frames: 0, reveal: Math.max(1, Math.round(reveal * fps)), blocks });
  });

  if (props.footer) {
    const f = fitBlock(
      { text: props.footer, small: true, max: 40, min: 34, maxLines: 2, height: 110, tooLong: `The footer is too long; shorten it to one line ("Data: USGS").` },
      theme,
      warnings,
      "footer",
    );
    if (f.lines.length > 1) warnings.push(`The footer wraps to two lines; shorten it to one ("Data: USGS").`);
    layout.forEach((l) => (l.blocks.footer = f));
  }

  // Cut points. With a tempo, each cut moves to the next beat (never earlier).
  let t = 0;
  let prevFrame = 0;
  const beat = props.bpm ? 60 / props.bpm : 0;
  secs.forEach((sec, i) => {
    t += sec;
    if (beat) t = Math.max(Math.ceil(t / beat - 0.15), Math.round(prevFrame / fps / beat) + 1) * beat;
    const end = Math.max(Math.round(t * fps), prevFrame + 1);
    layout[i].from = prevFrame;
    layout[i].frames = end - prevFrame;
    prevFrame = end;
    const actual = layout[i].frames / fps;
    if (actual < needs[i] * 0.75) {
      warnings.push(`Scene ${i + 1} (${props.scenes[i].type}): ${actual.toFixed(1)}s is too fast to read; it needs about ${needs[i].toFixed(1)}s.`);
    }
  });

  if (props.scenes[0].type !== "hook") warnings.push("Scene 1 is not a hook. The first second decides whether people stay; start with a hook scene.");
  if (props.scenes.length > 16) warnings.push(`${props.scenes.length} scenes is a lot for one short; cut to the strongest 8 to 12.`);
  void SAFE_H;

  return { theme, layout, warnings, durationInFrames: prevFrame, total: prevFrame / fps };
};
