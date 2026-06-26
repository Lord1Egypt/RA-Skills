## Description: <br>
Save 60-90% of LLM tokens on shell commands, file reads, and test outputs. Wraps rtk CLI for compressed output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erscoder](https://clawhub.ai/user/erscoder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route common shell, file, Git, test, build, container, and analytics commands through rtk so command output is compressed before it enters the agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wrapped commands can still commit, push, deploy, access clusters, or call networks with the same authority as the original command. <br>
Mitigation: Keep normal approval boundaries for sensitive commands and review compressed output before acting on it. <br>
Risk: Command output may include secrets or private data before or after compression. <br>
Mitigation: Avoid printing secret-bearing environment variables or logs unless values are redacted. <br>
Risk: Installing via a remote curl-to-shell command increases supply-chain exposure. <br>
Mitigation: Prefer Homebrew or a pinned rtk release when installing the dependency. <br>


## Reference(s): <br>
- [rtk CLI project](https://github.com/rtk-ai/rtk) <br>
- [OpenClaw feature request](https://github.com/openclaw/openclaw/issues/35053) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are recommendations and command patterns for using rtk; wrapped commands retain the permissions and privacy risks of the original commands.] <br>

## Skill Version(s): <br>
1.15.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
