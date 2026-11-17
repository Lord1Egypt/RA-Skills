---
name: vsd-craft-operations
description: "Configure keys, knobs, scenes, and pages in VSD Craft / VSDinside / StreamDock (also spelled VDS Craft); choose built-in actions; install or update plugins; back up settings; and diagnose USB/KVM recovery. For new plugin implementation or Elgato ports, use vsd-craft-plugin-development."
---

# VSD Craft Operations

1. Read the [confirmed workflows and model differences](references/operations.md), then classify the request as built-in action configuration, installation/update, or recovery. Reuse recorded findings; investigate only unverified behavior or differences in the target version or model. Done when the target operation and applicable procedure are identified.

2. Identify the application version, OS, model, connection path, and target scene/page. Confirm the data location through the application's Settings > General > Open Application Folder command. If needed, inspect its structure with `python3 scripts/inspect_data.py --root <data-root>`. Resolve relative paths from this skill's directory. Done when the application version and data path are recorded and the target is distinguished from Elgato's separate folders.

3. For built-in configuration, select the relevant key or knob and inspect its available actions. The observed basic hotkey action has separate fields for left rotation, right rotation, and press. Investigate additional behavior only when requirements such as state detection or long press demand it. Keep native scenes, native pages, and plugin-internal virtual pages distinct. Done when built-in coverage and any required custom implementation are explicit.

4. Export the target scene before making changes. For file-based updates or recovery, quit the application normally, then copy the target plugin, related scenes, and selection-state configuration into a separate timestamped directory. Follow [backup and restoration](references/operations.md#backup-and-restoration) and record the mapping between originals and restoration destinations. Done when the copies are readable and the previous layout and settings can be restored.

5. Apply the requested changes. Prefer the UI for settings; install plugins into the confirmed `plugins/<UUID>.sdPlugin` location. Preserve the old version and user settings during updates, and avoid editing profiles directly while the application is running. If several automatic installation targets exist, use the running executable's location and the path shown in the UI to identify the active one. Done when only the intended targets changed and existing scenes, manual titles, and other plugins are preserved.

6. Restart VSD Craft only when needed and complete the applicable rows of the [verification sheet](references/verification.md). Check application rendering, physical input, device display, USB reconnection, and KVM round trips separately. Trace recovery failures through application/device connectivity, the plugin process, WebSocket registration, and display contexts, in that order. Done when the requested behavior is observed and unperformed checks are not reported as passes.

7. Hand off a brief summary of changes, verified behavior, remaining unknowns, backup locations, and restoration steps. Exclude personal profiles, logs, device IDs, and credentials from shared artifacts. Done when others can reuse the procedure and the current change can be rolled back.

## Bundled Resources

- [Operations and findings](references/operations.md): Built-in features, folders, model differences, recovery, and sources.
- [Verification sheet](references/verification.md): Evidence template; copy it into the working directory before filling it in.
- [Read-only data inventory](scripts/inspect_data.py): Directory structure and plugin manifest summaries for a supplied root; excludes configuration bodies and logs.
- [Inventory test](scripts/test_inspect_data.py): Temporary fixtures check read-only behavior, content omission, and link exclusion.
- [User-facing README](README.md): Installation and example requests, in Japanese.
