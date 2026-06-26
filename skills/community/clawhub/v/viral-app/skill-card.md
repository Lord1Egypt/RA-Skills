## Description: <br>
Use the viral.app API from an agent with a local CLI for account analytics, tracked videos/accounts, projects, creator hub, and live data operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feliche93](https://clawhub.ai/user/feliche93) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to query viral.app analytics, manage tracked accounts and videos, build creator and viral-video reports, and perform approval-gated resource or payout operations through the viral-app CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A sufficiently privileged viral.app API key can expose or change account, creator, project, video, and payout data. <br>
Mitigation: Install only if the viral-app CLI is trusted, use an appropriately scoped VIRAL_API_KEY, avoid logging or committing keys, and rotate any exposed credential. <br>
Risk: Payout initiation and other write operations can create financial or data-changing side effects. <br>
Mitigation: Prefer read or review-first workflows, confirm intent before POST/PUT/PATCH/DELETE operations, verify recipients and amounts, and preserve the calculation payload and integrity token returned by payout calculation. <br>
Risk: Broad analytics queries and exports can produce excessive or misleading results when filters, dates, or org-scoped IDs are wrong. <br>
Mitigation: Collect platform IDs, org-scoped IDs, date ranges, and pagination limits first; start with narrow queries and include direct viral.app links for review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/feliche93/viral-app) <br>
- [Skill Homepage](https://github.com/fmd-labs/viral-app-skills/tree/main/viral-app) <br>
- [viral.app Application](https://viral.app/app) <br>
- [Leaderboard Report Template](assets/templates/leaderboard.md) <br>
- [Viral Video Library Report Template](assets/templates/viral-video-library-report.md) <br>
- [Creator Payments and CPM Report Template](assets/templates/creator-payments-cpm-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON-oriented CLI summaries, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read workflows should use narrow queries and JSON output by default; report templates produce Slack-ready Markdown.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
