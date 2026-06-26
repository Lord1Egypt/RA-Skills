## Description: <br>
Reduce OpenClaw AI costs by 97%. Haiku model routing, free Ollama heartbeats, prompt caching, and budget controls. Go from $1,500/month to $50/month in 5 minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smartpeopleconnected](https://clawhub.ai/user/smartpeopleconnected) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to preview, apply, verify, and roll back cost-saving OpenClaw configuration changes for model routing, heartbeat providers, prompt caching, session scope, and budget controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change OpenClaw cost settings and prompt files under ~/.openclaw/ when run with --apply. <br>
Mitigation: Run the default dry-run previews first, inspect diffs and generated prompt files, and apply only after confirming the routing, budgets, heartbeat provider, memory rules, and stats/report files are acceptable. <br>
Risk: Generated model routing, budget, heartbeat, and memory rules may not match every OpenClaw workflow. <br>
Mitigation: Review the generated configuration and prompt templates before use, then verify the setup with the provided health and verification commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smartpeopleconnected/token-optimizer) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, terminal text, JSON configuration, and generated prompt/template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run preview is the default for optimization and heartbeat setup commands; applying changes writes under ~/.openclaw/.] <br>

## Skill Version(s): <br>
1.0.18 (source: changelog, skill.json, _meta.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
