## Description: <br>
Article Taster evaluates Chinese articles for quality, genre fit, originality, AI-like patterns, and reading value. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forealmy](https://clawhub.ai/user/forealmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and editors use this skill to analyze Chinese article text before reading or sharing it. It classifies article type, scores content quality, estimates AI-generated characteristics, applies originality exemptions for classical literature, and returns reading recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency setup may drift or introduce vulnerable packages. <br>
Mitigation: Install in a virtual environment or container, pin dependencies, and scan Python packages before running. <br>
Risk: Article text is processed locally by an analysis tool and may include sensitive content. <br>
Mitigation: Only analyze documents that are appropriate to process in the local execution environment. <br>
Risk: AI-detection labels and scores are heuristic and may be misleading or overly harsh. <br>
Mitigation: Treat AI-detection results as advisory signals and review conclusions before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/forealmy/tmpz3kwrq8c) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON report and Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes article type, scores, AI-detection heuristics, originality signals, and reading advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
