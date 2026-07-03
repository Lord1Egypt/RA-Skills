# Lighting Product Selection

Use this reference when a lighting design request contains future device slots or product wording such as 格栅灯, 射灯, 筒灯, 青空灯, 爱思/S 系列, beam angle, color, opening size, wattage, or premium positioning.

## Product Selection Boundary

Product choice is a Skill/AI decision, not a Runtime decision.

- Run `node scripts/product-select.mjs --query "<slot wording>" --room "<room>" --goal "<design goal>" --limit 8` for each distinct slot family.
- Use `product.pedia.search` only when official product facts, product status, model, manual, FAQ, SKU resources, or attachments are needed.
- Treat product candidates as evidence, not automatic winners. Compare user constraints and room/design role before choosing.
- Each imported design slot must carry evidence-backed `skuCode`, `capabilityPid`, and `productComponentId` copied from the chosen candidate, plus useful readable product fields.
- Never invent SKUs, product names, categories, models, SKUs, grouping capability, or product support.

## Product Identity Terms

- `skuCode` is the concrete selected SKU number visible to designers and installers.
- `capabilityPid` is the capability/firmware identity shared by products with the same controllable capability. It is not a concrete SKU and not a user-facing product ID; multiple appearances or SKU variants can share it.
- `productComponentId` identifies the product capability component used by the product model.
- Product name, series, category, design attributes, and notes are readable evidence for the user and installer.
- If the user cares about exact model, color, shape, beam angle, opening size, or finish, choose a candidate whose readable evidence matches that constraint and keep the reason in notes.

## Constraint Order

1. Hard product constraints: category, install style, color, opening, size, beam angle, wattage, shape, head count, protocol, series, model, nickname, version words.
2. Room role: ambient, task, accent, decorative, path, wet-area ambience, low glare, high rendering, focused beam.
3. Future behavior: dimming, color temperature, RGB color, scene participation, automation action support.
4. Design positioning: entry/basic/value/professional/flagship/high-end only after hard facts fit.
5. Availability/status and practical installation notes.

## Accessory And Power Completeness

- Do not treat strip lights, drivers, power supplies, modules, dry-contact devices, and controllers as interchangeable lighting slots. Preserve each as its own product-selection family when the user mentions it.
- When selecting strip lights or low-voltage linear lighting, include required driver/power-supply planning notes or separate design slots when the design cannot be installed without them.
- Match power-supply capacity to strip/light length and per-meter wattage when those facts are present. Example heuristic from legacy design prompts: a 60W supply should not be planned for more than 12m of 5W/m strip without explicit product evidence.
- If wattage, voltage type, length, or installation type is missing and materially affects the accessory choice, ask one smallest question or record an explicit assumption in product notes.
- For dry-contact/control-module wording such as 干接点/干节点, preserve the normalized product family and do not convert it into an ordinary light action.

## Room Guidance

- Living room: ambient ceiling light plus accent layers; grille/spot lights support wall/object emphasis.
- Bedroom: low glare, warm defaults, calm transitions; use focused 24°/36° beams only for accent or task needs.
- Secondary bedroom/study: neutral task-friendly lighting with warmer rest scenes.
- Bathroom: clarity and comfort; 青空灯 is ambience evidence, not moisture certification.
- Corridor/entrance: path lighting and time-window logic when real sensors exist.
- Dining/table area: warm-neutral rendering for face and food; avoid direct glare.

Series guidance: D is entry/basic, E is professional value, S is flagship/high-performance, P is exploratory high-end. Treat this as positioning guidance, not a substitute for product facts.

## Ambiguity Policy

- For ambiguous but actionable full-design requests, choose a reasonable default and record the assumption in the slot product notes.
- Ask only when the missing choice materially changes product choice, room assignment, safety, or persistent configuration.
- Keep user-stated constraints even if the chosen candidate is not the highest scoring candidate.
