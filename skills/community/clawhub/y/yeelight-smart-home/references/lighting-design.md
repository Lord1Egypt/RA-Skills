# Lighting Design

Use this reference for full-room lighting plans, lighting moods, and design suggestions.

- Use `lighting.design.plan` when the user asks for a design, layout, ambience, or multi-room lighting plan.
- Use `lighting.experience.apply` only for temporary ambience or experience changes that Runtime can validate.
- Use `lighting.design.apply` only when the user asks to apply a design to real device lighting state. Runtime routes it through a pending plan and can apply verified device-level power (`p`), brightness (`l`), color temperature (`ct`), and RGB color (`c`) changes according to each device capability.
- Treat old habits and inferred preferences as suggestions, not authority to create persistent configuration.
- If needed devices or capabilities are missing, ask Runtime for clarification or return the blocked result.
- The user-facing answer should describe the proposed result, not internal rules.
- Use real home topology returned by Runtime when available. If the user asks for a design without topology, make assumptions explicit and keep output as a plan.
- Do not create physical sensors, default rooms, groups, scenes, or automations to satisfy a design idea.
- Do not describe `lighting.design.apply` as creating scenes, automations, groups, rooms, or areas. If a design requires persistent scene, automation, group, room, or area changes, split the answer into a proposal and the corresponding Runtime confirmation path only when that specific intent is supported.
