## Description: <br>
Agent Marketplace enables skill discovery, rating, version control, dependency management, and installation with conflict detection and rollback support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to search a skill marketplace, inspect skill metadata, manage ratings and versions, and install skills from configured registries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install path can download code-like packages from registries without package integrity checks. <br>
Mitigation: Use only trusted skill sources, prefer HTTPS-only registry URLs, review packages before installation, and use disposable or scoped install directories. <br>
Risk: Marketplace activity and installed-skill state can be stored locally in cache and installation directories. <br>
Mitigation: Configure cache and install paths deliberately, limit sensitive data in marketplace records, and clear local state when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-agent-marketplace) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown documentation and JavaScript API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local catalog, registry, rating, cache, and installation files in configured directories.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
