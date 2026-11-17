---
name: unity-2d-3d-building
description: >
  Use when an agent must build, wire, or ship a Unity game - 2D, 3D, or 2D art over a real 3D stage:
  installing the engine, creating a project from a template, driving the editor through Unity's own
  CLI bridge or an MCP server, sourcing CC0 assets, and building to WebGL that you verify in a browser.
  Carries the Battle TV painted-broadcast house style as a worked reference, and a living art-method log.
  Ships its own self-check (`scripts/check_skill.py`), which audits this package's own text only -
  absolute paths, pinned installs, version agreement, referenced files, licence claims - and never
  reads, scans or judges the caller's project, repository or machine.
  Use for Unity, Unity 6, 6000.x, Unity MCP, the unity CLI, WebGL build, sprite, Shader Graph,
  URP vs built-in, licence-cleared assets, or /unity-2d-3d-building.
version: 1.1.4
license: MIT-0
permissions:
  network: none - no script in this package fetches, posts or uploads anything
  filesystem_read: own package folder only
  filesystem_write: append references/techniques.md only, after a watched build confirms the method
  shell: false
  subprocess: false
  install: false
  publish: false
allowed-tools:
  - read this package's own folder
  - run python scripts/check_skill.py
metadata:
  openclaw:
    emoji: "🎮"
    homepage: "https://chatagent.ca/"
  publisher: deepseekoracle
---

# Unity 2D-3D Building

An agent's guide to Unity: get the engine, make a project, drive the editor without a human clicking,
source art you are allowed to ship, build it for the browser, and prove it runs. The Battle TV painted
broadcast style is the worked example at the end, with its method log kept alive.

Author's home and the worked picture are external links this package neither ships nor fetches - open
them in a browser: https://chatagent.ca/ · https://deepseekoracle.github.io/battle-tv-unity/

## When to use this

- An agent must produce or change a Unity project, and no human is going to click through the editor.
- A game has to run **in a browser page** and look like a real engine built it.
- Assets, templates or a licence answer are needed for a game build.
- A Unity WebGL build exists and must be served, verified, and shown.

## When not to use this

- **A 2D page game in a day.** Canvas/JS beats Unity for a quick 2D web game: instant load, no
  10-20 GB pipeline, no rebuild-to-change-anything loop. Say so instead of reaching for an engine.
- **A downloadable Unreal game** - different engine, different guide (Unreal cannot target the web).
- **A mobile/console shipping pipeline.** Getting to a playable, verified build is in scope; store
  submission, IAP and platform certification are not.
- **Retuning a live game's fight math.** Presentation work is guided here; balance numbers belong to
  the game that owns them.

## 1. Decide the target before anything is installed

Ask *where the game must be playable*. That one question eliminates engines:

| Target | Engine |
|---|---|
| **Plays in the browser page itself** | **Unity 6 (native WebGL build)** or Godot |
| A download the page offers | Unity or Unreal, either one |
| A quick 2D page game | canvas/JS - an engine is the wrong tool |
| Unreal, in-page | **does not exist**: Epic removed HTML5 export after UE 4.24 |

- **Unreal cannot target the web**: Pixel Streaming renders on a GPU server and streams video - not a
  standalone build, and not fit for games, so a UE game is always a download.
- **The engine does not make the game good, it makes it look good.** State the trade rather than
  implying a Unity rewrite upgrades a game by itself.
- Budget: Unity editor + WebGL module **10-20 GB**; Unreal 5 **110 GB**.

## 2. Get the engine

1. **Unity Hub**, then **Unity 6 (6000.x)** plus the **WebGL Build Support** module *for that exact
   version*. The Hub download is small; the editor is the download.
2. **Put it on a real SSD and check the medium, not the free space** - a drive letter says nothing
   (`Get-PhysicalDisk | Select-Object DeviceId,FriendlyName,MediaType,BusType,Size`): shader
   compilation belongs on the SSD, not on whichever external HDD has the most room.
3. **Unity requires a Unity ID login.** Never guess, ask for, or handle those credentials: the operator
   signs in on their own machine.
4. **Do not install Unreal "as well" to compare.** Section 1 already decided it, and 110 GB is a cost
   to the very drive the rest of the work needs.

## 3. Make a project from a template, never from an empty scene

```
unity templates list --editor 6000.5.9f1        # what this editor can actually pull
unity projects new "<Name>" --path "<parent-dir>" --editor-version 6000.5.9f1 --template com.unity.template.fps
```

- Templates are marked `ready` / `upgradable` / `downloadable`; creating one downloads and imports it.
- **`templates list` is authoritative, not the Hub GUI**, and the offering differs per editor version.
- Free complete playable bases exist for **FPS, 2D platformer/side-scroller, kart racer, board/chess,
  card, tower defence, puzzle/RPG** - not for **sports, boxing/fighting, farming/sim**, which are paid.
  Genre choice is constrained by budget; say that instead of searching longer.
