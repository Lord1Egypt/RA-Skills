## Description: <br>
Convert memory, conversation history, or completed tasks into publishable OpenClaw skills for reusable workflows, lessons, solved problems, and GitHub or ClawHub releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfanmy](https://clawhub.ai/user/zfanmy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to turn useful conversation history, memory notes, or completed work into reusable OpenClaw skills. It helps generate skill structure, markdown documentation, scripts, and optional publishing steps for GitHub and ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private conversations, memory files, or extracted code may be converted into publishable skill content without built-in redaction. <br>
Mitigation: Use narrow source files where possible, review all generated files, and remove secrets, private details, and sensitive context before publishing. <br>
Risk: Publishing workflows can push generated content to GitHub or ClawHub when publish scripts are run with repository or slug options. <br>
Mitigation: Confirm the target GitHub repository, ClawHub slug, version, and generated content before running publish.sh or create-and-publish.sh. <br>
Risk: Generated skill drafts may include incomplete scripts, placeholders, or misleading extracted guidance. <br>
Mitigation: Manually inspect and test SKILL.md, README.md, generated scripts, extracted summaries, and any copied code before reuse or release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zfanmy/skill-from-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell-script files with command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create skill directories, SKILL.md files, README.md files, helper scripts, extracted conversation summaries, and optional GitHub or ClawHub publishing commands.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
