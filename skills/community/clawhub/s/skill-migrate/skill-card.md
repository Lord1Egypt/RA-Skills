## Description: <br>
Skill Migrate converts WorkBuddy skills to OpenClaw and ClawHub format, checks common compliance requirements, and guides publishing to ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongsunyanming](https://clawhub.ai/user/gongsunyanming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to migrate WorkBuddy SKILL.md packages into OpenClaw and ClawHub-compatible skills, validate metadata and file constraints, and prepare or run ClawHub publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted skills may carry incorrect metadata, unsupported file types, or undeclared credential requirements. <br>
Mitigation: Run the compliance checklist and review generated files before publishing. <br>
Risk: Publishing or batch publishing can push incorrect content to ClawHub. <br>
Mitigation: Confirm the ClawHub login identity, review changes skill by skill, and publish only after manual approval. <br>
Risk: Long-lived ClawHub credentials could be exposed if pasted unnecessarily. <br>
Mitigation: Use normal ClawHub login practices and avoid sharing long-lived tokens. <br>


## Reference(s): <br>
- [Skill Migrate on ClawHub](https://clawhub.ai/gongsunyanming/skill-migrate) <br>
- [OpenClaw Skill Format](https://docs.openclaw.ai/clawhub/skill-format) <br>
- [OpenClaw Skill Spec](references/openclaw-skill-spec.md) <br>
- [Conversion Examples](references/conversion-examples.md) <br>
- [Text File Extensions](references/text-file-extensions.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, converted skill files or snippets, and shell commands when publishing is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file edits and ClawHub CLI commands; review converted files before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
