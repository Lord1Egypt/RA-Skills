## Description: <br>
Vouch signs, verifies, and manages cryptographic identity for AI agents using the Vouch CLI on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackpmorgan](https://clawhub.ai/user/jackpmorgan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to install and operate the Vouch CLI for identity onboarding, message signing and verification, agent discovery, endpoint publishing, allowlists, and account management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through workflows that affect keys, identity state, message handling, deployments, billing, and account configuration. <br>
Mitigation: Require explicit user approval before delegation, publishing, deployment, revocation, reset, teardown, billing/account-changing, or receiver-handler actions. <br>
Risk: The install path depends on the vouch.directory installer and the local Vouch CLI environment. <br>
Mitigation: Install only when the publisher and installer are trusted; inspect or verify the installer first and prefer a test network during evaluation. <br>
Risk: Wallet, API, and OpenAI credentials may be exposed through shell history, logs, or command output. <br>
Mitigation: Keep secrets out of prompts, shell history, logs, and shared transcripts; use environment-specific secret handling where available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jackpmorgan/vouch-cli) <br>
- [Vouch Website](https://vouch.directory) <br>
- [Vouch Documentation](https://vouch.directory/docs) <br>
- [Vouch Guides](https://vouch.directory/guides) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the vouch binary on PATH and jq for JSON processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
