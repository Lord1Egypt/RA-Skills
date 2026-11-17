## Description:

Seedance 2.0 Shot Design helps agents turn vague video ideas into structured cinematic prompts for Seedance 2.0, with bilingual output, storyboard segmentation, cinematography references, lighting guidance, and validation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woodfantasy](https://clawhub.ai/user/woodfantasy)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and video-production teams use this skill to convert short creative briefs into Seedance-ready video prompts with shot timing, camera motion, lighting, sound, and negative-prompt structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an unsafe remote CLI installer in the documentation.

Mitigation: Do not run the documented CLI installer as written; use a verified, versioned installer or an official package channel.

Risk: The security review notes broad auto-activation for video-prompt requests.

Mitigation: Install only when a Seedance-focused prompt-writing skill is desired, and review generated prompts before use.

Risk: The security review notes platform-bypass wording and moderation-related guidance.

Mitigation: Use only original, licensed, or clearly permitted content, and do not use the skill to evade platform or legal restrictions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/woodfantasy/skills/seedance-shot-design)
- [Agent Skills Specification](https://agentskills.io)
- [Seedance Specs](references/seedance-specs.md)
- [Cinematography](references/cinematography.md)
- [Director Styles](references/director-styles.md)
- [Quality Anchors](references/quality-anchors.md)
- [Scenarios](references/scenarios.md)
- [Audio Tags](references/audio-tags.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown with structured prompt code blocks and optional CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese/English prompt output; prompt-generation guidance is instruction-only and the packaged scripts are documented as standalone developer tools.]

## Skill Version(s):

1.9.1 (source: evidence.release.version, SKILL.md frontmatter, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
