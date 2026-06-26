## Description: <br>
Perform privacy-focused metasearch using local or remote SearXNG instances with retries, timeouts, category, time, safe-search, and engine-specific filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elmaslouhymouaad](https://clawhub.ai/user/elmaslouhymouaad) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to query configured SearXNG instances, retrieve structured web, image, video, news, science, and file search results, and apply common filters such as category, time range, safe search, language, and search engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and request metadata are sent to the configured SearXNG instance. <br>
Mitigation: Use a local or otherwise trusted SearXNG instance for private queries. <br>
Risk: Untrusted prompts could try to choose an unsafe instance URL or export path. <br>
Mitigation: Keep instance URLs and export file paths under operator control and validate them before use. <br>
Risk: Disabling SSL verification can expose traffic to interception on remote endpoints. <br>
Mitigation: Keep SSL verification enabled except for controlled local development. <br>
Risk: Unpinned or unaudited dependencies can introduce supply-chain risk. <br>
Mitigation: Pin and audit dependencies before production deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elmaslouhymouaad/searxng-search-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, configuration snippets, and structured SearXNG result data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return dictionaries or structured result objects from SearXNG responses and may export results to JSON or CSV when explicitly invoked.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact package metadata says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
