---
name: workled
description: "The Agent states: `thinking`, `waiting`, `idle`, and `error` are automatically synced to workled via the MCP protocol. Light‑effect parameters and touch macros can also be configured for the device over MCP."
description_zh: "Agent 状态：`thinking`（思考中）、`waiting`（等待响应）、`idle`（空闲）、`error`（异常报错），可经由 MCP 协议自动同步至 workled 设备；同时支持通过 MCP 协议对设备的灯效、触控宏进行配置。"
description_en: "The Agent states: `thinking`, `waiting`, `idle`, and `error` are automatically synced to workled via the MCP protocol. Light‑effect parameters and touch macros can also be configured for the device over MCP."
version: "0.1.31"
display_name: "workled"
display_name_en: "workled"
---

# workled MCP Controller

## MCP Tool Reference

| Tool | Property | Description | Usage |
|---|---|---|---|
| set_agent_state | state_name: string | Set LED to reflect agent state (`thinking`/`waiting`/`idle`/`error`) | `set_agent_state("thinking")` |
| get_agent_state | — | Returns current agent LED state (empty string if unset) | `get_agent_state()` |
| set_brightness | brightness: integer | LED brightness 0-255; 0 = off | `set_brightness(128)` |
| get_brightness | — | Returns current LED brightness 0-255; | `get_brightness()` |
| set_effect | effect_name: string, effect_json: string | effect_name ∈ `led`(manual effect)/`thinking`/`waiting`/`idle`/`error`/`touch`(touch effect); effect_json is a JSON string `{"type","hue","saturation","value","speed"}`. Light must be on first (set_brightness > 0). Map natural-language colors to HSV (see table below). | `set_effect("led", '{"type":"breathe","hue":180,"speed":50}')` |
| get_effect | effect_name: string | Get effect_name config as JSON | `get_effect("thinking")` |
| set_macro | macro_name: string, macro_json: string | Set the macro for a touch pad gesture; macro_name ∈ `single_click`/`double_click`/`long_press`; macro_json is a JSON array of segments (see Macro Format); empty macro_json resets | `set_macro("single_click", '[{"combo":"ctrl+c"}]')` |
| get_macro | macro_name: string | Returns the macro as a JSON array string, or empty string if unset (password values masked) | `get_macro("single_click")` |

### Mapping natural-language colors to `set_effect`

Use `type:"solid"` unless the user asks for an animation. Map a color name to HSV:

| Description | type | hue | saturation | value |
|---|---|---|---|---|
| pure white | solid | 0 | 0 | 255 |
| warm white | solid | 30 | 80 | 255 |
| red | solid | 0 | 255 | 255 |
| orange | solid | 30 | 255 | 255 |
| yellow | solid | 60 | 255 | 255 |
| green | solid | 120 | 255 | 255 |
| cyan/teal | solid | 180 | 255 | 255 |
| blue | solid | 240 | 255 | 255 |
| purple/violet | solid | 270 | 255 | 255 |
| pink | solid | 330 | 200 | 255 |
| dim/night mode | solid | 30 | 80 | 60 |
| rainbow (animated) | rainbow | - | - | - |

Rule of thumb: hue 0-359 picks the hue, saturation 0-255 (0 = white/pastel, 255 = vivid), value 0-255 brightness. Pastel/white tones use low saturation; vivid tones use 255.

## Verify & Troubleshooting

Whenever workled is newly installed, used for the first time in a session, or the LED is not responding:

- In the "Agent" dialog box, enter `Is the workled diagnosis in effect?` or `诊断workled生效了吗？`
- Or manually run the diagnostic program: `node <skill-dir>/index.js status [--client <name>]`

## Waiting-state coverage by client

`waiting` means "the agent asked you something and is blocked on your
answer". workled can only light it when the client itself emits an event for
the question — it cannot invent one. Coverage therefore differs per client.

| Client | Waiting state | Notes |
|---|---|---|
| opencode | ok | — |
| kilo | ok | — |
| dsh | ok | — |
| pi | no | No event is fired for the option prompt |
| openclaw | no | No event is fired for the option prompt |
| hermes | partial | Normal option prompts emit nothing; permission prompts do |
| workbuddy | ok | - |
| trae-cn | ok | - |

On the clients marked no (and on hermes for normal option prompts), the LED
stays on `thinking` while a question is pending. If you want "waiting for you"
to be visible there, call `set_agent_state("waiting")` yourself before asking
the question.

Measured 2026-09-07; re-check after a client update, since this depends on each
client's own hook/plugin surface.

## Reference

- Macro format reference [macro_format.md](references/macro_format.md)
- Device setup reference [device_setup.md](references/device_setup.md)

## Video Demo

https://www.bilibili.com/video/BV1FK4k6WEKe

## Contributing

- Repository: https://github.com/git-hub-cloud/workled
- Issues: https://github.com/git-hub-cloud/workled/issues
