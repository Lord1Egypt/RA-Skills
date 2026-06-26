## Description: <br>
Monitors ClawHub for skills gaining traction by tracking download and star growth, then reports surges and top movers through a local Node.js CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gabriel-Kaufman](https://clawhub.ai/user/Gabriel-Kaufman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor ClawHub trends, identify fast-moving skills, and surface surge alerts that can be captured by an agent or scheduled CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands fetch public ClawHub skill data over the network and may be run repeatedly when scheduled. <br>
Mitigation: Review scheduling frequency before deployment and expect outbound requests to clawhub.ai only when commands run. <br>
Risk: The skill stores profile and trend state in local files under the configured surge directory. <br>
Mitigation: Do not put secrets in the profile description or keywords, and review local state paths before running in shared environments. <br>


## Reference(s): <br>
- [Hot Skills on ClawHub](https://clawhub.ai/Gabriel-Kaufman/trending-skill-identifier) <br>
- [ClawHub Skills Catalog](https://clawhub.ai/skills) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with optional Markdown and shell command examples in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs trend lists, surge alerts, profile relevance scores, status summaries, and configuration guidance to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
