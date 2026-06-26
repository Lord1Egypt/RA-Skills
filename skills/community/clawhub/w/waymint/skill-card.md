## Description: <br>
Links an OpenClaw agent to its wayMint ERC-8004 on-chain identity certificate and helps the agent share a configured verification URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maksika](https://clawhub.ai/user/maksika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill to configure an OpenClaw agent with its wayMint chain and agent ID so it can answer identity or trust prompts with a certificate URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: On-chain identity data is public and persistent and may link an agent to an owner address or proof-of-human status. <br>
Mitigation: Review the identity information before registration and avoid publishing details that should not be permanently public. <br>
Risk: A certificate link alone could be mistaken for proof that an agent is safe or trustworthy. <br>
Mitigation: Verify certificate claims manually and evaluate the agent's behavior, source, and operational controls separately. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maksika/waymint) <br>
- [wayMint identity service](https://8004.way.je) <br>
- [wayMint agent registration](https://8004.way.je/register) <br>
- [wayMint agent lookup](https://8004.way.je/agent/{chain}:{id}) <br>
- [wayMint owner lookup](https://8004.way.je/owner/{address}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown text with identity URLs and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WAYMINT_CHAIN and WAYMINT_AGENT_ID configuration values.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
