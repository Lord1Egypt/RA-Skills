## Description: <br>
Runs a deterministic static safety audit for third-party AI skill or plugin repositories before install or execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modeioai](https://clawhub.ai/user/modeioai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to statically assess skill, plugin, or agent repositories before installation or execution and to produce evidence-backed findings, prompts, validation reports, and adjudication results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads the target repository during audit. <br>
Mitigation: Run it only on repositories you are authorized to inspect and treat generated reports as potentially sensitive. <br>
Risk: Evaluation can contact GitHub automatically when a GitHub origin is present. <br>
Mitigation: Run without GITHUB_TOKEN or in an environment with controlled outbound GitHub access when repository origin metadata is sensitive. <br>
Risk: Optional GITHUB_TOKEN use can expose repository metadata to GitHub API requests. <br>
Mitigation: Use a least-privilege token only when higher GitHub API rate limits are needed. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/mode-io/mode-io-skills/tree/main/skill-audit) <br>
- [Architecture](references/architecture.md) <br>
- [Prompt contract](references/prompt-contract.md) <br>
- [Output contract](references/output-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with command snippets and machine-readable JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic reports include scoring, highlights, findings, evidence references, validation results, and adjudication output.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
