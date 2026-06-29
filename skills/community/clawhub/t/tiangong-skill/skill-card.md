## Description: <br>
天工.Skill helps users design, create, and optimize AI agents or expert roles through persona distillation and job-oriented expert design workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebandao777-oss](https://clawhub.ai/user/ebandao777-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent builders, prompt engineers, and teams use this skill to turn a role, person, or expert workflow idea into a structured AI agent design with activation rules, quality gates, delivery standards, and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent or skill definitions may contain incorrect, overbroad, or misleading guidance. <br>
Mitigation: Review generated skills before installing, enabling, or deploying them. <br>
Risk: Broad trigger phrases may invoke the skill-design workflow when the user did not intend to generate an agent design. <br>
Mitigation: Confirm intent before using broad prompts such as "帮我写个" when agent design is not desired. <br>
Risk: The skill can create files in an output directory when a full deliverable is requested. <br>
Mitigation: Inspect generated files and their destination paths before using them in an agent environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ebandao777-oss/tiangong-skill) <br>
- [README](README.md) <br>
- [Quickstart](QUICKSTART.md) <br>
- [Persona Details](references/persona-details.md) <br>
- [Job Details](references/job-details.md) <br>
- [Extraction Framework](references/extraction-framework.md) <br>
- [Quality Verification](references/quality-verification.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured templates, checklists, and optional file or command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce generated skill files when the user requests a full deliverable; generated output should be reviewed before installation or enablement.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
