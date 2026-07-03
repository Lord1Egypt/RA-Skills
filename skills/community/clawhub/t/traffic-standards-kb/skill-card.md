## Description: <br>
Retrieves Chinese transportation standards (GB, JT, and GA) through the Solvex API and formats citations for smart transportation solution documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solvex-top](https://clawhub.ai/user/solvex-top) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, solution architects, and proposal writers use this skill when drafting Chinese smart transportation solutions, bids, or technical proposals that need GB/JT/GA standards citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends transportation-standard queries and relevant prompt context to solvexpert.net. <br>
Mitigation: Get explicit user approval before API calls and redact confidential bid, project, or internal planning text. <br>
Risk: The skill requires a sensitive Solvex API key and documents a shared searchAuthToken. <br>
Mitigation: Store STANDARDS_API_KEY outside source control, treat the documented searchAuthToken as sensitive, and avoid logging credentials or full request bodies. <br>
Risk: Automatically inserted standards citations can be incomplete or mismatched if API responses are empty or off topic. <br>
Mitigation: Validate successful responses and review citations before using them in formal solutions or proposals. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/solvex-top/traffic-standards-kb) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Traffic Standards Knowledge Base README](artifact/README.md) <br>
- [API Reference](artifact/api-reference.md) <br>
- [Solvex API key portal](https://solvexpert.net) <br>
- [Solvex Standards API endpoint](https://solvexpert.net/api/v1/standards/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell examples, JSON API examples, and formatted citation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STANDARDS_API_KEY and the documented searchAuthToken; sends transportation-standard queries and related prompt context to solvexpert.net.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
