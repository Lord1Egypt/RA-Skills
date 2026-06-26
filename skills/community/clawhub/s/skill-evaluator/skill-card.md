## Description: <br>
Evaluate Clawdbot skills for quality, reliability, and publish-readiness using a multi-framework rubric (ISO 25010, OpenSSF, Shneiderman, agent-specific heuristics). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Terwox](https://clawhub.ai/user/Terwox) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, maintainers, and reviewers use this skill to assess Clawdbot skills before publishing by combining automated structural checks with a 25-criteria manual rubric. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evaluator reads local skill folders selected by the user. <br>
Mitigation: Run it only against skill folders you intend to inspect. <br>
Risk: Generated EVAL.md content can influence publishing decisions. <br>
Mitigation: Review any generated evaluation before publishing or relying on its recommendations. <br>
Risk: Optional pip or npx tools may introduce third-party package risk. <br>
Mitigation: Install or run optional tools only in an environment where those packages are trusted. <br>


## Reference(s): <br>
- [Skill Evaluation Rubric](artifact/references/rubric.md) <br>
- [Evaluation Template](artifact/assets/EVAL-TEMPLATE.md) <br>
- [SkillLens](https://www.npmjs.com/package/skilllens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples, optional JSON output, and an evaluation template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces automated structural check results and supports manual scoring into EVAL.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
