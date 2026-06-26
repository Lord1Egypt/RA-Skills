## Description: <br>
Sinkron gives agents permanent email identities through the Sinkron CLI and Python SDK, with inbox management, message search, deletion, and health monitoring using a SINKRON_TOKEN credential. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zororaka00](https://clawhub.ai/user/zororaka00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use Sinkron to give agents persistent email addresses and automate inbox workflows through shell commands or the Python SDK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SINKRON_TOKEN to read and delete Sinkron inbox messages. <br>
Mitigation: Store SINKRON_TOKEN only in a secret manager or restricted environment variable, avoid logging tokens or message contents, and require explicit human confirmation before delete-inbox or other deletion commands. <br>
Risk: Server evidence does not provide resolved source provenance for this version. <br>
Mitigation: Verify package provenance before installation and keep the Sinkron package version pinned. <br>


## Reference(s): <br>
- [Sinkron homepage](https://www.sinkron.id) <br>
- [ClawHub skill page](https://clawhub.ai/zororaka00/sinkron) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include credential handling, pinned installation, inbox search, message retrieval, deletion flows, and health checks.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
