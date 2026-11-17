## Description:

Convert one public website URL or an explicit batch of public URLs into a reusable skill zip backed by rendered HTML snapshots and a bounded JSONL retrieval index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvisyaoht](https://clawhub.ai/user/jarvisyaoht)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn public documentation, help centers, knowledge bases, or explicit URL batches into reusable agent skills with saved HTML snapshots and a bounded search index.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill renders user-selected public pages and the security evidence flags weakened browser and HTTPS protections.

Mitigation: Run the skill in an isolated environment or container with minimal filesystem access, current browser binaries, pinned dependencies, normal Chromium sandboxing, and normal HTTPS certificate validation.

Risk: The skill can retain and package content from public websites selected by the user.

Mitigation: Use it only on public content you are permitted to retain and redistribute.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jarvisyaoht/skills/web-to-skill)
- [Metadata Contract](references/metadata.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON metadata, HTML snapshots, JSONL index records, configuration files, and a skill ZIP package.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bounded crawler artifacts and a packaged skill zip under the task workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
