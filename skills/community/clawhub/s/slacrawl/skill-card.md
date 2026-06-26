## Description: <br>
Slacrawl helps agents search Slack archives, check sync freshness, inspect threads and DMs, run SQL counts, and work with the Slacrawl repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw](https://clawhub.ai/user/openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams with local Slack archives use this skill to query bounded message slices, check archive freshness, refresh stale data, inspect threads or DMs, and report exact spans, counts, and token/source limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slack archive searches can surface sensitive personal, DM, or private-channel content to the agent. <br>
Mitigation: Install only where Slack archive access is intended, keep personal and company archives in separate configs, and limit searches to the minimum relevant slice. <br>
Risk: API sync and full thread or DM hydration may require Slack tokens with sensitive scopes. <br>
Mitigation: Review Slack token scopes before API sync and do not assume Slack tokens are present. <br>
Risk: Stale local archives can produce incomplete or misleading answers about recent Slack activity. <br>
Mitigation: Check archive freshness with Slacrawl status commands and refresh only when stale or explicitly requested. <br>


## Reference(s): <br>
- [OpenClaw Slacrawl repository](https://github.com/openclaw/slacrawl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and SQL snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports workspace and channel names, absolute date spans, counts, and token/source limits; queries should use bounded result slices.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
