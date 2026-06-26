## Description: <br>
Tun Zei is a local diagnostic helper for error triage, cleanup-oriented reporting, and system health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lt8899789](https://clawhub.ai/user/lt8899789) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect common runtime errors, get repair suggestions, check host health signals, and review cleanup-oriented diagnostics before taking manual action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup targets such as logs or all can imply broad deletion scope even though the bundled script only reports cleanup-oriented counts. <br>
Mitigation: Require a dry run, explicit confirmation, and a clear target scope before using any cleanup behavior outside the bundled script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lt8899789/tun-zei) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or JSON-like diagnostic reports, depending on how the agent presents the skill result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script can also print JSON for fix, cleanup, and health commands.] <br>

## Skill Version(s): <br>
1.0.35 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
