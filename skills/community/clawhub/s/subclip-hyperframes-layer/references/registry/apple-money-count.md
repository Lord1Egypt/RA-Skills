# Apple Money Count — curated registry block

Subclip bundles a controlled adaptation of the upstream HyperFrames `apple-money-count` block as the built-in HyperFrames template with ID `apple-money-count`.

## Source and license

- Upstream item: `heygen-com/hyperframes/registry/blocks/apple-money-count`
- Upstream title: **Apple Money Count**
- Upstream author: Stronkter
- License: Apache-2.0, covered by `references/official/LICENSE`
- Upstream duration and dimensions: 5 seconds, 1920×1080

The upstream block counts from `$0` to `$10,000`, changes the total to green, flashes the frame, and emits a deterministic 62-piece burst of bill and coin shapes. Its upstream package also contains `assets/sfx-production.wav`.

## Subclip adaptation

Use `list_runtime_layer_templates` with `kind: "hyperframes"`. When this block fits the creator's request, call it again with `includeSource: true`, select template ID `apple-money-count`, and adapt or add that returned source. Do not reconstruct the block from this prose and do not run `hyperframes add`.

Subclip's version:

- pins GSAP to `3.15.0`;
- defaults the layer background to transparent;
- retains deterministic counter, flash, landing scale, and money burst choreography;
- exposes editable flat variables;
- omits embedded audio because Subclip Audio owns SFX and mixing.

Available variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `target` | `10000` | Final numeric value, clamped to a safe finite range. |
| `decimals` | `0` | Fixed decimal places from `0` to `4`. |
| `prefix` | `$` | Currency or leading text. |
| `suffix` | empty | Trailing unit such as `M`, `%`, or ` ARR`. |
| `label` | empty | Optional small top label such as `ARR`. |
| `background` | `transparent` | Local block background. Keep transparent unless the creator requests a full scene. |
| `foreground` | `#111315` | Counter text color before impact. |
| `muted` | `#64706b` | Label color. |
| `accent` | `#30d158` | Landing, flash, and bill color. |
| `coin` | `#ffd54f` | Coin color. |

For requests such as `$4.2M`, set `target: 4.2`, `decimals: 1`, `prefix: "$"`, and `suffix: "M"`; if the creator expects individually rolling odometer columns rather than a formatted count, revise the returned source while preserving its deterministic timeline.

If SFX is requested, use Subclip's native audio tools to add and mix an appropriate sound on the project timeline. The upstream WAV is deliberately not executed from inside the isolated HyperFrames layer.
