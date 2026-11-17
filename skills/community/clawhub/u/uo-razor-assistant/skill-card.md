## Description:

Slash-invocable Razor and UO Outlands reference assistant for macros, scripts, hotkeys, profile XML, validation, and shard-safe guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neomagnetar](https://clawhub.ai/user/neomagnetar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review, generate, repair, and validate Ultima Online Razor macros, Razor scripts, hotkey bindings, and profile XML while preserving shard- and version-sensitive uncertainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Razor macros or scripts can automate in-game actions in ways that conflict with shard automation rules or PvP restrictions.

Mitigation: Review generated artifacts before use, test them in a safe area, and follow the shard's automation and PvP rules.

Risk: Profile XML, macro, or script changes can disrupt a user's local Razor setup if applied incorrectly.

Mitigation: Back up Razor profiles, macros, and scripts before applying changes, then validate behavior in the Razor client.

Risk: Razor command behavior, hotkey IDs, and Outlands-specific scripting features can vary by client, build, or shard.

Mitigation: Keep version-sensitive details visible and verify uncertain IDs, commands, and restrictions in-client before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neomagnetar/skills/uo-razor-assistant)
- [Razor Core Reference for OpenClaw Skill Pack](references/core_reference.md)
- [Glossary of Razor Terms](references/glossary.md)
- [Hotkey Action Map](references/hotkey_action_map.csv)
- [Macro Serialization Legend](references/macro_serialization_legend.md)
- [Outlands Constraints](references/outlands_constraints.md)
- [Profile XML Examples](references/profile_xml_examples.md)
- [Troubleshooting Registry](references/troubleshooting_registry.md)
- [User Guidance](references/user_guidance.md)
- [Validation Workflow](references/validation_workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with fenced code blocks and concise validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce copyable .macro lines, .razor script commands, profile XML snippets, troubleshooting steps, and shard/version caveats.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
