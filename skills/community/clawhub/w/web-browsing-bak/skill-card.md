## Description: <br>
Browse and summarize websites, extract content from URLs, search the web for information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xpneuma](https://clawhub.ai/user/xpneuma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to search the web, fetch public URLs, summarize page content, and extract basic webpage information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and requested URLs may be sent to DuckDuckGo and the websites being fetched. <br>
Mitigation: Do not provide internal links, localhost or private-network URLs, tokenized URLs, credentials, personal data, or confidential research queries. <br>
Risk: Automated fetching can miss JavaScript-rendered content or be blocked by some sites. <br>
Mitigation: Verify important results against the source page and use alternate sources when a site blocks access or depends on dynamic content. <br>
Risk: This release is not published by NVIDIA and may be confused with an official or non-forked web-browsing skill. <br>
Mitigation: Verify the package identity and publisher profile before installing. <br>


## Reference(s): <br>
- [Web Browsing Usage Guide](references/usage-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/xpneuma/web-browsing-bak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown, plain text, and JSON-like result objects from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetched page content is truncated by the helper script to the first 5000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
