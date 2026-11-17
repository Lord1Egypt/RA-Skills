## Description:

Guide for modifying USD ASCII (.usda) files, including prims, properties, composition arcs, variants, and transforms. Use when editing or reviewing .usda files by hand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomkrikorian](https://clawhub.ai/user/tomkrikorian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical artists use this skill to make focused edits to USD ASCII scene files while preserving composition, formatting, paths, transforms, and property types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested edits or commands could modify USD assets or write derived files unexpectedly.

Mitigation: Confirm target files and output paths before running commands, keep backups or version control, and use inspection-only options such as usdedit --noeffect when changes are not intended.

Risk: Incorrect USD paths, property types, transforms, or composition edits could break scene behavior.

Mitigation: Inspect the stage structure first, preserve existing authoring style, validate touched paths and connections, and run USD validation tools such as usdchecker when appropriate.

## Reference(s):

- [USD Editor on ClawHub](https://clawhub.ai/tomkrikorian/skills/usd-editor)
- [USD Syntax Essentials](references/usd-syntax.md)
- [Prims and Properties](references/prims-properties.md)
- [Composition Arcs and Variants](references/composition-variants.md)
- [Transforms and Units](references/transforms-units.md)
- [Time Samples](references/time-samples.md)
- [USD Command-Line Tools](references/command-line-tools.md)
- [usdcat](references/usdcat.md)
- [usdchecker](references/usdchecker.md)
- [usdedit](references/usdedit.md)
- [usdrecord](references/usdrecord.md)
- [usdtree](references/usdtree.md)
- [usdzip](references/usdzip.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown with inline USD ASCII and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces editing guidance and command suggestions; it does not execute tools itself.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
