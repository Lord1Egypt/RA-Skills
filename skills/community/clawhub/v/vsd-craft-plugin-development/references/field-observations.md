# Anonymized Implementation and Operational Findings

These notes extract transferable findings from existing M3 development records.
The compilation on 2026-10-09 does not represent new physical tests.
Primary logs, user settings, personal paths, scene/device IDs, and UI screenshots are not bundled.

## F1: Installation and Basic Rendering (2026-10-01)

- Recorded environment: Windows, VSD Craft **3.10.205.0918**, MagTran M3.
- A Node plugin started from `%APPDATA%\HotSpot\StreamDock\plugins\<uuid>.sdPlugin`.
- Logs confirmed host WebSocket registration and willAppear for four keys and three knobs.
- SVG images, numbers, state colors, manual titles, and knob rendering were checked in the application.
- The user confirmed that one physical key could switch to the target application.
- This does not verify all knobs, the actual LCD display, or KVM switching.
- Original source: `DEPLOYMENT-ja.md` from the existing development artifacts. The exact bundled Node patch version and firmware were not recorded.

Recheck method: Place one key in a new test scene and record registration, willAppear, setImage, application rendering, and physical input in order.

## F2: Controllers and Coordinates (2026-10-01 through 2026-10-02)

- The public manifest uses Knob; public dial-event examples use Encoder.
- Real application willAppear logs reported Knob as the knob controller.
- In the recorded M3 layout, key row=0 was at the bottom; knob column=5/row=0 was at the top.
- Therefore, accepting only controller===Encoder or assuming a top-left origin for every key can break valid paths.
- Original sources: `SDK-NOTES.md`, deployment notes, and `live-verification.txt` from 2026-10-02.

Recheck method: Record each knob's rotation and press separately, mapping event name, context, coordinates, and controller.
Keep coordinate rules specific to each model and display surface; do not generalize from knob counts or screen dimensions.

## F3: USB Reconnection Without a New willAppear (2026-10-02)

- The application retained placements, but the plugin deleted its context list on disconnect.
- No willAppear was resent after reconnect, leaving zero rendering targets even though external data retrieval remained healthy.
- The fix retained contexts within the same host connection, discarded held/pending input on disconnect, and invalidated the image cache to resume rendering on reconnect.
- The fix record confirmed that 16 contexts were retained and settings and 214 profiles remained unchanged.
- Original source: `deployment.json` for the reconnection fix. This probe did not independently recapture the host version; the associated deployment series is F1.

The scaffold's mock test reproduces disconnect followed by connect without a new willAppear.
Verify the same operation separately on hardware. When the host WebSocket closes, exit the plugin process and let the host relaunch it.

## F4: switchToProfile Accepted but Ineffective (Development Series of 2026-10-02)

- Existing SDK notes record that VSD Craft parsed switchToProfile but
  `SDActionCanvasWidget::onSwitchToProfile` performed no action.
- Inspection reached a bare return through Qt meta method 65. Addresses are binary-specific and must not be hardcoded into an implementation.
- Sending different names or IDs still did not switch scenes.
- The built-in scene-switching action worked. An alternative implementation used UI Automation to select an existing scene and page 1.
- Later live logs recorded scene-home success and preserved display state, but some attempts failed to preserve foreground state.
- Original sources: `SDK-NOTES.md` and `live-verification.txt` from 2026-10-02.
- **Scope limitation**: The deployment notes name version 3.10.205.0918, but the no-op inspection did not retain an executable hash or an independent version capture.
  Do not infer permanent non-support for every binary with that version number; recheck the target version if the API is needed.

Recheck method: Record the target version and executable hash, then observe both the sent command and the selected scene in a test setup.
Successful WebSocket transmission alone is not successful scene switching.
Prefer the built-in action as the alternative. For UI Automation, verify hidden-window operation, foreground preservation, the target device, and duplicate scene names.
The hidden-UI recovery checks on 2026-10-03 included simulated failures and did not include a physical KVM retest.

## F5: Backgrounds Are Separate from Ordinary Key Images (Research on 2026-10-04)

- Official M3 material advertises real-time interactive backgrounds and keypress effects.
- Creator SDK's setBackgroundImgData sends RGB data to a device path; it is not setImage addressed to an action context.
- Connection steps for safe coexistence with VSD Craft, update rates, and composition with keys remain unverified.
- Original sources: `README-ja.md` from the interactive-background research and [public sources C1/M2](sources.md).

Keep background commands out of the ordinary key-image scaffold. Investigate this separate path only when backgrounds are requested.
