---
name: "swf-game-port-decompiler"
description: "Decompile SWF games for engine ports using FFDec/JPEXS."
---

# SWF Game Port Decompiler

Use this skill to decompile old Flash/SWF games into a porting workspace: code, assets, frame/sprite renders, tag structure, XML timeline data, and a short audit that helps rebuild the game in a modern engine.

## Requirements

- JPEXS Free Flash Decompiler / FFDec installed.
- Prefer `ffdec-cli.exe` on Windows or `ffdec`/`ffdec.sh` elsewhere.
- Java available if running FFDec from `ffdec.jar`.
- Python 3.9+ for the bundled orchestration script.
- Optional: ImageMagick/ffmpeg for later contact sheets, spritesheet processing, audio conversion, or video inspection.

## Safety And Scope

- Only decompile files the user owns or is authorized to port, preserve, research, or migrate.
- Treat decompiled ActionScript as reference, not clean source. Expect obfuscation, compiler artifacts, timeline-side code, generated names, and dead code.
- Never overwrite the original `.swf`. Write all output to a separate decompile folder.
- Do not run the SWF in Flash Player unless explicitly needed and isolated; FFDec extraction is safer than executing unknown SWFs.
- Port behavior by understanding gameplay systems, not by blindly translating every decompiled line.

## Main Workflow

1. Locate FFDec:
   - Windows common path: `C:\Program Files (x86)\FFDec\ffdec-cli.exe`.
   - Otherwise search PATH for `ffdec-cli`, `ffdec`, or `ffdec.sh`.
2. Create a clean output folder named after the SWF.
3. Run the full extraction:
   - `python scripts/ffdec_game_decompile.py full game.swf out/game-decompile`
4. Inspect the produced folders:
   - `code/actionscript` for AS1/AS2/AS3 source.
   - `code/pcodehex` for lower-level P-code when source is missing, wrong, or obfuscated.
   - `assets/images`, `assets/shapes_svg`, `assets/shapes_png`, `assets/sounds`, `assets/fonts`, `assets/text`, `assets/binary`.
   - `timelines/frames` for rendered main timeline frames.
   - `timelines/sprites` for rendered movie clips/sprites.
   - `structure/tags.txt`, `structure/movie.xml`, `structure/symbolClass.csv`.
   - `PORTING_AUDIT.md` for a generated first-pass map.
5. Reconstruct scene/frame structure:
   - Use `movie.xml` and `tags.txt` to identify `DefineSprite`, `PlaceObject`, `ShowFrame`, `DoAction`, `DoABC`, labels, exports, and symbol classes.
   - Use rendered `frame` and `sprite` exports to understand visual state changes that are hard to infer from code alone.
6. Build a porting map:
   - Identify entry points: document class, frame scripts, button actions, exported symbols, preloaders.
   - Identify systems: input, physics/movement, collision, enemy/projectile spawns, score/state, inventory, audio, level loading.
   - Pair assets with code references and symbol IDs.
   - Separate reusable engine assets from timeline-only artifacts.
7. For modern engine migration:
   - Prefer recreating gameplay architecture natively.
   - Use extracted images/audio/vector art as assets when licensing allows.
   - Use frame/sprite renders as visual reference or temporary placeholders.
   - Translate coordinates and timing carefully: Flash uses stage/timeline/frame-rate assumptions that rarely map 1:1 to modern engine scenes.

## Useful FFDec CLI Commands

The helper script wraps these, but know the underlying calls:

- Export ActionScript:
  - `ffdec-cli -format script:as -export script out/code/actionscript game.swf`
- Export P-code with hex:
  - `ffdec-cli -format script:pcodehex -export script out/code/pcodehex game.swf`
- Export visual/audio assets:
  - `ffdec-cli -format image:png_gif_jpeg_alpha,shape:svg,sound:mp3_wav,text:plain -export image,shape,sound,text out/assets game.swf`
- Export timeline renders:
  - `ffdec-cli -format frame:png,sprite:png,button:png -export frame,sprite,button out/timelines game.swf`
- Dump tags:
  - `ffdec-cli -dumpSWF game.swf > out/structure/tags.txt`
- Export XML structure with externalized scripts/images/sounds:
  - `ffdec-cli -swf2xml -external all game.swf out/structure/movie.xml`

## Porting Heuristics

- If source and P-code disagree, trust P-code/tag structure more than decompiled high-level source.
- Timeline code may be gameplay code. Search decompiled code for `onEnterFrame`, `addEventListener`, `ENTER_FRAME`, `gotoAndStop`, `gotoAndPlay`, `attachMovie`, `duplicateMovieClip`, `hitTest`, `_root`, `_global`, `stage`, and exported class names.
- For AS2 games, expect frame scripts and dynamic movie clip attachment. For AS3 games, expect document classes, package directories, `DoABC`, and event listeners.
- Use `symbolClass.csv` to connect class names to character IDs.
- Use rendered frames/sprites to verify animations, frame counts, origin assumptions, and sprite nesting.
- Build a small behavior table before coding the port: original symbol/class, role, extracted assets, update loop, collision/input hooks, new engine node/component.

## Output Contract

When finishing a decompile-for-porting pass, report:

- SWF path and output folder.
- FFDec command/source used.
- Extracted categories and notable counts.
- Whether ActionScript, P-code, XML structure, frame renders, and sprite renders were produced.
- Important entry points and obvious game systems found.
- Gaps: failed exports, obfuscation, missing external assets, encrypted/protected SWF, or unsupported features.
- Suggested next porting step.
