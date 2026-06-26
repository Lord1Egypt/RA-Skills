## Description: <br>
Validate OpenClaw skills during authoring. Use when creating, revising, or preparing a skill for release and you need to scaffold `evals/` files, check readiness for a first eval pass, review whether the frontmatter description has clear trigger coverage, or generate static comparison artifacts before deeper runtime evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stonechen1014](https://clawhub.ai/user/stonechen1014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to prepare OpenClaw skills for first-pass evaluation before release. It scaffolds and checks eval files, reviews positive and negative trigger coverage, detects placeholder content, and produces static comparison artifacts before deeper runtime evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python helper scripts that inspect and create files in a skill directory. <br>
Mitigation: Review the scripts before running them on untrusted or sensitive skill folders. <br>
Risk: Static preflight results may be mistaken for live runtime evaluation or output quality scoring. <br>
Mitigation: Use the results as release-readiness checks and run a deeper evaluator for runtime behavior, factuality, tool-call quality, or production regression testing. <br>
Risk: Run artifact folders are created under the target skill's evals directory. <br>
Mitigation: Use simple run-group names such as demo-baseline and inspect generated artifacts before publishing. <br>


## Reference(s): <br>
- [Skill Eval File Formats](references/eval_format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/stonechen1014/skill-eval-preflight) <br>
- [Publisher Profile](https://clawhub.ai/user/stonechen1014) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated JSON or Markdown artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or inspect eval scaffolding and static run artifacts in a target skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
