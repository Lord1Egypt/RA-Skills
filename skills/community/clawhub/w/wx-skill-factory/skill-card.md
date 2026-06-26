## Description: <br>
Skill Factory helps an agent plan, generate, test, score, iterate, split, and deliver new skills in manual, semi-automatic, or fully automatic modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwangxiang](https://clawhub.ai/user/mwangxiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to create new skills, improve existing skills, or split reusable workflow steps into sub-skills. It guides requirements alignment, mode selection, draft generation, optional external AI execution, quality scoring, iteration, and delivery reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can draft and revise other skills, so generated content may introduce incorrect guidance or weak operating rules. <br>
Mitigation: Review generated skills before deployment and run security or quality scans as part of the release process. <br>
Risk: Optional external AI calls may expose prompts, workspace content, or secrets if users configure endpoints or test inputs carelessly. <br>
Mitigation: Use trusted AI endpoints, keep API keys private, and avoid sending secrets or confidential workspace content in prompts. <br>
Risk: Fully automatic iteration can continue producing low-value changes if the objective or reference material is unclear. <br>
Mitigation: Set a conservative iteration limit and require user review when quality gates are inconclusive. <br>


## Reference(s): <br>
- [Skill Factory release page](https://clawhub.ai/mwangxiang/wx-skill-factory) <br>
- [Publisher profile](https://clawhub.ai/user/mwangxiang) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [call-guide.md](artifact/call-guide.md) <br>
- [tech-library.md](artifact/tech-library.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with templates, tables, code blocks, shell command examples, and delivery reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated skill files, test reports, comparison reports, iteration records, API call templates, and sub-skill handoff guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
