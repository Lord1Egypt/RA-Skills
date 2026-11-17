## Description: <br>
Provides Chinese-language Rider-Waite tarot readings for personal daily guidance using one-card and past-present-future spreads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External individual users use this skill for symbolic self-reflection, daily guidance, and quick relationship or career questions through lightweight tarot readings. The skill is intended as reflective guidance, not a deterministic prediction or professional advice service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact requests exec and write access that is broader than a conversational tarot reading normally needs. <br>
Mitigation: Install or run the skill without exec and write permissions where possible, and review any command or file-write request before approving it. <br>
Risk: Save or export behavior is vague and could create records of personal readings unexpectedly. <br>
Mitigation: Keep readings in the current chat unless the user explicitly chooses a known destination, and avoid storing sensitive personal details. <br>
Risk: Users may over-rely on symbolic readings for consequential life decisions. <br>
Mitigation: Frame readings as reflective guidance only and encourage human judgment or qualified professional advice for high-impact topics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tarot-reader-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style conversational text with structured tarot-card sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free version describes current-chat readings without persistent history.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
