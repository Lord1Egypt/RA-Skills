## Description:

Use the viral.app API from an agent with a local CLI for account analytics, tracked videos/accounts, projects, creator hub, and live data operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feliche93](https://clawhub.ai/user/feliche93)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to guide an agent that reads viral.app analytics, manages tracked entities and projects, and prepares Slack-ready leaderboard, viral video library, and creator payout reports. It also guides cautious execution of creator payout workflows through the local viral-app CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external viral-app CLI and VIRAL_API_KEY can access account, project, creator, and payout data.

Mitigation: Install only after trusting the CLI and scope VIRAL_API_KEY permissions to the intended organization and tasks.

Risk: Payout initiation and auto-approval can create financial obligations.

Mitigation: Review payout amounts, recipients, campaign IDs, integrity tokens, and liability acknowledgements before allowing execution.

Risk: Mutation commands can change tracked accounts, projects, creator hub resources, or refresh state.

Mitigation: Confirm user intent before write actions, inspect command help for required fields, and prefer review-first behavior for payout mutations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feliche93/skills/viral-app)
- [Skill homepage](https://github.com/fmd-labs/viral-app-skills/tree/main/viral-app)
- [viral.app application](https://viral.app/app)
- [Leaderboard report template](assets/templates/leaderboard.md)
- [Viral Video Library report template](assets/templates/viral-video-library-report.md)
- [Creator payments + CPM report template](assets/templates/creator-payments-cpm-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and CLI command guidance, with JSON-oriented command output by default]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the local viral-app CLI, VIRAL_API_KEY, and bundled Markdown templates for report-style outputs.]

## Skill Version(s):

0.1.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
