## Description: <br>
社交情感分析免费版 helps agents guide personal users through local CSV-based social-media sentiment monitoring with keyword sentiment classification, basic topic extraction, and sentiment distribution reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal users, developers, and product teams use this skill to analyze exported social-media CSV data for brand reputation, product feedback, and topic sentiment trends. The skill is best suited to single-platform, lightweight monitoring with human review of important conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Social-media exports can contain usernames, timestamps, message text, and other personal data. <br>
Mitigation: Use only data authorized for processing, minimize or redact identifiers where possible, and avoid sending sensitive CSV contents to external APIs or LLM services unless intended and permitted. <br>
Risk: Platform API keys may be exposed when users collect social-media data through APIs. <br>
Mitigation: Protect platform API keys and avoid storing credentials in shared CSV files, prompts, or generated reports. <br>
Risk: Dictionary-based sentiment classification can misclassify context, negation, sarcasm, or domain-specific language. <br>
Mitigation: Treat results as directional, customize sentiment dictionaries for the domain, and manually review samples before acting on important conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/social-sentiment-tool-free) <br>
- [Python](https://python.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CSV-based sentiment labels, sentiment distribution counts, basic topic summaries, and brief reports when applied by an agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
