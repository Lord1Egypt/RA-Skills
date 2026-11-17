## Description:

Compile SKILL.md files into runtime artifacts, verify freshness and health, and prepare portable publish-ready skill folders for ClawHub-style registries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaoyanji](https://clawhub.ai/user/shaoyanji)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to compile skill source files into lower-token runtime artifacts and to prepare skill folders for ClawHub-style publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read skill files under a chosen skills directory when run.

Mitigation: Run it only against intended local skill directories and review the generated artifacts before publishing or loading them.

Risk: Generic execute-style triggers could be broader than intended in unrestricted runtimes.

Mitigation: Enable execute triggers only when the runtime restricts them to explicit skill invocations.

Risk: The submitted artifact describes script paths but does not bundle executable code.

Mitigation: Review or supply the referenced scripts before relying on compiler commands in production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shaoyanji/skills/skill-compiler)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact skill.yaml](artifact/skill.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and generated JSON/TOON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces sibling SKILL.struct.json and SKILL.toon artifacts for each input SKILL.md.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
