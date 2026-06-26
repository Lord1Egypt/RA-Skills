## Description: <br>
Professional search across news, places, maps, reviews, scholar, patents, and bulk scraping via the Serper API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinitngr](https://clawhub.ai/user/vinitngr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to run Serper-backed search and scraping workflows from the command line, including filtered web, news, places, maps, shopping, scholar, and patent searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses a globally installed npm package. <br>
Mitigation: Install it only from the trusted publisher and review package updates before use. <br>
Risk: Search queries, URLs, and scraped content may be sent through a Serper-backed workflow. <br>
Mitigation: Do not use secrets, signed URLs, private systems, internal-only endpoints, or sensitive customer data unless authorized. <br>
Risk: Bulk scraping can retrieve external web content that may be unreliable or unsuitable for downstream use. <br>
Mitigation: Review scraped results before relying on them in agent outputs or business workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vinitngr/serper-v) <br>
- [Setup instructions](artifact/SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and command-result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Serper API key and the globally installed @vinitngr/serper-v npm package.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
