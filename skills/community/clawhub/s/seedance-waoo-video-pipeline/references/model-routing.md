# Model Routing

## Configuration Principle

Upperstream and downstream must be configurable independently.

- **upstream Seedance** must support its own standalone 厂商 / 接口地址 / 模型名 / API Key
- **downstream waoowaoo image** may use another
- **downstream waoowaoo video** may use another
- **downstream waoowaoo TTS** may use another
- **downstream waoowaoo ambience** may use another or local assets only

Do not assume one shared key or one shared model across all stages.
Do not bind Seedance text generation to the same vendor/model as downstream video or TTS unless the user explicitly configures them that way.

## Default Routing Table

| Stage | Preferred | Fallback | Avoid / Notes |
|---|---|---|---|
| Seedance pre-production text (`E01_前置思考.md`, `E01_剧本.md`) | independently configured `upstream.seedance` text model | none for formal execution | do **not** silently use the chat model as Seedance |
| Analysis / planning | stable text model | another reliable text model | avoid wasting premium media quota |
| Image generation | configured image model | project-approved backup | keep prompt and style stable |
| Video generation | official `MiniMax-Hailuo-2.3` | approved backup such as Vidu when policy allows | do not assume all Hailuo variants are supported |
| TTS | official `speech-2.8-hd` | approved TTS backup | narration must match subtitle text |
| Ambience | local ambience library | AI ambience fallback | reject generic musical beds presented as ambience |
| Final packaging | FFmpeg | none | deterministic export preferred |

## Formal Seedance rule

- `upstream.seedance` is mandatory for formal Seedance-side script generation.
- Placeholder model names and demo API keys do **not** count as valid upstream configuration.
- If upstream Seedance is not runnable, the agent must say so plainly and enter configuration guidance instead of presenting the result as formal Seedance output.

## Video Rules

- Prefer official route when account and quota permit.
- Treat probe tasks as diagnostics, not formal deliverables.
- If token plan does not support a model, switch policy instead of retrying blindly.

## TTS Rules

- The active subtitle text is the default narration text.
- Keep narration short for short clips.
- Favor clarity over expressive flourish.

## Ambience Rules

- Prefer local environmental assets over generated music.
- Use AI ambience only when it clearly behaves like environment rather than song or score.
