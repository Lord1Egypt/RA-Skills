## Description: <br>
End-to-end encrypted, decentralized memory for OpenClaw agents, with setup, remember, recall, import, export, consolidation, and CLI fallback workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p-diogo](https://clawhub.ai/user/p-diogo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add encrypted, portable long-term memory to OpenClaw agents, including account setup, memory storage and recall, import/export, and maintenance actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags this release as suspicious because it can read broad local agent logs, change OpenClaw configuration, restart the gateway, and store some decrypted memory content locally. <br>
Mitigation: Install only after reviewing local OpenClaw configuration changes and files under ~/.totalreclaw, and avoid production or shared machines unless those behaviors are acceptable. <br>
Risk: The skill handles wallet-style recovery material and sensitive credentials as part of account setup and encrypted memory access. <br>
Mitigation: Use the browser-based pairing flow or explicit setup path, never paste a recovery phrase into chat, and rotate credentials if a phrase is exposed. <br>
Risk: Automatic memory extraction can use LLM/provider credentials and process conversation content. <br>
Mitigation: Review extraction settings and provider credentials before enabling the skill, and prefer explicit setup when tighter control is required. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/p-diogo/totalreclaw) <br>
- [TotalReclaw Homepage](https://totalreclaw.xyz) <br>
- [OpenClaw Setup Guide](https://github.com/p-diogo/totalreclaw/blob/main/docs/guides/openclaw-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool calls, shell commands, and JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update local TotalReclaw and OpenClaw configuration and can return plaintext memory exports when requested.] <br>

## Skill Version(s): <br>
3.3.12-rc.12 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
