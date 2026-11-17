## Description:

Story generation pipeline skill. Supports multi-episode continuous generation, graph management, AI quality check + human confirmation dual control mechanism.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexidyg](https://clawhub.ai/user/hexidyg)

### License/Terms of Use:


## Use Case:

External creators and developers use Shorts Builder to plan and continue serialized short-form story episodes with graph-backed continuity, AI quality review prompts, and human confirmation before proceeding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local graph storage can be misdirected through graph or pipeline ID handling to access JSON files outside the intended data folder.

Mitigation: Restrict pipeline IDs to a safe allowlist and verify resolved graph paths remain under the graph storage directory before use in shared or automated environments.

Risk: Generated story text is reused in later prompts and may contain untrusted or misleading instructions.

Mitigation: Treat generated story content as untrusted context, review episode outputs before continuation, and avoid placing secrets or privileged instructions in story prompts.

Risk: Story pipeline and review state are persisted locally.

Mitigation: Avoid storing confidential story material or personal data unless local retention is acceptable, and clear pipeline state when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexidyg/skills/shorts-builder)
- [Publisher profile](https://clawhub.ai/user/hexidyg)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, guidance]

**Output Format:** [Markdown story episode drafts, prompt text, and JSON review/status objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local pipeline and graph state; prompts and example content are mostly Chinese-language unless directed otherwise.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
