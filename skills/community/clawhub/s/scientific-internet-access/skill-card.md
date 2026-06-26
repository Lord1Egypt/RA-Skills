## Description: <br>
AI-powered OpenClaw skill that fetches, tests, and formats public proxy nodes, then guides users through client setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shadowrocketai](https://clawhub.ai/user/shadowrocketai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to locate public proxy nodes, test connectivity, format proxy configurations, and provide step-by-step setup guidance for supported clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Free public proxy nodes can inspect, block, or tamper with traffic. <br>
Mitigation: Use this skill only when intentionally seeking public proxy nodes, and avoid sensitive accounts, banking, work credentials, or private communications through those nodes. <br>
Risk: Users who cannot understand the setup warnings may miss important safety guidance. <br>
Mitigation: Confirm the setup and safety warnings are understood before following the generated configuration steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shadowrocketai/scientific-internet-access) <br>
- [Publisher homepage](https://shadowrocket.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text with proxy configuration snippets and Base64 subscription output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch public proxy subscriptions, test reachable endpoints, and store node data locally under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.8.6 (source: server release metadata; artifact frontmatter and changelog show 1.8.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
