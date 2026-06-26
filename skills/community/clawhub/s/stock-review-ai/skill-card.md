## Description: <br>
A-share market automated review and analysis system, generating daily market insights with Gemini AI, supporting publishing to Hugo blog and WeChat Official Account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donvink](https://clawhub.ai/user/donvink) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market analysts use this skill to fetch A-share market data, generate daily Markdown review reports, optionally analyze the report with Gemini, and publish outputs to a Hugo blog or WeChat Official Account draft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send generated market summaries to Gemini when a Gemini API key is configured. <br>
Mitigation: Run with AI analysis disabled or use an account and data handling mode appropriate for the sensitivity of the market data being processed. <br>
Risk: The skill can publish generated reports to local Hugo content files or create WeChat drafts when those platforms are enabled. <br>
Mitigation: Review config.yaml platforms, generated content, and publishing credentials before running in an environment connected to public channels. <br>
Risk: The skill loads credentials from environment variables and discovered .env files. <br>
Mitigation: Keep .env files in trusted locations, scope API credentials to the intended use, and avoid running the skill from directories containing untrusted configuration. <br>
Risk: Generated market analysis could be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational analysis, keep the included investment-risk disclaimer, and require human review before acting on or publishing trading guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/donvink/stock-review-ai) <br>
- [Project Homepage](https://github.com/donvink/stock-review) <br>
- [Live Demo Blog](https://donvink.github.io/stock-review/) <br>
- [AkShare Documentation](https://akshare.akfamily.xyz/index.html) <br>
- [Gemini API Key Portal](https://aistudio.google.com/) <br>
- [WeChat Official Account Platform](https://developers.weixin.qq.com/platform/) <br>
- [Hugo Documentation](https://gohugo.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, local data files, optional blog post files, optional WeChat draft identifiers, and JSON execution status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches market data, may call Gemini when GEMINI_API_KEY is configured, writes report/blog files locally, and can create WeChat drafts when WeChat credentials are configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
