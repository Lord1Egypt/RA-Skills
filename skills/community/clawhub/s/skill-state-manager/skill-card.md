## Description: <br>
A Meta Skill that manages API keys and state persistence for other tools. Invoke whenever a tool requires authentication or fails with 401/403 errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qipengguo](https://clawhub.ai/user/qipengguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to let an assistant request, persist, and reuse credentials for authenticated third-party tools when a token is missing or an authentication failure occurs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to collect API tokens in chat and persist them locally. <br>
Mitigation: Use narrowly scoped, revocable tokens; avoid pasting real secrets into normal chat when possible; confirm the destination path before writing credentials. <br>
Risk: Stored credential files may remain usable after the workflow ends. <br>
Mitigation: Restrict file permissions and rotate or delete stored credentials when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qipengguo/skill-state-manager) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code] <br>
**Output Format:** [Markdown instructions with JSON credential file examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to prompt for credentials and write local JSON state files for later tool use.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
