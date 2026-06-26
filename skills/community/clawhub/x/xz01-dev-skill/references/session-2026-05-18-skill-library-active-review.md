# Skill-library active review lesson

Session context: after the user stated the dual-end list pagination rule as “这是规范”, the assistant updated `xz01-dev-skill` immediately with SKILL.md edits, a session reference file, memory compression, metadata synchronization, and publishing.

Durable lesson for future xz01 work:

- A user phrase such as “这是规范” in xz01 context is a first-class skill signal, not a temporary chat note.
- Promote the rule into the class-level xz01 umbrella skill, not a narrow one-off skill.
- Prefer the structure: concise SKILL.md rule + `references/session-*.md` detail file.
- Keep the rule in dev scope, test scope, common pitfalls, and verification checklist when it affects implementation and acceptance.
- When ordinary tools are available, complete the xz01 publish workflow: bump version, sync `skill.json` and `_meta.json`, then publish with `clawhub publish`.
- If a later review asks to update the skill library and the rule was already captured, still look for a small class-level improvement: e.g. add the meta-lesson about how to handle “这是规范” corrections.
