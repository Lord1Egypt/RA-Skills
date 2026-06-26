## Description: <br>
Repo Scout helps agents discover, evaluate, and rank GitHub repositories by ecosystem or domain, producing a structured markdown ranking with repository health and contribution-friendliness signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sliverp](https://clawhub.ai/user/sliverp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and technical evaluators use this skill to scout open-source projects, compare technology options, plan contribution campaigns, or survey an ecosystem. It guides repository search, scoring, filtering, and markdown report creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require GitHub authentication for repository research, and mishandled tokens could expose account or private repository access. <br>
Mitigation: Authenticate locally with GitHub CLI where possible, avoid pasting tokens into chat or generated files, and use fine-grained tokens with the narrowest read access needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and structured tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an ecosystem ranking document such as {workspace}/ecosystem-top{N}.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
