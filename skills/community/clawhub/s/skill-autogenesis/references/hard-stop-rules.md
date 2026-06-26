# Hard Stop Rules

Use these rules to block invalid skill creation.

1. If the outcome is a preference, do not create a skill.
2. If the outcome is a policy, do not create a skill unless it also includes a complete executable procedure.
3. If the outcome is a one-off result, do not create a skill.
4. If the classification record ends with `recommended_action=memory`, `prompt`, or `none`, do not write skill files.
5. If there is no trigger, no ordered action sequence, or no verification signal, do not create a skill.
6. When uncertain, prefer no-op, memory, or prompt over skill creation.

## Fast test

A candidate may become a skill only if all three are true:
- trigger exists
- actionable ordered steps exist
- verification exists
