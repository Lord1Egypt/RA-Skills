## Description:

Turns Markdown or plain text into polished high-resolution long images, share cards, or posters using 18 built-in visual styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and AI-agent operators use this skill to convert Markdown or plain text into styled local PNG images for reports, knowledge cards, posters, and social sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can download npm packages during installation.

Mitigation: Review the visible install output and prefer pinned dependencies with a lockfile before using the skill in managed environments.

Risk: The renderer runs headless Chrome over generated local HTML with weakened browser protections.

Mitigation: Render only trusted local HTML, review or change the browser flags before deployment, and avoid using the skill as a general web fetcher.

Risk: Persisting output configuration in shell startup files can have lasting effects outside a single run.

Mitigation: Use explicit per-run output paths or temporary environment variables unless persistent output configuration is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/songhonglei/skills/text-to-elegant-image)
- [README](artifact/README.md)
- [Render Verification and Options](artifact/docs/VERIFICATION.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with HTML/CSS snippets, bash commands, and local PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local HTML and PNG files; default long-image width is 560 px, poster and cover modes use fixed 600 x 800 output.]

## Skill Version(s):

1.2.1 (source: evidence release metadata and SKILL.md; CHANGELOG released 2026-07-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
