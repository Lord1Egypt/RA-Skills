## Description: <br>
Fetches HTML or text from HTTP(S) URLs with Python stdlib, optional basic HTML-to-markdown conversion, and URL/path validation for safer local saves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johstracke](https://clawhub.ai/user/johstracke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to preview, save, or convert static web pages for research collection, content aggregation, and simple scraping workflows without API keys or external dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided URLs and may access network locations that are inappropriate in sensitive environments. <br>
Mitigation: Use it only where outbound HTTP(S) requests are acceptable, avoid untrusted URLs in sensitive networks, and review fetched sources before use. <br>
Risk: Fetched content can be saved to local files. <br>
Mitigation: Save only to intended non-sensitive paths and rely on the skill's path validation as a guardrail rather than a substitute for user review. <br>
Risk: Markdown conversion is basic and may omit or distort page structure. <br>
Mitigation: Review converted Markdown before using it as source material for downstream decisions or publication. <br>


## Reference(s): <br>
- [ClawHub URL Fetcher release](https://clawhub.ai/johstracke/url-fetcher) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/johstracke) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text preview or saved HTML/Markdown file content with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches static HTTP(S) content with a 10-second timeout; markdown conversion is basic and regex-based.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
