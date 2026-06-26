## Description: <br>
A local memory skill that combines Baidu Embedding semantic search, Git Notes structured storage, and filesystem-backed memory management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xqicxx](https://clawhub.ai/user/xqicxx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to set up and operate a local memory stack with semantic search, tagged structured memories, filesystem storage, health checks, and maintenance commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes local-only privacy claims while enabling Baidu API-based embedding. <br>
Mitigation: Treat the skill as hybrid local-plus-remote unless remote embedding is disabled or audited, and avoid storing secrets or sensitive personal or business data. <br>
Risk: Setup, fix, and maintenance scripts perform broad actions in /root/clawd. <br>
Mitigation: Review scripts before execution and run them only in a contained /root/clawd environment that is acceptable to modify. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xqicxx/secure-memory-stack) <br>
- [README](artifact/README.md) <br>
- [Documentation](artifact/DOCUMENTATION.md) <br>
- [Installation guide](artifact/INSTALLATION.md) <br>
- [Memory system guide](artifact/MEMORY_SYSTEM_GUIDE.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local files under /root/clawd and optional Baidu API environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
