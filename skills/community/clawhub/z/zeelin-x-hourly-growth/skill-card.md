## Description:

X hourly growth ops skill for finding AI/builder follow-back or mutual-connect posts, leaving high-quality English replies through the logged-in Chrome browser, and running on a daily hourly schedule with dedupe, safety filters, and daily caps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate a capped X engagement loop that finds AI/builder follow-back or mutual-connect posts, filters low-quality targets, posts short English replies through a logged-in Chrome browser, and maintains a ledger to avoid repeated replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended execution can post public X replies through a logged-in browser.

Mitigation: Use dry-run first, enable the hourly LaunchAgent only when intentional, keep daily caps in place, and remove the scheduler with the uninstall script when no longer needed.

Risk: Chrome debugging access exposes the selected browser profile broadly while the automation is running.

Mitigation: Keep the OpenClaw Chrome profile limited to X and avoid using a personal browsing profile for this skill.

Risk: Automated replies may be repetitive, mistargeted, or unwanted if candidate filters miss low-quality posts.

Mitigation: Review logs and ledger output, keep the provided safety filters and caps, and use dry-run output to inspect candidates before posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/zeelin-x-hourly-growth)
- [Comment templates](references/comment-templates.txt)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown instructions with inline bash commands; runtime output may include text logs, ledger files, or JSON dry-run candidates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime can post public X replies through a logged-in Chrome profile; dry-run mode lists candidates without posting.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
