## Description: <br>
Tracks public news about Donald Trump and produces a bilingual, sentiment-based novelty prediction of statement execution probability and market attention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneychen](https://clawhub.ai/user/kenneychen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts can use this skill to sample public RSS news about Donald Trump and generate bilingual novelty analysis from keyword and sentiment heuristics. Its predictions should be treated as entertainment or exploratory commentary, not reliable news verification, political forecasting, or market guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer fetches unpinned Python packages and TextBlob corpora. <br>
Mitigation: Run installation in a controlled environment and review or pin dependencies before use. <br>
Risk: RSS fetching disables TLS certificate verification. <br>
Mitigation: Remove verify=False and rely on normal certificate validation before using results operationally. <br>
Risk: Fallback data and novelty predictions can be stale or misleading as news or market guidance. <br>
Mitigation: Label the output as entertainment or exploratory analysis, verify current events independently, and remove stale fallback examples before relying on results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kenneychen/trump-tracker) <br>
- [Al Jazeera RSS Feed](https://www.aljazeera.com/xml/rss/all.xml) <br>
- [Hindustan Times World RSS Feed](https://www.hindustantimes.com/rss/world/rssfeed.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style bilingual console text with setup and execution commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs an unreliability score, execution probability, market-attention label, and bilingual comments for up to three news items.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
