## Description: <br>
Guides Hermes and Claude Code agents through xz01 template development, role boundaries, live-site validation gates, dual-end navigation, xz01_demo pagination, and full-page visual QA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amd5](https://clawhub.ai/user/amd5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site-maintenance agents use this skill to coordinate Hermes, Claude Code, and validation roles for xz01/900az theme-template work. It helps constrain writes, run template checks, validate PC and mobile pages, and package or publish only after required gates pass. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct agents toward broad live-site and publishing actions for the xz01/900az workflow. <br>
Mitigation: Install only for that intended workflow and require explicit approval before webroot writes, live theme replacement, runtime deletion, Docker/MCP setup, credential use, self-update, or clawhub publish. <br>
Risk: Template or validation actions may affect live site behavior if applied directly to production paths. <br>
Mitigation: Prefer staging paths, review diffs before release, and run the documented validation gates before packaging or publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/amd5/xz01-dev-skill) <br>
- [Skill metadata](artifact/skill.json) <br>
- [Release metadata](artifact/_meta.json) <br>
- [xz01 Template Factory Architecture Notes](artifact/references/xz01-template-factory-architecture.md) <br>
- [Lanhu MCP installation for xz01 workflow](artifact/references/lanhu-mcp-installation.md) <br>
- [Hermes-native xz01 live deploy validation](artifact/references/hermes-native-xz01-live-deploy-validation.md) <br>
- [Pagination data-volume validation correction](artifact/references/session-2026-05-18-pagination-data-volume-validation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline commands, file paths, code references, and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent outputs may include proposed template edits, validation commands, screenshot/report paths, and release notes.] <br>

## Skill Version(s): <br>
1.0.44 (source: server release metadata, SKILL.md frontmatter, skill.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
