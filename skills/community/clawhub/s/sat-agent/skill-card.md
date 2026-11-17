## Description:

Run the pure-LLM variant of the QLCoder workflow for both CVE samples and local Web App repositories, with multi-profile taint-flow source, sink, and sanitizer typing for Java Web and Python Web projects without CodeQL/database build steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[setg-git](https://clawhub.ai/user/setg-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run QLCoder pure-LLM analysis on CVE samples or local Java/Python web repositories and review generated taint-flow leads for XSS, SQL injection, and broken-access-control risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private source code may be included in prompts or generated reports depending on the local QLCoder configuration.

Mitigation: Run the workflow only on repositories approved for that analysis environment and review generated artifacts before sharing them.

Risk: Findings are heuristic taint-flow leads and may be incomplete or false positive, especially outside Ruoyi-style Java projects.

Mitigation: Confirm exploitability with targeted trace review and tests before acting on or reporting a finding.

Risk: The pure-LLM workflow does not provide CodeQL compilation, database analysis, or full dataflow proof.

Mitigation: Use CodeQL or another validated analysis path when formal dataflow confirmation is required.

## Reference(s):

- [Workflow](artifact/references/workflow.md)
- [Taint Profiles](artifact/references/taint_profiles.md)
- [ClawHub Skill Page](https://clawhub.ai/setg-git/skills/sat-agent)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Analysis, Markdown, JSON]

**Output Format:** [Markdown guidance with shell commands and generated JSON/Markdown analysis artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are draft candidate analyses and report artifacts under runs/.../pure-llm/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
