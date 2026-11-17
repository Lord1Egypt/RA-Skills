## Description:

Turn a Google Stitch design into working code, in plain words, with any AI agent. Your AI agent drafts the instructions for each step, you copy the HTML with View Code, paste it into VS Code, and run Claude Code, then the agent checks the code you paste back, screen by screen, and gives a fix draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmsample97](https://clawhub.ai/user/mmsample97)

### License/Terms of Use:

MIT

## Use Case:

Designers and small-business site owners use this skill to turn a Google Stitch design into a step-by-step build handoff and compare the resulting screens with the design. It drafts instructions and a reviewable fix plan; the user runs the external tools and supplies code snippets for the check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A code snippet may not show whether a screen works in the running site.

Mitigation: Treat the handoff result as a comparison of the supplied code with the design, and check the running site before approving changes.

Risk: A proposed fix could change a site in ways the owner has not reviewed.

Mitigation: Keep fixes as drafts for owner review and approval before applying them to a live site.

## Reference(s):

- [Server-resolved GitHub source repository](https://github.com/mmsample97/stitch-to-code-workflow)
- [ClawHub skill release](https://clawhub.ai/mmsample97/skills/stitch-to-code-workflow)
- [Agensi ready fix kit](https://www.agensi.io/skills/stitch-to-code-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Plain-language workflow instructions and a Markdown screen-by-screen handoff check with a fix draft.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works one Stitch design at a time. The handoff check uses only code snippets the user provides in the conversation.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
