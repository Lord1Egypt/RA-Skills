## Description: <br>
Performs a web search using a local SearXNG instance and returns raw search results for the given query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netobasilio](https://clawhub.ai/user/netobasilio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve up-to-date web search results through a locally configured SearXNG-backed helper command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local /usr/local/bin/websearch helper that is not shipped or verified by the release. <br>
Mitigation: Install and use this skill only after reviewing and trusting the local helper program and its configuration. <br>
Risk: Search results are external web content returned by the configured SearXNG instance and may be incomplete or untrusted. <br>
Mitigation: Verify important claims against reliable sources before acting on the results. <br>


## Reference(s): <br>
- [ClawHub WebSearch release](https://clawhub.ai/netobasilio/websearch) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [String containing raw SearXNG results as JSON or text, depending on local configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local /usr/local/bin/websearch helper and an accessible SearXNG instance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
