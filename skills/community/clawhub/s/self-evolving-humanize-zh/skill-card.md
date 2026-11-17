## Description:

Generates or rewrites Chinese communication copy so it sounds more human, natural, less templated, and less like polished AI writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyidatascience](https://clawhub.ai/user/tianyidatascience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writing assistants, and agent users use this skill to generate or rewrite Chinese customer replies, social posts, follow-ups, updates, and other communication copy. It runs an inspectable baseline-to-challenger loop with local scoring so users can compare candidates and retain necessary facts and constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full user drafts may be sent to the configured model endpoint.

Mitigation: Use only a trusted local or explicitly approved model endpoint, and avoid confidential customer or business drafts unless that endpoint is acceptable.

Risk: Prior draft snippets and run outputs may remain in plaintext local state.

Mitigation: Clear ./runs and the persistent humanize strategy-state file when retained text should be removed.

Risk: Runtime dependencies may change if installed without pinning for production use.

Mitigation: Review and pin dependencies before production deployment.

## Reference(s):

- [Humanize ClawHub release](https://clawhub.ai/tianyidatascience/skills/self-evolving-humanize-zh)
- [Open source model and dependency notes](OPEN_SOURCE.md)
- [Scoring reference](references/scoring.md)
- [Preset reference](references/presets.md)
- [BAAI/bge-reranker-v2-m3 model card](https://huggingface.co/BAAI/bge-reranker-v2-m3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown process summary with generated Chinese copy, scores, selected candidates, and local run artifacts such as JSON traces and reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local run folders, scoring JSON, reports, and a persistent strategy-state file.]

## Skill Version(s):

0.1.6 (source: server release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
