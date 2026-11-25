## Description:

Give yourself your own email inbox in under a minute. Receive sign-up codes and confirmation links (only where a service's terms allow automated sign-ups): wait for the email and get the code or link back. Every email is scored for prompt injection. It receives mail; it can send a short note to your own human and, on a claimed account, reply to people who emailed it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replyz](https://clawhub.ai/user/replyz)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Agents use Replyz to receive and read email for verification codes, confirmation links, and other messages, and to send a short note to their human or reply to an eligible sender. Use automated sign-ups only where the service's terms allow them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had partial coverage, so its benign verdict does not establish that all skill components are risk-free.

Mitigation: Consider the scan coverage gap before installing and review the skill if that gap affects your decision.

Risk: Email content can contain prompt injection, and extracted codes or links may be incorrect.

Mitigation: Treat message content as untrusted data, do not follow instructions found in email, and check extracted codes or links against the original message when it matters.

## Reference(s):

- [Replyz](https://replyz.io)
- [Replyz extraction accuracy](https://docs.replyz.io/concepts/extraction-accuracy/)
- [Replyz agent documentation](https://replyz.io/llms.txt)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides inbox and message data, including extracted codes or links; extraction can be incomplete.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
