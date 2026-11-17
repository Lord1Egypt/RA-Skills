## Description:

Turns one theme into a 7, 14, or 30 post social-media series with narrative continuity and controlled repetition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to turn a theme, audience, tone, and post count into a reviewable social-media content plan with a storyline, post distribution, CTA pacing, asset checklist, and review reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated social posts may repeat claims, invent facts, or turn incomplete input into misleading content.

Mitigation: Use the skill for reviewable drafts only, confirm missing information, and review factual claims before publishing.

Risk: Sensitive or private material supplied as input can appear in the generated content plan.

Mitigation: Remove or anonymize sensitive information before using the skill unless the user is comfortable with it appearing in output.

Risk: The artifact includes unused audit helper modes in scripts/run.py that may confuse reviewers about intended behavior.

Mitigation: Maintainers should remove or document those unused modes; users should rely on the documented structured-brief drafting workflow.

Risk: Users may expect direct social posting or external-system changes.

Mitigation: Keep usage to draft generation, dry-run planning, and human-reviewed checklists; do not use it for automatic posting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/social-post-batcher)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)
- [Artifact README](artifact/README.md)
- [Output Template](artifact/resources/template.md)
- [Structured Spec](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Structured Markdown, with optional JSON output from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs reviewable drafts and checklists; the packaged script can write Markdown or JSON to a local file when explicitly invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
