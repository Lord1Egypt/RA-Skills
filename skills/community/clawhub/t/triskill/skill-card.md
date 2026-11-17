## Description:

Triskill helps agents fact-check live claims, diagnose failed commands through bounded retries, and coordinate shared state through a local locked JSON store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welove111](https://clawhub.ai/user/welove111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Triskill to check factual claims against live search results, inspect failed command runs before retrying, and coordinate small shared state across local agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The self-healing helper can execute arbitrary commands with the agent's normal filesystem, network, environment, and account access.

Mitigation: Run it only with commands the user or agent already trusts, keep retries bounded, and review each proposed fix before rerunning.

Risk: Command, stdout, and stderr details are logged in plaintext by the self-healing helper.

Mitigation: Avoid running commands that expose secrets, credentials, or sensitive output, and delete logs when they are no longer needed.

Risk: Fact-check queries may be sent to DuckDuckGo, and shared-memory state is stored locally without encryption.

Mitigation: Do not submit private queries or store secrets in shared memory; use it only for non-sensitive local coordination data.

## Reference(s):

- [Triskill on ClawHub](https://clawhub.ai/welove111/skills/triskill)
- [welove111 publisher profile](https://clawhub.ai/user/welove111)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fact-check, self-heal, and shared-memory scripts return JSON or text for the agent to interpret.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
