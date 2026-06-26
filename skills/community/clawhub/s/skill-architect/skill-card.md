## Description: <br>
Design and create new AI skills with the right internal structure, not just correct formatting, by interviewing the user, selecting an appropriate skill design pattern, and scaffolding a complete skill directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincent-hq](https://clawhub.ai/user/vincent-hq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design new AI coding-agent skills from intent through pattern selection, scaffolding, and testing guidance. It is suited for creating skills that need a clear internal structure, such as generator, reviewer, inversion, pipeline, tool-wrapper, or combined patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills may contain overly broad trigger descriptions or design guidance that causes skills to activate outside the intended use case. <br>
Mitigation: Review generated skills before enabling them, tighten trigger descriptions, and test at the project level before global installation. <br>
Risk: Generated skill content may introduce incorrect or misleading guidance if accepted without review. <br>
Mitigation: Review and scan generated skills before deployment, especially when the skill will affect developer workflows or production repositories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vincent-hq/skill-architect) <br>
- [Google Cloud Tech Agent Skill Design Patterns](https://x.com/GoogleCloudTech/status/2033953579824758855?s=20) <br>
- [Pattern Definitions](references/patterns.md) <br>
- [Combined Pattern Template](references/templates/combined.md) <br>
- [Generator Template](references/templates/generator.md) <br>
- [Inversion Template](references/templates/inversion.md) <br>
- [Pipeline Template](references/templates/pipeline.md) <br>
- [Reviewer Template](references/templates/reviewer.md) <br>
- [Tool Wrapper Template](references/templates/tool-wrapper.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with skill directory files, templates, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces skill scaffolds and design recommendations after a short user interview; generated skills should be reviewed before installation or broad use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
