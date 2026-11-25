# VHS tape DSL reference

A `.tape` is a sequence of commands executed top to bottom against a live PTY.
Comments start with `#`. Generate a starter with `vhs new demo.tape`, render with
`vhs demo.tape`.

## Table of contents

- [Output commands](#output-commands)
- [Settings (`Set`)](#settings-set)
- [Typing and keys](#typing-and-keys)
- [Timing](#timing)
- [Hiding setup (`Hide` / `Show`)](#hiding-setup-hide--show)
- [Other commands](#other-commands)
- [Sizing the canvas (and the real trap: undersizing)](#sizing-the-canvas-and-the-real-trap-undersizing)
- [Annotated example: a still PNG](#annotated-example-a-still-png)
- [Annotated example: a motion GIF](#annotated-example-a-motion-gif)

## Output commands

| Command | Effect |
|---|---|
| `Output demo.gif` | Record the whole session to an animated GIF. |
| `Output demo.mp4` | Record to MP4 (smaller than GIF for long/complex motion; needs a player). |
| `Output demo.webm` | Record to WebM. |
| `Output frames/` | Write the raw PNG frame sequence to a directory (advanced). |
| `Screenshot still.png` | Capture a **single frame** at this point in the script. |

You can have multiple `Output` lines (emit gif + mp4 in one run) and multiple
`Screenshot` lines (capture several stills mid-session). **`Output x.png` is NOT
a still** — it records a frame sequence directory. For a single image use
`Screenshot`.

## Settings (`Set`)

Set these near the top, before the session starts.

| Setting | Purpose | Notes |
|---|---|---|
| `Set Shell "bash"` | Shell to spawn. | `bash` is the most predictable for scripted setup. |
| `Set FontSize 14` | Font size in px. | The main size lever — bump it to make the whole capture bigger. ≈18-22 reads well. |
| `Set FontFamily "..."` | Font. | Pick one present on the render machine. |
| `Set Width 1200` | Output width in **pixels**. | Usually omit it — VHS defaults to 1200. Extra width becomes right margin, not wider text. |
| `Set Height 700` | Output height in **pixels**. | Usually omit it — VHS defaults to 600. |
| `Set Padding 30` | Window padding in px. | VHS's default padding is generous (~60px/side); set it lower for a tighter frame. |
| `Set Theme "Catppuccin Mocha"` | Terminal colour theme. | Use a named VHS theme, or a JSON palette object. Lock this for determinism. |
| `Set CursorBlink false` | Stop cursor blink. | Removes frame-to-frame noise. |
| `Set TypingSpeed 50ms` | Delay between typed chars. | Lower = faster typing. Set `0ms` for instant. |
| `Set LoopOffset 50%` | Where the GIF loop "starts" when embedded. | Cosmetic. |
| `Set PlaybackSpeed 1.0` | Speed multiplier for the final render. | |
| `Set WindowBar Colorful` | Draw a fake title bar (traffic lights). | Optional chrome; many pipelines draw their own. |
| `Set Margin` / `Set MarginFill` | Outer margin + fill colour. | Optional framing. |

## Typing and keys

| Command | Effect |
|---|---|
| `Type "text"` | Type literal characters (respects `TypingSpeed`). |
| `Type@10ms "text"` | Override typing speed for this line. |
| `Enter` | Press Return. `Enter 3` presses it 3×. |
| `Backspace` / `Tab` / `Space` / `Escape` | The named keys. All accept a count. |
| `Up` `Down` `Left` `Right` | Arrows (accept a count: `Down 5`). |
| `Ctrl+C` `Ctrl+D` `Ctrl+L` | Modifier combos. |
| `Alt+.` `Shift+Tab` | Other modifiers. |
| `PageUp` / `PageDown` | Paging keys. |
| `Sleep 800ms` / `Sleep 2s` | Pause (see Timing). |

To send an app-specific chord (two keys the app reads as a unit), type them
together: `Type "gd"` rather than `Type "g"` then `Type "d"` — though a tiny
`Sleep` between them can be useful if you *want* the intermediate state on camera.

## Timing

`Sleep` is your camera-hold. Units: `ms` or `s`. Timing is the whole craft of a
good demo:

- Lead-in / settle before the first capture: enough for cold-start + data load.
- Hold after each meaningful action so a viewer can read it.
- Keep total duration tight — every second is frames, and frames are bytes.

## Hiding setup (`Hide` / `Show`)

Everything between `Hide` and `Show` executes but is **not recorded**. Use it for
the unglamorous setup so the recording starts on a clean, ready state:

```
Hide
Type "export PATH=/repo/node_modules/.bin:$PATH" Enter   # unquoted $PATH!
Type "export MYAPP_NOW=2024-01-15T12:00:00Z" Enter        # pin time
Type "cd /tmp/fixture && clear" Enter
Show
Type "myapp ui" Enter
Sleep 2s
```

## Other commands

| Command | Effect |
|---|---|
| `Source other.tape` | Include another tape (share common setup). |
| `Require myapp` | Fail fast if `myapp` isn't on PATH before recording. |
| `Env KEY value` | Set an environment variable for the session. |

## Sizing the canvas (and the real trap: undersizing)

VHS sizes output in *pixels* (`Set Width`/`Set Height`), but the terminal renders
its character grid at the font's natural cell width. Worth knowing exactly how
those two interact, because it's easy to invent a problem that isn't there:

> **VHS does not stretch glyphs.** The grid is laid out at the font's real cell
> width, top-left aligned, and any leftover canvas is just margin. A too-wide
> `Width` gives you empty space on the right, not spread-out letters; a tight
> `Width` gives you a smaller image, not broken kerning. So the pixel count
> doesn't change how the text looks *at its own size* — you don't need to
> pixel-fit a `cols × multiplier` target, and a "mismatched" canvas won't smear
> the type.

> **The real trap is undersizing.** A small capture renders perfectly crisp on
> its own, but the moment a README or docs page scales it up to fill a content
> column, bitmap upscaling makes the text soft and blurry. That blur is what
> reads as "bad" — and it's a *scale* problem, not a rendering one.

**The reliable approach: pick a `FontSize` and let VHS size the canvas.** Omit
`Set Width`/`Set Height` entirely. VHS uses its roomy defaults (1200×600 at the
default font), which is large enough that pages rarely need to upscale it, so it
stays sharp. To make the capture bigger or smaller, change `FontSize` (≈18-22
reads well).

Only set explicit `Width`/`Height` when you genuinely need a fixed canvas across a
set of captures, and keep it generous. If a capture looks soft on your page, the
fix is almost always *bigger*, not different dimensions.

## Annotated example: a still PNG

```
# --- determinism + framing ---
Set Shell "bash"
Set FontSize 20         # readable; canvas left to VHS defaults (big enough to stay sharp)
Set Padding 24
Set Theme "Catppuccin Mocha"
Set CursorBlink false
Set TypingSpeed 50ms
# No Set Width/Height — VHS defaults render tight monospace. Set them only if you
# need a fixed canvas across many shots — and keep it generous so pages don't upscale it.

# --- hidden setup (not recorded) ---
Hide
Type "export PATH=/repo/node_modules/.bin:$PATH" Enter
Type "export MYAPP_NOW=2024-01-15T12:00:00Z" Enter   # pin relative dates
Type "cd /tmp/fixture && clear" Enter
Show

# --- the scene ---
Type "myapp ui --repo /tmp/fixture" Enter
Sleep 5s                # generous settle: cold-start + async load, stills get one frame
Type "gd"               # drive to the diff view
Sleep 1s
Screenshot myapp-diff.png
```

## Annotated example: a motion GIF

```
Set Shell "bash"
Set FontSize 20          # canvas left to VHS defaults — big enough to stay sharp when scaled
Set Padding 24
Set Theme "Catppuccin Mocha"
Set CursorBlink false
Set TypingSpeed 50ms

Output demo-views.gif    # motion → Output (gif), not Screenshot

Hide
Type "export PATH=/repo/node_modules/.bin:$PATH" Enter
Type "cd /tmp/fixture && clear" Enter
Show

Type "myapp ui --view history" Enter
Sleep 1500ms             # shorter settle than a still — loading frames read as startup
Type "gd"                # open diff
Sleep 2400ms             # hold so the viewer can read it
Escape
Sleep 600ms
Type "gb"                # switch to branches — show contrast
Sleep 2400ms
# NOTE: no trailing quit — end on the UI, not a shell prompt
```

After rendering, optimize losslessly:

```bash
gifsicle -O3 --batch demo-views.gif     # or scripts/optimize_gif.sh demo-views.gif
```
