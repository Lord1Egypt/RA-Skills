# Driving Unity as an agent

The point of this file: an agent that can move the editor itself, and *prove* each move, with no human
clicking. Read it before wiring anything to an editor.

## 1. Unity ships its own bridge - check it before installing anything

Recent Unity Hub installs put a `unity` CLI on the machine (typically
`%LOCALAPPDATA%\Unity\bin\unity.exe`, user-relative, no admin needed). It talks to a running editor:

```
unity status                                     # project, editor version, PID, port, state
unity list                                       # every built-in editor tool this editor exposes
unity command <tool> --project-path "<project>" --result-only --json
unity command <tool> --project-path "<project>" --detach     # long job
unity command <tool>_status --project-path "<project>"       # poll a detached job
```

Measured on one rig (Unity 6000.5.9f1): `unity status` returned the open project, editor version, PID,
port and `ready`, and `unity list` returned **142 tools** - scene / GameObject / component / asset /
animator authoring, `build` + `build_status` (full BuildReport), `capture_game_view` /
`capture_scene_view` (PNGs), `console` (log tail), `recompile`, test runs, audits, lighting and NavMesh
bakes. That is an agent limb with no subscription and no third-party server.

- Prefer `--result-only --json`: it returns the tool's result rather than the CLI's chatter, and it is
  the shape a caller can assert on.
- `--detach` returns immediately with a job handle; poll the matching `*_status` tool. Do not hold a
  foreground call open for a build or a bake.
- `unity skill show` / `unity skill install <client>` is Unity's own agent guide; read it rather than
  guessing at flags, since the surface changes between editor versions.

## 2. When the CLI lacks the tool you need, use a free MCP server

| Server | Licence / cost | Surface |
|---|---|---|
| `JESVN/unity-mcp-server` (AnkleBreaker) | free, open source | ~288 tools / 30+ categories: Hub control, scenes, GameObjects, builds, profiling, Shader Graph, terrain, NavMesh, animation, multi-instance |
| `CoplayDev/unity-mcp` (MCP for Unity) | **MIT** | ~34 tools: assets, scenes, scripts, tests (same makers ship Godot AI) |
| Unity's own Unity MCP | **needs Unity Cloud + a Unity AI subscription** | built-in, credit-based, cannot use external models |

- **Recommend the free servers.** Unity's official MCP gates on a subscription and cannot be pointed at
  an external model, so never put that gate in front of an experiment.
- An MCP client entry points at the server's entry script. Unity's own relay, when used, lives at
  `%USERPROFILE%\.unity\relay\relay_win.exe` and takes `--mcp`.
- **The operator approves the first external connection in the editor** (Project Settings > AI). Expect
  a dialog on first connect and tell the user to watch for it; a silent failure here looks like a
  broken server.

## 3. Create a project non-interactively

```
unity templates list --editor 6000.5.9f1
unity projects new "<Name>" --path "<parent-dir>" --editor-version 6000.5.9f1 --template com.unity.template.fps
```

Templates come back `ready` / `upgradable` / `downloadable`; `new` downloads and imports the one you
name. The offering is per editor version - do not read it off the Hub GUI.

## 4. The working rule: edit, then read the console back

1. One change at a time (one fighter, one prop, one material - not a batch).
2. Apply it through the CLI/MCP tool.
3. Read the editor console back through the same connection and look for errors *before* the next edit.
4. For visual work, capture a view (`capture_game_view`) and look at the PNG. A tool returning
   `ok: true` is not a picture; the picture is the picture.

An agent that chains five edits on an unverified first edit is how a project ends up in a state nobody
can explain.

## 5. Builds from the CLI

```
unity build "<project>" --create-profile WebGL          # writes Assets/Settings/Build Profiles/WebGL.asset
unity build "<project>" --profile WebGL -o "<out-dir>" --no-tail --log-file "<log>"
```

- `unity build --target WebGL` fails by design: *"Target WebGL has no built-in command-line build. Pass
  --execute-method, or use a Unity 6+ build profile with --profile. Only desktop targets build without
  them."*
- **Never wrap the build in a shell `timeout`.** A microgame-sized WebGL build takes ~8-12 minutes; a
  cap kills it mid-way and leaves a half-written output plus `exitCode: 143` in the provenance file.
  Run it as a tracked background process and poll the log file and the output directory.
- Success looks like `Exiting batchmode successfully now!` with code 0. The line
  `[license] [Licensing::Module] LicensingClient has failed validation; ignoring` is benign and appears
  on successful runs.

## 6. Before you touch the editor: what is holding the GPU

A Unity editor needs the GPU and a large slice of RAM. A resident local LLM engine (or a diffusion /
video renderer) on the same card will fight it and both will crawl. Measured on an 8 GB card with a
local model loaded: **719 MiB free of 8188 MiB VRAM**.

**Pausing or stopping another program is the operator's decision, never the agent's.** That process may
be doing work this skill knows nothing about, and an agent that suspends it on its own initiative has
stepped outside the job it was given. So: report which process is holding the card, ask the operator to
park it, and wait. Only with their agreement run the sequence - park what they named, open Unity, do the
work, then restore it in a `finally` so a failure cannot leave the machine dark - and restore it when
the editor exits whether or not the work succeeded.
