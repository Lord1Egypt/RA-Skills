## Description: <br>
Scrape Reddit stock pages and use DeepSeek AI with Yahoo Finance data to analyze which stock has the highest 1-week return potential. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[altusrossouw](https://clawhub.ai/user/altusrossouw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to combine public Reddit stock discussion, Yahoo Finance market data, and DeepSeek analysis into short-term stock-pick analysis. It supports CLI and FastAPI web app workflows, including optional European exchange equivalents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends public Reddit and Yahoo Finance-derived market data to DeepSeek using the user's API key. <br>
Mitigation: Run it only where DeepSeek processing is acceptable, protect DEEPSEEK_API_KEY as a sensitive credential, and avoid adding private portfolio or personal financial data to prompts. <br>
Risk: The output can look like actionable investment guidance even though it is AI-generated short-term market analysis. <br>
Mitigation: Treat results as educational analysis rather than financial advice, and require independent review before making investment decisions. <br>
Risk: Dependency versions are broad in requirements.txt, which can make runtime behavior change over time. <br>
Mitigation: Use a pinned or locked dependency environment before running the skill in sensitive or production-like environments. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/AltusRossouw/reddit-stonks) <br>
- [ClawHub skill page](https://clawhub.ai/altusrossouw/reddit-stonks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style analysis in CLI output or server-sent web app responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock data tables, top pick, runner-up, wildcard, risk factors, confidence score, and optional European exchange equivalents.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
