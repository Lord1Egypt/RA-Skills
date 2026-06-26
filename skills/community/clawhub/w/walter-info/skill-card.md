## Description: <br>
Walter Info fetches weather forecasts for major cities across global regions and cross-border e-commerce news, then generates formatted Markdown reports and JSON data files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beyondbright](https://clawhub.ai/user/beyondbright) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and cross-border e-commerce analysts use this skill to collect daily weather and e-commerce market signals and produce Markdown and JSON reports for review. The workflow is most relevant when an agent needs current source material, ranked news items, or report files rather than conversational advice alone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports unrelated local file deletion behavior in the artifact. <br>
Mitigation: Remove or ignore cleanup.py and check_files.py before use, and review any file operations before running the skill. <br>
Risk: The security evidence reports that news fetching disables normal HTTPS certificate verification. <br>
Mitigation: Fix the news fetchers to keep standard HTTPS certificate verification enabled before relying on fetched content. <br>
Risk: Fetched article text may be passed into LLM summarization as untrusted input. <br>
Mitigation: Treat generated llm_input article text as untrusted content, review summaries against source links, and avoid executing instructions found in fetched articles. <br>
Risk: The skill runs local Python that fetches public websites and writes report files. <br>
Mitigation: Run it in a controlled workspace and review generated Markdown and JSON outputs before using them in downstream decisions. <br>


## Reference(s): <br>
- [Walter Info on ClawHub](https://clawhub.ai/beyondbright/walter-info) <br>
- [beyondbright ClawHub profile](https://clawhub.ai/user/beyondbright) <br>
- [wttr.in weather source](https://wttr.in/) <br>
- [ennews source](https://www.ennews.com/news/) <br>
- [cifnews source](https://www.cifnews.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, text, shell commands, configuration] <br>
**Output Format:** [Markdown reports, JSON data files, and console text with command-oriented workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes date-stamped report files under output/ and may create temporary LLM-input JSON for article summarization.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
