## Description:

Session Memory helps OpenClaw agents preserve context by converting session transcripts into searchable Markdown, generating a structured memory glossary, and suggesting memory-aware cron prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to retain searchable context across compacted or isolated OpenClaw sessions, including session transcripts, entity indexes, decisions, and cron job memory prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy broad private OpenClaw conversation history, names, decisions, file paths, and cron prompts into durable searchable files.

Mitigation: Enable it only in workspaces where this retention is acceptable, and add redaction or role filtering before indexing sensitive sessions.

Risk: Weak session scoping may index more history than the operator intended.

Mitigation: Narrow session selection, review configured input paths, and use retention limits before running full or scheduled indexing.

Risk: Cron-based updates can keep sensitive memory artifacts current without repeated manual review.

Mitigation: Require review before enabling cron jobs and maintain a cleanup process for generated memory files and state.

Risk: Artifact claims about scanner cleanliness conflict with the server security verdict.

Mitigation: Rely on the server security summary and review the skill before installation rather than trusting promotional safety claims in the artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moltbotmolty-del/skills/sessionmemory)
- [Publisher profile](https://clawhub.ai/user/moltbotmolty-del)
- [AI Advantage](https://aiadvantage.ai)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and setup guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces durable local memory artifacts such as memory/sessions/*.md, memory/SESSION-GLOSSAR.md, state JSON files, and cron optimization reports.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
