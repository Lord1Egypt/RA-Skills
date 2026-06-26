## Description: <br>
Satori gives agents persistent long-term memory by saving notable facts through the Satori CLI and retrieving relevant context across AI sessions and tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelachance](https://clawhub.ai/user/joelachance) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Satori to preserve project decisions, preferences, deadlines, names, and other durable context so future AI sessions can retrieve relevant facts across tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save and reuse conversation details through an external CLI without clear confirmation or deletion controls. <br>
Mitigation: Use it only when persistent memory is intended, ask before saving sensitive facts, and establish review and deletion practices before routine use. <br>
Risk: The artifact invokes the Satori CLI with an automatically resolved latest package version. <br>
Mitigation: Pin or inspect the Satori CLI package before use when package drift or supply-chain review matters. <br>
Risk: The CLI auto-provisions credentials and local configuration on first run. <br>
Mitigation: Review where credentials are stored and define how to rotate or remove them before enabling the skill in shared or regulated environments. <br>


## Reference(s): <br>
- [Satori ClawHub Page](https://clawhub.ai/joelachance/satori) <br>
- [Fact Extraction Criteria](artifact/references/fact-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and retrieves facts through an external Satori CLI using local terminal access.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
