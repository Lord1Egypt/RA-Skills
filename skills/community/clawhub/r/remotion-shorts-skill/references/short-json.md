# short.json format

One JSON file is one short. File paths (music, images, video) are relative to the JSON file;
the renderer copies them into the project. URLs are refused: download the file first.

## Top level

| Field | Type | Default | What it does |
|---|---|---|---|
| `scenes` | array | required | The scenes, in order. See below. |
| `theme` | string or object | `"ink"` | `ink`, `paper`, `volt`, `ocean`, `clean`, or your own colours (below). |
| `font` | string | from theme | `Anton`, `Poppins` or `Inter`. Overrides the theme's font. |
| `highlightStyle` | string | `"box"` | `box` puts an accent block behind highlighted words; `color` colours them instead. |
| `sfx` | boolean | `true` | Built-in sound effects: a hit on the hook, a whoosh on each cut, a pop on highlights, ticks on count-ups. Made for this template, MIT, safe on every app. |
| `sfxVolume` | number | `1` | Sound effect volume, 0 to 1. Lower it to about 0.5 under music. |
| `progress` | boolean | `false` | Shows "2/5" above each list item, so viewers know how much is left. |
| `footer` | string | none | Small credit line at the bottom of the safe area, e.g. `"Data: USGS"`. Keep it to one line. |
| `handle` | string | none | Shown under the end scene, e.g. `"@yourhandle"`. |
| `pace` | number | `1` | Multiplies speed. `1.15` is 15% faster, `0.9` slower. Stay between 0.85 and 1.2. |
| `bpm` | number | none | Snaps every cut to the beat of the music (40 to 220). |
| `music` | object | none | `{ "src": "music.mp3", "volume": 0.5, "start": 12 }`: file, volume 0 to 1, seconds to skip. Fades in and out. |
| `background` | string | none | Photo or video file behind the whole short, dimmed under the theme colour. |
| `fps` | number | `30` | Frames per second. Leave it at 30. |

### Custom theme

```json
"theme": { "bg": "#0B1020", "fg": "#FFFFFF", "accent": "#FF5A36", "accentText": "#FFFFFF", "font": "Poppins", "uppercase": false }
```

Any field you leave out comes from `ink`. `accentText` is the colour of words on top of the
accent box. Check contrast: text on `bg`, and `accentText` on `accent`, should both be 7:1 or
better (WebAIM's contrast checker is fine for this).

## Scenes

Every scene can also take:

- `highlight`: a word or phrase, or a list of them, to mark in the accent colour. It must appear
  in the text exactly (case and punctuation don't matter). Every match is marked.
- `image`: a photo or video file behind this scene only.
- `seconds`: force the length. The renderer warns if it's too short to read.

### hook

The first scene. States the payoff. About 10 words or fewer.

```json
{ "type": "hook", "text": "5 free tools that replace a $300 design stack", "highlight": "$300" }
```

With a number, set it big on its own line with `big` and keep the rest short:

```json
{ "type": "hook", "big": "2.5%", "text": "of Earth's water is fresh" }
```

`big` works on `text` scenes too.

### text

One statement, set big. Up to about 14 words.

```json
{ "type": "text", "text": "Most of it is locked in ice", "highlight": "ice" }
```

### stat

A number that counts up, with a label under it. `value` is the number as text so you keep its
format (`"96.5"`, `"1,200"`, `"3"`); `prefix` and `suffix` are set smaller (`"$"`, `"%"`, `"x"`,
`"M"`). Only plain numbers count up; anything else (`"#1"`, `"24/7"`, `"1e6"`) is shown as
written. For big numbers use a suffix (`"8"` and `"B"`) or commas (`"8,000,000"`).

```json
{ "type": "stat", "prefix": "$", "value": "4.2", "suffix": "B", "label": "spent on coffee in a year", "highlight": "coffee" }
```

### item

One entry in a list: a big rank, a title and an optional line under it (under 10 words; people
skim it). Ranks that are whole numbers show as `#3`, for countdowns. For features or steps that
aren't a ranking, write the rank as `"01"`, `"02"` and it's shown as written. Leave `rank` out
for no number.

```json
{ "type": "item", "rank": 3, "title": "Penpot", "text": "Open-source design tool that runs in the browser." }
```

### quote

A quote with an accent bar and the speaker. Quote people accurately and only with a source.

```json
{ "type": "quote", "text": "Simplicity is prerequisite for reliability", "author": "Edsger W. Dijkstra" }
```

### end

The last scene: one action or a line that leads back into the hook. `sub` is a smaller line;
`handle` from the top level shows under it.

```json
{ "type": "end", "text": "Follow for part 2", "sub": "Tomorrow: the 3 paid ones worth it" }
```

## Templates (scene patterns)

- **Stat short (12 to 20 s):** hook, 2 to 4 stat scenes, end.
- **Top-N list (25 to 45 s):** hook with the promise, items counting down to #1, end. Put the
  best item last and say so in the hook so people stay.
- **Launch or changelog (15 to 35 s):** hook with what changed for the viewer, 3 to 5 item scenes
  (one feature each, in the user's words, ranks `"01"` to `"04"`, `progress` on), a stat if there
  is a real number, end with where to get it. Mark it `isYourBrand` on TikTok.
- **Quote (10 to 15 s):** hook with the context, quote, one text scene on why it matters, end.
- **Kinetic script (20 to 45 s):** hook, then text scenes, one sentence each, end.

## What the renderer decides for you

- **Font size and line breaks:** as large as fits, preferring 2 to 3 lines, no single word on
  the last line, lines of similar length. Never below a readable floor; room is kept for the
  highlight boxes and the small punch when the emphasis lands, so text never leaves the safe box.
- **Timing:** each scene lasts long enough to read: the longer of 0.3 s per word and 17
  characters per second, plus a moment to land. People read while the words appear, so the
  reveal mostly overlaps the reading. Stats get time for the count; the line under a list item
  counts at 60% because it's skimmed.
- **Safe box:** text stays between 288 px from the top, 672 px from the bottom, 96 px from the
  left and 192 px from the right, the strictest edge of TikTok, Reels and Shorts. Centred scenes
  use 192 px on both sides, so they sit on the true centre line of the frame; list items and
  quotes are left-aligned and use the full width.
