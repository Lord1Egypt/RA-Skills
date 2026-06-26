## Description: <br>
Fasterizy provides answer-first writing rules for coding-agent Q&A, planning, and technical documentation so responses are terser while preserving exact technical identifiers and requested detail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veezvg](https://clawhub.ai/user/veezvg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to make coding-agent responses shorter, answer-first, and easier to scan during Q&A, planning, debugging, and technical documentation work. It is intended to shape agent prose rather than generate application code directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marks this release suspicious because its installer persistently changes local agent configurations and hook or plugin behavior beyond the terse-answer skill summary. <br>
Mitigation: Install only when persistent multi-agent integration is needed; otherwise review and use the plain SKILL.md manually. <br>
Risk: Running the CLI may write under Claude, Codex, Cursor, or Windsurf configuration paths, fetch from GitHub, copy hook scripts, and change plugin or settings files. <br>
Mitigation: Review selected agents before installation, inspect backups, and know how to run fasterizy stop and uninstall hooks or plugins before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veezvg/veezvg-fasterizy) <br>
- [Fasterizy README](README.md) <br>
- [Fasterizy npm package](https://www.npmjs.com/package/fasterizy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands for installation and operation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent agent-response style guidance; installer commands can modify local agent configuration paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
