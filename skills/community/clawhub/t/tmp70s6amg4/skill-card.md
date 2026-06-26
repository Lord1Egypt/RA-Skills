## Description: <br>
Article Taster evaluates article quality across article types, estimates AI-generation signals, and produces reading recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forealmy](https://clawhub.ai/user/forealmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Article Taster to classify Chinese articles, score technical, essay, novel, and other writing, estimate AI-generation signals, and generate reading recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-generation and originality scores are heuristic and may misclassify human or AI-assisted writing. <br>
Mitigation: Treat AI-detection results as review signals rather than definitive judgments, especially before user-facing or high-impact decisions. <br>
Risk: AI-detection wording may include harsh labels that are unsuitable for public reports. <br>
Mitigation: Review generated Markdown before sharing it externally and adjust labels for the target audience. <br>
Risk: Spoiler controls for novel analysis may be unreliable. <br>
Mitigation: Review novel-analysis output before presenting it to readers who require spoiler avoidance. <br>
Risk: The skill reads local article files supplied by the user. <br>
Mitigation: Run it in a virtual environment and pass only files intended for analysis. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/forealmy/tmp70s6amg4) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Markdown, JSON, Guidance] <br>
**Output Format:** [JSON report or Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI supports direct text input or local article files; batch analysis is declared but not implemented.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
