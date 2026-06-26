## Description: <br>
One-click skill publishing automation covering duplicate checks, Bear notes sync, GitHub push, and ClawHub publish. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to publish new or updated ClawHub skills by checking duplicates, optionally syncing a Bear development note, pushing to GitHub, and invoking ClawHub publish. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing can push unintended files or metadata to GitHub and ClawHub if the resolved skill path, repository, branch, version, or changelog is wrong. <br>
Mitigation: Run with --dry-run first, verify all resolved values, and inspect the skill directory for private or unintended files before executing the publish step. <br>
Risk: Bear notes sync may write release metadata or changelog text to a local Bear note. <br>
Mitigation: Use --skip-bear when Bear sync is not desired or when changelog content should not be written to Bear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skill-quick-publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, CLI flags, and environment variable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The publish script supports dry-run, skip, force, and continue-on-error options; it may call git, clawhub, and grizzly when executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
