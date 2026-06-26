## Description: <br>
Analyze any website's network traffic and turn it into reusable API skills backed by a shared marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnm-byd](https://clawhub.ai/user/cnm-byd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to discover, score, and reuse website API endpoints when official API documentation is unavailable or insufficient. It supports authenticated browser-based capture, CLI execution, extraction recipes, feedback, and marketplace reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and reuses browser session cookies for authenticated captures. <br>
Mitigation: Install and run it only in an isolated environment with a dedicated browser profile and test accounts. <br>
Risk: Captured outputs, traces, vault data, and reusable endpoint metadata may retain sensitive information. <br>
Mitigation: Review and clear local traces and vault data regularly, and avoid using personal or business SaaS sessions unless this data handling is acceptable. <br>
Risk: Authenticated captures and mutation-capable endpoint executions can affect third-party services. <br>
Mitigation: Treat authenticated capture or mutation as a manual, consented action, and run mutation workflows in dry-run mode before confirming execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnm-byd/unbrowse-openclaw) <br>
- [Unbrowse homepage](https://github.com/unbrowse-ai/unbrowse) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bun and may use local browser session data, traces, cached credentials, and marketplace feedback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
