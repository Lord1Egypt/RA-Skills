import React from "react";
import { AbsoluteFill, Freeze } from "remotion";
import { Short } from "./Short";
import { HEIGHT, SMALL, WIDTH } from "./theme";
import type { SceneLayout, ShortProps } from "./types";

export const TILE = 0.3;
const GAP = 16;
const PAD = 24;
const LABEL = 44;

export type Tile = { frame: number; label: string };
export type SheetProps = ShortProps & { tiles?: Tile[]; cols?: number };

export const sheetSize = (n: number, cols: number) => {
  const rows = Math.ceil(n / cols);
  const c = Math.min(cols, n);
  return {
    width: Math.round(PAD * 2 + c * WIDTH * TILE + (c - 1) * GAP),
    height: Math.round(PAD * 2 + rows * (HEIGHT * TILE + LABEL) + (rows - 1) * GAP),
  };
};

/** Review sheet: the last frame of every scene (everything shown, punch at its largest). */
export const sceneTiles = (layout: SceneLayout[], props: ShortProps, fps: number): Tile[] =>
  layout.map((l, i) => ({ frame: l.from + l.frames - 1, label: `${i + 1}. ${props.scenes[i].type}  ${(l.frames / fps).toFixed(1)}s` }));

/** Cut sheet: frame 0, then around every cut the last frame before it and frames 0, 2, 4 and 8 after it. */
export const cutTiles = (layout: SceneLayout[], fps: number): Tile[] => {
  const tiles: Tile[] = [{ frame: 0, label: "frame 0" }];
  for (let k = 0; k < 4; k++) tiles.push({ frame: Math.min(layout[0].frames - 1, [3, 8, 15, 30][k]), label: `1: +${[3, 8, 15, 30][k]}` });
  layout.slice(1).forEach((l, i) => {
    tiles.push({ frame: l.from - 1, label: `end of ${i + 1}` });
    for (const d of [0, 2, 4, 8]) tiles.push({ frame: Math.min(l.from + d, l.from + l.frames - 1), label: `${i + 2}: +${d}` });
  });
  void fps;
  return tiles;
};

export const Sheet: React.FC<SheetProps> = (props) => {
  const tiles = props.tiles ?? [];
  const cols = props.cols ?? 4;
  return (
    <AbsoluteFill style={{ background: "#1b1b1f", padding: PAD, display: "grid", gridTemplateColumns: `repeat(${cols}, ${WIDTH * TILE}px)`, gap: GAP, alignContent: "start" }}>
      {tiles.map((t, i) => (
        <div key={i} style={{ width: WIDTH * TILE }}>
          <div style={{ height: LABEL, color: "#ddd", fontFamily: SMALL.family, fontWeight: 700, fontSize: 22, display: "flex", alignItems: "center" }}>{t.label}</div>
          <div style={{ width: WIDTH * TILE, height: HEIGHT * TILE, overflow: "hidden", position: "relative" }}>
            <div style={{ width: WIDTH, height: HEIGHT, transform: `scale(${TILE})`, transformOrigin: "top left", position: "absolute" }}>
              <Freeze frame={t.frame}>
                <Short {...props} guides mute />
              </Freeze>
            </div>
          </div>
        </div>
      ))}
    </AbsoluteFill>
  );
};
