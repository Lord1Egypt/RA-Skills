## Description:

Render and summarize a public X (Twitter) link when you need to read the tweet/article content without logging in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tylordius](https://clawhub.ai/user/tylordius)

### License/Terms of Use:

ISC

## Use Case:

External users, developers, and agents use this skill to read public X/Twitter permalinks and convert the visible tweet, thread, linked article, and media details into a concise Markdown summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill can browse arbitrary URLs in an unsandboxed Chromium process.

Mitigation: Run only in an isolated or hardened environment, restrict use to trusted X/Twitter permalinks, and prefer a release that validates allowed hosts, blocks local or private-network destinations and redirects, and restores browser sandboxing.

Risk: The security review reports dependency and logging risks.

Mitigation: Review dependencies before installation, update or pin dependencies as appropriate, and prefer a release that removes raw debug page logging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tylordius/skills/x-read)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown thread summary with source URL, author, timestamp, tweet text, linked article, media URLs, and ALT text when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads one public X/Twitter permalink per run and may include up to the main tweet plus three replies.]

## Skill Version(s):

1.0.1 (source: package.json, CHANGELOG, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
