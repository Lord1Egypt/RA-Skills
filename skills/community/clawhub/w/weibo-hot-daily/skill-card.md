## Description:

Fetches Weibo hot-search rankings and can present basic summaries or export trend data for monitoring workflows.

This skill is for research and development only.

## Publisher:

[mkt-agents](https://clawhub.ai/user/mkt-agents)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current Weibo trending topics, inspect hot-search metadata, and save results for lightweight reporting or monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled Weibo session cookie could expose or reuse someone else's credential.

Mitigation: Prefer a release that removes the embedded cookie and requires user-managed authentication only when needed.

Risk: The package may overstate features such as push delivery, scheduling, or AI capabilities.

Mitigation: Verify required behavior against the shipped code and treat the release as a Weibo fetch and export tool until those features are proven.

Risk: The documented installation command uses the latest installer instead of a pinned installer version.

Mitigation: Pin installer and skill versions during deployment, and verify package hashes against the release evidence.

Risk: Running the skill sends requests to Weibo endpoints and returns live public trend data.

Mitigation: Review local policy and Weibo terms before use, and avoid processing sensitive monitoring targets without approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkt-agents/skills/weibo-hot-daily)
- [Weibo hot-search API endpoint](https://weibo.com/ajax/side/hotSearch)
- [Weibo search result links](https://s.weibo.com/weibo?q=...)

## Skill Output:

**Output Type(s):** [text, json, csv, shell commands, guidance]

**Output Format:** [Terminal text plus optional JSON or CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on live responses from Weibo endpoints and command-line options such as top count, summary, file path, and format.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
