## Description: <br>
Unofficial Bitwarden CLI written in Rust. Manage passwords, TOTP codes, and secure notes from the terminal with a background agent for stateful sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxhoio](https://clawhub.ai/user/sxhoio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other terminal users can use this skill to configure and operate the rbw Bitwarden CLI for vault access, password generation, TOTP retrieval, secure notes, profiles, and SSH-agent integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides access to a Bitwarden vault through rbw, which can expose sensitive password-manager data if run on an untrusted system. <br>
Mitigation: Install rbw only from a trusted package source or the upstream project, and use the skill only in environments where vault access is intended. <br>
Risk: rbw-agent may keep unlocked session material in memory for the configured timeout. <br>
Mitigation: Use a shorter lock timeout for shared or higher-risk machines, and lock or stop the agent when vault access is no longer needed. <br>
Risk: Clipboard and SSH-agent features can expose secrets or signing capability beyond the immediate command. <br>
Mitigation: Avoid clipboard copying on shared machines, and enable SSH-agent integration only when rbw should sign SSH challenges. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sxhoio/rbw-bitwarden) <br>
- [rbw upstream project](https://github.com/doy/rbw) <br>
- [Bitwarden personal API key documentation](https://bitwarden.com/help/article/personal-api-key/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill for configuring and using rbw and rbw-agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
