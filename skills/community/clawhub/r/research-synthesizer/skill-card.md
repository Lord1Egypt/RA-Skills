## Description: <br>
Multi-source research synthesizer that takes a question, runs 3-5 parallel web searches with varied phrasings, deduplicates results, and returns a concise cited answer, searching in Hebrew and English for Hebrew questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, analysts, and developers use this skill to turn open-ended research questions into concise, source-cited summaries. It is especially oriented toward multi-source web research, competitor or company checks, and bilingual Hebrew-English research when the user asks in Hebrew. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run web searches and synthesize from sources that can be incomplete, stale, biased, or conflicting. <br>
Mitigation: Prefer high-credibility sources, cite the sources used, flag conflicts or stale information, and keep factual claims tied to retrieved evidence. <br>
Risk: The skill includes behavior to save important research summaries into contact-linked local memory without clear opt-in or retention controls. <br>
Mitigation: Disable the memory-write rule or require explicit user confirmation before storing summaries, especially for sensitive business, personal, health, legal, financial, or political topics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/research-synthesizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with key points and cited source URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise human-facing answer, generally under about 400 words.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
