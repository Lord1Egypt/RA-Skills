## Description:

Generates platform-optimized social posts, captions, images, and content calendar artifacts for Twitter/X, Instagram, LinkedIn, and Facebook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinanping-cpu](https://clawhub.ai/user/yinanping-cpu)

### License/Terms of Use:


## Use Case:

Marketing teams, creators, and developers use this skill to draft platform-specific social content, optional images, and calendar outputs before human review or scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topics and prompts can expose secrets, embargoed campaign plans, customer data, or confidential business details to OpenAI APIs.

Mitigation: Do not include sensitive or confidential content in prompts unless that use has been approved for the connected OpenAI account and data handling policy.

Risk: Generated social content can be inaccurate, off-brand, or unsuitable for publication without review.

Mitigation: Install and use the skill as a draft-generation tool, with explicit human review before publishing or scheduling content.

Risk: Optional upload workflows and platform API credentials can affect real social accounts if enabled without governance.

Mitigation: Treat upload credentials cautiously, store them outside generated artifacts, and require explicit review before any post is published to a real account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinanping-cpu/skills/yinan-social-content-generator)

## Skill Output:

**Output Type(s):** [Text, Images, JSON metadata, Files, Shell commands, Configuration guidance]

**Output Format:** [Plain text posts, PNG images, JSON metadata, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call OpenAI APIs for text and image generation; can fall back to template-based text generation when AI dependencies are unavailable.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
