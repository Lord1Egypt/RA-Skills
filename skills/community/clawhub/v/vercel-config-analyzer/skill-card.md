## Description: <br>
Analyze Vercel project configurations, including vercel.json, framework detection, build settings, edge functions, headers, redirects, rewrites, environment variables, and deployment performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and deployment engineers use this skill to review, debug, and optimize Vercel deployments before production incidents occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A meaningful audit requires reading project files and may surface environment variable names or hardcoded secrets already present in the project. <br>
Mitigation: Review findings before sharing, avoid including secret values in prompts or reports, and rotate any hardcoded secrets identified in source. <br>
Risk: Generated deployment guidance or configuration snippets may be incomplete for a specific framework, Vercel plan, or project architecture. <br>
Mitigation: Review proposed changes, validate them with local builds and project tests, and apply them through the normal deployment review process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/vercel-config-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown report with findings, security header audit, environment variable review, performance notes, and suggested vercel.json snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed configuration snippets and commands for local validation; does not modify files automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
