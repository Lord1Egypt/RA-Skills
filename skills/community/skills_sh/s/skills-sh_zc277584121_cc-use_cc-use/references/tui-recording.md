# TUI / tmux session recording

A workflow for turning a live TUI session (Claude Code, Codex CLI, or any
ratatui-like full-screen app running in tmux) into a small, clean animated GIF
suitable for a README header, blog post, or docs page.

The point of this reference is not to lock in one canonical GIF spec. It is to
describe the pipeline, the principles behind each step, and the judgment calls
the outer agent should make in each session.

## When to use

Use this workflow when the user asks to:

- Record an inner cc-use'd CC TUI doing a demo.
- Capture a tmux pane running a TUI tool (vim, htop, k9s, lazygit, mfs, etc.)
  for documentation.
- Produce a GIF for a GitHub README, blog post, or release announcement.

If the goal is real-time screen video (with cursor, window chrome, OS desktop),
use a screen recorder instead — this pipeline records terminal state only, not
pixels.

## Toolchain

| Tool | Role | Where it comes from |
|---|---|---|
| `asciinema` | Record terminal as a timestamped JSON cast | apt / brew / pip |
| `agg` | Render cast to animated GIF | `cargo install --locked --git https://github.com/asciinema/agg` or brew |
| `gifsicle` | Optimize / quantize GIF | apt / brew |
| `Pillow` (optional) | Crop cruft, add window chrome | `uv add pillow` in throwaway project |
| `fonts-noto-color-emoji` (optional) | Render emojis in agg output | apt / brew |

## Dependency check

Before doing any work, probe the host:

```bash
which asciinema agg gifsicle
fc-list | grep -i emoji
python3 -c "from PIL import Image" 2>&1
```

Report what is missing. **Ask the user before installing anything**, listing
the install commands and what each tool is for. Do not install silently.

Reasonable installers:

- Linux (apt): `sudo apt-get install -y asciinema gifsicle fonts-noto-color-emoji`
- macOS: `brew install asciinema agg gifsicle`
- Linux `agg`: `cargo install --locked --git https://github.com/asciinema/agg`
  (Rust toolchain required; takes a couple of minutes the first time.)
- Pillow: do this inside a scratch `uv init --bare` project rather than polluting
  the system Python.

## Recording method

The recording target is a tmux session — either one already started by cc-use
(`ccu-<project>`) or a fresh tmux session created for the demo. The general
pattern is:

1. Ensure the inner tmux session exists and is at a stable starting state.
2. Background-start `asciinema rec` wrapped around `tmux attach -r -t <session>`
   with a hard `timeout` cap. Read-only attach prevents asciinema from
   accidentally delivering keystrokes into the inner session.
3. In the foreground, drive the demo via `cc-use delegate ...` or `tmux
   send-keys`. The inner session renders output; asciinema captures it.
4. Wait for the asciinema timeout to detach and finalize the cast.

A worked example (writing to a project-local scratch dir):

```bash
OUT=/path/to/project/tmp/recording-$(date +%s)
mkdir -p "$OUT"

( asciinema rec -y --overwrite \
    -c "timeout 50 tmux attach -r -t ccu-<project>" \
    --idle-time-limit 2 \
    "$OUT/demo.cast" > "$OUT/asciinema.log" 2>&1 ) &
ASCII_PID=$!

sleep 3   # let asciinema attach so initial state is captured

# Drive the demo (blocks until inner agent goes quiet)
<skill_dir>/scripts/cc-use delegate "<demo prompt>" \
    --project "$HOME/project" --agent claude \
    --initial-quiet-seconds 12

wait $ASCII_PID 2>/dev/null
```

Important details:

- `-r` (read-only attach) is critical. Without it, any stray input typed in the
  outer shell can interfere with the inner agent.
- `timeout 50` is the maximum recording window. Pick it to comfortably cover
  the demo duration + LLM latency budget + a small margin.
- `--idle-time-limit 2` lets the cast preserve long pauses as 2-second pauses,
  which keeps the cast file small.
- When asciinema is run from the outer agent's `Bash` tool (no real TTY), the
  PTY defaults to 80×24. To record at a specific size, ask the user to run the
  pipeline from their interactive terminal at the desired window size, or use
  `tmux set-option -t <session> window-size manual; tmux resize-window
  -t <session> -x W -y H` before starting the recording.

## Always keep the .cast file

A `.cast` is small (kilobytes), is the canonical intermediate, and contains
every keystroke and ANSI sequence with timestamps. Keep it indefinitely.

The agent (now or in a later session) can re-derive any GIF from the cast:

- Re-render with a different theme, font, or speed without re-recording.
- Edit cast events directly (cut idle segments, speed up a region, insert a
  pause) — it is plain JSON-lines.
- Re-quantize idle compression at render time without touching the source.

