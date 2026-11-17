## Description:

Helps agents find video assets from tested sources, check their licenses, and record credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and creative teams can use this skill to find B-roll, music, sound effects, motion elements, fonts, icons, LUTs, and HDRIs for an edit. It guides them through checking each asset's license and recording credits when required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Asset terms can vary by item, and a successful download does not establish permission for the intended use.

Mitigation: Check each item's license and attribution requirements; skip assets with unclear or restricted terms.

Risk: The skill's install examples use unpinned npx commands, and searches may share query terms with third-party services.

Mitigation: Review the install command and package before running it, and avoid sending sensitive search terms to outside providers.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/vargai/skills/video-asset-sources)
- [Source and license guide](artifact/references/all-sources.md)
- [Tested queries](artifact/references/tested-queries.md)
- [Source traps](artifact/references/traps.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance and shell commands; downloaded media assets and a JSON credits file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The credits file records source and license details, with an attribution line when required.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata; embedded metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
