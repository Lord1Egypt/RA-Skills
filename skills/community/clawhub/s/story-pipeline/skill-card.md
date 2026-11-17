## Description:

Story generation pipeline skill. Supports multi-episode continuous generation, graph management, AI quality check + human confirmation dual control mechanism. Automatically manages relationships between characters, scenes, and hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexidyg](https://clawhub.ai/user/hexidyg)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to coordinate multi-episode story generation with continuity tracking, AI quality review, and human approval checkpoints. It is intended for serial story drafting workflows that need pause, resume, modification, and graph-backed continuity management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local graph storage can access JSON files outside its intended folder when pipeline_id is not strictly contained.

Mitigation: Validate pipeline_id against an allowlist pattern and enforce resolved-path containment before any graph read, write, or delete.

Risk: Broad filesystem access or untrusted direct calls to graph management methods could expand the impact of the path containment issue.

Mitigation: Install only after review in shared or automated environments, limit filesystem permissions, and avoid exposing GraphManager methods to untrusted callers.

Risk: AI review pass or fail decisions may rely on unvalidated model output.

Mitigation: Derive pass or fail locally from validated numeric scores and keep human confirmation before storing accepted episode state.

Risk: Chinese-first prompts and outputs may surprise users expecting English-only behavior.

Mitigation: Document the default language behavior and configure prompt language expectations before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexidyg/skills/story-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown story drafts and review prompts, plus JSON status and review objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first prompts, local JSON state, AI review scoring, and human confirmation checkpoints.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
