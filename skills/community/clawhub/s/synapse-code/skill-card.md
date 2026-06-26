## Description: <br>
Synapse Code is an intelligent workflow skill for project initialization, code delivery, knowledge capture, pipeline execution, and impact analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankechenlab-node](https://clawhub.ai/user/ankechenlab-node) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical teams use this skill to coordinate code development workflows, initialize projects, run multi-agent pipelines, persist project knowledge, query prior work, and assess change impact. It also supports adjacent workflow scenarios such as writing, design, analytics, translation, and research when those tasks are routed through the skill's agent templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python and npm tools and execute configured pipeline scripts. <br>
Mitigation: Install only in trusted environments, review config.json before use, and keep pipeline.workspace and paths.pipeline_script pointed at trusted files. <br>
Risk: The skill can index project knowledge and write persistent project logs that may include sensitive project context. <br>
Mitigation: Avoid broad analytics or research modes with sensitive databases, APIs, cookies, or private documents unless access has been deliberately scoped. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ankechenlab-node/synapse-code) <br>
- [Synapse Code homepage](https://github.com/ankechenlab-node/synapse-code) <br>
- [README](README.md) <br>
- [Production scenario matrix](PRODUCTION_SCENARIOS.md) <br>
- [Pipeline architecture](PIPELINE_ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, code snippets, shell commands, configuration files, reports, and structured status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent project logs, knowledge records, pipeline summaries, generated files, and status reports in configured project paths.] <br>

## Skill Version(s): <br>
2.0.1 (source: release evidence and SKILL.md frontmatter; package.json and CHANGELOG list 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
