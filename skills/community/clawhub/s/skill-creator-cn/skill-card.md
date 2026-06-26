## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create new agent skills, refine existing skills, design test prompts, run qualitative and quantitative evaluations, and package the final skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit skill files, run bundled Python helpers, spawn evaluations, and write local workspaces. <br>
Mitigation: Use a dedicated workspace without secrets and review generated files before keeping or publishing them. <br>
Risk: Evaluation viewers and reports may expose prompt content or proprietary skill details. <br>
Mitigation: Prefer the static viewer or an unused local port, and avoid verbose or result logs for sensitive prompts or private content. <br>
Risk: Generated trigger descriptions may change when and how an agent invokes the skill. <br>
Mitigation: Inspect generated descriptions and evaluation results before adopting them. <br>


## Reference(s): <br>
- [ClawHub Skill Creator release page](https://clawhub.ai/yang1002378395-cmyk/skill-creator-cn) <br>
- [Publisher profile](https://clawhub.ai/user/yang1002378395-cmyk) <br>
- [Evaluation schemas](artifact/references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with optional JSON, Python scripts, shell commands, generated reports, packaged skill files, and evaluation artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local workspaces, evaluation outputs, reports, feedback files, and packaged skill artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
