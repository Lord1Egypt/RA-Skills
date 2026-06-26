## Description: <br>
Extracts article content from URLs as clean Markdown using a Scrapling-based fetch script with fast and stealth modes plus a Jina Reader fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haanya168](https://clawhub.ai/user/haanya168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to fetch a web page or article URL and convert the main content into Markdown for reading, summarization, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching arbitrary web pages may expose private, signed, localhost, internal-network, or confidential URLs. <br>
Mitigation: Only pass URLs that are acceptable to fetch from the agent environment; avoid sensitive, internal, or confidential targets. <br>
Risk: The Jina Reader fallback sends the target URL to an external service. <br>
Mitigation: Avoid the Jina Reader fallback for sensitive URLs and use the local Scrapling-based fetch path only when confidentiality matters. <br>
Risk: Unpinned Python dependencies can change behavior over time. <br>
Mitigation: Install the skill in a virtual environment and pin dependency versions for reviewed deployments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/haanya168/web-content-fetcher-hanya) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON with URL, mode, selector, content length, and extracted content when JSON output is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default extracted-content limit is 30000 characters unless a caller supplies a smaller max_chars value.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
