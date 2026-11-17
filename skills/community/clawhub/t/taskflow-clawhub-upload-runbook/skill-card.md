## Description:

Step-by-step runbook for pairing TaskFlow (business process orchestration) with ClawHub (skill registry ingestion) to publish a digital skill artifact to the ClawHub resource center.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this runbook to follow a repeatable TaskFlow-to-ClawHub process for validating, publishing, and verifying a skill release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following the final publish command can upload or update a skill in ClawHub using the user's authenticated account.

Mitigation: Run the dry-run publish command and inspect or verify commands first, then publish only the intended skill folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/taskflow-clawhub-upload-runbook)
- [ClawHub publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides runbook steps and ClawHub CLI commands; no generated files or API calls are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
