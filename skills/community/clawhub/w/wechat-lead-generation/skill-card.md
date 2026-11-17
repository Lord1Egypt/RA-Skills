## Description:

Automates WeChat lead capture, intent analysis, scoring, and optional personalized reply draft generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ling-qian](https://clawhub.ai/user/ling-qian)

### License/Terms of Use:

MIT

## Use Case:

Sales, community operations, and marketing users use this skill to identify potential leads from WeChat conversations, score intent signals, and prepare follow-up reports or reply drafts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill profiles WeChat contacts and can persist private message data, contact names, inferred interests, scores, and message excerpts in local reports and long-term memory records.

Mitigation: Install only when authorized to process the relevant conversations; protect generated reports and memory records; avoid enabling memory or broad collection permissions until consent, redaction, retention, and deletion controls are clear.

Risk: Automatically generated replies could be sent based on incomplete or incorrect lead inferences.

Mitigation: Keep auto-reply disabled by default and use the generated replies as drafts for human review before sending.

Risk: A WeChat cookie or login state used for real collection is a session secret.

Mitigation: Store WeChat credentials securely, limit access to the runtime environment, and avoid sharing or committing session material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ling-qian/skills/wechat-lead-generation)
- [Publisher Profile](https://clawhub.ai/user/ling-qian)
- [Project Homepage](https://github.com/ling-qian/openclaw-skills/tree/main/wechat-lead-generation)

## Skill Output:

**Output Type(s):** [markdown, json, text, guidance, configuration]

**Output Format:** [Markdown reports, JSON profile artifacts, reply draft text, and optional memory records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include contact names, message excerpts, inferred interests, lead scores, and suggested replies.]

## Skill Version(s):

0.1.0 (source: frontmatter, changelog, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
