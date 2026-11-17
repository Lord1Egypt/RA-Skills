# Editorial print — the composition grammar

When the surface is a *page you read* rather than a UI you scan, these rules are what make it look
printed instead of decorated. They apply to web sheets, PDFs, LaTeX documents and slides alike.

For the dot screen itself (angles, cell maths, cutouts, sticker stock) load `halftone-art` and use
its `templates/halftone-core.js`.

## The rules

1. **Stock is never `#fff`; ink is never `#000`.** Warm stock `#F2EEE2`–`#FDF3E3`, press black
   `#12100E`–`#1D1D1D`. That pairing alone is most of the print illusion.
2. **Rectilinear.** `border-radius: 0`. 1px hairlines for internal separators, 1.5px where the
   composition changes.
3. **Three faces, no more.** High-contrast Didone (or a strong display face) for display, a quiet
   grotesque for body, mono for captions. Captions uppercase, 9.5–11px, `0.14–0.2em` tracking.
   Body copy never in the display face — at 14px its hairlines disappear.
4. **One photographic panel per section; flat fields everywhere else.** Halftone the panel, not the
   page. Halftone everything and there is no figure/ground.
5. **Metadata strips earn their space.** Fill composition voids with the numbers a press sheet would
   carry — ruling, angles, register, plate count, inks — never with decoration.
6. **Number and caption everything.** `01 — the inks`, `02 — also pulled`, with a mono caption under
   every plate. The numbering is what makes a page read as a studio sheet.
7. **Highlights go to paper, shadows go solid.** If neither end is clean, the screen (or the
   gradient, or the photo treatment) is wrong.

## Composition recipes

| recipe | structure |
|---|---|
| **Masthead + plates** | rule · kicker · giant display line · lede · metadata strip ǀ hero plate |
| **Ink story** | two coverage ramps at their real angles, plus the overprint |
| **Swatch ledger** | 4 flat chips, hex + share + role under each |
| **Type in dots** | one enormous word masked into the screen, nothing else in the band |
| **Component kit** | buttons, input, pills, code, table — the system proving itself |
| **Specimen grid** | same subject at 4 cell sizes (5/8/12/18 px), mono captions |

## Type in dots (CSS mask)

```css
.halftone-type {
  font-family: 'Bodoni Moda', serif; font-weight: 700; text-transform: uppercase;
  color: var(--accent);                       /* leave background UNSET */
  -webkit-mask-image: radial-gradient(circle at 50% 50%, #000 58%, transparent 61%);
  mask-image: radial-gradient(circle at 50% 50%, #000 58%, transparent 61%);
  -webkit-mask-size: 5.2px 5.2px; mask-size: 5.2px 5.2px;
  -webkit-mask-repeat: round; mask-repeat: round;
}
```

A background on the element turns the glyph box into a solid bar — the mask eats the box too. Never
below 40px type; 5–6px pitch at 100–200px.

## Pitfalls

1. **A Didone's hairline serifs look like a rendering ghost.** At 120px+ the top serifs of M, A and I
   detach visually from the stem. Before "fixing" the font, measure the edge profile: serifs give
   dark runs of `8, gap 8, 60`; a real double-paint gives a *second full letterform* offset 2–4px.
2. **Font weight ranges.** `wght@0,400;0,600;0,700` returns the variable file; pin the exact faces
   (`ital,wght@0,700;1,400`) — smaller and predictable.
3. **Rotated overlays need `inset: -40%`** before rotation, or corners go empty.
4. **`printToPDF` drops canvases.** Re-render plates as images for any print export.
5. **A rotated halftone is not re-screenable.** Separate it into per-ink tone maps first (downsample
   ~6×, blur, then screen the tone at your own angles) or you get moiré.
6. **Headless screenshots can drop canvas layers** — flatten canvases to CSS backgrounds before
   capture.
7. **Two sources of truth rot.** If the page shows a ratio table, it must read it from the token
   JSON the build produced.

## Worked example

`~/Downloads/JACKAL_THEME_ENGINE` — 150-theme marble engine, specimen sheet, previews. Read
`preview/*.png` before starting; it is the reference for what "finished" looks like.
