## Description: <br>
yan-watchman is a Rust-based multi-platform AI assistant message watchdog with intelligent importance scoring and adaptive monitoring frequency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eightroad](https://clawhub.ai/user/eightroad) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill as guidance for a multi-platform AI assistant message monitoring workflow that scores message importance, adapts monitoring frequency, and documents configuration and release commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is documentation-only and does not include the claimed Rust source tree or configuration files, so build and publish commands cannot be independently verified from the artifact. <br>
Mitigation: Do not execute build or publish commands until the maintainer provides the full source tree and configuration; review and scan those files before installation. <br>
Risk: Cross-platform message monitoring can expose sensitive message content and metadata. <br>
Mitigation: Deploy only with user or administrator authorization, confirm platform terms, and define storage location, retention, access, and deletion controls before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eightroad/yan-watchman) <br>
- [Publisher profile](https://clawhub.ai/user/eightroad) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command blocks and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
