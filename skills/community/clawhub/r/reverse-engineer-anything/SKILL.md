---
name: reverse-engineer-anything
description: "Reverse engineers Android APKs and other software without source code using REA (rea-agents) in a locked-down Docker container: APK package overview, class search, decompiled Java/Kotlin classes and methods via JADX, reference tracing, decoded resources and strings via Apktool, adb device inspection, plus JavaScript/Electron, .NET, Go, Rust, WASM, SQLite and network-capture analysis, and native decompilation with Ghidra when enabled. Runs as a Streamable HTTP MCP server or as one-off CLI commands. Use when the user wants to understand how an app or feature works from its APK or binary, inspect what an APK contains, or find where behavior lives in decompiled code."
license: WTFPL
homepage: https://github.com/psyb0t/docker-reverse-engineer-anything
user-invocable: true
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      bins:
        - docker
permissions:
  filesystem: "Mounts the one directory you name read-only at /work. Writes nothing outside the container except the output you redirect."
  shell: "Docker, through the bundled wrapper or a docker run you show the user. The CLI wrapper runs with no network, a read-only root and all capabilities dropped."
  network: "Docker pulls psyb0t/reverse-engineer-anything from Docker Hub. With REA_INSTALL=ghidra the container downloads Ghidra once from its official GitHub release, checked against a pinned SHA-256. The CLI wrapper runs with --network=none unless --network is passed for adb over TCP or website analysis. The MCP server listens only where the user publishes its port."
---

# Reverse engineer anything

This skill runs [REA](https://github.com/morluto/rea) (`rea-agents`) from the
`psyb0t/reverse-engineer-anything` image. The image bundles a full JDK 21, the
JADX bridge REA pins, Apktool 3.0.3 and adb, so APK analysis works with no
host setup beyond Docker.

## Security & safety

- Analyze only software the user owns or is authorized to examine. Do not help
  bypass DRM, license checks, anti-cheat or authentication, and do not copy
  proprietary code or assets.
- Static APK analysis never runs the app. Tools that install, start or drive
  apps on a device, capture processes or instrument code change real state:
  confirm the exact device and action with the user first.
- Mount only the directory that holds the targets, read-only. Never mount `/`,
  a home directory or the Docker socket.

## When to use

- Get an APK's manifest summary, permissions, components and package name.
- Find where a feature lives: search classes, decompile a class or method, and
  trace who calls it.
- Read an APK's decoded resources and strings, per locale.
- Inspect a connected or networked Android device with adb.
- Analyze Electron/JavaScript bundles, .NET assemblies, Go or Rust binaries,
  WASM, SQLite databases or network captures.
- Decompile native code, such as the `.so` libraries inside an APK, once the
  container runs with `REA_INSTALL=ghidra` (amd64 only; see
  [setup](references/setup.md#opt-in-tools)).

## When NOT to use

- Hopper-based analysis: Hopper is a desktop app and is not supported here.
- Running or instrumenting malware outside an isolated, disposable host.
- Anything the user is not authorized to analyze.

## One-off CLI commands

`scripts/rea.sh`, relative to this skill's directory, runs one REA command
with the target directory mounted read-only at `/work`:

```bash
scripts/rea.sh --dir ./apks inspect-android-package /work/app.apk
scripts/rea.sh --dir ./apks search-android-classes /work/app.apk MainActivity
scripts/rea.sh --dir ./apks inspect-android-method /work/app.apk com.example.MainActivity onCreate
scripts/rea.sh --dir ./apks trace-android-references /work/app.apk com.example.MainActivity --method-name onCreate
scripts/rea.sh --dir ./apks decode-android-resources /work/app.apk --locale de
```

Results are JSON on stdout. Pass container paths (`/work/...`), never host
paths. `scripts/rea.sh --help` prints REA's full command list.

## MCP server

For an agent session, run the container as a Streamable HTTP MCP server and
connect to `http://localhost:8080/mcp` with the bearer token. Setup, client
configuration and every environment variable are in
[setup](references/setup.md). Each MCP session gets its own REA process, so
analysis state never leaks between sessions.

## Workflow for an APK

1. `inspect_android_package` for the package name, components and permissions.
2. `search_android_classes` with a word from the feature (an activity, a
   string, a domain term).
3. `inspect_android_class`, then `inspect_android_method` on the candidates.
4. `trace_android_references` to follow callers and callees.
5. `decode_android_resources` when the feature hinges on strings, layouts or
   configuration.

Report what the evidence shows and what it cannot show: static decompilation
does not prove runtime behavior, and obfuscated names stay obfuscated.
