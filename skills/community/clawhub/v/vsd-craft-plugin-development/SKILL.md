---
name: vsd-craft-plugin-development
description: "Build VSD Craft / VSDinside / StreamDock plugins (also spelled VDS Craft), port Elgato Stream Deck plugins, and implement SDK communication, inspectors, key/knob input, reconnection, and packaging. Includes an Elgato compatibility matrix and verified differences. For built-in configuration only, use vsd-craft-operations."
---

# VSD Craft Plugin Development

1. Read the [bundled Elgato compatibility matrix](references/elgato-compatibility.md) first. Select the rows relevant to the request and use the verified wire formats and porting guidance. Limit further research to unverified APIs and target-version differences. Done when the parts to reuse, adapt, or reimplement are identified.

2. Establish the device model, application version, OS, requested behavior, and coverage of existing built-in features. Use the [field observations](references/field-observations.md) to align assumptions about scenes, coordinates, and reconnection. Treat the Creator SDK background-rendering path separately from VSD Craft's plugin socket. Done when the APIs, display surfaces, and operations to implement are explicit.

3. For a new plugin, generate the [minimal scaffold](assets/template/plugin.js) with `python3 scripts/scaffold.py --id com.example.counter --name "Counter" --output <new-directory>/com.example.counter.sdPlugin`. For a port, separate domain logic from host-dependent registration, rendering, and settings UI. Resolve relative paths from this skill's directory. Done when the manifest, entry point, images, inspector, and tests exist without reusing another plugin's UUID.

4. Implement the request using the [development and verification guide](references/development.md). Dispatch input by event name and maintain separate state for each placement context, even when action UUIDs match. Execute actions in response to user input; discard held-input state and pending operations on disconnect or disappearance. Done when settings, input, rendering, and reconnection paths are complete and user-owned settings such as manual titles remain intact.

5. In the generated directory, run `npm install --ignore-scripts --omit=optional --no-audit --no-fund` and `npm test`. For subsequent installs, use `npm ci` with the lockfile. The [mock-host tests](assets/template/test/smoke.cjs) use only temporary localhost ports and do not connect to VSD Craft. Done when manifest references, registration, input, PI settings, multiple contexts, reconnection, and host shutdown pass.

6. Package only allowlisted files with `python3 scripts/package_plugin.py <generated-directory> --output <new-zip>`, then review the contents. This helper targets the bundled counter scaffold; update its explicit file list when adding dependencies or assets to a production plugin. Done when the archive includes runtime dependencies but excludes personal settings, logs, test records, and secrets.

7. If installation is within the request's scope, confirm the real VSD Craft plugins directory, preserve the old version, and install. Perform the [hardware checks](references/development.md#hardware-checks). Do not install on a real device when only authoring was requested. Done when the report distinguishes static validation, mock-host tests, the real application, and physical hardware results.

## Resources

- [Compatibility matrix](references/elgato-compatibility.md): API differences and concrete porting guidance.
- [Field observations](references/field-observations.md): Findings from existing implementations and reproduction conditions.
- [Sources](references/sources.md): Official URLs, reference commit, and verification dates.
- [Development guide](references/development.md): Scaffold, packaging, and hardware verification.
- [scaffold.py](scripts/scaffold.py), [package_plugin.py](scripts/package_plugin.py), and [Python helper tests](scripts/test_helpers.py).
- [Scaffold PI](assets/template/ui/inspector.js), [HTML](assets/template/ui/index.html), and [mock-host tests](assets/template/test/smoke.cjs).
- [README](README.md): User-facing quick start, in Japanese.
