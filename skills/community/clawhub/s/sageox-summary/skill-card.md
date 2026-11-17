## Description:

Generate an overall team summary covering the last 24 hours across all SageOx-enabled teams. Reads distilled daily entries via `ox distill history` and produces a structured, Slack-ready overview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galexy](https://clawhub.ai/user/galexy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team leads use this skill to collect new SageOx daily distill entries across configured teams and synthesize them into a Slack-ready status summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and checks a pinned local ox binary under the user's home directory.

Mitigation: Use the bundled checksum-pinned install flow and review the install guidance before running it.

Risk: Selected SageOx team activity is sent to Claude through the user's existing Claude credentials.

Mitigation: Confirm the data is appropriate for Claude processing and review the generated Slack summary before posting.

Risk: Distilled entries may contain user-supplied or adversarial text that can influence the generated summary.

Mitigation: Treat the summary as a draft and check citations and claims against the underlying distill entries.

## Reference(s):

- [SageOx homepage](https://sageox.ai)
- [SageOx Distill skill](https://clawhub.ai/skills/sageox-distill)
- [ClawHub skill page](https://clawhub.ai/galexy/skills/sageox-summary)
- [ox distill history PR](https://github.com/sageox/ox/pull/507)
- [Installing ox](references/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Slack mrkdwn summary with setup and shell-command guidance when prerequisites need attention.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ox, claude, and jq; uses existing Claude credentials to summarize selected SageOx distill entries.]

## Skill Version(s):

0.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
