## Description: <br>
Finds Buddhist temples, Taoist shrines, Confucian temples, and sacred sites, with etiquette, visiting details, meditation opportunities, and related travel services powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to find temples, shrines, monasteries, sacred sites, and related booking options from flyai CLI results. It is intended for user-facing travel discovery with markdown summaries and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run a global npm CLI before answering travel queries. <br>
Mitigation: Review and install the flyai CLI yourself when possible, or require agent approval before package installation or external lookup. <br>
Risk: Travel recommendations and booking links depend on flyai CLI output rather than the model's built-in knowledge. <br>
Mitigation: Require successful CLI output with detailUrl booking links before presenting results, and treat missing CLI data as a stop condition. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should follow the user's input language and only summarize data returned by the flyai CLI.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
