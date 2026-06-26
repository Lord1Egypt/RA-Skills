## Description: <br>
Verosight Monitor integrates the Verosight API so agents can perform social media intelligence and cyber monitoring across major social, video, thread, and news sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrrqd](https://clawhub.ai/user/jrrqd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect agents to Verosight for sentiment analysis, trend monitoring, influencer discovery, bot-detection workflows, and report generation. It is suited to approved social listening, digital reputation, and cyber monitoring tasks that require credentialed API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and JWTs may be exposed when passed directly on shared command lines, copied into prompts, or retained in shell history. <br>
Mitigation: Use test or limited-scope keys where possible, pass credentials through protected environment variables, avoid shared terminals, and rotate credentials after exposure. <br>
Risk: Search terms, platform selections, returned posts, and generated reports may contain sensitive monitoring data or personal information. <br>
Mitigation: Run only approved monitoring, minimize retained data, restrict report access, and treat returned posts and reports as sensitive outputs. <br>
Risk: Sentiment, trend, influencer, and bot-detection outputs can be incomplete or misleading if source coverage is uneven or automated classifications are wrong. <br>
Mitigation: Use the results as decision support, manually review high-impact findings, and document source coverage and uncertainty in reports. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/jrrqd/verosight-monitor) <br>
- [Verosight API](https://verosight.com) <br>
- [Verosight Documentation](https://verosight.com/docs) <br>
- [Sentiment Analysis Workflow](references/sentiment-workflow.md) <br>
- [PDF Report Generation with pdfkit](references/pdf-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API examples, JSON response descriptions, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API requests, analysis summaries, monitoring reports, and PDF-generation code snippets for agent use.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
