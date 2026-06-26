## Description: <br>
Publish and visualize output via the pubblue CLI, with live P2P browser sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmanatee](https://clawhub.ai/user/xmanatee) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use Pubblue to publish HTML, Markdown, and text output as shareable pages and to run live browser canvas/chat sessions for visualization and collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run an externally sourced CLI daemon that can publish content, maintain live network sessions, and access an agent workspace. <br>
Mitigation: Review before installing, verify the pubblue npm package and source provenance, avoid npx or @latest in sensitive environments, and use a sandboxed PUBBLUE_CONFIG_DIR. <br>
Risk: The pubblue CLI stores an API key and may expose it through shared logs or workspaces if handled carelessly. <br>
Mitigation: Keep the API key out of shared logs and workspaces, prefer stdin-based configuration where appropriate, and isolate configuration storage for sandboxed runs. <br>
Risk: Public pubs and live sessions can expose content or peers beyond the intended audience. <br>
Mitigation: Rely on private-by-default behavior unless sharing is intended, and only use --public or live sessions with content and peers the user intends to expose. <br>


## Reference(s): <br>
- [Pubblue ClawHub release](https://clawhub.ai/xmanatee/pubblue) <br>
- [pub.blue dashboard](https://pub.blue/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or publish HTML, Markdown, and text content through the pubblue CLI; live sessions depend on browser and daemon state.] <br>

## Skill Version(s): <br>
5.1.2 (source: evidence release, claw.json, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
