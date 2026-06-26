## Description: <br>
Interactive guide to deploy a production-ready WordPress site for international trade businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Trade companies, WordPress beginners, and developers use this skill to guide an agent through server setup, Docker-based WordPress deployment, SSL, SEO, multilingual content setup, performance configuration, and security verification for B2B trade websites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad server-administration authority over a VPS and WordPress deployment. <br>
Mitigation: Use it only on a fresh or fully backed-up VPS you control, prefer temporary SSH keys or a limited sudo account, and review each command before execution. <br>
Risk: The workflow handles SSH details, generated passwords, API keys, and certificate material. <br>
Mitigation: Avoid pasting private keys into chat, save generated secrets outside the conversation, and rotate or revoke temporary credentials after deployment. <br>
Risk: Remote downloads and optional AI-crawler or Cloudflare robots.txt changes can affect site security and exposure. <br>
Mitigation: Review remote download sources before running them and treat AI-crawler access changes as optional deployment choices. <br>


## Reference(s): <br>
- [wordpress-trade-starter template referenced by the skill](https://github.com/iPythoning/wordpress-trade-starter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive phased workflow that collects business, server, domain, and credential inputs before proposing deployment commands.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
