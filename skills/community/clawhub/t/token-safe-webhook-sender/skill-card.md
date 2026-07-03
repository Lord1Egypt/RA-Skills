## Description: <br>
Secure webhook token management using MGC Blackbox for DingTalk, WeCom, Feishu, Telegram, Slack, and similar notification webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkeviny](https://clawhub.ai/user/zkeviny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this documentation skill to store webhook credentials in MGC Blackbox and retrieve them when sending deployment, CI/CD, monitoring, collaboration, or workflow notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reports that this credential-management workflow can give agents enough detail to read a local MGC auth token and retrieve stored secrets despite zero-exposure claims. <br>
Mitigation: Prefer the WebUI for entering secrets, do not let agents read the MGC token file directly, and restrict agent access to secret-retrieval tools unless the workflow requires it. <br>
Risk: Temporary plaintext token files or logs can expose webhook credentials during setup or troubleshooting. <br>
Mitigation: Avoid plaintext token files where possible, never log webhook tokens, and delete any temporary token files immediately after import. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zkeviny/skills/token-safe-webhook-sender) <br>
- [MGC Blackbox project](https://github.com/zkeviny/MGC-Blackbox) <br>
- [MGC Blackbox issues](https://github.com/zkeviny/MGC-Blackbox/issues) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands, code] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and conceptual code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
