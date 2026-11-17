## Description:

Test internet connection speed using Ookla's Speedtest CLI. Measure download/upload speeds, latency, and packet loss. Format results for social sharing on Moltbook/Twitter. Track speed history over time. Use when asked to check internet speed, test connection, run speedtest, or share network performance stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spsneo](https://clawhub.ai/user/spsneo)

### License/Terms of Use:


## Use Case:

Developers, operators, and external users can use this skill to run internet speed tests, interpret download/upload and latency results, track connection history, and prepare user-reviewed social posts about network performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions include mutable internet-fetched scripts run as root.

Mitigation: Use a verified vendor or package-manager installation path and avoid the documented curl-to-sudo-shell flow.

Risk: Speedtest results can include network and location-adjacent metadata.

Mitigation: Review generated result text before sharing and remove sensitive connection, server, or location details when needed.

Risk: Publishing to Moltbook or Twitter can expose results through stored credentials or broad social tokens.

Mitigation: Use narrowly scoped, revocable tokens and publish only after explicit user review.

## Reference(s):

- [Speedtest CLI Reference](references/speedtest-cli.md)
- [Ookla Speedtest CLI Documentation](https://www.speedtest.net/apps/cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON speed-test data examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save JSON Lines speed history under the user's home directory and may prepare social post text for review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
