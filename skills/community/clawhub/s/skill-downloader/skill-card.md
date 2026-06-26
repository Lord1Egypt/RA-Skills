## Description: <br>
Discover, compare, review, install, or update OpenClaw skills from trusted sources with a review-first workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyang100](https://clawhub.ai/user/yyang100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find, compare, inspect, install, or update OpenClaw skills while preserving explicit approval and source review before write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or updating an unfamiliar skill can write files into a workspace or global skill directory. <br>
Mitigation: Inspect source material first, prefer official registry workflows, require explicit user approval before writes, and use a workspace-local install when testing an unfamiliar skill. <br>
Risk: Partial or minimal metadata can lead to unsupported comparisons or recommendations. <br>
Mitigation: Disclose missing fields, mark unavailable values as unknown, and give a firm recommendation only when the inspected information is complete enough to support it. <br>


## Reference(s): <br>
- [Advanced Workflows](references/advanced-workflows.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yyang100/skill-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured review summaries and inline commands when installation is approved] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source labels, unknown-field disclosure, recommendation status, and approval gating before write actions.] <br>

## Skill Version(s): <br>
0.1.20 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