Never auto-delete cast files as part of cleanup. Treat them the way you treat
source code, not the way you treat build artifacts.

## Rendering principles (agg)

For README-grade GIFs, aim for the **pixel-perfect** look rather than the
**smooth/realistic** look. The reason is GIF's palette limit: anti-aliased text
introduces dozens of subtle edge colors that GIF quantization mangles into
visible "fuzz". Pure-color rendering avoids the problem entirely.

Principles:

1. **Disable font anti-aliasing**: `--font-antialiasing off`
   - Each glyph collapses to a binary foreground / background mask.
   - Palette shrinks dramatically — often to fewer than 32 distinct colors.
   - GIF quantization becomes effectively lossless.
2. **Increase font size**: `--font-size 22` (or 28 for high-density / slide use)
   - Larger glyphs make the aliased stair-steps disappear visually.
   - Larger glyphs also help readability when the GIF is embedded at thumbnail
     scale in a README.
3. **Pick a small-palette theme**: `monokai`, `dracula`, `solarized-dark`,
   `nord`. Avoid themes with subtle gradients.
4. **Speed up + clamp idle**: `--speed 1.5 --idle-time-limit 1.5 --fps-cap 30`.

A baseline command:

```bash
agg --theme monokai \
    --font-size 22 \
    --font-antialiasing off \
    --speed 1.5 \
    --idle-time-limit 1.5 \
    --fps-cap 30 \
    "$OUT/demo.cast" "$OUT/demo.raw.gif"
```

## Optimization (gifsicle)

With anti-aliasing off, `gifsicle` is usually **lossless and still effective**
because the source palette is already tiny:

```bash
gifsicle -O3 --colors 32 "$OUT/demo.raw.gif" -o "$OUT/demo.opt.gif"
```

Do NOT reach for `--lossy=N` by default. Lossy quantization is designed to
smooth over photographic gradients; on pure-color terminal output it tends to
introduce noise rather than reduce size. Try lossy only if the file is too
large for the target platform after lossless `-O3 --colors`.

## Produce a slate of options, not one canonical GIF

Do not lock the user into one resolution / quality combination. Render a small
panel of variants and let them pick:

| Variant | Font | Typical use | Typical size for 30s |
|---|---|---|---|
| compact | 16 | inline screenshot in dense docs | 70–90 KB |
| standard | 22 | README header on a small project | 90–120 KB |
| hi-dpi | 28 | screencast for slides or blog | 130–180 KB |

Produce all three, report the file paths and sizes, and let the user pick. If
the user has stated a target (e.g., "this is for a README header"), bias the
recommendation but still render the other variants so they can compare.

Do not render more than 3 variants by default. The user only ever picks one.

## Cropping bottom cruft

When recording a TUI in tmux, the bottom of every frame typically contains
content the user does NOT want in the final GIF:

- Tmux status bar (full-width row with session name, time).
- Shell prompt info that leaked through (e.g., `user@host:`).
- TUI footer hints ("bypass permissions on (shift+tab to cycle)" etc.).

Do not hard-code a fixed crop ratio or a brittle pixel-pattern detector. The
right cut depends on the TUI and the theme. Apply the principles below; the
outer agent has eyes — use them.

### What to look at

Pick a **busy mid-recording frame**, not the very last frame. The very last
frame of a `tmux attach` recording is often a cleared screen because the
alternate screen buffer was restored when tmux client detached. Look at a frame
about 50%–80% through the recording, where the TUI is still rendered.

Convenient way to grab one for inspection:

```bash
# Extract frame 20 of the GIF as PNG
python3 -c "from PIL import Image; \
  img = Image.open('demo.raw.gif'); img.seek(20); \
  img.convert('RGB').save('frame.png')"
```

Then read it.

### Decision principles

For each candidate cut, look at the frame and decide based on these rules:

1. **Tmux status bar** (if present): scan rows from the bottom. A row where
   almost every pixel is the same saturated color is the status bar.
   Everything from that row down is recording artifact and must go.

2. **Shell / agent footer** (just above the status bar): inspect a few rows up
   from the status bar. If they show shell prompt info or hint text the user
   did not ask to display, cut them too.

3. **User-meaningful bottom edge**: this is the row to keep as the last visible
   row in the output. Identify by what the TUI looks like:

   - Claude Code / Codex CLI: there is a visible input box with a top and
     bottom border (a long horizontal rule of `─` or `═`). The bottom border
     is the natural last row. Keep through it (+ a few pixels of padding).
   - Plain REPL prompts (`>`, `❯`, `$`): there is no border. The prompt row
     itself is the last row. Keep through it.
   - Full-screen TUIs without a distinct input area (vim, top, htop, k9s):
     there is no footer line to cut. The status bar is the only thing to
     remove.
   - Custom TUIs without recognizable structure: pick a row by content. If
     unsure, err on the side of keeping too much rather than cutting into
     real content.

