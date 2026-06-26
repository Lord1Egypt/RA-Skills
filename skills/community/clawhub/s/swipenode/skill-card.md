## Description: <br>
SwipeNode Web Extractor fetches web pages and extracts structured JSON or clean readable text without rendering JavaScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirToby99](https://clawhub.ai/user/sirToby99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to read webpages, summarize articles, check news, or extract structured data from URLs while avoiding browser rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching third-party webpages can access sites whose terms, permissions, or rate limits do not allow automated extraction. <br>
Mitigation: Use the skill only for authorized targets, respect site terms and rate limits, and avoid authenticated or protected sites unless permission is clear. <br>
Risk: TLS fingerprint impersonation and bypass-oriented options can be inappropriate on blocked or high-security sites. <br>
Mitigation: Require explicit user approval before using impersonation options and prefer ordinary HTTP or official APIs when they are available. <br>
Risk: Broad page-reading activation can cause unintended network requests when a user asks for news, summaries, or URL extraction. <br>
Mitigation: Confirm the target URL and purpose before fetching, keep requests narrow, and report network errors without aggressive retries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sirToby99/swipenode) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [JSON to stdout with optional clean text fields and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to target URLs and can use explicit TLS fingerprint impersonation options.] <br>

## Skill Version(s): <br>
1.6.4 (source: server release evidence; install.sh pins v1.6.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
