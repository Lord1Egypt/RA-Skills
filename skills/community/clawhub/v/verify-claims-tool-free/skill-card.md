## Description: <br>
事实核查助手免费版 helps personal users check claims by comparing them against multiple professional fact-checking sources and returning a structured assessment with supporting evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal users, students, researchers, and content creators use this skill to verify news, social media posts, article claims, and other public information. It guides an agent to search multiple fact-checking sources, compare findings, and summarize a confidence-oriented verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use broad shell-based web retrieval and may save claim history, which can expose sensitive claims or private drafts in the agent environment. <br>
Mitigation: Avoid submitting private drafts, personal communications, credentials, or sensitive claims unless execution, storage, retention, and deletion controls are clear. <br>
Risk: Fact-checking results can be incomplete or misleading when source coverage is limited, web retrieval fails, or the claim is too vague. <br>
Mitigation: Use clear, specific claims; compare multiple reputable sources; preserve citations; and require human review before using results for consequential decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/verify-claims-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or structured text with optional JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include verdicts, confidence labels, source summaries, citations, logs, and optional claim-history entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence, frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