- Kenney's *Starter Kits* are Godot, not Unity: his CC0 **assets** import fine, his **kits** do not.

## 4. Drive the editor as an agent

**Check for Unity's own CLI bridge before installing anything** - it is often already live, and free:

```
unity status                       # open project, editor version, PID, port, state
unity list                         # ~142 built-in editor tools
unity command <tool> --project-path "<project>" --result-only --json
unity command <tool> ... --detach  # long jobs; poll the matching *_status tool
```

`unity list` covers scene/GameObject/component/asset authoring, `build` + `build_status` (full
BuildReport), game/scene captures, `console`, `recompile`, tests, audits and bakes; `unity skill show`
is Unity's own agent guide.

When the CLI lacks a tool, fall back to a free MCP server (**`CoplayDev/unity-mcp`**, MIT, 34 tools, or
**`JESVN/unity-mcp-server`**, 288 tools) - never Unity's own MCP, which needs Unity Cloud plus an AI
subscription. **The first connection is approved by the operator in the editor** (Project Settings > AI),
so tell the user a dialog is coming, and **verify every edit by reading the console back**: edit,
confirm, edit again, never chain edits on an unread result. Full CLI surface, detach/poll pattern and
MCP setup: `references/editor-cli.md`.

## 5. 2D, 3D, or 2D art over a 3D stage

Pick **2D** for flat art and precise silhouettes, **3D** for camera movement and lighting worth the
payload, or **2D art over a 3D stage** for the painted broadcast look with depth - budgeting both
pipelines when you do.

- **Decide built-in vs URP at the start**: changing pipeline later re-shades every material, and a WebGL
  build wants the smallest shader surface you can use. The worked style here is built-in.
- **A 3D mesh joins the 2D look only after a watched frame matches the 2D art** - and verify a mesh
  (dimensions, normals, bounds) *before* wiring physics to a deformed import, which loads, looks wrong
  and never drives. A prop parented to a differently-scaled parent also lands in the wrong place.
- Sorting in a sprite stack is **sibling order**. Stage choice, sorting and pipeline in full:
  `references/2d-and-3d.md`.

## 6. Assets: licence first, download second

Nothing gets pulled until it is clear it can ship. The gate, in order:

- **CC0 is the target** - public domain, sellable, remixable, no attribution, safe in a public repo -
  but **a free kit's art can be CC0 while its code is not** (Extension Asset EULA): take the CC0 art,
  write the logic yourself, and the kit never becomes a runtime dependency.
- **No "free download" aggregators** that redistribute paid Asset Store packages (`unityassetpack.com`,
  `unityassetcollection.com`, `opengameasset.net`, "50 Unity Source Codes" bundles); **a real licence at
  the file** for any GitHub repo (MIT/Apache only - no LICENSE, or "for educational purposes", is not
  permission to ship); **no redistributing raw files** from Mixamo-class services, which forbid it.

