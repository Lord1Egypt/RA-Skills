## Description: <br>
Saves markdown content to a remote Obsidian vault via SSH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to save generated markdown notes into a configured remote Obsidian vault while keeping Obsidian-friendly formatting for diagrams, tables, links, and filenames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected markdown content to a remote Obsidian vault over SSH. <br>
Mitigation: Confirm that the configured host, vault path, and SSH key are under the user's control before use. <br>
Risk: A matching destination filename may overwrite an existing note. <br>
Mitigation: Choose filenames deliberately and confirm overwrite intent before saving important notes. <br>
Risk: Broad SSH access could expose more remote filesystem access than the skill needs. <br>
Mitigation: Use a restricted SSH account where possible and limit access to the intended vault location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chunhualiao/save-to-obsidian) <br>
- [Obsidian Markdown Guide](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax) <br>
- [Mermaid Documentation](https://mermaid.js.org/) <br>
- [Obsidian Mermaid Support](https://help.obsidian.md/Editing+and+formatting/Advanced+formatting+syntax#Diagram) <br>
- [Artifact references](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and terminal output from SSH copy commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves selected markdown content to a configured remote Obsidian vault path; filenames are sanitized and matching names may overwrite existing notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, skill.yml, and changelog; SKILL.md frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
