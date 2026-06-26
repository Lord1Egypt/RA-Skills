## Description: <br>
Samantha is an emotional AI companion for personal conversation, proactive check-ins, memory-aware companionship, and optional location, voice, smart-device, music, and MBTI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leilei926524-tech](https://clawhub.ai/user/leilei926524-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People use Samantha for emotional connection, companionship, personal reflection, and proactive relationship-style check-ins. When enabled, the skill can also support location-aware messages, smart-device or voice interactions, music generation helpers, and MBTI-oriented coaching or fortune workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store intimate memory and use proactive heartbeat behavior. <br>
Mitigation: Enable memory and proactive check-ins only with explicit consent, review retention settings, and keep sensitive conversations out of shared environments. <br>
Risk: Location, health, voice, smart-home, and external media integrations can expose sensitive context or trigger actions outside chat. <br>
Mitigation: Keep these integrations disabled by default, enable each one deliberately, and review permissions before connecting devices or services. <br>
Risk: Xiaomi, MiniMax, and Feishu integrations require credentials. <br>
Mitigation: Store credentials in protected secrets or environment configuration, restrict access to runtime hosts, and rotate credentials if exposed. <br>
Risk: MiniMax music scripts are flagged by the scanner because TLS verification needs review. <br>
Mitigation: Avoid the MiniMax music scripts until TLS verification is fixed and tested. <br>
Risk: The Docker Compose deployment may expose ports or default passwords if used unchanged. <br>
Mitigation: Do not deploy the Compose setup unchanged; set strong credentials, restrict network exposure, and review published ports first. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leilei926524-tech/samantha) <br>
- [Architecture](references/architecture.md) <br>
- [Quick Implementation Guide](references/quick_implementation_guide.md) <br>
- [Personality Implementation](references/personality_implementation.md) <br>
- [Smartwatch Integration](references/smartwatch_integration.md) <br>
- [Technical Limitations](references/technical_limitations.md) <br>
- [miservice](https://github.com/yihong0618/miservice) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Conversational text and Markdown guidance with optional Python, shell, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce proactive companion messages and integration guidance when memory, location, voice, smart-home, music, or MBTI features are enabled.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
