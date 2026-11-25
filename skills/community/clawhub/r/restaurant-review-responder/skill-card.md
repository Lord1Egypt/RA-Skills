## Description:

Drafts separate public replies and private recovery notes for US restaurant reviews, tracks recurring themes, and flags cases for a manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US independent restaurant owners and local marketing managers use the skill to classify Google and Yelp reviews, draft separate public replies and private recovery notes, track recurring themes, and flag cases for a manager.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious with medium confidence and incomplete coverage because referenced paths were missing; it reports a permissions-scope concern and a possible tool reference.

Mitigation: Before installation, review the skill's file-writing needs and the runtime permissions it would receive, and account for the incomplete scan.

Risk: The skill describes an optional, separately downloaded Windows executable that is not code-signed.

Mitigation: Keep the download optional, verify its SHA-256 against the value in the skill, and run it only if you accept an unsigned program; avoid running it as administrator without a reason.

Risk: The theme tally copies up to three matching input lines per theme into its Markdown report, which may expose customer details if the report is shared.

Mitigation: Review the generated report for personal or sensitive review details and remove them before sharing.

## Reference(s):

- [US review reply rules](artifact/references/review-reply-rules.md)
- [ClawHub release page](https://clawhub.ai/rapidworker1/skills/restaurant-review-responder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text and Markdown, including public replies, private recovery notes, escalations, and a theme tally]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The tally report includes up to three example input lines for each theme.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
