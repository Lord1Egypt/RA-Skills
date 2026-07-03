## Description: <br>
End-to-end encrypted, decentralized memory for OpenClaw, with native recall through memory_search and memory_get and background fact capture. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[p-diogo](https://clawhub.ai/user/p-diogo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to add persistent encrypted memory, recall user facts, and guide setup or recovery flows without putting recovery phrases into chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence places this release in Review before install because it can read recent OpenClaw session logs and use configured model credentials for extraction. <br>
Mitigation: Install only when TotalReclaw is intended to be the memory backend, use a dedicated model API key, and review extraction settings before use. <br>
Risk: The skill writes TotalReclaw credentials and state under the user's home directory. <br>
Mitigation: Keep the recovery phrase private, use the browser pairing flow, and re-pair if a recovery phrase is exposed in chat. <br>
Risk: The skill can change OpenClaw plugin configuration and restart the gateway. <br>
Mitigation: Review the install and setup flow in a controlled environment before enabling it in a regular OpenClaw workspace. <br>
Risk: This is a release-candidate build whose release evidence says it is not recommended for production. <br>
Mitigation: Prefer a stable release unless the user specifically needs to test this RC version. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/p-diogo/skills/totalreclaw) <br>
- [TotalReclaw homepage](https://totalreclaw.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include account setup URLs, PINs, CLI commands, memory recall guidance, and status or export instructions.] <br>

## Skill Version(s): <br>
3.3.12-rc.19 (source: server release, SKILL.md frontmatter, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
