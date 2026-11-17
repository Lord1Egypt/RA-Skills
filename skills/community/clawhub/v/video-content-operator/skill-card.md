## Description:

Helps creators decide what video or social content to make, how to package it for platforms, which source materials to use, and what to do next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, founder-builders, operators, and small teams use this skill to turn creator context, goals, platforms, and available source materials into content direction, draft packages, and execution handoff briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local OpenClaw MEMORY.md and USER.md files and print or write derived creator profile details.

Mitigation: Run it only against an explicit workspace, avoid --output unless a profile file is intended, and review logs and generated artifacts before sharing them.

Risk: Content recommendations may be based on incomplete creator state, inferred goals, or lightweight platform defaults.

Mitigation: Confirm the creator goal, platform priority, and source material before using a recommendation for public content or handing it off to an editing tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/video-content-operator)
- [Video Content Operator MVP](artifact/references/mvp.md)
- [Sparki Content Operator MVP Spec](artifact/references/mvp-spec.md)
- [Input Schema (MVP)](artifact/references/input-schema.md)
- [Output Examples](artifact/references/output-examples.md)
- [Implementation Notes](artifact/references/implementation-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Structured Markdown recommendations and JSON execution briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve creator context, separate content decisions from editing execution, and avoid exposing private memory-derived context unless the user chooses to share or save it.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
