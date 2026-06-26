## Description: <br>
Mokshya agent-wallet helps agents troubleshoot public REST API and TEE signing flows, GKE deployment, rate limits, transaction creation and signing, and agent_id lookup issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evilboyajay](https://clawhub.ai/user/evilboyajay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to debug Mokshya wallet API behavior, deployment configuration, and signing flows without confusing API-owned agent IDs with TEE state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction or deployment guidance could be applied to the wrong wallet, cluster, or namespace. <br>
Mitigation: Verify transaction payloads and confirm the target GKE project, cluster, namespace, and rollback plan before applying changes. <br>
Risk: Sensitive wallet shares, HMAC secrets, or database credentials could be exposed in prompts, logs, or generated commands. <br>
Mitigation: Keep key_share values, HMAC secrets, and database credentials out of chat, logs, and pasted command output. <br>


## Reference(s): <br>
- [Mokshya agent-tee-wallet homepage](https://github.com/mokshyaprotocol/agent-tee-wallet) <br>
- [ClawHub skill page](https://clawhub.ai/evilboyajay/tee-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only troubleshooting guidance; does not execute commands directly.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; artifact frontmatter reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