Per-source caveats, formats and the gate as a checklist (Kenney, Quaternius, Poly Haven, KayKit,
Freesound / Sonniss, the Asset Store's free tier): `references/assets-and-licences.md`.

**Enumerate before you fetch, then import selectively.** Keep one library directory outside the
project and import only what the levels call for - importing thousands of models inflates the project,
slows every import, and bloats the shipped build with assets nobody sees. A browser-rendered catalogue
can return zero links to `curl`; look for an index file (`kits.tsv`, an API) before writing a scraper.

## 7. Build it for the web, and prove it

```
unity build "<project>" --create-profile WebGL     # writes Assets/Settings/Build Profiles/WebGL.asset
unity build "<project>" --profile WebGL -o "<out-dir>" --no-tail --log-file "<log>"
```

- **`unity build --target WebGL` fails by design**: use a build profile, or `--execute-method`.
- **Never wrap a build in a shell `timeout`**, and keep it off the foreground path: a microgame-sized
  WebGL build takes **~8-12 minutes** and a killed run leaves a half-written `Build/` with
  `exitCode: 143`. Run it tracked in the background and poll for arriving artifacts - the files are the
  proof, not the exit code.
- `[license] ... LicensingClient has failed validation; ignoring` with
  `Exiting batchmode successfully now!` and code 0 is a **success**, not an error.
- **A gzip WebGL build stalls on a static host** (GitHub Pages serves `.gz` with no `Content-Encoding`,
  so the loader waits at the progress bar forever): ship the decompression-fallback build instead
  (`PlayerSettings.WebGL.decompressionFallback = true`, confirmed by logging the value back).
- **Serve it, load it in a browser, click into gameplay**: the intro menu proves the loader, the first
  gameplay frame proves scene, scripts and wasm - a file list proves nothing. Say the payload size out
  loud before it reaches a landing page (~24 MB gzipped for a first visitor).

Full ship rules - canvas centring, short windows, Escape never being a game key, proving the new code
shipped, numeric layout asserts: `references/webgl-shipping.md`.

## 8. The loop, and what "done" means

The order is the section order: target, engine on an SSD, template, agent + console read-back, cleared
art, then build/serve/load/click.

- **A verifiable milestone beats a long build.** Get the untouched template running and building to
  WebGL *first*: that proves editor, bridge, build and browser as one chain before a single asset or
  gameplay change is paid for. Every later claim carries its evidence - console read-back, artifact on
  disk, loaded page.
- **A WebGL build is not a live page you can edit**: iteration is change -> rebuild -> reload.

## 9. Traps that have actually cost time

Four that bite hardest, each with its fix: **the GPU is one resource** (a loaded local LLM and a Unity
editor cannot share a small card - name what holds the card and ask the operator to park it; only on
their word, restore it in a `finally`); **slow work outlives a tool call** (builds, imports and bulk
downloads run tracked in the background, polled by artifact, never relaunched while live); **never
`git add -A`** in a shared repo, and delete `*_BurstDebugInformation_DoNotShip/`; **report counted
numbers**, never a download list.

All fourteen, ordered by time actually lost, with the failure each caused: `references/traps.md`.

## 10. The worked style: Battle TV painted broadcast

The house look - painted side-view fighters on a plate, additive shader overlays, a ground ring as the
quality bar, HUD above the plate - is whole in **`references/battle-tv-style.md`**, with its standing
rules (built-in pipeline, linear colour space, one fighter at a time, presentation only, never retune
fight math to fix a picture).

**Art methods have one home: `references/techniques.md`** - read it before generating a frame, importing
a sprite, parenting a prop, writing a shader or placing a hit, and treat the log as current where the two
disagree. Append one dated line under Confirmed only after a watched build shows the picture you
intended; a method merely tried is not logged, an overturned one gets a new line saying what replaced it,
and rejected tools stay listed in Rejected so the next session does not retry them.

## Files

| File | What it is |
|---|---|
| `references/getting-started.md` | first-hour checklist, install to first verified build |
| `references/editor-cli.md` | the `unity` CLI surface, detach/poll, MCP fallback, console read-back |
| `references/2d-and-3d.md` | stage choice, sorting, sprites vs meshes, pipeline decision |
| `references/assets-and-licences.md` | CC0 sources with caveats, the licence gate, import rules |
| `references/webgl-shipping.md` | build to a served and verified page, with the traps |
| `references/traps.md` | the failures that cost the most, and the fix for each |
| `references/battle-tv-style.md` | the worked painted-broadcast style, whole |
| `references/techniques.md` | the living art-method log (one home for methods) |

## Self-check

```bash
python scripts/check_skill.py           # add --json for machine-readable findings
```

Named rules, each answering with a named boolean: no absolute local paths in the shipped text, no
floating versions in install commands, version agreement between this entry document and the package
manifest, every referenced file present, licence claims limited to hosts named in
`references/assets-and-licences.md`.

## Scope, permissions and limits

What this package is allowed to do, stated here so an agent host can grant exactly this and no more:

- **Reads** its own folder only: this entry doc, `claw.json`, the eight reference pages beside it, and
  `scripts/check_skill.py`. **Runs** exactly one program, `python scripts/check_skill.py` (stdlib,
  optional `--json`); nothing else in the package is executable.
- **Writes** nothing except an append to `references/techniques.md`, after a watched build confirms the
  method.
- **Network:** none, from any packaged script (`claw.json` declares `network.https_get: false`,
  `http_post: false`). The asset hosts in `references/assets-and-licences.md` are for **your** agent to
  browse under that licence gate - nothing here fetches or uploads anything.
- **Never:** install or upgrade software, run a shell or subprocess, invoke `git`, publish or push
  anywhere, read outside the package folder, or place a local disk path, drive letter or user folder in
  the shipped text. The self-check audits **this package's files only** - it cannot see the caller's
  repository and does not judge it.

If your host needs `allowed-tools`: read the package folder and run `python scripts/check_skill.py`.
Treat every other capability as undeclared.

## Install

```bash
npx clawhub@0.23.3 install deepseekoracle/unity-2d-3d-building@1.1.4   # pin BOTH sides: CLI and package
```

Do not republish this skill unless the user asks. Do not put a local disk path, drive letter, or user
folder in it: it is loaded on other people's machines.
