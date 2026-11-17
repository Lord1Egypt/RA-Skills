## Description:

An outbound egress guard for agents that scans messages for leaked secrets and private identifiers before they are sent, then either blocks the send path or redacts findings in place.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workloftai](https://clawhub.ai/user/workloftai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as a pre-send guard for email, social drafts, chat replies, and public-site writes that may accidentally include credentials or private infrastructure details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private-key redaction can leave key material in outbound text.

Mitigation: Use scan mode as a blocking warning gate for private-key findings and manually inspect high-severity findings before any message is sent.

Risk: The scanner is lightweight and should not be treated as a complete DLP control.

Mitigation: Pair it with human review and established credential handling controls for sensitive release paths.

Risk: The benchmark script can read local files under /home/workloft.

Mitigation: Run bench.py only in environments where access to that local corpus is intended, or skip the benchmark during deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workloftai/skills/sluice)
- [Workloft Labs](https://workloft.ai/labs)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text findings on stderr, optional JSON findings, redacted text on stdout, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan mode exits non-zero at or above the configured severity threshold; previews avoid printing full secrets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
