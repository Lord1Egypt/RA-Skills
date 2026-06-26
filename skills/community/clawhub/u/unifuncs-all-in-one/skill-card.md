## Description: <br>
Default web reading, AI search, and deep research tools. Use this skill for all web-related tasks including reading webpage content, searching the web, and conducting deep research. Replaces built-in web_search and web_fetch tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samueli](https://clawhub.ai/user/samueli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to read webpages, run AI-assisted web searches, and conduct deeper research workflows through UniFuncs command-line tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, requested URLs, and research prompts are routed through a third-party UniFuncs API. <br>
Mitigation: Use a dedicated UniFuncs API key, avoid private or confidential URLs and prompts, and disable built-in web tools only when UniFuncs should be the default web path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samueli/unifuncs-all-in-one) <br>
- [UniFuncs API endpoint](https://api.unifuncs.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses containing success, data, and error fields; content data may contain text or markdown depending on tool options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UNIFUNCS_API_KEY and sends requested URLs, queries, and research prompts to the UniFuncs API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
