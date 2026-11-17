## Description:

Orchestrates script-to-final-video production through a strict stage-gated workflow that prepares storyboards, generates Seedream images, renders Seedance multi-shot videos, supports checkpointed confirmation and resume, and optionally concatenates the final mp4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkenny0](https://clawhub.ai/user/kkenny0)

### License/Terms of Use:


## Use Case:

Developers and video workflow builders use this skill to convert raw text, JSON, or staged artifacts into auditable storyboard assets, rendered shot videos, and an optional final merged mp4 while reviewing each checkpoint before continuing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Storyboards and prompts may be sent to configured external generation providers.

Mitigation: Use non-sensitive source material and install only when external provider processing is acceptable.

Risk: Video download and filename handling were flagged as under-scoped by the authoritative security scan.

Mitigation: Use a dedicated project directory, review generated storyboard JSON before confirming stages, and avoid untrusted storyboard JSON until identifiers and downloaded URLs are constrained or patched.

## Reference(s):

- [Design Document v0.2.0 Phase 1](docs/design-doc-v0.2.0-phase1.md)
- [Logic Flow v0.2.0 Phase 1](docs/logic-flow-v0.2.0-phase1.md)
- [Storyboard v1 Schema](references/storyboard-v1.schema.json)
- [Assets v1 Schema](references/assets-v1.schema.json)
- [Staged Artifacts v1 Schema](references/staged-artifacts-v1.schema.json)
- [Sub-Agent Parser Contract](references/subagent-parser-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with shell commands, Python CLI usage, JSON storyboard/assets artifacts, checkpoint files, generated images, shot videos, run summaries, and optional final mp4 output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+, ARK_API_KEY, access to the seedance-video-generation skill, and FFmpeg for final video concatenation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