4. **Sanity check after cropping**: render the cropped result, look at a
   busy frame, confirm that real content is intact. If the cut went into
   meaningful pixels, raise the crop boundary by one row-height and retry.

### Pseudocode

```text
frame = pick_busy_frame(gif)   # not the last frame

status_top = scan_from_bottom(frame, predicate = uniform_saturated_row)
if status_top is None:
    # no tmux status bar; the TUI fills to the screen edge
    cut_y = frame.height
else:
    # there is a status bar; check the rows above it for cruft
    cruft_top = status_top
    for row in rows_above(status_top, up_to = 5):
        if looks_like_shell_or_hint_text(row):
            cruft_top = row.y

    # now find the meaningful bottom edge above cruft_top
    if tui_has_visible_border():
        cut_y = bottom_border_row + few_pixels_padding
    elif tui_has_prompt_only():
        cut_y = prompt_row + few_pixels_padding
    else:
        cut_y = cruft_top  # safe default

return cut_y
```

This is pseudocode on purpose. Implement it as small judgment calls each time
the agent processes a recording, not as a frozen script. Themes change, TUIs
change, font sizes change — a frozen script ages badly.

### Hard fallback

If the agent really cannot decide (e.g., batch processing with no chance to
inspect), the safest no-knowledge cut is:

- Remove only the bottom `gif_height / cast_rows` pixels — exactly one
  cast-text-row. This kills the tmux status bar (if any) and nothing else.

This preserves more than wanted but never destroys real content.

## Adding window chrome

A fake macOS-style window frame is purely cosmetic and can be a fixed script —
there is no judgment call here.

Composite onto each cropped frame:

- A solid horizontal title bar at the top (~36 px tall, dark gray for a dark
  theme; light gray for a light theme).
- Three traffic-light circles on the left of the title bar (red, yellow,
  green).
- A 1px separator line between title bar and content.

Pillow snippet:

```python
TITLE_H = 36
DOT_R = 7
DOT_GAP = 10
DOT_LEFT = 18
TITLE_BG = (40, 40, 44)
BORDER = (60, 60, 64)
TRAFFIC = [(255, 95, 87), (254, 188, 46), (40, 200, 64)]

canvas = Image.new("RGB", (w, h + TITLE_H), TITLE_BG)
canvas.paste(frame, (0, TITLE_H))
draw = ImageDraw.Draw(canvas)
draw.line([(0, TITLE_H - 1), (w, TITLE_H - 1)], fill=BORDER)
cx = DOT_LEFT
for color in TRAFFIC:
    draw.ellipse(
        [(cx - DOT_R, TITLE_H // 2 - DOT_R),
         (cx + DOT_R, TITLE_H // 2 + DOT_R)],
        fill=color,
    )
    cx += DOT_R * 2 + DOT_GAP
```

Do not add rounded corners by default. GIF alpha is binary, so rounded corners
look jagged. Keep the rectangle.

If the user has a strong preference (Linux GTK style, Windows style, no chrome
at all), respect it — chrome is the easiest thing to change.

## Output location

Put intermediate and final files in one directory under the project, named
unambiguously. Preferred order:

- `<project>/tmp/recording-<timestamp>/`
- `<project>/.tmp/recording-<timestamp>/`
- `<project>/.cc-use/recordings/<timestamp>/` (only if no good project home)

Always report the exact paths of every artifact back to the user. The cast
path matters because they may want to re-render later.

## End-to-end checklist

1. Probe dependencies; ask the user before installing anything.
2. Confirm or create the inner tmux session.
3. Decide an output directory under the project; create it.
4. Start `asciinema rec` in background, wrapped around `tmux attach -r` with a
   timeout.
5. Drive the demo (cc-use `delegate` or direct `tmux send-keys`).
6. Wait for the asciinema timeout; verify the cast file exists and is non-empty.
7. Render 2–3 GIF variants with `agg --font-antialiasing off` at different
   font sizes.
8. Optimize each with `gifsicle -O3 --colors N` (lossless first; reach for
   `--lossy` only if size requires it).
9. Inspect a busy mid-recording frame; decide the crop policy from principles.
   Crop all frames.
10. Composite the macOS-style window chrome.
11. Report every artifact path and file size to the user. Recommend one variant
    based on their stated target (README header, slides, etc.).
12. Keep the cast file. Do not auto-delete intermediates.

## When to stop and ask the user

- Dependencies missing → list and ask before installing.
- Output target dimensions / theme / font unspecified → propose defaults but
  let them override.
- Recording longer than ~2 minutes → confirm intent (long cast files and
  long renders cost minutes).
- Cropping decision ambiguous (no visible border, theme out of distribution) →
  show the frame and ask.
- User uses a non-mac chrome style or wants no chrome at all → ask before
  composing.
