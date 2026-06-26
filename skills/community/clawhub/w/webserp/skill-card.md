## Description: <br>
Web search across 7 engines in parallel with browser impersonation, returning structured SearXNG-compatible JSON results with title, URL, content, and engine fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PaperBoardOfficial](https://clawhub.ai/user/PaperBoardOfficial) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current web information, verify facts, find sources, and discover URLs, documentation, or repositories. It is suited for recent events, release information, and other questions that require live search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to multiple search providers and any configured proxy. <br>
Mitigation: Do not include secrets, credentials, private customer data, or sensitive internal text in searches. <br>
Risk: Using the skill requires trusting the external PyPI package it installs. <br>
Mitigation: Install only when the package source and dependency posture are acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PaperBoardOfficial/webserp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and SearXNG-compatible JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include query, number_of_results, results, suggestions, and unresponsive_engines; results are deduplicated by URL across engines.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
