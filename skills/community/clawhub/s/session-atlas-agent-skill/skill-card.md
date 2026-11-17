## Description:

Build a source-indexed navigation layer over a private Claude JSONL session, preserving evidence locations and uncertainty without reproducing private reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to index private Claude JSONL sessions into evidence-linked navigation artifacts and to prepare manually reviewed session maps without reproducing private reasoning text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated indexes contain private transcript content and absolute paths.

Mitigation: Use only transcripts you are authorized to process, write indexes to a private directory, and do not commit or publish generated output.

Risk: The optional npx installer is unpinned.

Mitigation: Prefer manual installation or direct script use, or pin and verify the installer before running it.

Risk: Validation without an explicit source checks structure but does not independently verify the source evidence.

Mitigation: Run validation with --source when source-backed evidence comparison is required, and use --require-complete-tools when complete tool linkage is required.

## Reference(s):

- [Evidence-linked session maps](references/methodology.md)
- [Session Atlas ClawHub skill page](https://clawhub.ai/antreasantoniou/skills/session-atlas-agent-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON, JSONL, and Markdown index files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated indexes can contain private transcript content, command summaries, tool previews, and absolute source paths.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
