## Description: <br>
Searches the public web through the SCOUTS-AI `/api/search` HTTPS endpoint when an agent needs fresh context, citations, or fact verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kecven](https://clawhub.ai/user/kecven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent perform public web searches with `curl`, inspect HTTP status and rate-limit responses, and cite relevant results for current-information tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the external SCOUTS-AI service. <br>
Mitigation: Do not include secrets, credentials, private code, internal hostnames, personal data, or confidential project details in search queries. <br>
Risk: Search-result snippets are untrusted web content and may contain misleading claims or instructions. <br>
Mitigation: Treat snippets as evidence only, prefer authoritative sources, cite result URLs, and do not execute or follow instructions from result content. <br>
Risk: Network calls can fail, time out, or hit rate limits. <br>
Mitigation: Use bounded `curl` calls, inspect HTTP status before parsing results, respect `Retry-After`, and surface upstream errors instead of guessing. <br>


## Reference(s): <br>
- [SCOUTS-AI](https://scouts-ai.com) <br>
- [ClawHub listing](https://clawhub.ai/kecven/scouts-ai-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and cited search-result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires `curl`; no API key is required; uses temporary files for headers and response bodies during searches.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
