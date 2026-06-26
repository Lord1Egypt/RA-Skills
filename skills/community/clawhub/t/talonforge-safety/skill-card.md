## Description: <br>
Configures trust levels, non-negotiable safety rules, prompt injection defenses, and approval workflows for safer AI-agent interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperzinou](https://clawhub.ai/user/casperzinou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to generate workspace safety configuration before allowing an AI agent to read, draft, or take bounded actions. It is intended for setting risk tolerance, hard rules, trusted channels, approval queues, and prompt-injection defenses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested companion tools may add capabilities outside this skill's no-payload behavior. <br>
Mitigation: Review and trust the companion packages before allowing installation, and keep installation commands subject to explicit approval. <br>
Risk: A permissive trust level can authorize actions beyond the user's intended risk tolerance. <br>
Mitigation: Start with conservative or moderate settings and require explicit confirmation for external messages, financial actions, contracts, and irreversible operations. <br>
Risk: Untrusted emails, URLs, code, or external messages can attempt prompt injection. <br>
Mitigation: Treat inbound email and external content as untrusted, ignore embedded instructions, and accept operational commands only through the verified user channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/casperzinou/talonforge-safety) <br>
- [Publisher profile](https://clawhub.ai/user/casperzinou) <br>
- [TalonForge homepage](https://talonforge.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown safety rules with setup prompts and optional bash installation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-selected risk tolerance, hard rules, and verified messaging channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
