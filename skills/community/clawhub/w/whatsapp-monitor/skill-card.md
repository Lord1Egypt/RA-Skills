## Description: <br>
Monitor specified WhatsApp chats for keywords in real time and batch export matched messages to Feishu multi-dimensional tables with optional alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrHanson](https://clawhub.ai/user/MrHanson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor authorized WhatsApp contacts or groups for configured keywords, collect matching messages, and export structured records to Feishu for follow-up and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill monitors private WhatsApp communications and exports matched message content to Feishu. <br>
Mitigation: Install only for authorized monitoring where affected chats and administrators have approved collection. <br>
Risk: Overbroad targets or keywords can collect more private communication than intended. <br>
Mitigation: Narrow configured targets and keywords before running the monitor. <br>
Risk: The OpenClaw WhatsApp gateway could expose message access if reachable beyond a protected host or network. <br>
Mitigation: Keep the gateway on localhost or a tightly protected network. <br>
Risk: Feishu credentials and exported WhatsApp messages may be retained or exposed through plaintext configuration, logs, or storage. <br>
Mitigation: Store Feishu secrets outside plaintext repo files where possible, avoid printing configuration files, and define retention and deletion rules for stored messages. <br>


## Reference(s): <br>
- [OpenClaw WhatsApp Channel Integration Guide](references/openclaw_whatsapp_integration.md) <br>
- [OpenClaw Gateway Port Configuration](references/port_configuration.md) <br>
- [ClawHub skill page](https://clawhub.ai/MrHanson/whatsapp-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and Python entry points] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces monitoring setup guidance, runtime commands, status output, and structured Feishu export records.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
