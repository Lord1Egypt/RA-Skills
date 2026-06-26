## Description: <br>
Tabstack helps agents read web pages and PDFs, extract structured data, transform content into JSON, run web research, and perform browser automation through the Tabstack API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmorchard](https://clawhub.ai/user/lmorchard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to fetch and summarize web or PDF content, extract JSON from documents, run cited research, and automate browser tasks when a normal page fetch is not enough. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web queries, processed URLs, schemas, instructions, and data payloads are sent to Tabstack for processing. <br>
Mitigation: Avoid private URLs, confidential PDFs, passwords, tokens, and sensitive data unless the Tabstack service is approved for that use. <br>
Risk: Browser automation can click, navigate, fill forms, and submit data. <br>
Mitigation: Use guardrails for automation tasks and review task scope before allowing form submission or multi-step interactions. <br>
Risk: The skill depends on npm packages and an external API key. <br>
Mitigation: Install from the provided lockfile, protect TABSTACK_API_KEY, and consider pinning dependency versions for reproducible deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lmorchard/tabstack) <br>
- [Publisher profile](https://clawhub.ai/user/lmorchard) <br>
- [Tabstack](https://tabstack.ai) <br>
- [Tabstack Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, or plain text emitted by shell commands, depending on the selected operation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npx, npm dependencies, and TABSTACK_API_KEY.] <br>

## Skill Version(s): <br>
0.3.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
