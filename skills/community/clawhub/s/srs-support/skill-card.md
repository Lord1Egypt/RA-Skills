## Description:

SRS Support helps users, operators, and DevOps teams answer practical questions about Simple Realtime Server protocols, configuration, codecs, deployment, monitoring, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winlinvip](https://clawhub.ai/user/winlinvip)

### License/Terms of Use:

MIT-0

## Use Case:

External users, operators, DevOps teams, and developers use this skill to deploy, configure, operate, monitor, and troubleshoot SRS media-server workflows. It provides practical protocol, codec, configuration, scaling, and troubleshooting guidance rather than SRS source-code modification support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger wording is broad enough that non-SRS streaming questions could be routed to this skill.

Mitigation: For ambiguous streaming questions, confirm SRS relevance or explicitly name the intended technology before applying the skill guidance.

Risk: Oryx-specific questions are outside the skill's supported scope.

Mitigation: State that Oryx support is planned but not available yet, and do not provide Oryx-specific operational guidance.

## Reference(s):

- [SRS Support Skill Page](https://clawhub.ai/winlinvip/skills/srs-support)
- [SRS overview knowledge base](memory/srs-overview.md)
- [SRS documentation set](trunk/3rdparty/srs-docs/doc/)
- [SRS full configuration reference](trunk/conf/full.conf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, URLs, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in SRS knowledge files and relevant documentation; no generated files are described by the skill.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
