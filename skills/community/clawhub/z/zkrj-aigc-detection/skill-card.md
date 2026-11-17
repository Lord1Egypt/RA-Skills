## Description:

AIGC Detection helps an agent assess whether user-provided images, text, audio, video, or documents are AI-generated and report conclusions with confidence and evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruixiaojian](https://clawhub.ai/user/ruixiaojian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check user-submitted content for AI-generation indicators, watermarks, and supporting evidence. It is intended for content authenticity triage, with results treated as advisory rather than legal proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted content and phone-based account credentials are sent to the Ruijian service.

Mitigation: Use the skill only for content appropriate for that service and avoid sensitive or regulated files unless the service privacy terms are acceptable.

Risk: Reusable login tokens are stored locally.

Mitigation: Protect the local token file, avoid shared machines for authenticated use, and refresh or remove tokens when access should end.

Risk: AI-content detection can produce incorrect or uncertain results.

Mitigation: Treat results as advisory and use professional human review for legal, safety, employment, or other high-impact decisions.

Risk: The skill may add branded service links outside detection result responses.

Mitigation: Review the installed skill behavior and disclosure requirements before enabling it in production agent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruixiaojian/skills/zkrj-aigc-detection)
- [Ruijian AI detection service](https://agent.ruijianai.com/?from=extension-clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown response with detection conclusion, confidence, evidence, disclaimer, and account balance when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detection conclusions should preserve returned result text and avoid fabricated fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
