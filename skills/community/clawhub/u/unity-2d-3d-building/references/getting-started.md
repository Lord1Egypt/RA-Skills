# Getting started: first hour, install to verified build

Do these in order. Each step has an acceptance check - do not move on until it passes, because every
later step assumes it.

## 0. Decide the target (2 minutes)

Where must the game be playable? A browser page -> Unity WebGL. A download -> any engine. A quick 2D page
game -> canvas/JS, no engine. Write the answer down; it decides everything below.

## 1. Engine on the right disk

- Install Unity Hub, then Unity 6 (6000.x) **plus the WebGL Build Support module for that exact
  version**.
- Choose the disk by *medium*, not free space:
  `Get-PhysicalDisk | Select-Object DeviceId,FriendlyName,MediaType,BusType,Size`
  and `Get-Partition | Where-Object DriveLetter`.
- Budget 10-20 GB. Unreal, for comparison, is ~110 GB - and cannot target the web at all.

**Acceptance:** the editor version is the one you intend, and the WebGL module is listed for it.

## 2. Project from a template

```
unity templates list --editor 6000.5.9f1
unity projects new "<Name>" --path "<parent-dir>" --editor-version 6000.5.9f1 --template com.unity.template.fps
```

Take a template; do not start from an empty scene. The offering is per editor version, and `templates
list` is authoritative - not the Hub GUI.

**Acceptance:** the project opens and the template's own scene plays in the editor.

## 3. Connect the agent

```
unity status
unity list
unity command console --project-path "<project>" --result-only --json
```

If the CLI is not present, install a free MCP server (`CoplayDev/unity-mcp` MIT, or
`JESVN/unity-mcp-server`) and expect the operator to approve the connection in the editor
(Project Settings > AI).

**Acceptance:** a tool call returns a result *and* you can read the editor console back through the same
connection.

## 4. Make one verified change

Change one thing (a colour, one GameObject, one component value) through the bridge, then read the
console back. This proves the edit path end to end - and it is the pattern for all later work.

**Acceptance:** the console shows no error and a captured view shows the change.

## 5. First WebGL build, before any art work

```
unity build "<project>" --create-profile WebGL
unity build "<project>" --profile WebGL -o "<out-dir>" --no-tail --log-file "<log>"
```

Run it as a tracked background process (~8-12 min). Set
`PlayerSettings.WebGL.decompressionFallback = true` before the first build if the output will be served
from a static host.

**Acceptance:** the output folder contains `Build/*` and no `.gz`-only payload set; the log ends with
`Exiting batchmode successfully now!`.

## 6. Serve it and actually play it

Serve the folder over HTTP (not `file://`), load it in a browser, and click into gameplay.

**Acceptance:** the intro/menu renders (loader works) and the first gameplay frame appears (scene,
scripts, wasm all up). A file list is not acceptance.

## 7. Then art, audio, and gameplay - one thing at a time

- Licence-clear art before pulling it (`references/assets-and-licences.md`).
- Import selectively into the project; keep the library outside it.
- Rebuild, reload, look. A WebGL build is not a live page you can edit.

**Definition of done for any change:** it is in the editor, it is in a build, it is on the served page,
and you have looked at it there.
