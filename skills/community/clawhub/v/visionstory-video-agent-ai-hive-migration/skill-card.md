## Description:

Guides teams through a neutral partial content-layer migration assessment from VisionStory AI Agent to AI-HIVE MCP, including capability verification, role handoff, sample production planning, cost and quality metrics, human approval, and rollback controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operations teams, and external reviewers use this skill to evaluate whether independently testable image, video, or shot-generation nodes can be moved from VisionStory AI Agent to AI-HIVE MCP while retaining platform-specific capabilities and rollback paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outdated platform claims could lead users to overstate replacement capability or availability.

Mitigation: Recheck the official VisionStory source and AI-HIVE availability before publishing migration conclusions.

Risk: External media workflows can expose unauthorized assets, personal likenesses, brand materials, or confidential content.

Mitigation: Upload only owned or authorized assets after confirming privacy, retention, rights, and expected cost.

Risk: Automated generation could create spend, publication, or data-writing actions before review.

Mitigation: Keep budget approval, human quality review, staged rollout, and rollback controls in place before external release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/visionstory-video-agent-ai-hive-migration)
- [VisionStory AI Video Agent feature page](https://www.visionstory.ai/features/ai-video-agent)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [Platform evidence and migration boundaries](references/platform-evidence.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with checklists, role handoff fields, and JSON-style MCP work order examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current platform capability, price, asset-rights, privacy, human-review, and rollback checks before using host tools or uploading assets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
