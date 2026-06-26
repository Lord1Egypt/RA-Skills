## Description: <br>
Qqbot Persona lets an OpenClaw QQ bot switch independent personas by private chat, group chat, or OpenID without changing the default OpenClaw persona. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wdwdwd000](https://clawhub.ai/user/wdwdwd000) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw QQ bot operators use this skill to apply different persona prompts for one-to-one chats, group chats, and specific OpenID targets. It is intended for deployments where QQ channel behavior should be isolated from the agent's default persona. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured persona files can be read into prompts, including absolute file paths if operators allow them. <br>
Mitigation: Keep personas.json writable only by trusted operators and use reviewed relative persona files rather than absolute file: paths. <br>
Risk: QQ session identifiers and OpenID values may be written to hook.log. <br>
Mitigation: Protect hook.log with appropriate file permissions and rotate or remove it according to the deployment's retention policy. <br>
Risk: Some bundled or configured personas may obscure the assistant's AI identity. <br>
Mitigation: Review persona text before deployment and require truthful AI disclosure where policy, law, or user expectations require it. <br>
Risk: FORCE_QQBOT_PERSONA can force persona injection outside normal QQ channel detection. <br>
Mitigation: Do not set FORCE_QQBOT_PERSONA in normal use and audit runtime environment variables before production deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wdwdwd000/qqbot-persona) <br>
- [OpenClaw Hooks documentation](https://docs.openclaw.ai/hooks) <br>
- [OpenClaw SOUL.md persona guide](https://docs.openclaw.ai/soul) <br>
- [Publisher profile](https://clawhub.ai/user/wdwdwd000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown persona prompt text, JSON configuration examples, JavaScript hook code, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The hook injects a virtual SOUL.md bootstrap file for QQ bot sessions when a configured persona matches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
