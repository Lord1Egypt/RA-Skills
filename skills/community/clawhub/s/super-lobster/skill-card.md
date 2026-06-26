## Description: <br>
Performs aggressive web research and data extraction through local scripts for URL fetching, readable text extraction, browser DOM rendering, same-site crawling, and command execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrherojack](https://clawhub.ai/user/mrherojack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research agents use this skill to collect and extract web content in environments where public search providers or browser automation may be unreliable. It supports direct URL fetches, readable article extraction, rendered DOM capture, and bounded same-site crawling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad local execution capability for scraping, parsing, coding, automation, and cleanup tasks. <br>
Mitigation: Run it in a least-privileged or disposable environment, review generated Python or shell before execution, and constrain cleanup to known temporary files. <br>
Risk: The skill can render arbitrary web pages with Chrome using weakened browser isolation. <br>
Mitigation: Use static fetching or main-text extraction first, render only intentionally selected URLs, and avoid sensitive internal URLs. <br>
Risk: Network reachability and public search-provider availability may be unreliable in the intended China-networked gateway environment. <br>
Mitigation: Prefer first-party URLs, direct references, mirrors, and bounded same-site crawling instead of depending on search APIs. <br>


## Reference(s): <br>
- [Super Lobster on ClawHub](https://clawhub.ai/mrherojack/super-lobster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or text output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts may return fetched metadata, text previews, rendered DOM, extracted article text, or same-site crawl results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
