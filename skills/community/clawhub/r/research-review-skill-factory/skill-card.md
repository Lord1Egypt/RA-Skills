## Description: <br>
Builds custom peer-review skills for specific research areas, problem families, and method combinations using public OpenReview evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, academic writers, and developers use this skill to build reusable reviewer skills for a defined research area or method family. It gathers public OpenReview precedent, synthesizes reviewer concern patterns, and generates a child skill with an area profile, review-response bank, and revision guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public OpenReview data and writes generated evidence or validation files into the workspace. <br>
Mitigation: Run it in a dedicated project directory and review output paths before executing commands. <br>
Risk: Using the workflow with confidential drafts or private review material could expose sensitive research context in generated artifacts. <br>
Mitigation: Use public inputs by default and avoid confidential manuscripts or private review data unless a separate privacy process approves it. <br>
Risk: Generated reviewer skills can encode incomplete or misleading precedent if evidence is sparse. <br>
Mitigation: Label limited evidence, keep OpenReview precedent separate from reviewer inference, and manually review generated banks before reuse. <br>


## Reference(s): <br>
- [Research Area Profile Schema](references/research_area_profile_schema.md) <br>
- [OpenReview Area Evidence Workflow](references/openreview_area_evidence_workflow.md) <br>
- [Generated Area Review Skill Contract](references/generated_area_review_skill_contract.md) <br>
- [Subtle Logic Flaws Checklist](references/subtle_logic_flaws.md) <br>
- [OpenReview API v2](https://api2.openreview.net) <br>
- [ClawHub Skill Release](https://clawhub.ai/c-narcissus/research-review-skill-factory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON specifications, shell commands, and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated child skill directories and local evidence or validation files; raw review dumps are excluded by design.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
