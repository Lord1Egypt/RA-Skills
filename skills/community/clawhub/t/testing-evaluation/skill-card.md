## Description: <br>
Design eval test cases, run regression tests, and generate quality reports for AI Agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and agent builders use this skill to design evaluation suites, run manual or scripted regression checks, and summarize agent quality in reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated test cases or reports may be written locally or, when connectors are available, proposed for repository or project-tracker publication. <br>
Mitigation: Specify the intended output location before use and explicitly approve any Git commits, pull request links, or issue creation. <br>
Risk: Evaluation results can be misleading if scoring criteria, expected outputs, or pass thresholds are incomplete. <br>
Mitigation: Review generated criteria and reports against the target agent requirements before using them for release decisions. <br>


## Reference(s): <br>
- [Testing Case Template](references/eval-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown reports and test cases, with optional JSON test-suite examples and Python script skeletons] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local Markdown evaluation reports, regression comparisons, issue summaries, and evaluation script templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
