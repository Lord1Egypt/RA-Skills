## Description: <br>
Use when asked to safely inspect, sandbox, detonate, run, or dynamically observe untrusted release artifacts, closed-source binaries, JARs, installers, wallet/private-key software, crypto trading bots, or suspicious GitHub releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[remixmm](https://clawhub.ai/user/remixmm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and operators use this skill to plan staged static and dynamic observation of untrusted binaries, installers, wallet tools, and trading bots before deciding whether further testing or deployment is appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running untrusted binaries can expose host secrets, wallet material, or funded accounts. <br>
Mitigation: Use a disposable VM or tightly restricted container, and never mount real wallets, SSH keys, browser profiles, cloud credentials, production .env files, or funded accounts. <br>
Risk: Dynamic execution can contact undeclared endpoints, download payloads, or behave differently when network access is available. <br>
Mitigation: Start with static analysis and offline or mock-network tiers, then use controlled egress with explicit allowlists and logging only after approval. <br>
Risk: Docker containment alone may be insufficient for hostile samples, kernel exploit risk, or live-fund testing. <br>
Mitigation: Use a sacrificial VM or disposable VPS for hostile samples and any live tiny-fund tier. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/remixmm/untrusted-binary-sandbox) <br>
- [Docker And VM Sandbox Reference](references/docker-sandbox.md) <br>
- [Observation Checklist And Report Template](references/observation-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and structured findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sandbox scaffolding commands, Docker configuration, evidence checklists, and go/no-go recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
