# Reference Router

Use this file only when you are unsure which Yeelight Smart Home reference to load. It is a navigation index, not a domain rulebook.

## Fast Paths

| User goal | Load |
| --- | --- |
| Turn on/off lights, brightness, color temperature, RGB, state query, scene execute, automation toggle | `device-control.md` |
| Product consultation, manual, FAQ, SKU, pedia result | `product-knowledge.md` |
| Homes, rooms, areas, members, sorting, favorites around home structure | `home-room-area.md` |
| Groups and grouped lighting targets | `groups.md` |
| Existing cloud scene create/update/delete/detail/execute | `scenes.md` plus `payload-shapes.md` when actions are involved |
| Existing cloud automation create/update/delete/detail/enable/disable | `automations.md` plus `payload-shapes.md` when conditions/actions are involved |
| Full-home lighting design or future device-slot materialization | `lighting-design.md` first |
| Standard lighting design import model | `lighting-design-import.md` |
| Product selection for not-yet-installed lighting slots | `lighting-product-selection.md`, then `product-knowledge.md` for official facts |
| Scene recipe conversion for lighting design | `scene-recipes.md` and optionally `lighting-experience.md` |
| Automation recipe conversion for lighting design | `automation-recipes.md` and optionally `automation-events.md` |
| Runtime payload schema, nested actions, button events, items, operations | `payload-shapes.md`; use Runtime `intent.explain` when still unclear |
| Memory, preferences, personalization | `memory-and-personalization.md` |
| Recommendations and recommendation feedback | `recommendations.md` |
| Operation lessons, known pitfalls, fastest paths, reliable fallback paths | `operation-lessons.md` |
| Diagnostics, partial evidence, gateway/panel/knob read surfaces | `diagnostics.md` |
| Risk, confirmation, destructive actions, mixed batches | `safety-and-confirmation.md` |
| Blocked capabilities or non-enabled internal capability classes | `capability-boundaries.md` |
| Device/product words, aliases, typo-prone wording | `device-lexicon.md` |
| Thing model, categories, property keys, capability language | `thing-model.md` |
| Runtime status, auth, cache, errors, clarification handling | `runtime-status-and-errors.md` |
| Response shape, tables, cards, dashboards, notifications, memory/recommendation result wording, product help display | `response-presentation.md` |

## Do Not Confuse

- `scenes.md` is for existing cloud scene entities; `scene-recipes.md` is for converting design intent into action rows.
- `automations.md` is for existing cloud automation entities; `automation-recipes.md` is for simple design-import automation rows.
- `automation-events.md` is trigger and condition vocabulary evidence, not the complete payload contract.
- `lighting-experience.md` is lighting design judgment and ambience interpretation, not Runtime schema.
- `lighting-design-import.md` is for full standard design import. Do not use it for a small edit in a heavily configured existing home unless the user explicitly asks for full design materialization.
- `action-payloads.md` is only a routing index. Prefer `payload-shapes.md`, `scene-recipes.md`, `automation-recipes.md`, and `lighting-design-import.md`.
- `response-presentation.md` shapes the final answer only. It must not override Runtime facts, counts, states, warnings, or failure status.

## Shortest Path Rule

Load one reference first. Add a second reference only when the first file explicitly routes you there or the user goal crosses domains.
