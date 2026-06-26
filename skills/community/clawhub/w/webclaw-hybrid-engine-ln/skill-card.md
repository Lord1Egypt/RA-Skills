## Description: <br>
Uses a local WebClaw Gateway service to fetch web pages and return cleaned Markdown for scraping, summarization, and research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngoclinh15994](https://clawhub.ai/user/ngoclinh15994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route webpage scraping through a local engine that returns cleaner Markdown for downstream answering, summarization, and multi-page research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags the skill as suspicious because it forces web access through an unverified local npm engine. <br>
Mitigation: Review before installing and run the local engine only if you trust the npm package and understand its data handling. <br>
Risk: URLs and page content may be handled by the local service, including potentially sensitive internal or authenticated pages. <br>
Mitigation: Avoid using this skill for internal, private, authenticated, or sensitive pages unless the engine and its data handling have been independently verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ngoclinh15994/webclaw-hybrid-engine-ln) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, API calls, Guidance] <br>
**Output Format:** [Markdown and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local WebClaw service on port 8822; no API key is declared.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
