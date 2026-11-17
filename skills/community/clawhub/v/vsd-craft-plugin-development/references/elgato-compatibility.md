# Elgato Stream Deck to VSD Craft / StreamDock Compatibility

Compiled and checked against public documentation: **2026-10-09**. Scope: host JSON/WebSocket communication and manifests.
Conclusion: **Basic registration, key/knob events, settings, and image updates share wire formats.
Manifests, SDK libraries, distribution formats, and device-specific features require separate adaptation.**

Use the relevant rows as implementation starting points rather than researching confirmed details from scratch every time.
Source IDs refer to [links and retrieval dates](sources.md); F numbers refer to [field observations](field-observations.md).

## Assessments and Evidence

- **Shared**: Official documentation agrees on the format and meaning of the listed fields. This does not guarantee compatibility of all extension fields.
- **Adaptation required**: The difference and porting approach are known.
- **Observed no-op**: The operation failed in a particular existing installation, not necessarily every version.
- **Unverified / separate path**: Use through an ordinary plugin is not established. This does not deny that the API itself exists.
- Keep specifications, official source code, application observations, and physical tests separate. Mock tests validate custom code, not host compatibility.

## Compatibility Matrix

| Feature | Elgato | VSD Craft / StreamDock | Assessment and implementation | Evidence |
|---|---|---|---|---|
| Host registration | `-port -pluginUUID -registerEvent -info`, `{event,uuid}` | Same launch information and JSON registration | **Shared**. Parse arguments by name and use the host-supplied registration event | E1 / S1 / G1; real application registration F1 |
| Endpoint | WebSocket on the host-supplied port | localhost WebSocket | **Shared**. No arbitrary fixed port or custom public server is needed | E1 / S1 / G1 |
| Keys | `keyDown` / `keyUp`, `action/context/device/payload` | Same event names and basic fields | **Shared**. Distinguish action UUID from placement context. Do not require Elgato-specific additions such as `resources` | E1 / S3; limited physical verification F1 |
| Knob rotation | `dialRotate`, integer `ticks`, `pressed` | Same name, sign convention, and pressed-rotation information | **Shared by specification**. Use tick magnitude, not event count. Check model-reserved operations separately | E1 / S3 |
| Knob press | `dialDown` / `dialUp` | Same names | **Shared by specification**. Handle press and release separately; do not trigger an action on an orphaned release | E1 / S3 |
| Controller declaration | `Controllers:["Encoder"]` | `Controllers:["Knob"]` | **Adaptation required**. Use Knob in the manifest. Received-event examples use Encoder while real willAppear events use Knob, so dispatch by event name | E2 / S2 / S3 / F2 |
| Visibility lifecycle | `willAppear` / `willDisappear` | Same names, also settings and coordinates | **Partially shared**. Do not depend on resending after reconnect. Do not persist contexts as stable IDs across host processes | E1 / S3 / F3 |
| Device connection/disconnection | `deviceDidConnect` / `deviceDidDisconnect` | Same names | **Shared by specification**. Distinguish USB disconnection from host-socket disconnection | E1 / S3 / G1 / F3 |
| System wake | `systemDidWakeUp` | Same name, with a warning about duplicate delivery | **Shared by specification**. Wake does not mean the device is ready. Tolerate duplicates without triggering the action again | E1 / S3 |
| Settings | `setSettings {context,payload}` / `didReceiveSettings` | Same format: the sent payload is the settings object; received settings are in `payload.settings` | **Shared**. Keep the PI registration UUID and action context roles separate | E1 / S4 / S3 |
| Global settings | `getGlobalSettings` / `setGlobalSettings` / `didReceiveGlobalSettings` | Same names; use the registered plugin UUID | **Shared by specification**. Keep separate from per-action settings. Not used by the minimal scaffold | E1 / S3 / S4 / G1 |
| Key images | `setImage {context,payload:{image,target,state?}}` | Same format; examples include SVG data URLs and PNG/JPG/GIF | **Partially shared**. Use data URLs. GIF acceptance does not guarantee video playback or FPS | E1 / S4; SVG rendering in the application F1 |
| title/state/alert | `setTitle` / `setState` / `showAlert` / `showOk` | Same names | **Shared by specification**. Do not continually send setTitle when preserving user-entered titles | E1 / S4 |
| PI connection function | `connectElgatoStreamDeckSocket(...)` | Same name for compatibility; official template also exposes `connectSocket` | **Shared with an alias**. Expose both and register using the supplied arguments | S1 / G1 |
| PI messages | `sendToPlugin` / `sendToPropertyInspector` | Same names, but StreamDock documentation also specifies `action` | **Adaptation required**. Include action explicitly and add actionContext to the custom payload to distinguish it from the PI ID | E1 / S4 / G1. actionContext is a scaffold-defined field |
| Manifest SDK | Current documentation specifies `SDKVersion:2` or `3` | `SDKVersion:1` | **Adaptation required**. Generate a VSD-specific manifest | E2 / S2 |
| Node declaration | Current documentation lists Node 20 / 24 | `Nodejs:{Version:"20"}`; minimum Windows host `3.10.188.226`, with bundled 20.8.1 documented at introduction | **Adaptation required**. Distinguish the local development Node version from the host's bundled version | E2 / S2. Exact Node patch version on the physical setup was not captured |
| Manifest image paths | Icon/Image paths omit extensions | Examples use relative paths including `.png` or other extensions | **Adaptation required**. Use actual filenames in the VSD manifest | E2 / S2 / F1 |
| Application SDK library | `@elgato/streamdeck` Action classes and registration APIs | Official Node examples exchange JSON directly through `ws` | **Replace the adapter**. Reuse domain logic and replace the host boundary. Unmodified use of the entire Elgato SDK is untested | G1 / F1 |
| Scene switching | `switchToProfile` targets **only profiles bundled with the plugin**, not arbitrary user profiles | Not listed in public sent-event documentation S4; an existing installation accepted it but performed no action | **Observed no-op**. Prefer built-in scene switching. If needed, verify UI Automation separately | E1 / F4. Exact inspected binary hash was not recorded |
| Touch/feedback layouts | `setFeedback` / `setFeedbackLayout`, etc. | Not listed in S4 | **Unverified**. Do not reuse Elgato Stream Deck + rendering layouts unchanged on M3 | E1 / S4 |
| Model-specific information and new APIs | Elgato device enums, Neo, `resources`, etc. | Not all corresponding values and events have been compared | **Unverified**. Do not hardcode numeric enums or require unnecessary extension fields | E1 / E2 / S3 |
| Distribution | Elgato distribution paths such as `.streamDeckPlugin` | For development, place `<uuid>.sdPlugin` in plugins | **Adaptation required**. This skill's ZIP is for extraction and copying; do not rename it to an Elgato package format | S5 / F1 |
| Full-screen background | Separate from ordinary key images | Creator SDK exposes `setBackgroundImgData {path,payload:{imgData}}` | **Separate path**. This is not setImage addressed to an action context. Direct use on the plugin socket and coexistence with the application are unverified | C1 / M2 / F5 |

## Ready-to-use Wire Examples

Registration:

```js
socket.send(JSON.stringify({event: launch.registerEvent, uuid: launch.uuid}));
```

Image update (`target:0` targets both display surfaces):

```json
{"event":"setImage","context":"action-instance","payload":{"image":"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='144' height='144'><rect width='144' height='144' fill='#2563eb'/></svg>","target":0}}
```

Saving and receiving settings use different shapes:

```json
{"event":"setSettings","context":"action-instance","payload":{"step":2}}
{"event":"didReceiveSettings","context":"action-instance","payload":{"settings":{"step":2}}}
```

S4's getSettings description refers to the plugin UUID, which can be confused with its per-action description.
The scaffold uses `willAppear.payload.settings` and `didReceiveSettings` instead of depending on this ambiguous path.

## What This Matrix Does Not Establish

Unmodified installation of arbitrary Elgato plugins, physical macOS operation, video/GIF playback on every model,
compatibility with all KVM products, and simultaneous use of the background API and VSD Craft remain unverified.
Update only the rows needed for the task, using target-version official documentation, then source/implementation evidence, then a focused hardware test.
