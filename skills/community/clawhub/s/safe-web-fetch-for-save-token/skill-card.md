## Description: <br>
Fetches web pages for agents as cleaned Markdown or JSON through a Python helper that validates URLs, enforces SSL verification, and can route content through Jina Reader. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bg1avd](https://clawhub.ai/user/bg1avd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when an agent needs to retrieve public web content in a cleaner, token-efficient format. It is suited to public URLs and should not be used for private, internal, credential-bearing, or sensitive links without additional review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched URLs and page content may be routed through Jina Reader, a third-party service. <br>
Mitigation: Use only with public, non-sensitive URLs unless the skill is updated to clearly disclose third-party routing and the deployment owner accepts that routing. <br>
Risk: Default configuration allows outbound fetching for any public HTTP or HTTPS domain not otherwise blocked. <br>
Mitigation: Configure a concrete allowed_domains list for approved domains before using the skill in controlled or enterprise workflows. <br>
Risk: Sensitive-data scanning does not cover all returned content when Jina Reader is used. <br>
Mitigation: Avoid credential-bearing or private links, and add scanning of all returned content before relying on the output in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bg1avd/safe-web-fetch-for-save-token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text by default, or JSON when called with --json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3; output may include source URL, original URL, fetched content, content length, source type, and error status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
