## Description: <br>
A testing gate checker for test coverage, strategy validation, and regression verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terr123123](https://clawhub.ai/user/terr123123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and release engineers use this skill as a quality gate before merges or releases to assess supplied coverage metrics, test strategy completeness, and regression evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pass/fail results can be mistaken for automatic release approval. <br>
Mitigation: Treat the result as an advisory quality signal and keep human review in the release decision. <br>
Risk: Gate outcomes depend on the supplied coverage, strategy, and regression inputs. <br>
Mitigation: Source inputs from trusted CI test artifacts and review unexpected pass/fail changes before relying on the result. <br>


## Reference(s): <br>
- [Testing Gate Skill Page](https://clawhub.ai/terr123123/skills/testing-gate) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks, plus JSON-serializable gate results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports pass/fail status, scores, and details for coverage, test strategy, and regression checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
