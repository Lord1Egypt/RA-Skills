## Description: <br>
A wheel-spotting scout that finds reusable solutions before you build from scratch. Cost-controlled intelligent search with complexity-aware filtering, intent-based platform selection, and form consistency checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garylooop](https://clawhub.ai/user/garylooop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use WheelSpotter to check public package, code, and service registries for reusable libraries, tools, APIs, or references before implementing from scratch. It helps classify the request, search relevant platforms, filter stale or weak candidates, and return actionable recommendations or a self-build decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms or summarized requirements may be sent to public package and code registries. <br>
Mitigation: Avoid using highly sensitive unreleased project details in searches; summarize requirements at a level appropriate for public registry queries. <br>
Risk: The skill can use a GitHub token to increase API limits. <br>
Mitigation: Use a low-scope GitHub token only when needed, and do not provide broader credentials than registry search requires. <br>
Risk: Broad trigger phrases may start registry searches when the user only wanted general advice. <br>
Mitigation: Confirm intent before network searches when a request is ambiguous or contains confidential implementation context. <br>


## Reference(s): <br>
- [WheelSpotter ClawHub page](https://clawhub.ai/garylooop/wheelspotter) <br>
- [Publisher profile](https://clawhub.ai/user/garylooop) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Search script](artifact/scripts/search.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON search results and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include package names, source URLs, install commands, filtering notes, warnings, and cost metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
