## Description: <br>
Maps sensor-like physical readings into stylized subjective states and drives local HTML cockpit visualizations for the Taohuayuan Alpha watcher concept. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents can use this skill to turn environmental sensor-like inputs into first-person affective descriptions, 5D state updates, and local cockpit visualization behavior. It is best suited for evaluating the demo interaction model rather than factual sensor reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stylized emotional interpretations can obscure the underlying sensor facts. <br>
Mitigation: Preserve raw sensor values alongside subjective descriptions whenever factual reporting or auditability matters. <br>
Risk: Adding a real hardware or WebSocket bridge could introduce new local data exposure or execution risks. <br>
Mitigation: Keep any bridge local, review the added bridge code before use, and limit it to the minimum sensor data needed for the demo. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/s2-silicon-perception-cockpit) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON-style state data, Python examples, and local HTML cockpit files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local demo behavior; no hidden data access, persistence, exfiltration, or destructive behavior reported by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, skill frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
