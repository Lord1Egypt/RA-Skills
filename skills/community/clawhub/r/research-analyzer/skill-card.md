## Description: <br>
Research Analyzer uses the Tavily API to search the web and generate structured research reports for deep research, competitive analysis, market research, and technical investigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyqdq888](https://clawhub.ai/user/hyqdq888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to run Tavily-backed web research and produce structured Markdown reports for market, competitive, deep research, and technical analysis tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries are sent to Tavily and may expose sensitive or regulated text. <br>
Mitigation: Use a dedicated Tavily API key and avoid submitting confidential, personal, or regulated information in queries. <br>
Risk: The skill can write a generated report to a user-selected output path. <br>
Mitigation: Choose output paths deliberately and review generated reports before relying on or sharing them. <br>


## Reference(s): <br>
- [Research Analyzer on ClawHub](https://clawhub.ai/hyqdq888/research-analyzer) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown report printed to the console or saved to a user-selected file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; deep mode can include raw Tavily content and max results are capped at 20.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
