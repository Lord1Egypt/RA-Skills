## Description:

Speech Paper Daily searches recent arXiv speech and audio preprints, reads each relevant paper from a domain-expert perspective, produces structured Chinese summaries with technical details and scores, and can write the digest to Tencent Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jusperlee](https://clawhub.ai/user/jusperlee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to find recent speech and audio arXiv papers, review concise Chinese technical digests, and create a daily Tencent Docs report when document-writing tools are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create Tencent Docs in a fixed folder through local script execution without a clear confirmation step.

Mitigation: Use it only in environments where Tencent Docs writes and local helper execution are approved, and confirm the intended document creation before running the write step.

Risk: Broad trigger phrases may activate document-writing behavior when a user only expects a chat summary.

Mitigation: Review the skill before installation and prefer chat-only use unless Tencent Docs creation is explicitly desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jusperlee/skills/speech-paper-daily)
- [arXiv cs.SD new submissions](https://arxiv.org/list/cs.SD/new)
- [arXiv eess.AS new submissions](https://arxiv.org/list/eess.AS/new)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Chinese Markdown digest with paper metadata, links, technical summaries, experiment notes, scores, and optional Tencent Docs creation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May split long digests into multiple documents when content exceeds the documented length threshold.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
