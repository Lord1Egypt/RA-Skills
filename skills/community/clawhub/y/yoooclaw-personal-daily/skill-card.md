## Description: <br>
Generates a personalized daily news briefing from configured user interest topics, using bounded web searches and strict recency and source-quality filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn selected topics, such as AI models, electric vehicles, startup financing, humanoid robotics, companies, or products, into a concise daily news digest with links to selected sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured interest topics may be exposed through web searches. <br>
Mitigation: Avoid confidential or highly sensitive topics in the interests file or scheduled message. <br>
Risk: Daily search filtering can miss relevant current news or exclude items without explicit date signals. <br>
Mitigation: Treat the briefing as a high-density digest and follow source URLs before relying on a news item for decisions. <br>
Risk: Accidental activation could run searches using saved interests. <br>
Mitigation: Use explicit prompts for personalized daily reports and review configured topics before scheduled use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vivalavida-say-hi/yoooclaw-personal-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-like conversational briefing text with topic sections, source URLs, summaries, and a fallback message when no current news is found.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs no files; target length is under 1500 Chinese characters with each item summarized in no more than three sentences.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
