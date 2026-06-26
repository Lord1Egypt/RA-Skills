## Description: <br>
Dada provides hosted backend infrastructure for OpenClaw agents, including managed databases, webhooks, and file hosting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rotemtam](https://clawhub.ai/user/rotemtam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Dada to add persistent structured storage, webhooks, and file hosting to OpenClaw workflows through CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags behavior that may run a nested review helper with reduced sandbox and approval protections. <br>
Mitigation: Install only if you trust the publisher; before using an autoreview helper, prefer --no-yolo or set AUTOREVIEW_YOLO=0. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/rotemtam/usedada) <br>
- [Dada homepage](https://usedada.dev) <br>
- [Dada releases](https://github.com/honeybadge-labs/dada/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLI flags such as -j for machine-readable JSON, --select for field projection, and --fail-empty for empty-result handling.] <br>

## Skill Version(s): <br>
0.3.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
