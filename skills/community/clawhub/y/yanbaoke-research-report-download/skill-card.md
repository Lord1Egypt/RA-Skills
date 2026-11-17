## Description:

Search Yanbaoke research reports across industry, brokerage, and institutional sources, return report metadata and summaries, and provide paid report download links when the user supplies a Yanbaoke API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanbaoke](https://clawhub.ai/user/yanbaoke)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Yanbaoke's report corpus, inspect report details, and request short-lived PDF, DOC, or PPT download links. Downloading requires a Yanbaoke API key and may consume account credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guidance uses mutable remote curl downloads without integrity checks.

Mitigation: Prefer the packaged artifact or a signed, checksum-pinned release before installing or executing the skill.

Risk: The setup guidance encourages persistent plaintext storage of YANBAOKE_API_KEY in shell startup files.

Mitigation: Use a session-scoped environment variable, secret manager, or agent credential store instead of committing the key to shell profile files.

Risk: Search terms and filters are sent to Yanbaoke's API.

Mitigation: Avoid submitting confidential or regulated search queries unless the deployment has approved that data sharing.

Risk: Downloads may consume Yanbaoke account credits.

Mitigation: Require explicit user confirmation before invoking downloads that may charge the account.

Risk: The skill text encourages investment recommendations based on report content.

Mitigation: Treat outputs as informational research support and do not rely on the skill for personalized investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanbaoke/skills/yanbaoke-research-report-download)
- [Yanbaoke platform](https://pc.yanbaoke.cn)
- [Yanbaoke API key setup](https://pc.yanbaoke.cn/openclaw)
- [Yanbaoke search API endpoint](https://api.yanbaoke.cn/skills/search_report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report summaries, report metadata, error messages, and short-lived download URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped at 500 items; download links are reported as expiring after about 60 seconds.]

## Skill Version(s):

2.1.0 (source: server release metadata, artifact _meta.json, and scripts/version.mjs)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
