## Description: <br>
OpenClaw Skill template generator for creating skill scaffolds, validating structure, enhancing SKILL.md, generating command frameworks, tips, and publish checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to scaffold ClawHub/OpenClaw skill directories, validate required files, generate starter command scripts, and prepare publish checklists. The shipped scripts also include a local text log utility for adding, listing, searching, and exporting dated entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local data and history logs can retain secrets, private prompts, or sensitive project details entered through the CLI. <br>
Mitigation: Do not enter sensitive data; set SKILL_TEMPLATE_DIR to an isolated location and review or delete data.log and history.log after use. <br>
Risk: The release is marketed as a template generator but also ships a persistent local note/log manager, which can surprise users reviewing only the summary. <br>
Mitigation: Review the shipped scripts and expected commands before deployment, and expose only the commands needed for the intended workflow. <br>
Risk: The documented remove command should not be treated as reliable data purging for retained records. <br>
Mitigation: Manually inspect and delete retained local files when records must be removed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ckchzh/skill-template) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with shell command examples and generated Bash/Python template content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local data.log and history.log files when CLI scripts are executed.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
