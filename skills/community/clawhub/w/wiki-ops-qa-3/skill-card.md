## Description: <br>
Use when an agent should answer simple operations questions by retrieving internal wiki content through wiki MCP, and must refuse to answer when the wiki does not provide enough evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glylovechina](https://clawhub.ai/user/glylovechina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and support teams use this skill to answer document-oriented questions about deployments, releases, rollbacks, restarts, logs, alerts, SOPs, permissions, and configuration using internal wiki evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may be asked to answer operational questions without enough wiki evidence. <br>
Mitigation: Use only retrieved wiki content and refuse or answer conservatively when evidence is missing, incomplete, or conflicting. <br>
Risk: The skill depends on access to configured internal wiki MCP tools. <br>
Mitigation: Install only where the agent is authorized to query those wiki tools and treat the skill as documentation Q&A, not permission to inspect live systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/glylovechina/wiki-ops-qa-3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown response with Conclusion, Evidence, and Unknown sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers must be grounded only in retrieved wiki evidence; missing, incomplete, or conflicting evidence leads to refusal or conservative output.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
