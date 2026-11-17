import React from "react";
import { Composition } from "remotion";
import { planShort } from "./layout";
import { Sheet, cutTiles, sceneTiles, sheetSize, type SheetProps } from "./Sheet";
import { Short } from "./Short";
import { HEIGHT, WIDTH } from "./theme";
import type { ShortProps } from "./types";
import sample from "./sample.json";

// Studio shows the sample; renders pass their own props (render.mjs nulls every option they leave out).
const defaults = sample as ShortProps;

const plan = async (props: ShortProps) => {
  const fps = props.fps ?? 30;
  const p = await planShort(props, fps);
  return { fps, p, props: { ...props, fps, layout: p.layout, warnings: p.warnings, resolvedTheme: p.theme } };
};

const sheet = (mode: "scenes" | "cuts") => async ({ props }: { props: SheetProps }) => {
  const { fps, p, props: out } = await plan(props);
  const tiles = mode === "scenes" ? sceneTiles(p.layout, props, fps) : cutTiles(p.layout, fps);
  const cols = mode === "scenes" ? 4 : 5;
  const size = sheetSize(tiles.length, cols);
  // Same length as the short: frames past the end would be clamped.
  return { fps, durationInFrames: p.durationInFrames, width: size.width, height: size.height, props: { ...out, tiles, cols } };
};

export const Root: React.FC = () => (
  <>
    <Composition
      id="Short"
      component={Short}
      width={WIDTH}
      height={HEIGHT}
      fps={30}
      durationInFrames={300}
      defaultProps={defaults}
      calculateMetadata={async ({ props }) => {
        const { fps, p, props: out } = await plan(props);
        return { fps, durationInFrames: p.durationInFrames, props: out };
      }}
    />
    <Composition id="Sheet" component={Sheet} width={WIDTH} height={HEIGHT} fps={30} durationInFrames={1} defaultProps={defaults as SheetProps} calculateMetadata={sheet("scenes")} />
    <Composition id="Cuts" component={Sheet} width={WIDTH} height={HEIGHT} fps={30} durationInFrames={1} defaultProps={defaults as SheetProps} calculateMetadata={sheet("cuts")} />
  </>
);
