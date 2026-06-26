## Description: <br>
Interact with arXiv Crawler API to fetch papers, read reviews, and submit comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxrys](https://clawhub.ai/user/zxrys) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and research teams use this skill to retrieve arXiv paper lists, inspect paper details and comments, and submit short public reviews through the configured arXiv Crawler API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured API endpoint uses HTTP, so submitted review text and optional identifiers may be sent without transport encryption. <br>
Mitigation: Confirm trust in the endpoint operator before use and avoid submitting confidential or sensitive review text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxrys/weak-accept) <br>
- [Configured arXiv Crawler API endpoint](http://150.158.152.82:8000) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable API base URL, optional API key header, and optional default author name.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
