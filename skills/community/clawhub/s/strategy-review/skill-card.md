## Description: <br>
Use when reviewing, critiquing, or stress-testing an existing strategy document. Evaluates seven dimensions: diagnosis quality, guiding policy strength, action coherence, assumption exposure, and falsifiability, with optional 7S, Five Forces, Balanced Scorecard, and Hoshin Kanri lenses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external reviewers, and strategy teams use this skill to pressure-test existing strategy documents for structural gaps, weak assumptions, failure paths, and missing falsifiability. It reviews strategy rather than creating a replacement strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as "poke holes in this plan" or "what's weak here" may invoke the skill and lead to persistent review artifacts. <br>
Mitigation: Use explicit wording when requesting strategy review, and inspect proposed .beagle state files or strategy-review outputs before accepting persistent changes. <br>


## Reference(s): <br>
- [Review Dimensions](references/review-dimensions.md) <br>
- [Review Lenses](references/review-lenses.md) <br>
- [Interview Lens Audit](references/interview-lens-audit.md) <br>
- [Review Output Template](references/review-template.md) <br>
- [Judge Artifact Schema](references/judge-artifact-schema.md) <br>
- [Pressure-test Scenarios](references/pressure-tests.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/strategy-review) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown review, optional JSON judge artifact, and optional durable state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create strategy-review outputs and .beagle review state when the user requests formal or durable review artifacts.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
