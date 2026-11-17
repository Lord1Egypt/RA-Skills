# VSD Craft: Operational Findings and Scope

Compiled: 2026-10-09. This is a summary of public documentation and existing verification, not a generic caution list.
Reuse findings that match the version and model; verify only the differences.

## Reading the Evidence

- **Specification**: Vendor manuals or public SDK documentation; separate from successful hardware tests.
- **Application observation**: Records from 2026-10-01 through 2026-10-02 on Windows / VSD Craft **3.10.205.0918** / M3.
- **Physical verification**: Only the explicitly recorded operations. Do not infer LCD rendering or KVM recovery from application rendering.
- Later recovery tests included simulated failures. The 2026-10-03 records still did not include a physical KVM retest.

Personal scenes and primary logs are not distributed. The observations below are anonymized, transferable findings,
not independent hardware guarantees for another unit.

## Built-in Features and Configuration Paths

| Goal | Confirmed path | Evidence and scope |
|---|---|---|
| Manage scenes/pages | Add, edit, reorder, import, and export scenes. The common manual describes 1-10 pages per scene | Specification [M1]. Use the target version's UI for the actual limit |
| Configure a key | Select the key and drag a function from the right-hand list | Specification [M1] |
| Configure an M3 knob | Select the knob position and drag a supported function | Specification [M1] |
| Configure an N1/N4 Pro knob | Select the screen position corresponding to the knob | Specification [M1]. Not the same selection position as on M3 |
| Assign shortcuts to left/right rotation and press | Separate left-rotation, right-rotation, and press fields in the built-in `com.hotspot.streamdock.system.hotkey` action | Application observation on 2026-10-02. A complete physical-knob replacement test was not performed |
| Switch pages/scenes | Built-in `page.change` / `profile.rotate` actions appear among knob candidates | Observed in the application's action list. Test the required operation at the target placement |
| Long press or switcher-state detection | The basic hotkey inspector had no separate long-press field | Same observation. This does not prove that all built-in functions, including composite actions, lack the capability |
| Back up/restore a scene | Settings > Scenes > select the scene > export/import arrows at the lower left | Specification [M1] |
| Obtain plugins | Open the distribution site through VSD Craft's Space icon | Specification [M2]. Browsing requires no login; downloading does |

Native scenes, native pages, and virtual pages implemented by replacing plugin images are different concepts.
Adding virtual pages does not increase the page count in the VSD Craft editor.

## Data Location and Installation

Observed Windows layout:

```text
%APPDATA%\HotSpot\StreamDock\
  plugins\<plugin-uuid>.sdPlugin\manifest.json
  profiles\...sdProfile\manifest.json
  StreamDockConfig.ini
```

This layout was used by an existing VSD Craft 3.10.205.0918 installation and matches the standard StreamDock development documentation [M3].
For multiple installations, other users, or other brands, use the location shown by
Settings > General > Open Application Folder.
Elgato's `%APPDATA%\Elgato\StreamDeck\Plugins` is not this skill's installation target.

1. Check the distribution source and the manifest's UUID, version, supported OS, and CodePath.
2. Take the backup described below and quit VSD Craft normally.
3. Move the old `<uuid>.sdPlugin` folder outside the plugins directory.
4. Place the new folder and carry over only user settings compatible with the new version's schema.
5. Start VSD Craft and check the action list, inspector, logs, and physical operation in order.

A ZIP is an archive to extract, not the same installer format as Elgato's `.streamDeckPlugin`.
Plugins store settings in different places; do not assume that `config.json` exists.

## Backup and Restoration

Prefer a scene export for ordinary configuration changes.
For updates or recovery requiring file operations, copy files after the application exits and finishes writing its state.

Record:

- Original application version, plugin UUID/version, and target device, scene, and page.
- The complete target plugin, required scene trees, and their image assets.
- `StreamDockConfig.ini` when selection state must be restored.
- Original paths, backup paths, file counts, and verification data such as SHA-256 hashes.

To restore, quit the application and preserve the currently failing version in another location.
Restore the old plugin, scenes, and required settings according to the path mapping, then restart and verify.
Profile edits made while the application is running may be overwritten when it exits.
Do not directly edit SQLite databases or caches for ordinary settings restoration.

## Missing Display or Unresponsive Input

1. Does the application recognize the device?
2. Are the target folder, manifest, and dependencies complete, and is the plugin running?
3. Are localhost WebSocket registration, `willAppear`, and rendering messages for the target context present?
4. Are key/knob assignments, manual titles, and the distinction between native and virtual pages correct?
5. For USB recovery, were contexts incorrectly deleted after `deviceDidDisconnect`?

In an existing failure on 2026-10-02, the application retained the key placements across reconnection
but did not resend `willAppear`. The plugin had deleted all contexts, so rendering stopped.
Pause rendering and input while disconnected, retain contexts within the same host connection, and redraw on reconnect.
Use `willDisappear` to remove a context. Treat loss of the host WebSocket itself separately.

[M2] also recommends clearing `Storeache` when plugins do not appear after installation.
If that procedure proves necessary, confirm the actual folder, quit the application, and move its contents aside before testing.
Do not begin by deleting all caches, settings, or scenes.

## Model-specific Display Behavior

- In the recorded M3 layout, key `row=0` was the bottom row. Knobs used `column=5`, with `row=0` at the top.
  These are placement observations, not a coordinate-transformation rule for every model.
- The official M3 guide [M4] describes interactive backgrounds, keypress effects, and dynamic screensavers.
  That does not establish that they share the rendering surface or API used by an ordinary plugin's `setImage`.
- The official N1 description [M5] lists GIF icon support. Accepting GIFs, decoding video, and rendering real-time backgrounds are different capabilities.
  Do not classify the entire N series as static-image-only. Verify codecs, FPS, and simultaneous rendering across surfaces separately.

## Sources

- [M1: Common VSD manual](https://cdn.shopify.com/s/files/1/0657/8690/4620/files/VSD_Stream_Dock___User_Manual___English_b4c5939a-dad2-4e31-8b0e-54f79f983fde.pdf?v=1777109994): Saved text retrieved on 2026-10-01 and rechecked on 2026-10-09; sections 7-9.
- [M2: Official plugin installation guide](https://www.vsdinside.com/blogs/tutorial/plugin-download): Text checked on 2026-10-09.
- [M3: StreamDock local development](https://sdk.key123.vip/en/guide/get-started.html): Research record from 2026-10-01.
- [M4: M3-specific guide](https://www.vsdinside.com/blogs/tutorial/user-guide-magtran-m3-quick-start-beginner-tutorial): Researched on 2026-10-04 and retrieved again on 2026-10-09.
- [M5: Official N1 product description](https://www.vsdinside.com/products/vsd-stream-dock-n1): Research record from 2026-10-01.
- Original records behind the anonymized application observations: `DEPLOYMENT-ja.md` (2026-10-01), `findings.md` (built-in knob research, 2026-10-02), and `deployment.json` (reconnection fix, 2026-10-02). Personal paths, scene IDs, and original logs are not bundled.
