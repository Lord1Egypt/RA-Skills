# Export

Read before producing a PDF, PNG, PPTX or MP4, and before telling the user what a format keeps. Every export starts from the built, self-contained file (`node scripts/build.mjs deck.html` writes `out/deck.html`), so what you export is what you linted. Every export is checked by opening it and looking, never by reading the script's log alone.

## Which format

| Format | Script | Use for | Keeps | Loses |
|---|---|---|---|---|
| HTML | `build.mjs` | presenting, sharing, archiving | everything: motion, boil, steps, sound, notes | nothing; needs a browser |
| PDF | `export-pdf.mjs` | sending, printing, reading | vector art, real text, fonts, every step shown | motion, boil, sound, click order, speaker notes |
| PNG | `shoot.mjs` | review, social cards, thumbnails | the still picture | text as text, motion, sound |
| PPTX faithful | `export-pptx.mjs --mode faithful` | presenting from PowerPoint or Keynote | the exact look, speaker notes, searchable text | editable text, motion, boil, sound |
| PPTX editable | `export-pptx.mjs --mode editable` | someone must change the words | real text boxes, notes | the handwriting, exact line breaks, motion |
| MP4 | `render-video.mjs` | explainer video, launch clip, recap | motion, boil, music and effects, timing | interaction, notes, pausing on a step |

Scripts live in `scripts/`. `doctor.mjs` checks Node, Playwright with Chromium, FFmpeg and fonts, and prints the exact fix for anything missing.

## PDF

```bash
node scripts/export-pdf.mjs out/deck.html              # -> out/deck.pdf
node scripts/export-pdf.mjs out/report.html -o report.pdf
```

- Opens the file with `?print`: every slide stacked at 1920 x 1080 px with a page break after each, every step revealed, counters at their final value, the boil stopped on variant 0, controls hidden, and each page carrying its own paper and sky.
- Decks get one 1920 x 1080 px page per slide. Other pages print as A4 unless the file sets its own `@page` size or margin.
- Vector: lines, hatching and text stay sharp at any zoom. Courier Prime is embedded as a font. Caveat, a variable font, is drawn by Chromium as vector glyphs with a Unicode map, so the text still selects and searches.
- The script counts pages and warns when they do not match the slide count.

**Check:** page count equals slide count and there is no blank last page; zoom to 400% on a hatched shape (it must stay crisp); search the PDF for one figure and one title word; look at the first and the busiest page at 100%.

## PNG

```bash
node scripts/shoot.mjs out/deck.html                          # 1920x1080 per slide, 390x844 of slide 1
node scripts/shoot.mjs out/deck.html --slides                 # every slide at every size
node scripts/shoot.mjs out/card.html --sizes 1200x800         # a postcard or social card
```

- Writes to `shots/<name>/` next to the file: `slide-01.png` ..., `slide-01-390x844.png`, `contact-sheet.png` (more sheets for long decks), or `page-1920x1080.png` for pages.
- Shoots with `?static` and reduced motion, so every drawing is complete and every step is visible.
- Exits 1 when the page logs an error or a request fails: a missing local file is a bug, not noise.
- Social sizes: 1200 x 800 (3:2 postcard) and 1080 x 1350 (portrait).

**Check:** open `contact-sheet.png`, then each image at full size. These are also the images for the review ([review.md](review.md)).

## PPTX

```bash
node scripts/export-pptx.mjs out/deck.html --mode faithful
node scripts/export-pptx.mjs out/deck.html --mode editable
```

| | Faithful | Editable |
|---|---|---|
| Slide art | each slide baked as one picture at 2x (3840 x 2160) | the drawn art (paper, pencil lines, sketches, props) as a picture |
| Text | the slide's text added as hidden text, for search, screen readers and copy | real text boxes at the same places, in a safe system font |
| Handwriting | kept, it is in the picture | lost: Caveat is replaced; figures go to a monospace system font |
| Speaker notes | from `data-notes` or `.sk-notes-speaker` | the same |
| Motion, boil, sound | none | none |
| Pick when | presenting or sending as PPTX | someone has to edit the words in PowerPoint |

PowerPoint renders fonts on the viewer's machine, which never has Caveat installed. That is why faithful mode bakes the handwriting into the picture and editable mode gives it up. Say which mode you used and what it loses when you deliver.

**Check:** open the file in PowerPoint, Keynote or LibreOffice. Slide count matches. Notes are present on two slides you pick. Faithful: zoom on a slide, the art is sharp. Editable: every text box fits its place (safe fonts run wider or narrower than Caveat, so look for overflow and odd line breaks), and no text box sits on top of the same words baked into the picture. If LibreOffice is available, convert the PPTX to PDF and look at the pages as images.

## MP4

```bash
node scripts/render-video.mjs out/deck.html --fps 30      # MP4 next to the built file; needs FFmpeg
```

How it works:

1. Opens the deck with `?video` (autoplay, no controls, no cursor) and replaces the page clock with a virtual one.
2. For each frame at t = n / 30 s: `SketchyDeck.seek(t)` sets the slide and its revealed steps, every CSS animation and transition from `document.getAnimations()` is set to its time, counters and the boil read the virtual clock, and the frame is captured at 1920 x 1080.
3. The soundtrack is rendered offline from the deck's `data-seed` with `SketchySound.renderOffline()`: music in the deck's `data-music` mood, changes at `data-music-section`, effects on page turns, stamps and steps (`sound.md`). Same seed, same piece, sample for sample.
4. FFmpeg encodes H.264, `yuv420p`, 1920 x 1080 at 30 fps, muxes the audio, and normalizes loudness to **-16 LUFS integrated with true peak below -1.5 dBTP**.

Length is the sum of every slide's `data-duration` (default 6 s). Steps reveal by themselves inside the first 60% of each slide ([motion.md](motion.md)), so give step-heavy slides more time.

What it loses: interaction, speaker notes, and some crispness on thin red lines (`yuv420p` halves the color resolution). What it keeps that no other format does: the boil, the page turns, the stamps, the music.

**Check:** watch it start to end with sound on. The first frame is the cover, not a blank page. Every page turn has its sound on the same frame. No slide cuts off before its stamp lands. Then measure:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 out/deck.mp4
ffmpeg -i out/deck.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -n 12   # I: about -16 LUFS, Peak under -1.5 dBFS
```

## Before you deliver

| Check | Done when |
|---|---|
| Built file opens from disk with no network | it renders with Wi-Fi off |
| Every export opened and looked at | not just generated |
| Counts match | PDF pages, PNG files and PPTX slides equal the slide count; MP4 duration equals the timeline |
| Losses stated | the report says what the chosen format drops (handwriting in editable PPTX, motion in PDF) |
| Paths given | the report lists the exact output paths |
