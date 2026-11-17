# Compatibility Research Sources

The [compatibility matrix](elgato-compatibility.md) summarizes the necessary facts and differences rather than reproducing public manuals.
Documentation changes; retain retrieval dates as well as URLs.

## StreamDock Plugin SDK

- [S1: Registration](https://sdk.key123.vip/en/guide/registration.html): Retrieved 2026-10-09. Explicitly states that the same function name is used for Elgato compatibility.
- [S2: Manifest](https://sdk.key123.vip/en/guide/manifest.html): Retrieved 2026-10-09. SDK 1, Knob, Node 20, and the minimum Windows host version.
- [S3: Received Events](https://sdk.key123.vip/en/guide/events-received.html): Retrieved 2026-10-09. Input, settings, and connection events.
- [S4: Events Sent](https://sdk.key123.vip/en/guide/events-sent.html): Retrieved 2026-10-09. Settings, images, titles, and PI communication.
- [S5: Get Started](https://sdk.key123.vip/en/guide/get-started.html): Research record from 2026-10-01. Local installation.
- [G1: Official Node template](https://github.com/MiraboxSpace/StreamDock-Plugin-SDK/tree/a3fb38490a36f507a09af8b78bdddac49c10668f/SDNodeJsSDKV2): Pinned to commit `a3fb38490a36f507a09af8b78bdddac49c10668f`; registration and PI source retrieved again on 2026-10-09.
  - `plugin/utils/plugin.js`: ws, launch arguments, and exit on host close.
  - `propertyInspector/utils/action.js`: connectSocket alias, registration UUID, and action context.
  - This skill neither bundles nor runs the vendor's automatic copy/delete scripts.

## Elgato

- [E1: Plugin WebSocket](https://docs.elgato.com/streamdeck/sdk/references/websocket/plugin/): Retrieved 2026-10-09. Basic events, setImage, setSettings, feedback, and switchToProfile target restrictions.
- [E2: Manifest](https://docs.elgato.com/streamdeck/sdk/references/manifest/): Retrieved 2026-10-09. SDK 2/3, Node 20/24, Encoder, and image paths without extensions.

The comparison concerns **JSON communication**. It does not establish compatibility of Elgato TypeScript SDK objects or binaries.

## VSDinside and Device-level SDK

- [M1: VSD Craft Plugin Download](https://www.vsdinside.com/blogs/tutorial/plugin-download): Retrieved 2026-10-09. Official direction from VSD Craft to StreamDock Space.
- [M2: MagTran M3-specific guide](https://www.vsdinside.com/blogs/tutorial/user-guide-magtran-m3-quick-start-beginner-tutorial): Researched 2026-10-04 and retrieved again 2026-10-09. Backgrounds, keypress effects, and screensavers.
- [C1: Creator WebSocket Commands](https://creator.key123.vip/en/websocket/events-sent.html): Retrieved 2026-10-09. RGB background data addressed to a device path; instructs clients not to send other commands while setting the background.
  - C1's model table, including the M3 knob count, differs from the recorded MagTran M3 setup. Do not reuse a specification table based on model name alone.
  - Treat C1 as a different contract from the ordinary VSD Craft plugin socket. Coexistence remains unverified.

## Scaffold Dependency API

- [ws README](https://github.com/websockets/ws#readme) / [API](https://github.com/websockets/ws/blob/master/doc/ws.md): Also checked through Context7 `/websockets/ws` on 2026-10-09. open/message/error/close, maxPayload, and loopback WebSocketServer.
- The scaffold was implemented independently, not copied from official source. Fetch `ws` from npm and pin it through the generated project's lockfile.
- Observations from existing installations are in the [field notes](field-observations.md). Primary logs and personal data are not bundled.
