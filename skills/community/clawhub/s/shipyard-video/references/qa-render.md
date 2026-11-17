# Check with stills, then render

All commands run inside `<appDir>/video` (use `cd "<appDir>/video" && ...`). `scripts/stills.mjs` and `scripts/vspecs.mjs` belong to the video engine, not to the Shipyard plugin: they exist only after `video-setup.mjs` has copied the engine into that folder. One command at a time, in the foreground.

## Stills first (cheap)

```
node scripts/stills.mjs <tag> light                 # one frame near the end of every scene, tiled
node scripts/stills.mjs <tag> dark
VERTICAL=1 COLS=6 node scripts/stills.mjs <tag> light $(node scripts/vspecs.mjs <tag>)   # on Windows run vspecs first and paste its output
SILENT=1 node scripts/stills.mjs <tag> light
```

Stills land in `out/stills/`. Open each sheet with the Read tool and look. Check:

- cropped or empty frames, text running out of its box
- a cursor or highlight ring that is not on its target
- wrong or invented claims, wrong spelling of the product name
- light and dark looked at separately (low contrast shows up in only one)
- phone cut: content cut off at the edges, captions covering the UI
- the same fake scenario everywhere

Real-app footage, also check:

- each scene shows the right moment of its recording, not an earlier frame (a long recording in a short scene is where this goes wrong)
- the text in the recording is sharp at the zoom the camera uses
- the phone cut follows the part of the page the voice talks about
- every moment that must match a sound: the word spoken and the word on screen land together

To find a moment in a recording (a bar appearing, a price changing), `node scripts/scan.mjs <video.mp4> <x,y,w,h>` prints when that box changes colour. To measure how far the page lags a sound, make a tile of frames with their times (`ffmpeg -ss <s> -t 2 -i <video.mp4> -vf "fps=10,scale=480:-1,tile=5x4" tile.jpg`) and look.

Fix, run the stills again for the changed scenes (`<scene>@<frame>` picks a frame, for example `add@60`), repeat. Only then render.

## Render

```
node "${CLAUDE_PLUGIN_ROOT}/scripts/video-render.mjs" <appDir> <tag>:light
node "${CLAUDE_PLUGIN_ROOT}/scripts/video-render.mjs" <appDir> <tag>:dark <tag>:light::vertical <tag>:light::silent
```

A cut is `<tag>:<theme>[:<music>][:silent][:vertical]`. Cuts run one after the other. For each one the script prints:

- the mp4 path and a contact sheet path. Read the sheet.
- a dead-air warning if a stretch of 0.5 s or more is frozen. Fix it: lower `minSec` or `holdSec` in the script and run the voice step again (voice for lines that did not change is reused, so it costs nothing extra), or add motion (`Drift`) to that moment. `--strict` makes dead air a failure.
- loudness: average and loudest level, and a note if the sound may crackle or is too quiet.

After every render: nothing cropped wrongly, late animations not cut off, voice clear, no wrong claims. Silent cut: the captions read well without sound.

## Music (optional)

None ships. To add one: a royalty-free source whose licence you have read and that allows this use; normalise it (`ffmpeg -i in.mp3 -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -b:a 192k public/music/<name>.mp3`); render with `<tag>:light:<name>`; record the source and licence in `public/music/SOURCES.txt`. Avoid sources that only allow YouTube use or non-commercial use. The music is ducked under the voice automatically.

## Memory and disk

- Each render adds several MB to `video/out/`. Delete old renders when you are done (`out/` is not committed).
- A render needs a few GB of free disk to work in; `video-render.mjs` will not start one with less than 3 GB free, and it removes Remotion's working folder (about 250 MB per render) from the temp folder afterwards.
- "Could not extract frame from compositor ... disk space is low" means the computer ran out of memory or disk, not a bug in the scenes. Close other apps, free disk space, and render again with `--low-memory` (one frame at a time, a smaller frame cache: slower). Long real-app footage needs it most.
- One render at a time, in the foreground, on the whole computer. `video-render.mjs` does not start while another video render runs (another project or chat), and never removes that render's working folder. Never check with `pgrep -l` or `-fl`: they print other programs' settings, keys included.
