# Implementation, Verification, and Packaging

## New Scaffold

`scripts/scaffold.py` creates only a new directory and never overwrites an existing path.
The scaffold uses Node CommonJS + `ws`; its property inspector (PI) uses ordinary browser JavaScript. No build step is required.
The manifest specifies SDK 1, Node 20, Windows 10, and minimum host version 3.10.188.226.
These lower bounds come from public specifications, not tests on every matching version.

```sh
python3 scripts/scaffold.py --id com.example.counter --name "Counter" \
  --output /tmp/vsd-demo/com.example.counter.sdPlugin
```

Run `npm install` and then `npm test` in the generated directory. Keep the generated `package-lock.json` and use `npm ci` to reproduce the dependency set.
The demo counter value lives in memory; the step setting is saved to the host with `setSettings`.
Use the Node 20-compatible `ws` 8.x series. Do not raise `Nodejs.Version` merely to match the development machine's Node version.

## Implementation Boundaries

1. **Registration**: Parse arguments by name. Validate the port, UUID, and registerEvent. Do not depend on an arbitrary fixed port.
2. **Input**: The action UUID identifies the type; the context identifies the placement. Distinguish keys and knobs by event name. Handle rotation magnitude through ticks.
3. **Settings UI**: The PI registration UUID and action context are different. Include action in sendToPlugin and an explicit actionContext in the custom payload so replies reach the intended placement.
4. **Rendering**: Use an SVG data URL with target 0. Unchanged images may be skipped, but force a resend on reconnect. Do not erase manual titles with setTitle.
5. **Shutdown/reconnection**: Retain contexts and discard input on USB disconnect. Remove contexts on willDisappear. Exit when the host socket closes.
6. **Adding external actions**: Keep domain logic in separate functions and do not execute pre-disconnect pending input after recovery. Do not start a child process for every high-frequency dialRotate event.

Opening the PI HTML shows its status, but it connects to the host only when VSD Craft invokes the connection function.
The scaffold tests also simulate the PI's browser environment. They do not verify layout in a real browser.

## Mock-host Tests

`npm test` connects the actual plugin child process to a temporary loopback WebSocket and checks JSON round trips.
It does not connect to VSD Craft or a USB device.

- Reordered launch arguments and use of the supplied registration event.
- Key press/release and the sign and magnitude of knob ticks.
- Step changes from the inspector, a distinct PI UUID, and replies to the action context.
- Delayed events from the old connection cannot disrupt the new connection after reopening the inspector.
- State isolation across multiple contexts.
- Discarding orphaned releases on disconnect and redrawing on connect alone.
- Ignoring input after willDisappear, continuing after invalid JSON, and exiting on host close.
- Existence of manifest targets and icons.

When implementation changes, verify the added contracts with a small number of meaningful tests.
Do not treat this suite as a compatibility checker for arbitrary other plugins.

## Packaging

```sh
python3 scripts/package_plugin.py /tmp/vsd-demo/com.example.counter.sdPlugin \
  --output /tmp/vsd-demo/counter.zip
```

This helper is specific to the counter scaffold. It packages an explicit allowlist: manifest, plugin.js, UI, PNG images,
package metadata, lockfile, and the ws runtime and LICENSE. It fails if the output already exists.
When extending the implementation, update the dependency and asset lists and review the contents.
Do not gather and compress runtime logs, user settings, profiles, or credentials.
The deliverable is a ZIP rooted at `<uuid>.sdPlugin/`. Marketplace publication and git push are outside this procedure.

## Hardware Checks

If the request includes installation, confirm VSD Craft's actual folder through the UI.
Quit the application normally and preserve the old plugin, target scenes, and required selection settings before installing.
Do not replace existing personal settings with scaffold defaults. The standard data location is `%APPDATA%\HotSpot\StreamDock`, but the observed active path takes precedence.

Record each item as `Pass / Fail / Not tested / Not applicable (reason)`:

| Layer | Check |
|---|---|
| Static and mock tests | Manifest references, npm test, archive contents, dependency licenses |
| Real application | Startup, actual Node version, WebSocket registration, willAppear, PI display, and settings persistence |
| Application rendering | Key/knob images, manual title preservation, and isolation across placements |
| Physical operation | Key press/release, left/right rotation, knob press and rotation while pressed, and physical display |
| Recovery | USB unplug/replug, KVM round trip, and application restart; verify each separately |
| Non-interference | No unintended changes to existing scenes, other plugins, the foreground application, or notifications |

Include the application version, OS, model, firmware (or "unknown"), connection path, and verification date in the results.
On failure, quit the application, move the current version aside, and restore the old folder and settings.

## Skill Maintenance

1. Add new versions, evidence, and observations to the relevant API rows. Do not generalize a past, scoped failure into non-support across all versions.
2. Run the skill-format validator and verify that relative Markdown links resolve when the skill is distributed independently.
3. Run `python3 -m unittest discover -s scripts -p 'test_*.py'` and verify fresh generation, npm install, npm test, and ZIP extraction.
4. For publication, obtain the user's publishing instruction and stage only this skill's tracked files. Do not publish the entire day-to-day development directory.
