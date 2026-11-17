## Description:

Collect recent high-interaction Xiaohongshu/Rednote notes and cleaned comments using demand-style keywords for small-scale user need discovery and downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zev55555](https://clawhub.ai/user/zev55555)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect recent Xiaohongshu public notes and cleaned comment data for demand discovery, product validation, content research, and later LLM analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores authenticated Xiaohongshu cookies locally.

Mitigation: Use a dedicated or low-risk account, restrict permissions on the cookie file, and do not share or commit the cookie directory.

Risk: Authenticated publishing and commenting commands can post under the user's account if explicitly invoked.

Mitigation: Use publishing and comment commands only when posting is intended, and review local content before reuse or publication.

Risk: The security scan verdict is suspicious because authenticated session handling and posting paths require review.

Mitigation: Review the skill before deployment, keep collection runs small, and stop when login, captcha, or platform risk controls appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zev55555/skills/xiaohongshu-demand-discovery-skill)
- [Publisher profile](https://clawhub.ai/user/zev55555)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated collection artifacts are JSONL, JSON, and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Demand discovery writes notes_clean.jsonl, comments_clean.jsonl, collection_summary.json, and collector_report.md under data/demand_discovery/<timestamp>/ by default.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
