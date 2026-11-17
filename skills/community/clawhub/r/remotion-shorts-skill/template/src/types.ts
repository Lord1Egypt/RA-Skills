export type SceneType = "hook" | "text" | "stat" | "item" | "quote" | "end";

export type Scene = {
  type: SceneType;
  /** Main words on screen (hook, text, quote, end, item body). */
  text?: string;
  /** hook and text: a word or number set very large on its own line above the text. */
  big?: string;
  /** Word or phrase (or list of them) to mark in the accent colour. */
  highlight?: string | string[];
  /** stat: the number, e.g. "96.5", "1,200", 40. */
  value?: string | number;
  prefix?: string;
  suffix?: string;
  /** stat: what the number means. */
  label?: string;
  /** item: the list position, e.g. 3. */
  rank?: number | string;
  /** item: the headline of the list item. */
  title?: string;
  /** quote: who said it. */
  author?: string;
  /** end: the smaller line under the main text. */
  sub?: string;
  /** Optional photo or video behind this scene (file in public/assets). */
  image?: string;
  /** Override the computed on-screen time. */
  seconds?: number;
};

export type Theme = {
  bg: string;
  fg: string;
  accent: string;
  /** Text colour on top of the accent box. */
  accentText: string;
  font: FontName;
  uppercase: boolean;
};

export type FontName = "Anton" | "Poppins" | "Inter";

export type Block = { fontSize: number; lines: string[][]; marks: boolean[][] };

export type SceneLayout = {
  from: number;
  frames: number;
  /** Frames the word-by-word reveal takes. */
  reveal: number;
  blocks: Record<string, Block>;
};

export type ShortProps = {
  theme?: string | Partial<Theme> | null;
  font?: FontName | null;
  fps?: number | null;
  /** 1 is normal. Above 1 is faster, below 1 slower. */
  pace?: number | null;
  /** Snap every cut to the beat of the music. */
  bpm?: number | null;
  music?: { src: string; volume?: number; start?: number } | null;
  /** Photo or looping video behind every scene. */
  background?: string | null;
  /** Small credit line, e.g. "Data: USGS". */
  footer?: string | null;
  /** Shown on the end scene, e.g. "@yourhandle". */
  handle?: string | null;
  highlightStyle?: "box" | "color" | null;
  /** Show "2/5" on list items. */
  progress?: boolean | null;
  /** Built-in sound effects (cut whoosh, highlight pop, count ticks, hook hit). On unless false. */
  sfx?: boolean | null;
  /** Sound effect volume, 0 to 1 (default 1). */
  sfxVolume?: number | null;
  scenes: Scene[];
  /** Filled in by calculateMetadata. */
  layout?: SceneLayout[];
  warnings?: string[];
  resolvedTheme?: Theme;
};
