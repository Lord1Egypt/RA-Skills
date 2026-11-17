## Description:

Search public LinkedIn, X, and Reddit posts for brand monitoring, competitor monitoring, public-conversation research, and weekly marketing briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shash7](https://clawhub.ai/user/shash7)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers and growth teams use this skill to search public social posts, review sourced brand or competitor mentions, and prepare concise monitoring or weekly brief notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to SocialListeningAPI and may consume account credits.

Mitigation: Use only intended monitoring queries, confirm the selected platforms before running the search, and install the skill only when sending those queries to SocialListeningAPI is acceptable.

Risk: API keys could be exposed if copied into prompts, command arguments, or committed files.

Mitigation: Keep SOCIALLISTENING_API_KEY in the process environment and pass search query/platform values through the execution environment rather than the command string.

Risk: Public social search results can be irrelevant, incomplete, or misleading.

Mitigation: Review returned errors and cited URLs before summarizing or taking action, and treat results as research leads rather than verified conclusions.

## Reference(s):

- [Monitoring workflows](references/monitoring-workflows.md)
- [SocialListeningAPI](https://sociallisteningapi.com)
- [SocialListeningAPI API key settings](https://app.sociallisteningapi.com/settings/api-key)
- [ClawHub skill page](https://clawhub.ai/shash7/skills/social-listening-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON search results and sourced Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are sorted newest first, include public source URLs, and should be reviewed by a person before action.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
