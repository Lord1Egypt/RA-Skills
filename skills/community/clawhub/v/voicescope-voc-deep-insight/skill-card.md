## Description:

VoiceScope VOC Deep Insight helps agents analyze customer feedback by guiding VoiceScope login, data upload, viewpoint extraction and clustering, taxonomy generation or validation, batch tagging, per-row sentiment, keyword, summary, scenario, and action analysis, and result retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z18211674869-maker](https://clawhub.ai/user/z18211674869-maker)

### License/Terms of Use:

MIT-0

## Use Case:

Product, CX, support, and user research teams use this skill to turn reviews, tickets, surveys, and interview notes into customer-experience insights. It supports feedback clustering, tagging, taxonomy work, and row-level analysis while keeping users in control of column selection and taxonomy confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected customer feedback data is uploaded to VoiceScope and analysis results are stored in the user's VoiceScope project.

Mitigation: Use only data approved for VoiceScope processing, avoid regulated or highly sensitive customer data unless organizational review has approved it, and confirm the target text column before uploading.

Risk: The local VoiceScope token file is sensitive, and the security evidence notes broad credentials with weak local permission controls.

Mitigation: Treat the local token file as secret material, log out when finished, and prefer a version with narrower OAuth scopes and hardened credential-file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z18211674869-maker/skills/voicescope-voc-deep-insight)
- [VoiceScope platform](https://voiceaiscope.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, concise result summaries, direct platform links, and optional CSV, JSON, or Excel downloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task IDs, table and column IDs, taxonomy IDs, exported file paths, row counts, cluster summaries, sentiment distributions, and VoiceScope result links.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
