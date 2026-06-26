## Description: <br>
Create, improve, evaluate, benchmark, package, and optimize agent skills through guided drafting, test-case design, qualitative review, and quantitative evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create new skills, revise existing skills, design realistic eval prompts, compare skill behavior against baselines, and optimize skill descriptions for better triggering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can run local Python workflows, write evaluation artifacts, package skill directories, and start a localhost review server. <br>
Mitigation: Review target paths before execution, prefer the static viewer when possible, avoid ports used by other services, and inspect generated artifacts before reuse. <br>
Risk: Skill drafts, eval prompts, and benchmark content may be sent through nested Claude CLI evaluations. <br>
Mitigation: Do not include secrets, credentials, proprietary data, or sensitive user content in skill drafts, eval prompts, or benchmark outputs. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/pupuking723/skill-creator-anthropic) <br>
- [Skill Creator schemas](artifact/references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline code blocks, JSON schemas, Python helper scripts, and generated review or benchmark files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update skill files, eval metadata, benchmark outputs, packaged .skill archives, static HTML reports, and feedback files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
