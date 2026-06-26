## Description: <br>
Parses raw technology event search results, removes stale or duplicate entries, scores relevance, and produces a standardized digest for scheduled delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, sales engineers, and marketing operations teams use this skill to turn public technology event search results into a concise Markdown daily digest for Feishu, WeCom, or email workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured webhook can expose event digests or webhook credentials if left as a placeholder or shared too broadly. <br>
Mitigation: Replace the placeholder webhook with a controlled destination, protect the webhook token, and confirm channel access before enabling scheduled delivery. <br>
Risk: The digest is generated from public search results that may be stale, incomplete, or incorrect. <br>
Mitigation: Review event dates, speakers, fees, and registration links against organizer announcements before relying on the digest. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [Input and output schema](schema.json) <br>
- [OpenClaw workflow template](assets/workflow.yaml) <br>
- [ClawHub skill page](https://clawhub.ai/boboy-j/tech-event-intelligence-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown digest with supporting JSON and YAML configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits results by configured count and relevance threshold, marks missing fields for verification, and includes a public-information disclaimer.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
