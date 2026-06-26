## Description: <br>
Xiaohongshu Proxy Manager helps agents manage proxy pools, account-to-proxy mappings, latency tests, and proxy export snippets for Xiaohongshu multi-account operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External operators and developers use this skill to configure proxy pools, bind accounts to proxies, test proxy reachability, and generate environment variable, Python requests, or curl proxy snippets. Review any use against applicable law, platform rules, and credential-handling requirements before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill is built for multi-account Xiaohongshu ban and detection avoidance. <br>
Mitigation: Use only for lawful, policy-compliant proxy management; do not use it to evade service rules, bans, or abuse controls. <br>
Risk: Proxy usernames and passwords can be stored in JSON configuration and emitted in terminal output, environment variables, Python snippets, or curl commands. <br>
Mitigation: Avoid real proxy passwords in checked-in JSON, restrict file access, backups, logs, and terminal sharing, and redact proxy credentials before reuse or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/xiaohongshu-proxy-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, environment variables, Python requests snippets, and curl commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output may include proxy URLs and credentials from configuration; handle generated proxy output as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
