## Description: <br>
Tarot Reading provides bilingual Rider-Waite-Smith tarot card draws and interpretations for yes/no, advice, reminder, and lost-item questions using Python's secrets module for randomness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafei0007](https://clawhub.ai/user/jiafei0007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill for entertainment-oriented tarot readings, including yes/no questions, advice or reminder spreads, and lost-item prompts. Agents use it to draw cards, summarize structured draw data, and present a concise interpretation with an entertainment-only disclaimer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake tarot readings for medical, legal, financial, safety, or practical decision guidance. <br>
Mitigation: Keep responses entertainment-oriented, include the entertainment-only disclaimer, and avoid presenting readings as authoritative advice for consequential decisions. <br>
Risk: Broad activation language may make ordinary yes/no, advice, reminder, or lost-item requests eligible for tarot-style handling. <br>
Mitigation: Use the skill when the user requests tarot-style output or accepts that framing, and keep interpretations concise and clearly labeled as entertainment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiafei0007/tarot-reading-new) <br>
- [Tarot card database](artifact/references/cards.py) <br>
- [Chinese spread definitions](artifact/references/spreads.py) <br>
- [English spread definitions](artifact/references/spreads_en.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON draw data plus Markdown-style readable interpretation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Chinese and English output and includes an entertainment-only disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
