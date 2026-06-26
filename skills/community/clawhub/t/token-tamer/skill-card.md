## Description: <br>
Monitor, budget, and optimize AI API spending across any provider. Tracks every call, enforces budgets, detects waste, provides optimization recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add local AI API cost tracking, budget checks, waste detection, and reporting to projects that call LLM providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local usage JSON file and generated reports can reveal provider usage, business activity, task names, sessions, or metadata. <br>
Mitigation: Set the usage file path to a private location, restrict file permissions, avoid sensitive values in task/session/metadata fields, and review reports before sharing. <br>
Risk: Budget status and cost calculations depend on manually logged calls and manually maintained model pricing. <br>
Mitigation: Centralize API calls through a wrapper that logs every request, periodically compare totals with provider dashboards, and update model pricing when providers change rates. <br>
Risk: The kill switch is application-level and only works when integrated into the caller's workflow. <br>
Mitigation: Call the pre-call budget check before every API request and persist or re-check budget state if restart behavior matters. <br>


## Reference(s): <br>
- [Token Tamer README](artifact/README.md) <br>
- [Token Tamer Limitations](artifact/LIMITATIONS.md) <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/token-tamer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; JSON or text reports when the bundled scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python scripts and a configurable JSON usage file.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
