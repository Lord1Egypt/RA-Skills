## Description: <br>
Unified AI workflow with persistent memory, TDD execution, and 15 productivity skills. Use when starting any coding project or when you need planning, execution, debugging, or code review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mok888](https://clawhub.ai/user/mok888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI-agent users use this skill collection to plan, execute, debug, review, and verify coding work with persistent project memory files and TDD-oriented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent project memory files can capture sensitive project details or work history. <br>
Mitigation: Keep .superpower-with-files out of commits when it may contain sensitive information and review the files before sharing or publishing a repository. <br>
Risk: Session recovery behavior may inspect prior local AI session history. <br>
Mitigation: Use the skill only where local-session review is acceptable and where users have clear consent and redaction practices. <br>
Risk: Generated git or pull-request actions may not match the user's intent. <br>
Mitigation: Review proposed git and PR commands before allowing the agent to run them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mok888/superpower-with-files) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell commands; workflows may create or update local planning and progress files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist task plans, progress logs, findings, and implementation guides under .superpower-with-files.] <br>

## Skill Version(s): <br>
2.20.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
