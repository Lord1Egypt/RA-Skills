## Description:

Browser-based song creation with Suno (suno.ai), including gathering a song brief, generating lyrics, setting Persona/Custom mode, and producing new tracks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[machinesbefree](https://clawhub.ai/user/machinesbefree)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide an agent through browser-based Suno song creation, from collecting a song brief and drafting lyrics to operating Custom mode, reviewing generated tracks, and returning links or downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may submit lyrics, style tags, persona choices, and generation actions to Suno through a browser session.

Mitigation: Confirm the user's intent before generation and avoid sending sensitive or private material in prompts, lyrics, or style instructions.

Risk: Generated links or downloads may be shared outside the current workspace.

Mitigation: Review generated links and downloaded files before distributing them more broadly.

## Reference(s):

- [Suno Browser Workflow](references/suno-workflow.md)
- [Suno](https://suno.ai)
- [ClawHub Skill Page](https://clawhub.ai/machinesbefree/skills/suno-browser-songmaking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown with song briefs, lyrics, style tags, browser guidance, links, and file paths when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party Suno track links or local download paths after browser generation.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
