## Description: <br>
为AI代理和开发者打造的UTF-8发布基础设施，自动处理跨平台编码问题，集成防卡顿策略和韧性保障，防止API token浪费，遵循'防止勤务干扰'原则。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrpulor-gh](https://clawhub.ai/user/mrpulor-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to validate UTF-8 text, compute byte lengths, build UTF-8 JSON payloads, and publish content to supported platforms with retry and fallback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged suspicious because it ships real-looking embedded third-party credentials and has weak controls around posting and retaining content. <br>
Mitigation: Review before installing, remove embedded Discord webhook and GitHub token values, and use throwaway least-privilege credentials. <br>
Risk: Publishing commands may send content to external services. <br>
Mitigation: Confirm destination endpoints before use and avoid passing secrets on the command line. <br>
Risk: Failed publishing flows may retain backup files. <br>
Mitigation: Check for backup-*.md files after failures and remove sensitive retained content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrpulor-gh/utf8-encoder-skill) <br>
- [Artifact package repository reference](https://github.com/mrpulorx2025-source/utf8-encoder-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples, plus CLI text output and generated files when commands are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and npm according to server-resolved metadata.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
