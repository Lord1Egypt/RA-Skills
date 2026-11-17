## Description:

Parse ChatGPT or Gemini shared conversation links and save Q&A pairs as notes to GetNote (biji.com).

This skill is ready for commercial/non-commercial use.

## Publisher:

[silentforce](https://clawhub.ai/user/silentforce)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract Q&A turns from public ChatGPT or Gemini shared conversations, review the extracted note titles, and save selected notes to GetNote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak URL validation could allow the browser automation to open unintended or internal URLs.

Mitigation: Use the skill only in a constrained environment and prefer a release that strictly validates HTTPS hostnames and share-link paths before browser navigation.

Risk: Runtime installation of mutable browser dependencies can change behavior between runs.

Mitigation: Review before installing and prefer a release that pins Playwright and requires explicit consent before downloading browser artifacts.

Risk: Imported shared conversations may contain sensitive user or business information.

Mitigation: Avoid links from untrusted people, review extracted notes before saving, and treat imported conversations as potentially sensitive.

## Reference(s):

- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
- [GetNote skill](https://clawhub.ai/iswalle/getnote)
- [Share to GetNote on ClawHub](https://clawhub.ai/silentforce/skills/share2getnote)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON note objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The parsing script emits a JSON array of note objects with title and markdown content fields.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
